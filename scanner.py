import argparse
import socket
import threading

def parse_args():
    parser = argparse.ArgumentParser(prog='scanner',
        description='Scans for open ports on a host',
        epilog='Example: scanner.py -t 127.0.0.1 -p 22,80,443 -b "Hello\r\n')

    parser.add_argument('-t', '--target', type=str, required=True, help='Target IP address')
    parser.add_argument('-p', '--ports', type=str, required=True, help='Ports to scan (e.g. 22,80,443 or 1-1000)')
    parser.add_argument('-g', '--get-banner', action="store_true", default=False, help="Get banner for open ports")
    parser.add_argument('-b', '--banner', type=str, required=False, default="hello\r\n", help="Data to send in banner request, default is 'hello\\r\\n'")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode", default=False)

    return parser.parse_args()

class Scanner():

    errs = {
        "range_value_err": "*** Error: please Enter the correct format .e.g 1-1000(with no spaces in between)\n*** values all should be numbers",
        "single_value_err": "*** Error: values should all be positive numeric values from 1-65535"
        }

    def __init__(self, target, ports, get_banner,banner, verbose):
        self.target = target
        self.ports = ports
        self.banner = banner
        self.verbose = verbose
        self.get_banner = get_banner
    
    
    def __check_range(self, *args):
        for arg in args:
            if not (1 <= arg <= 65535) :
                return False
        return True
    
    def parse_ports(self):
        port_exprs = self.ports.split(',')
        self.ports = []
        for p in port_exprs:
            if '-' in p:
                port_start, port_end = p.split('-')
                try:
                    port_start, port_end = int(port_start), int(port_end)
                except ValueError:
                    print(self.errs['range_value_err'])
                    return False

                if not self.__check_range(port_start, port_end):
                    print(self.errs["single_value_err"])
                    return False
                    
                for p in range(int(port_start), int(port_end)+1):
                    self.ports.append(p)
                
            else:
                try:
                    p = int(p)
                except ValueError:
                    print(self.errs["single_value_err"]) 
                    return False

                if not self.__check_range(int(p)):
                    print(self.errs["single_value_err"])
                    return False
                self.ports.append(p)
                
            
        self.ports = sorted(set(self.ports))
        return True
    
    def scan_operations(self, port, status_list):
        sock, is_open = self.is_port_open(port)
        banner = None
        if is_open:
            if self.verbose:
                print(f"Port {port} is open")
            if self.get_banner:
                banner = self.get_banner_func(sock)
        if is_open:
            status_list.append((port, banner))
                
        self.close_sock(sock)
    def scan_ports(self):
        status_list = []
        threads = []
        for port in self.ports:
            thread = threading.Thread(target=self.scan_operations, args=(port, status_list), daemon=True)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        
        return status_list

    def get_banner_func(self, sock:socket.socket):
        try:
            banner = sock.recv(1024)
        except socket.timeout:
            banner = None
        if banner:
            if self.verbose:
                print(f"[Banner]\n{banner.decode(errors='ignore').strip()}\n")
            return f"[Banner]\n{banner.decode(errors='ignore').strip()}\n"
        sock.sendall(bytes(self.banner, 'utf-8'))
        try:
            banner = sock.recv(1024)
            if self.verbose:
                print(f"[Banner] {banner.decode(errors='ignore').strip()}")
            return f"[Banner] {banner.decode(errors='ignore').strip()}"
        except socket.error:
            if self.verbose:
                print(">>> no Banner recieved")
            return ">>> no Banner recieved"

    def is_port_open(self, port):
        sock = socket.socket()
        sock.settimeout(5)

        conn = sock.connect_ex((self.target, port))
        if conn != 0:
            return sock, False 
        return sock, True 

    def close_sock(self, sock):
        sock.close()

def main():
    args = parse_args()

    scanner = Scanner(args.target, args.ports, args.get_banner, args.banner, args.verbose)
    if not scanner.parse_ports():
        exit(1)

    status_list = scanner.scan_ports()

    for port, banner in sorted(status_list, key=lambda x: x[0]):
        print(f"Port {port} is open")
        if banner:
            print(banner)
        print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass