# Hacker News Roundup Generator
# Version 0.1.0

import operator

import time

from pick import pick
from textblob import TextBlob
from tqdm import trange

import functions as fn
import goodies
import variables

# 0. Asking for user preferences ============================================
variables.usr_option, variables.usr_index = pick(
    variables.usr_options, variables.options["selection_prompt"]
)

fn.set_options(variables.usr_index)

# debug measure
if variables.options["debug"]:
    print(variables.usr_option)
    print(variables.options["opt_mood_happy"])
    print(variables.options["opt_polarity_threshold"])

# 1. Let's see how long it takes to run the code ============================
variables.start_time = time.time()

fn.cls()  # first, clear the screen

# debug measure
if not variables.options["debug"]:
    goodies.echo_badge()  # For aesthetic purposes only @-}


# 2. Scraping Process =======================================================
list_t, list_u = fn.hn_scraper("https://news.ycombinator.com/news")
variables.final_list = list(
    zip(list_t, list_u)
)  # The zip() function takes iterables (can be zero or more), aggregates them in a ==tuple==, and returns it.

if variables.options["pages_to_scrape"] > 1:  # Scraping more pages
    for x in trange(
        variables.options["pages_to_scrape"] - 1,
        desc="🧹 Scraping HN",
        total=variables.options["pages_to_scrape"],
    ):
        list_t, list_u = fn.hn_scraper(f"https://news.ycombinator.com/news?p={x+2}")
        variables.final_list = variables.final_list + list(zip(list_t, list_u))

fn.cls()  # again, clear the screen

# 3. SA Process =============================================================
for index, item in enumerate(variables.final_list):
    sa = TextBlob(str(variables.final_list[index][0]))
    comp = operator.ge if variables.options["opt_mood_happy"] else operator.le

    if comp(sa.polarity, variables.options["opt_polarity_threshold"]):
        new_item_dict = {
            "title": variables.final_list[index][0],
            "url": variables.final_list[index][1],
            "polarity": sa.polarity,
        }
        variables.filtered_list.append(new_item_dict)

# Sorting filtered list by polarity descendingly
variables.filtered_list_sorted = sorted(
    variables.filtered_list, key=lambda c: c["polarity"], reverse=True
)

# 4. Report Generation ======================================================

if not fn.report_generator(variables.options["report_filename"]):
    print("Failed to generate the output.")

# 5. Final Prompt ==========================================================
if variables.options["debug"]:
    for item in variables.filtered_list_sorted:
        print(f"Polarity {item['polarity']}: {item['title']}")
        print(f"URL: {item['url']}")

    print("\n▐░░░░ Summary Reports")
    print(f"▐░░░░░ Total filtered items: {len(variables.filtered_list)}\n")
else:
    goodies.echo_badge_end()  # For aesthetic purposes only @-}

print("\nYou can find your report via: " + variables.options["report_filename"])
print(
    "\n▐░░ Processs finished in: %s seconds"
    % round((time.time() - variables.start_time), 3)
)
print(f"▐░░ Total items processed: {len(variables.final_list)}")
