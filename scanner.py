import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog='scanner',
        description='Scans for open ports on a host',)

    parser.add_argument('-t', '--target', type=str, required=True, help='Target IP address')
    parser.add_argument('-p', '--ports', type=str, required=True, help='Ports to scan (e.g. 22,80,443 or 1-1000)')
    parser.add_argument('-b', '--banner', action='store_true', help='Print banner', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode", default=False)

    return parser.parse_args()

class Scanner():
    def __init__(self, target, ports, banner, verbose):
        self.target = target
        self.ports = ports
        self.banner = banner
        self.verbose = verbose
    
    def parse_ports(self):
        pass

if __name__ == '__main__':
    args = parse_args()

    scanner = Scanner(args.target, args.ports, args.banner, args.verbose)