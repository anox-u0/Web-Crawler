# 🔗 Distributed Web Crawler

A Python-based **distributed web crawler** designed for efficient, parallel website crawling. It features polite crawling practices, rate limiting, multithreaded processing, and structured data output in JSON format.

---

## ✨ Features

* **🔎 Configurable Start URL**
  Specify the starting URL via the terminal when launching the script.

* **🔢 JSON File Limit**
  Control how many pages to crawl by setting a maximum JSON file limit (or enter `0` for unlimited).

* **⚡ Parallel Processing**
  Uses Python's `threading` module to simulate a distributed crawler across multiple workers.

* **🤝 Politeness & Rate Limiting**

  * Respects `robots.txt` to avoid restricted paths.
  * Includes configurable delay between requests to avoid overloading servers.

* **🔢 Data Extraction**
  For each page, extracts:

  * Page URL
  * Page title
  * Plain text content
  * All internal links

* **📄 JSON Output**
  Stores extracted data as separate `.json` files in a `crawled_data/` folder.

* **⏰ Formatted Timestamps**
  Each JSON file includes a human-readable timestamp (e.g., `19 June 13:45:30`).

---

## 🚀 How to Run

### ✅ Prerequisites

Make sure you have **Python 3** and the following libraries:

```bash
pip install requests beautifulsoup4
```

### 🔹 Execution Steps

1. **Save the Code**
   Save the crawler script as `crawler.py` (or any `.py` file).

2. **Open Terminal**
   Navigate to the script's directory.

3. **Run the Script**

```bash
python crawler.py
```

4. **Follow Prompts**

   * Enter the starting URL (e.g., `http://quotes.toscrape.com/`)
   * Enter the max number of JSON files (or `0` for unlimited)

The crawler will start and print progress logs in your terminal.

---

## 📂 Output

All crawled pages are saved under `crawled_data/`. Each file contains structured data:

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

## ⚠️ Limitations & Future Improvements

* **Single-Machine Simulation**
  Threading is used for concurrency on a single machine. For true distributed crawling, consider message brokers like **RabbitMQ** or **Kafka** with **Celery**.

* **Same-Domain Limitation**
  Crawling is limited to internal links. Cross-domain support can be added if needed.

* **No JavaScript Rendering**
  JavaScript-heavy sites aren't fully supported. Consider integrating **Selenium** or **Playwright** for dynamic content.

* **Basic Error Handling**
  Retry logic is minimal. Production-grade systems should include backoff strategies and dead-letter queues.

* **Hardcoded Configuration**
  Move settings like delays and worker count into a config file (`config.yaml`, `settings.toml`, etc.) for flexibility.

---
