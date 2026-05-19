import csv
import time
from time import strftime, localtime

import requests
from bs4 import BeautifulSoup

WIKIPEDIA_ROOT = "https://en.wikipedia.org"
BREAKING_BAD_EPISODES = "https://en.wikipedia.org/wiki/List_of_Breaking_Bad_episodes"
HEADERS = {"User-Agent": "BreakingBadScraperBot/0.1.0 (https://github.com/harriebird/breaking-bad-scraper) breaking-bad-scraper/0.1.0"}
SCRAPE_TIMESTAMP = strftime("%Y%m%d-%H%M%S", localtime())

csv_file = open(f'scrape-{SCRAPE_TIMESTAMP}.csv', 'a')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(['episode', 'title', 'plot', 'link'])

response = requests.get(BREAKING_BAD_EPISODES, headers=HEADERS)

if response.ok:
    soup = BeautifulSoup(response.content, "html.parser")
    episodes = soup.find_all("td", {"class": "summary"})
    episode_number = 1
    for episode in episodes:
        if episode.find("a"):
            time.sleep(1)
            episode_route = episode.find("a")["href"]
            episode_title = episode.find("a").text
            episode_link = f"{WIKIPEDIA_ROOT}{episode_route}"
            response = requests.get(episode_link, headers=HEADERS)
            if response.ok:
                soup = BeautifulSoup(response.content, "html.parser")
                plot_heading = soup.find("h2", {"id": "Plot"}).parent
                current_element = plot_heading.find_next_sibling()
                plot_text = ""
                while current_element.name == "p" or current_element.name == "figure":
                    if current_element.name == "figure":
                        current_element = current_element.find_next_sibling()
                        continue

                    plot_text += current_element.text
                    current_element = current_element.find_next_sibling()

                csv_writer.writerow([episode_number, episode_title, plot_text, episode_link])
            print(f"Episode {episode_number}: {episode_title} was successfully added!")
            episode_number += 1

csv_file.close()
print("Scraping done! enjoy!")
