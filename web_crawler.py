import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import queue
import threading
import json
import os
import time
from datetime import datetime

OUTPUT_DIR = "crawled_data"
NUM_WORKERS = 5
CRAWL_DELAY_SECONDS = 1

url_queue = queue.Queue()
crawled_urls = set()
robot_parsers = {}
lock = threading.Lock()
json_files_saved_count = 0
MAX_JSON_FILES = -1
stop_crawling_event = threading.Event()

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_robot_parser(domain):
    if domain not in robot_parsers:
        rp = RobotFileParser()
        robots_url = urljoin(f"http://{domain}", "/robots.txt")
        try:
            rp.set_url(robots_url)
            rp.read()
            with lock:
                robot_parsers[domain] = rp
        except Exception as e:
            with lock:
                robot_parsers[domain] = None
    return robot_parsers.get(domain)


def is_allowed(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if not domain:
        return False

    rp = get_robot_parser(domain)
    if rp:
        return rp.can_fetch("*", url)
    return True

def save_data(url, title, text_content, links):
    global json_files_saved_count, MAX_JSON_FILES

    parsed_url = urlparse(url)
    filename_safe = "".join(c if c.isalnum() else "_" for c in parsed_url.netloc + parsed_url.path + parsed_url.query)[:100]
    if not filename_safe:
        filename_safe = "index"

    import hashlib
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    file_path = os.path.join(OUTPUT_DIR, f"{filename_safe}_{url_hash[:8]}.json")

    current_time_formatted = datetime.now().strftime("%d %B %H:%M:%S")

    data = {
        "url": url,
        "title": title,
        "text_content": text_content,
        "extracted_links": links,
        "timestamp": current_time_formatted
    }
    with lock:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            json_files_saved_count += 1
            print(f"Saved {json_files_saved_count}/{MAX_JSON_FILES if MAX_JSON_FILES != -1 else '∞'}: {url}")

            if MAX_JSON_FILES != -1 and json_files_saved_count >= MAX_JSON_FILES:
                print(f"Reached limit of {MAX_JSON_FILES} JSON files. Signaling workers to stop.")
                stop_crawling_event.set()
        except IOError as e:
            print(f"Error saving data for {url}: {e}")

def worker():
    while True:
        if stop_crawling_event.is_set():
            break

        try:
            url = url_queue.get(timeout=5)
            if url is None:
                url_queue.task_done()
                break

            with lock:
                if url in crawled_urls:
                    url_queue.task_done()
                    continue
                crawled_urls.add(url)

            print(f"Crawling: {url}")

            if not is_allowed(url):
                print(f"Skipping {url} due to robots.txt")
                url_queue.task_done()
                continue

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                time.sleep(CRAWL_DELAY_SECONDS)

                soup = BeautifulSoup(response.text, 'html.parser')

                title = soup.title.string if soup.title else "No Title"
                text_content = soup.get_text(separator=' ', strip=True)

                extracted_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    parsed_full_url = urlparse(full_url)

                    if parsed_full_url.scheme in ['http', 'https']:
                        initial_domain = urlparse(START_URLS[0]).netloc if START_URLS else ""
                        if parsed_full_url.netloc == initial_domain and full_url not in crawled_urls:
                            with lock:
                                if full_url not in crawled_urls:
                                    url_queue.put(full_url)
                                    extracted_links.append(full_url)

                save_data(url, title, text_content, extracted_links)

            except requests.exceptions.RequestException as e:
                print(f"Request error for {url}: {e}")
            except Exception as e:
                print(f"An error occurred while processing {url}: {e}")
            finally:
                url_queue.task_done()
        except queue.Empty:
            if stop_crawling_event.is_set():
                print("Queue empty and stop event set, worker stopping.")
                break
            else:
                print("Queue temporarily empty, worker waiting...")
                time.sleep(1)
        except Exception as e:
            print(f"Worker experienced an unexpected error: {e}")
            url_queue.task_done()

if __name__ == "__main__":
    ensure_output_dir()

    start_url_input = input("Enter the starting URL for crawling (e.g., http://quotes.toscrape.com/): ").strip()
    if not start_url_input:
        print("No URL entered. Exiting.")
        exit()
    START_URLS = [start_url_input]

    while True:
        try:
            max_files_input = input("Enter the maximum number of JSON files to crawl (enter 0 for unlimited): ").strip()
            max_files = int(max_files_input)
            if max_files < 0:
                print("Please enter a non-negative number.")
            else:
                MAX_JSON_FILES = max_files if max_files != 0 else -1
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    for url in START_URLS:
        url_queue.put(url)

    threads = []
    for _ in range(NUM_WORKERS):
        t = threading.Thread(target=worker)
        t.daemon = True
        threads.append(t)
        t.start()

    while not stop_crawling_event.is_set() or not url_queue.empty():
        try:
            url_queue.join(timeout=1)
        except Exception:
            pass

        if stop_crawling_event.is_set() and url_queue.empty():
            print("Stop event set and queue is empty. Initiating worker shutdown.")
            break

    for _ in range(NUM_WORKERS):
        url_queue.put(None)

    for t in threads:
        t.join()

    print("Crawling finished.")
    print(f"Total unique URLs crawled: {len(crawled_urls)}")
    print(f"Total JSON files saved: {json_files_saved_count}")
