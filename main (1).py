import threading
import requests
from bs4 import BeautifulSoup
from queue import Queue
import time

# Thread-safe queue for URLs
url_queue = Queue()

# Lock for safe writing to shared storage
write_lock = threading.Lock()

# Storage file for crawled data
output_file = "crawled_data.txt"

# Crawler class
class WebCrawler(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        while not url_queue.empty():
            url = url_queue.get()
            try:
                print(f"Thread-{self.thread_id} crawling: {url}")
                self.crawl(url)
            except Exception as e:
                print(f"Thread-{self.thread_id} encountered an error with {url}: {e}")
            finally:
                url_queue.task_done()

    def crawl(self, url):
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # Parse the content
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            
            # Store the data
            with write_lock:
                with open(output_file, "a") as f:
                    f.write(f"URL: {url}\nTitle: {title}\n\n")
            print(f"Thread-{self.thread_id} successfully processed: {url}")
        else:
            print(f"Thread-{self.thread_id} failed with status code: {response.status_code}")

# Main function to set up and run the crawler
def main():
    # URLs to crawl (example)
    urls = [
        "https://example.com",
        "https://www.python.org",
        "https://www.wikipedia.org",
        "https://www.github.com",
    ]

    # Populate the queue
    for url in urls:
        url_queue.put(url)

    # Number of threads
    num_threads = 4

    # Start threads
    threads = []
    for i in range(num_threads):
        thread = WebCrawler(i)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("Crawling completed.")

if __name__ == "__main__":
    # Start the crawler
    main()

