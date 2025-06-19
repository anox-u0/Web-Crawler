# 🔗 Distributed Web Crawler

A Python-based **distributed web crawler** designed to efficiently crawl a large number of websites in parallel. It handles politeness towards web servers, implements basic error handling with retries, and stores the extracted data in JSON files.

---

## ✨ Features

* **⚙️ Configurable Settings**
  Core crawler settings are loaded from `config.json`, including:

  * `num_workers`: Number of concurrent threads
  * `crawl_delay_seconds`: Delay between requests to the same domain
  * `max_retries`: Retry attempts for failed requests
  * `retry_backoff_factor`: Exponential backoff multiplier
    A default `config.json` is generated if one doesn't exist.

* **🔎 Configurable Start URL**
  Specify the starting URL via terminal input when running the script.

* **🔢 JSON File Limit**
  Control how many pages to crawl by setting a maximum JSON file count (or enter `0` for unlimited).

* **⚡ Parallel Processing**
  Uses Python’s `threading` module to simulate a distributed crawler across multiple workers on a single machine.

* **🤝 Politeness & Rate Limiting**

  * Respects `robots.txt` to avoid disallowed paths.
  * Enforces a configurable delay between requests to avoid overwhelming servers.

* **🛡️ Enhanced Error Handling**
  Features a retry mechanism with exponential backoff for improved reliability against network issues.

* **🌐 Cross-Domain Crawling**
  Follows HTTP and HTTPS links across different domains for broader exploration.

* **📝 Data Extraction**
  For each crawled page, the following information is extracted:

  * Page URL
  * Title
  * Plain text content
  * All discoverable HTTP/HTTPS links

* **📄 JSON Output**
  Saves each crawled page to an individual `.json` file in a `crawled_data/` directory.

* **⏰ Formatted Timestamps**
  Each JSON file includes a timestamp in human-readable format (e.g., `19 June 13:45:30`).

---

## 🚀 How to Run

### ✅ Prerequisites

Ensure you have **Python 3** installed and the required libraries:

```bash
pip install requests beautifulsoup4
```

### 🔹 Execution Steps

1. **Save the Code**
   Save the crawler script as `crawler.py` (or any `.py` file).

2. **Open Terminal**
   Navigate to the directory containing the script.

3. **Run the Script**

```bash
python crawler.py
```

4. **Configuration File**
   On first run, a `config.json` file is auto-generated in the same directory. You can edit it to customize:

```json
{
  "num_workers": 5,
  "crawl_delay_seconds": 1,
  "max_retries": 3,
  "retry_backoff_factor": 0.5
}
```

5. **Follow Prompts**

   * Enter the starting URL (e.g., `http://quotes.toscrape.com/`)
   * Enter the maximum number of JSON files to crawl (enter `0` for unlimited)

The crawler will begin processing and display its progress in the terminal.

---

## 📂 Output

All crawled pages are saved under a `crawled_data/` directory. Each `.json` file includes:

```json
{
  "url": "http://quotes.toscrape.com/",
  "title": "Quotes to Scrape",
  "text_content": "Quotes to Scrape...",
  "extracted_links": [
    "http://quotes.toscrape.com/page/1/",
    "http://quotes.toscrape.com/page/2/"
  ],
  "timestamp": "19 June 13:45:30"
}
```
---
