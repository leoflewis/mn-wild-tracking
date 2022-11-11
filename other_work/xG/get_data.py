import hockey_scraper, pandas


print("Begining to scrape pbp. No shifts.")
data = hockey_scraper.scrape_games([2022020210], False, data_format='Pandas')
print("Finished scraping.")
print(data)

