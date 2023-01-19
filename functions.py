import os
import sys
import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import requests as req
from bs4 import BeautifulSoup as BS

import template
import variables


### Function Defenitions @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def set_options(usr_index):
    """This function evaluates user selected type of retrieval.

    Args:
        usr_index (int): The index of the selected prompt from pick.

    Returns:
        None.
    """
    if usr_index == 0:
        variables.options["opt_polarity_threshold"] = 0.8
    elif usr_index == 1:
        variables.options["opt_polarity_threshold"] = 0.5
    elif usr_index == 2:
        variables.options["opt_mood_happy"] = False
        variables.options["opt_polarity_threshold"] = -0.2
    else:
        sys.exit()


def hn_scraper(url):
    """This scraper function is used to scrape HN website.

    Args:
        url (string): a HN URL.

    Returns:
        list: lists of titles and urls.
    """
    webpage = req.get(url)

    soup = BS(webpage.content, "html.parser")

    list_titles = []
    list_urls = []

    for p in soup.select(".athing"):
        for item in p.select("span.titleline > a"):

            item_url = item.get("href")
            item_title = item.text

            if not item_url.startswith("http"):  # Fixing internal links
                item_url = internal_link_compiler(item_url)

            list_titles.append(item_title)
            list_urls.append(item_url)

    return list_titles, list_urls


def internal_link_compiler(url):
    """This fixes HN internal links.

    Args:
        url (string): an internal HN endpoint; e.g. "item?id=34342890".

    Returns:
        string: a functional URL pointing to the page on HN.
    """

    return "https://news.ycombinator.com/" + url


def report_generator(filename):
    """Generates a report with a chart inside of a markdown file.

    Args:
        filename(string): export filename.

    Returns:
        bool: True for success or False for failure.
    """

    # Chart generator
    y = np.array(
        [
            len(variables.final_list) - len(variables.filtered_list_sorted),
            len(variables.filtered_list_sorted),
        ]
    )
    mylabels = ["", f"Highlights (n={len(variables.filtered_list_sorted)})"]
    myexplode = [0.2, 0]

    plt.pie(y, labels=mylabels, explode=myexplode)
    plt.savefig(variables.options["chart_filename"])

    # And saving the report
    with open(filename, "w", encoding="UTF-8") as f:
        f.write(template.report_header)
        f.write(f"*{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        f.write(f"{variables.usr_option}\n")
        f.write(f"## 🗞️ Headlines\n")
        f.write(
            f"> Here's your curated list of {len(variables.filtered_list)} item(s) out of {len(variables.final_list)}:\n\n"
        )
        for item in variables.filtered_list_sorted:
            f.write(f"1. {item['title']}\n")
            f.write(f"{item['url']}\n\n")
        f.write(f"### 📊 Graph\n")
        f.write(f"![Visualization]({variables.options['chart_filename']})\n\n")
        f.write(f"***\n")
        f.write(
            "▐░░ Processs finished in: %s seconds\n"
            % round((time.time() - variables.start_time), 3)
        )
    return True


def cls():
    """Clears the screen.

    Args:
        None.

    Returns:
        None.
    """
    os.system("cls" if os.name == "nt" else "clear")
