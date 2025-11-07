#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""
Nmap Parser - Extract IPs with specific open ports from Nmap scan results
Supports: Normal output, Grepable output, and XML output
"""

import re
import sys
import argparse
import xml.etree.ElementTree as ET
from colorama import Fore, init

init(autoreset=True)

# Colors
RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
BLUE = Fore.LIGHTBLUE_EX
CYAN = Fore.LIGHTCYAN_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
RESET = Fore.RESET

def print_banner():
    """Print banner"""
    print(GREEN + r'''
    ╔══════════════════════════════════════════════════════════╗
    ║           🔍 Nmap Parser - IP Extractor 🔍              ║
    ║                                                          ║
    ║  Extract IPs with open ports from Nmap scan results    ║
    ╚══════════════════════════════════════════════════════════╝
    ''' + RESET)

def parse_normal_output(file_path, ports, states):
    """Parse normal nmap output format"""
    results = {}
    current_ip = None

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Find all host blocks
        host_blocks = re.split(r'Nmap scan report for ', content)[1:]

        for block in host_blocks:
            # Extract IP
            ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', block)
            if not ip_match:
                continue

            ip = ip_match.group(1)
            results[ip] = []

            # Find PORT STATE SERVICE section
            port_section = re.search(r'PORT\s+STATE\s+SERVICE.*?\n(.*?)(?:\n\n|\Z)', block, re.DOTALL)
            if not port_section:
                continue

            # Parse each port line
            for line in port_section.group(1).split('\n'):
                for port in ports:
                    # Match port number and state
                    pattern = rf'(\d+)/tcp\s+(\w+)'
                    match = re.search(pattern, line)
                    if match:
                        port_num = int(match.group(1))
                        state = match.group(2)

                        if port_num == port and state in states:
                            results[ip].append({'port': port_num, 'state': state})

        return results

    except Exception as e:
        print(f"{RED}Error parsing normal output: {str(e)}{RESET}")
        return {}

def parse_grepable_output(file_path, ports, states):
    """Parse grepable nmap output format (.gnmap)"""
    results = {}

    try:
        with open(file_path, 'r') as f:
            for line in f:
                if not line.startswith('Host:'):
                    continue

                # Extract IP
                ip_match = re.search(r'Host:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                if not ip_match:
                    continue

                ip = ip_match.group(1)
                results[ip] = []

                # Find Ports section
                ports_section = re.search(r'Ports:\s+(.*?)(?:\t|$)', line)
                if not ports_section:
                    continue

                # Parse each port entry
                port_entries = ports_section.group(1).split(',')
                for entry in port_entries:
                    entry = entry.strip()
                    # Format: 80/open/tcp//http///
                    parts = entry.split('/')
                    if len(parts) >= 2:
                        try:
                            port_num = int(parts[0])
                            state = parts[1]

                            if port_num in ports and state in states:
                                results[ip].append({'port': port_num, 'state': state})
                        except:
                            continue

        return results

    except Exception as e:
        print(f"{RED}Error parsing grepable output: {str(e)}{RESET}")
        return {}

def parse_xml_output(file_path, ports, states):
    """Parse XML nmap output format"""
    results = {}

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Find all host elements
        for host in root.findall('.//host'):
            # Get IP address
            address = host.find('.//address[@addrtype="ipv4"]')
            if address is None:
                continue

            ip = address.get('addr')
            results[ip] = []

            # Find all ports
            for port_elem in host.findall('.//port'):
                protocol = port_elem.get('protocol')
                if protocol != 'tcp':
                    continue

                port_num = int(port_elem.get('portid'))
                state_elem = port_elem.find('state')

                if state_elem is not None:
                    state = state_elem.get('state')

                    if port_num in ports and state in states:
                        results[ip].append({'port': port_num, 'state': state})

        return results

    except Exception as e:
        print(f"{RED}Error parsing XML output: {str(e)}{RESET}")
        return {}

def detect_format(file_path):
    """Auto-detect nmap output format"""
    try:
        with open(file_path, 'r') as f:
            first_lines = f.read(1000)

        if first_lines.startswith('<?xml'):
            return 'xml'
        elif 'Host:' in first_lines and 'Ports:' in first_lines:
            return 'grepable'
        elif 'Nmap scan report' in first_lines:
            return 'normal'
        else:
            return 'unknown'

    except Exception as e:
        print(f"{RED}Error detecting format: {str(e)}{RESET}")
        return 'unknown'

def main():
    """Main function"""
    print_banner()

    parser = argparse.ArgumentParser(
        description='Extract IPs with specific open ports from Nmap scan results',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Extract IPs with port 80 open
  python nmapparser.py -i scan.txt -o ips.txt

  # Extract IPs with port 443 open
  python nmapparser.py -i scan.xml -p 443 -o https_ips.txt

  # Extract IPs with multiple ports
  python nmapparser.py -i scan.gnmap -p 80 443 8080 -o web_ips.txt

  # Include filtered ports
  python nmapparser.py -i scan.txt -p 80 -s open filtered -o ips.txt

  # Auto-detect format
  python nmapparser.py -i scan.txt -o ips.txt

  # Specify format manually
  python nmapparser.py -i scan.txt -f grepable -o ips.txt

  # Add http:// prefix
  python nmapparser.py -i scan.txt -o urls.txt --http
        '''
    )

    parser.add_argument('-i', '--input', required=True,
                        help='Input nmap scan file')
    parser.add_argument('-o', '--output', required=True,
                        help='Output file for extracted IPs')
    parser.add_argument('-p', '--ports', nargs='+', type=int, default=[80],
                        help='Port numbers to filter (default: 80)')
    parser.add_argument('-s', '--states', nargs='+', default=['open'],
                        help='Port states to include (default: open)')
    parser.add_argument('-f', '--format', choices=['normal', 'grepable', 'xml', 'auto'],
                        default='auto',
                        help='Nmap output format (default: auto-detect)')
    parser.add_argument('--http', action='store_true',
                        help='Add http:// prefix to IPs')
    parser.add_argument('--https', action='store_true',
                        help='Add https:// prefix to IPs')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    # Detect format if auto
    if args.format == 'auto':
        detected_format = detect_format(args.input)
        if detected_format == 'unknown':
            print(f"{YELLOW}Could not detect format, trying all parsers...{RESET}")
            args.format = 'normal'  # Default fallback
        else:
            args.format = detected_format
            print(f"{BLUE}Detected format: {args.format}{RESET}\n")

    # Parse based on format
    print(f"{CYAN}Parsing {args.input} as {args.format} format...{RESET}")

    if args.format == 'normal':
        results = parse_normal_output(args.input, args.ports, args.states)
    elif args.format == 'grepable':
        results = parse_grepable_output(args.input, args.ports, args.states)
    elif args.format == 'xml':
        results = parse_xml_output(args.input, args.ports, args.states)
    else:
        print(f"{RED}Unknown format!{RESET}")
        sys.exit(1)

    # Filter results - only keep IPs that have matching ports
    filtered_ips = [ip for ip, ports_found in results.items() if ports_found]

    if not filtered_ips:
        print(f"{YELLOW}No IPs found with specified ports!{RESET}")
        print(f"{YELLOW}Searched for ports: {args.ports}{RESET}")
        print(f"{YELLOW}States: {args.states}{RESET}")
        sys.exit(0)

    # Sort IPs
    filtered_ips.sort()

    # Write to output file
    with open(args.output, 'w') as f:
        for ip in filtered_ips:
            if args.http:
                f.write(f"http://{ip}\n")
            elif args.https:
                f.write(f"https://{ip}\n")
            else:
                f.write(f"{ip}\n")

            if args.verbose:
                ports_info = results[ip]
                ports_str = ', '.join([f"{p['port']}/{p['state']}" for p in ports_info])
                print(f"{GREEN}[+] {ip}{RESET} - Ports: {ports_str}")

    # Summary
    print(f"\n{GREEN}{'='*60}{RESET}")
    print(f"{GREEN}✓ Extraction completed!{RESET}")
    print(f"{GREEN}{'='*60}{RESET}\n")
    print(f"{BLUE}Input file:{RESET} {args.input}")
    print(f"{BLUE}Format:{RESET} {args.format}")
    print(f"{BLUE}Ports searched:{RESET} {args.ports}")
    print(f"{BLUE}States:{RESET} {args.states}")
    print(f"{BLUE}IPs found:{RESET} {len(filtered_ips)}")
    print(f"{BLUE}Output file:{RESET} {args.output}\n")

    if not args.verbose and len(filtered_ips) > 0:
        print(f"{CYAN}Sample IPs:{RESET}")
        for ip in filtered_ips[:5]:
            ports_info = results[ip]
            ports_str = ', '.join([f"{p['port']}/{p['state']}" for p in ports_info])
            print(f"  {GREEN}{ip}{RESET} - {ports_str}")
        if len(filtered_ips) > 5:
            print(f"  {YELLOW}... and {len(filtered_ips) - 5} more{RESET}")

    print(f"\n{GREEN}{'='*60}{RESET}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}")
        sys.exit(1)
