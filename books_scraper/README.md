# Books Scraper

Quick Scrapy demo that pulls book data from a single site and exports at least 500 rows per run while staying respectful to the target website.

## Website Used
- **Base URL:** https://books.toscrape.com/

## Fields Extracted
- title  
- price  
- rating (the textual rating scraped from the star CSS classes)  
- stock availability  
- product detail page link  
- image URL  

## Total Records Collected
- The spider grabs **500** records before shutting down (change `item_goal` in `books_scraper/spiders/books.py` if you need a different number).

## Pagination Method
- Each listing page exposes a `li.next` link. The spider follows that link with `response.follow(next_page, callback=self.parse)` until the quota is met, so pagination is automatic—no hard-coded page counts.

## Challenges & Fixes
- Tuning request speed without crawling at a snail’s pace. I settled on a one-second delay and Scrapy’s AutoThrottle to keep the demo site happy while still finishing quickly. That balance took a couple of test runs.

## Step-by-Step: Run the Script
1. **Set up / activate the virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   (If the `.venv` folder is already in place, just activate it.)

2. **Install dependencies (first run only)**
   ```bash
   pip install --upgrade pip
   pip install scrapy
   ```

3. **Run the spider for JSON output**
   ```bash
   cd books_scraper
   scrapy crawl books -O output/books.json
   ```

4. **Optional: export to CSV instead**
   ```bash
   scrapy crawl books -O output/books.csv
   ```

5. **Check your data**
   - Open the file in `output/` and confirm you see 500 rows with the fields above.

## Project Structure
- `books_scraper/spiders/books.py` – spider logic, pagination, and item parsing.
- `books_scraper/settings.py` – global throttling/retry defaults.
- `output/` – where the JSON/CSV exports land.

That’s the whole flow. Activate the env, run the command, and you’ve got a clean dataset. Adjust the delay or quota if you want to experiment further.*** End Patch



