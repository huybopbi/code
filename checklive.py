# _*_ coding: utf-8 _*_
import requests
import os
import sys
import time
import logging
import argparse
import urllib3
from threading import Thread, Lock
from queue import Queue

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create Results directory
try:
    os.mkdir('Results')
except:
    pass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Results/checklive.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Suppress urllib3 warnings
logging.getLogger('urllib3').setLevel(logging.ERROR)

# Global variables
FILE_LOCK = Lock()
PROGRESS_LOCK = Lock()
TOTAL_URLS = 0
PROCESSED_URLS = 0
LIVE_COUNT = 0
DEAD_COUNT = 0
SESSION = None
ARGS = None

# ANSI Colors
GREEN = '\033[32;1m'
RED = '\033[31;1m'
YELLOW = '\033[33;1m'
BLUE = '\033[34;1m'
CYAN = '\033[36;1m'
RESET = '\033[0m'

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

def check_url(url):
    """Check if URL is live"""
    global PROCESSED_URLS, LIVE_COUNT, DEAD_COUNT

    # Normalize URL
    url = url.strip()
    if not url:
        return

    if "://" not in url:
        url = f"http://{url}"

    is_live = False
    status_code = None

    try:
        response = SESSION.get(
            url,
            timeout=ARGS.timeout if ARGS else 5,
            verify=False,
            allow_redirects=ARGS.redirects if ARGS else True,
            stream=True
        )

        status_code = response.status_code

        # Check if live based on status code or content
        if response.status_code == 200:
            is_live = True
        elif '<title>' in response.text[:1000] or '</body>' in response.text[:1000] or '</html>' in response.text[:1000]:
            is_live = True
        elif response.status_code in [301, 302, 303, 307, 308]:
            is_live = True

        response.close()

    except requests.exceptions.Timeout:
        logger.debug(f"Timeout: {url}")
    except requests.exceptions.ConnectionError:
        logger.debug(f"Connection error: {url}")
    except Exception as e:
        logger.debug(f"Error checking {url}: {str(e)}")

    # Update counters
    with PROGRESS_LOCK:
        PROCESSED_URLS += 1
        if is_live:
            LIVE_COUNT += 1
        else:
            DEAD_COUNT += 1

    # Save results
    with FILE_LOCK:
        if is_live:
            with open('Results/live.txt', 'a') as f:
                f.write(f"{url}\n")
            print(f"{GREEN}[LIVE]{RESET} {url} {CYAN}[{status_code}]{RESET}")
        else:
            with open('Results/dead.txt', 'a') as f:
                f.write(f"{url}\n")
            if ARGS and ARGS.verbose:
                print(f"{RED}[DEAD]{RESET} {url}")

    # Progress update every 50 URLs
    with PROGRESS_LOCK:
        if PROCESSED_URLS % 50 == 0:
            progress = f"[{PROCESSED_URLS}/{TOTAL_URLS}] Live: {LIVE_COUNT}, Dead: {DEAD_COUNT}"
            logger.info(progress)
            print(f"{CYAN}{progress}{RESET}")

def main():
    global TOTAL_URLS, SESSION, ARGS

    print(f'''{GREEN}
    ╔══════════════════════════════════════════════╗
    ║        🌐 URL/IP Live Checker 🌐           ║
    ║                                              ║
    ║  Fast multithreaded live/dead checker       ║
    ╚══════════════════════════════════════════════╝
    {RESET}''')

    # Parse arguments
    parser = argparse.ArgumentParser(description='Check if URLs/IPs are live')
    parser.add_argument('--list', '-l', dest='list', help='Path to file containing URLs (one per line)')
    parser.add_argument('--threads', '-t', dest='threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('--timeout', dest='timeout', type=float, default=5.0, help='Request timeout in seconds (default: 5)')
    parser.add_argument('--redirects', dest='redirects', action='store_true', help='Follow redirects (default: True)')
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Show dead URLs in output')
    parser.add_argument('--retries', dest='retries', type=int, default=2, help='Max retries per request (default: 2)')

    args = parser.parse_args()
    ARGS = args

    # Get URL list
    if not args.list:
        args.list = input(f"{YELLOW}Enter path to URL list file: {RESET}")

    try:
        with open(args.list, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{RED}Error: File '{args.list}' not found!{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Error reading file: {str(e)}{RESET}")
        sys.exit(1)

    TOTAL_URLS = len(urls)

    if TOTAL_URLS == 0:
        print(f"{RED}Error: No URLs found in file!{RESET}")
        sys.exit(1)

    print(f"{BLUE}Loaded {TOTAL_URLS} URLs{RESET}")
    print(f"{BLUE}Threads: {args.threads}{RESET}")
    print(f"{BLUE}Timeout: {args.timeout}s{RESET}")
    print(f"{YELLOW}Starting check...{RESET}\n")

    # Setup session with retry mechanism
    SESSION = requests.Session()
    try:
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        retry = Retry(
            total=args.retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"]
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
        SESSION.mount('http://', adapter)
        SESSION.mount('https://', adapter)
    except Exception:
        pass

    # Start time
    start_time = time.time()

    # Create thread pool and process URLs
    pool = ThreadPool(args.threads)

    for url in urls:
        pool.add_task(check_url, url)

    pool.wait_completion()

    # End time
    end_time = time.time()
    duration = end_time - start_time

    # Final summary
    print(f"\n{'='*60}")
    print(f"{GREEN}✅ Scan completed!{RESET}")
    print(f"{'='*60}")
    print(f"{BLUE}Total URLs checked:{RESET} {TOTAL_URLS}")
    print(f"{GREEN}Live:{RESET} {LIVE_COUNT}")
    print(f"{RED}Dead:{RESET} {DEAD_COUNT}")
    print(f"{YELLOW}Duration:{RESET} {duration:.2f} seconds")
    print(f"{YELLOW}Speed:{RESET} {TOTAL_URLS/duration:.2f} URLs/second")
    print(f"{'='*60}")
    print(f"{CYAN}Results saved to:{RESET}")
    print(f"  - {GREEN}Results/live.txt{RESET} ({LIVE_COUNT} URLs)")
    print(f"  - {RED}Results/dead.txt{RESET} ({DEAD_COUNT} URLs)")
    print(f"  - {BLUE}Results/checklive.log{RESET}")
    print(f"{'='*60}\n")

    # Cleanup
    if SESSION:
        SESSION.close()

    logger.info(f"Scan completed: {LIVE_COUNT} live, {DEAD_COUNT} dead in {duration:.2f}s")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Scan interrupted by user{RESET}")
        print(f"{CYAN}Partial results saved to Results/ directory{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}Fatal error: {str(e)}{RESET}")
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)
