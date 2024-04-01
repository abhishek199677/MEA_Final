import pandas as pd
from scrapy import Spider, Request, FormRequest
from scrapy.crawler import CrawlerProcess

class EamVisitsSpider(Spider):
    name = 'eam_visit'
    page_number = 1  # Initialize page_number

    def __init__(self):
        self.base_url = "https://www.mea.gov.in/eam-visits.htm"
        self.data = []

    def start_requests(self):
        yield Request(
            url=self.base_url,
            callback=self.parse,
            meta={'page_number': self.page_number}
        )

    def parse(self, response):
        page_number = response.meta.get('page_number', 1)
        titles = response.css("#innerContent a::text").extract()
        self.data.append(titles)

        print(f"Page {page_number} titles: {titles}")

        next_button_disabled = response.css('input#ContentPlaceHolder1_EAMVisitsMap1_CustomPager1_ibtnMoveNext[disabled]').get() is not None

        if not next_button_disabled:
            page_number += 1
            yield FormRequest.from_response(
                response,
                callback=self.parse,
                formdata={
                    'ctl00$ContentPlaceHolder1$EAMVisitsMap1$CustomPager1$ibtnMoveNext': 'Next',
                },
                meta={'page_number': page_number}
            )
        else:
            self.save_to_csv()

            pass

    def save_to_csv(self):
        flat_data = [item for sublist in self.data for item in sublist]
        clean_data = [title.strip() for title in flat_data if title.strip()]
        data = pd.DataFrame({'titles': clean_data})
        
        folder_path = r"C:\Users\putta\OneDrive\Desktop\My_Projects\Project\eam_visits_output.csv"
        data.to_csv(folder_path, index=False)

# Main function to run the scraper
def main():
    process = CrawlerProcess()
    process.crawl(EamVisitsSpider)
    process.start()

if __name__ == "__main__":
    main()
