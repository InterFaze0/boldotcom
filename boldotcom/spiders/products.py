import scrapy
import time

class ProductsSpider(scrapy.Spider):
    name = "products"
    
    def start_requests(self):
        yield scrapy.Request('https://www.bol.com/nl/nl/w/alle-artikelen-easyup/1817090/?sort=wishListRank1',meta={'playwright':True})

    productList = []
    def parse(self, response):
        for item in response.css("a[class='product-title px_list_page_product_click list_page_product_tracking_target']::attr(href)"):
            yield response.follow(item.get(),callback = self.parse_detail)
        
        #PAGINATION
    def parse_detail(self,response):
        itemTitle = response.css("span[class = 'u-mr--xs']::text").get()
        itemPrice = response.css("span[class = 'promo-price']::text").get().strip() + "," + response.css("sup[class='promo-price__fraction']::text").get()

        for i in response.css("div[class = 'specs__row']"):
            if i.css("dt[class='specs__title']::text").get().strip()=="EAN":
                itemEan =i.css("dd[class='specs__value']::text").get().strip()
                break
        yield {
            'TITLE':itemTitle,
            'Price':itemPrice,
            'EAN':itemEan
        }
        
     