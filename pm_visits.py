from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request, FormRequest
import csv
import pandas as pd

class Pm_visits(scrapy.Spider):
    name = 'pm_visit'
    page_number = 1  # Initialize page_number

    def __init__(self):
        self.base_url = "https://www.mea.gov.in/prime-minister-visits.htm"
        self.data = []

    def start_requests(self):        #starting the spider to making the initial request
        yield Request(
            url=self.base_url,
            callback=self.parse,
            meta={'page_number': self.page_number}

        )
    
    def parse(self, response):
        page_number = response.meta.get('page_number', 1)  # Retrieve page_number from metadata
        titles = response.css("#innerContent a::text").extract()
        self.data.append(titles)
        
        if not titles:
            print('file saved')
            self.save_to_csv()
            return
        print(f"Page {page_number} titles: {titles}")
        # print(f"Page {page_number} count: {len(titles)}")

        # Check if the "Next" button is enabled
        next_button_disabled = response.css('input#ctl00_ContentPlaceHolder1_PMVisitsMap1_CustomPager1_ibtnMoveNext[disabled]' ).get() is not None

        if not next_button_disabled:
            page_number += 1  # Increment page_number for the next request
            yield FormRequest.from_response(
                response,
                callback=self.parse,
                formdata={
                    'ctl00$ContentPlaceHolder1$PMVisitsMap1$CustomPager1$ibtnMoveNext': 'Next',
                },
                meta={'page_number': page_number}  # Pass the updated page_number as metadata
            )
        else:
            pass
        

    def save_to_csv(self):
    # Combine nested lists into a flat list 
        flat_data = [item for sublist in self.data for item in sublist]

        # Remove any empty strings
        clean_data = [title.strip() for title in flat_data if title.strip()]

        # Create a DataFrame from the cleaned data
        data = pd.DataFrame({'titles': clean_data})

        # Save the DataFrame to a CSV file
        folder_path = r"C:\Users\putta\OneDrive\Desktop\My_Projects\Project\pm_visits_output.csv"
        data.to_csv(folder_path, index=False)

        
       
        
# Main function to run scraper
def main():
    # Create a CrawlerProcess
    process = CrawlerProcess()
    process.crawl(Pm_visits)
    process.start()  # The script will block here until the crawling is finished

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
