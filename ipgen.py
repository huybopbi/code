# _*_ coding: utf-8 _*_
import random
import argparse
import sys
import os
from colorama import Fore, init

init(autoreset=True)

# ANSI Colors
RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
BLUE = Fore.LIGHTBLUE_EX
CYAN = Fore.LIGHTCYAN_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
WHITE = Fore.WHITE
RESET = Fore.RESET

def print_banner():
    """Print tool banner"""
    print(RED + r'''
    ╔══════════════════════════════════════════════════════════╗
    ║              🌐 IP Generator & Range Tool 🌐            ║
    ║                                                          ║
    ║  Generate random IPs, IP ranges, and .env URLs          ║
    ╚══════════════════════════════════════════════════════════╝
    ''' + RESET)

def generate_random_ips(count, output_file, add_env=False):
    """Generate random IPs"""
    print(f"{YELLOW}Generating {count} random IPs...{RESET}")

    generated = 0
    with open(output_file, 'a') as f:
        for i in range(count):
            a = random.randrange(0, 256)
            b = random.randrange(0, 256)
            c = random.randrange(0, 256)
            d = random.randrange(0, 256)

            ip = f"{a}.{b}.{c}.{d}"

            if add_env:
                ip += "/.env"

            f.write(ip + '\n')
            generated += 1

            # Progress update
            if generated % 1000 == 0:
                print(f"{CYAN}Generated: {generated}/{count}{RESET}")

    print(f"{GREEN}✓ Generated {generated} IPs and saved to {output_file}{RESET}")

def generate_ip_range(input_file, output_file):
    """Generate IP ranges from a list of IP prefixes"""
    print(f"{YELLOW}Generating IP ranges from {input_file}...{RESET}")

    try:
        with open(input_file, 'r') as f:
            ip_list = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{RED}Error: File '{input_file}' not found!{RESET}")
        return
    except Exception as e:
        print(f"{RED}Error reading file: {str(e)}{RESET}")
        return

    if not ip_list:
        print(f"{RED}Error: No IPs found in file!{RESET}")
        return

    total_generated = 0

    with open(output_file, 'w') as f:
        for idx, ip_prefix in enumerate(ip_list, 1):
            parts = ip_prefix.split('.')

            if len(parts) < 2:
                print(f"{YELLOW}Warning: Invalid IP format '{ip_prefix}', skipping...{RESET}")
                continue

            print(f"{CYAN}Processing [{idx}/{len(ip_list)}]: {ip_prefix}.x.x{RESET}")

            # Generate x.x.0.0 to x.x.255.255
            for j in range(256):
                for k in range(256):
                    ranged_ip = f"{parts[0]}.{parts[1]}.{j}.{k}"
                    f.write(ranged_ip + '\n')
                    total_generated += 1

    print(f"{GREEN}✓ Generated {total_generated:,} IPs from {len(ip_list)} prefixes{RESET}")
    print(f"{GREEN}✓ Saved to {output_file}{RESET}")

def generate_custom_range(start_ip, end_ip, output_file):
    """Generate IPs in a custom range"""
    print(f"{YELLOW}Generating custom IP range from {start_ip} to {end_ip}...{RESET}")

    try:
        start_parts = [int(x) for x in start_ip.split('.')]
        end_parts = [int(x) for x in end_ip.split('.')]
    except:
        print(f"{RED}Error: Invalid IP format!{RESET}")
        return

    if len(start_parts) != 4 or len(end_parts) != 4:
        print(f"{RED}Error: IPs must be in format x.x.x.x{RESET}")
        return

    generated = 0
    with open(output_file, 'w') as f:
        for a in range(start_parts[0], end_parts[0] + 1):
            for b in range(start_parts[1], end_parts[1] + 1):
                for c in range(start_parts[2], end_parts[2] + 1):
                    for d in range(start_parts[3], end_parts[3] + 1):
                        ip = f"{a}.{b}.{c}.{d}"
                        f.write(ip + '\n')
                        generated += 1

                        if generated % 10000 == 0:
                            print(f"{CYAN}Generated: {generated:,}{RESET}")

    print(f"{GREEN}✓ Generated {generated:,} IPs{RESET}")
    print(f"{GREEN}✓ Saved to {output_file}{RESET}")

