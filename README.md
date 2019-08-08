## Raffle Ticket Checker

This project is a simple raffle ticket checker using Selenium WebDriver and Python 3.
The project checks the numbers of the Michigan Lotto Daily 3 evening drawing, and scrapes the dates for the Saturday drawing.  I used python Pandas to process the csv file into a DataFrame, then used the datetime.datetime library to select the dates that fall on Saturday.

This project can be modified to scrape other websites for a similar use.  To use this project, you need to install the ChromeDriver into your path, by copying it to /usr/local/bin.  You will need to change the site url, element id, class, and xpath to fit the site you are scraping.  

Watch the video for a [demo](#Raffle_Ticket_Checker.mp4)
