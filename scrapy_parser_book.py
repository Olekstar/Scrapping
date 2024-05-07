import scrapy
from scrapy.crawler import CrawlerProcess

class BooksGraberPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["rating"] = adapter["rating"].replace("One", "1").replace("Two", "2").replace("Three", "3").replace("Four", "4").replace("Five", "5")
        return item
    
    # def close_spider(self, spider):
    #     with open("books_scrapy.csv", "w") as file:
    #         f.write ("title,link,price,thumbnail,rating\n")
    #         for book in spider.book_list:
    #             f.write(f"{book['title']},{book['link']},{book['price']},{book['thumbnail']},{book['rating']}\n")

class GetBooksSpider(scrapy.Spider):
    name = "get_books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    custom_settings = {
        "FEEDS": {"books_scrapy.csv": {"format": "csv", "overwrite": True}},
        "FEED_EXPORT_ENCODING": "utf-8",
        "ITEM_PIPELINES": {"books_graber.books_graber.pipelines.BooksGraberPipeline": 300},
    }

    def parse(self, response, **kwargs):
        cards = response.css("article.product_pod")

        for card in cards:
            yield {
                "title": card.css("h3 a::attr(title)").get(),
                "link": card.css("h3 a::attr(href)").get(),
                "price": card.css("p.price_color::text").get(),
                "thumbnail": card.css("img::attr(src)").get(),
                "rating": card.css("p.star-rating::attr(class)").get()[12:]
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(GetBooksSpider)
    process.start()