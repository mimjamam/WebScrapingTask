import scrapy
from scrapy.exceptions import CloseSpider


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1.0,
        "AUTOTHROTTLE_MAX_DELAY": 3.0,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    item_goal = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items_scraped = 0

    def parse(self, response, **kwargs):
        for book in response.css("article.product_pod"):
            item = self.extract_book(book, response)
            self.items_scraped += 1
            yield item

            if self.items_scraped >= self.item_goal:
                raise CloseSpider(reason="item_goal_reached")

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
                errback=self.handle_error,
            )

    def extract_book(self, book, response):
        title = book.css("h3 a::attr(title)").get()
        price_text = book.css("p.price_color::text").get()
        rating_class = book.css("p.star-rating::attr(class)").get()
        availability_text = book.css("p.instock.availability::text").getall()
        detail_url = book.css("h3 a::attr(href)").get()
        image_url = book.css("div.image_container img::attr(src)").get()

        rating = None
        if rating_class:
            rating_words = rating_class.split()
            rating = rating_words[1] if len(rating_words) > 1 else None

        cleaned_price = price_text.replace("Â", "").strip() if price_text else None
        cleaned_availability = (
            " ".join(text.strip() for text in availability_text if text.strip())
            if availability_text
            else None
        )

        return {
            "title": title,
            "price": cleaned_price,
            "rating": rating,
            "stock": cleaned_availability,
            "product_page_url": response.urljoin(detail_url) if detail_url else None,
            "image_url": response.urljoin(image_url) if image_url else None,
        }

    def handle_error(self, failure):
        self.logger.error("Request failed: %s", failure)