def interactive_mode():
    """Interactive menu mode"""
    print_banner()

    print(f"{CYAN}Select an option:{RESET}\n")
    print(f"{WHITE}[1]{RESET} Generate random IPs")
    print(f"{WHITE}[2]{RESET} Generate random IPs with /.env")
    print(f"{WHITE}[3]{RESET} Generate IP ranges from file (x.x.0.0 - x.x.255.255)")
    print(f"{WHITE}[4]{RESET} Generate custom IP range")
    print(f"{WHITE}[5]{RESET} Exit\n")

    choice = input(f"{YELLOW}Enter your choice [1-5]: {RESET}").strip()

    if choice == '1':
        count = int(input(f"{YELLOW}How many IPs to generate? {RESET}"))
        output = input(f"{YELLOW}Output file (default: ips.txt): {RESET}") or 'ips.txt'
        generate_random_ips(count, output, add_env=False)

    elif choice == '2':
        count = int(input(f"{YELLOW}How many IPs to generate? {RESET}"))
        output = input(f"{YELLOW}Output file (default: ips_with_env.txt): {RESET}") or 'ips_with_env.txt'
        generate_random_ips(count, output, add_env=True)

    elif choice == '3':
        input_file = input(f"{YELLOW}Input file with IP prefixes (e.g., 192.168): {RESET}")
        output = input(f"{YELLOW}Output file (default: ranged_ips.txt): {RESET}") or 'ranged_ips.txt'
        generate_ip_range(input_file, output)

    elif choice == '4':
        start = input(f"{YELLOW}Start IP (e.g., 192.168.0.0): {RESET}")
        end = input(f"{YELLOW}End IP (e.g., 192.168.1.255): {RESET}")
        output = input(f"{YELLOW}Output file (default: custom_range.txt): {RESET}") or 'custom_range.txt'
        generate_custom_range(start, end, output)

    elif choice == '5':
        print(f"{GREEN}Goodbye!{RESET}")
        sys.exit(0)

    else:
        print(f"{RED}Invalid choice!{RESET}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='IP Generator & Range Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Interactive mode
  python ipgen.py

  # Generate 1000 random IPs
  python ipgen.py --random 1000 -o ips.txt

  # Generate 1000 random IPs with /.env
  python ipgen.py --random 1000 --env -o ips_env.txt

  # Generate IP ranges from file
  python ipgen.py --range-file prefixes.txt -o ranged.txt

  # Generate custom range
  python ipgen.py --custom-range 192.168.0.0 192.168.1.255 -o custom.txt
        '''
    )

    parser.add_argument('--random', type=int, metavar='COUNT', help='Generate random IPs')
    parser.add_argument('--env', action='store_true', help='Add /.env to generated IPs')
    parser.add_argument('--range-file', metavar='FILE', help='Generate ranges from IP prefix file')
    parser.add_argument('--custom-range', nargs=2, metavar=('START', 'END'), help='Generate custom IP range')
    parser.add_argument('-o', '--output', default='ips.txt', help='Output file (default: ips.txt)')

    args = parser.parse_args()

    # If no arguments, run interactive mode
    if len(sys.argv) == 1:
        interactive_mode()
        return

    print_banner()

    if args.random:
        generate_random_ips(args.random, args.output, add_env=args.env)

    elif args.range_file:
        generate_ip_range(args.range_file, args.output)

    elif args.custom_range:
        generate_custom_range(args.custom_range[0], args.custom_range[1], args.output)

    else:
        parser.print_help()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}")
        sys.exit(1)
