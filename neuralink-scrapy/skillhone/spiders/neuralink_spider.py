import scrapy
from scrapy.selector import Selector
from skillhone.items import SkillhoneItem
import csv

class NeuralinkSpider(scrapy.Spider):
    name = "neuralink"

    allowed_domains = ["neuralink.com", "boards.greenhouse.io", "greenhouse.io"]
    start_urls = [
        "https://boards.greenhouse.io/neuralink",
    ]

    def parse(self, response):
        positions = Selector(response).xpath('//*[@id="main"]/section/div')

        for position in positions:
            print(position.xpath('a/text()').extract()[0])
            href = position.xpath('a/@href').extract()[0]

            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parse_dir_contents)

    def parse_dir_contents(self, response):
        dictionary = dict()

        # Different Fromats :(
        sentences = Selector(response).xpath('//*[@id="content"]/ul/li/span')
        if (len(sentences) == 0):
            sentences = Selector(response).xpath('//*[@id="content"]/div[3]/div/ul/li')
        if (len(sentences) == 0):
            sentences = Selector(response).xpath('//*[@id="content"]/div[2]/div/div/div[1]/ul/li')
        if (len(sentences) == 0):
            sentences = Selector(response).xpath('//*[@id="content"]/div[2]/div/div/div/div/ul/li')
        if (len(sentences) == 0):
            sentences = Selector(response).xpath('//*[@id="content"]/ul/li')

        # Just using the item class
        item = SkillhoneItem()
        item['title'] = Selector(response).xpath('//*[@id="header"]/h1/text()').extract()[0]

        # Loop sentences
        for sentence in sentences:
            text = sentence.xpath('text()').extract()[0]
            # print(text)
            ## Seperate words that have special characters
            text = text.strip().lower().replace("," , " ").replace("/" , " ").split(" ")
            for word in text:
                ## Remove special characters
                w = word.replace("," , "").replace("/" , "").replace(")" , "").replace("(" , "").replace("." , "").replace("!" , "")
                # print(w)
                if w in dictionary:
                    dictionary[w] = dictionary[w] + 1
                else:
                    dictionary[w] = 1
        
        ## Write to csv
        with open('../results/Neuralink.csv', 'a+') as f:  
            writer = csv.writer(f)
            for k, v in dictionary.items():
                writer.writerow([k, v])

        yield item