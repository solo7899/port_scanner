import argparse
import socket


def parse_args():
    parser = argparse.ArgumentParser(prog='scanner',
        description='Scans for open ports on a host',)

    parser.add_argument('-t', '--target', type=str, required=True, help='Target IP address')
    parser.add_argument('-p', '--ports', type=str, required=True, help='Ports to scan (e.g. 22,80,443 or 1-1000)')
    parser.add_argument('-b', '--banner', action='store_true', help='Print banner', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode", default=False)

    return parser.parse_args()

class Scanner():

    errs = {
        "range_value_err": "*** Error: please Enter the correct format .e.g 1-1000(with on spaces in between)\n*** values all should be numbers",
        "single_value_err": "*** Error: values should all be positive numeric values from 1-65535"
        }

    def __init__(self, target, ports, banner, verbose):
        self.target = target
        self.ports = ports
        self.banner = banner
        self.verbose = verbose
    
    
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

                if not self.__check_range(int(port_start), int(port_end)):
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
    
    def scan_ports(self):
        for port in self.ports:
            is_opon = self.is_port_open(port)
            if is_opon:
                print(f"Port {port} is open")

    def is_port_open(self, port):
        sock = socket.socket()
        sock.settimeout(5)

        conn = sock.connect_ex((self.target, port))
        if conn != 0:
            return False 
        return True 

if __name__ == '__main__':
    args = parse_args()

    scanner = Scanner(args.target, args.ports, args.banner, args.verbose)
    if not scanner.parse_ports():
        exit(1)

    scanner.scan_ports()