options = {
    "selection_prompt": "What kind of headlines do you want to see today?",
    "pages_to_scrape": 20,  # Must be a num >= 1;
    "debug": False,  # Default False
    "opt_mood_happy": True,  # Default True
    "opt_polarity_threshold": 0.6,  # range [-1,1] Default 0.6
    "report_filename": "report.md",  # Default "report.md"
    "chart_filename": "chart.png",  # Default "chart.png"
}

usr_options = [
    "😍 Very happy! (fewer headlines)",
    "😇 Give me good ones. (more headlines)",
    "😶 Gloomy is fine! (peek into the dark side)",
    "🚪 Exit",
]

usr_option = ""  # Env Var
usr_index = ""  # Env Var
start_time = ""  # Env Var

final_list = []  # A list of tuples (title, url)
filtered_list = []  # A list of dictionaries of filtered results
filtered_list_sorted = []  # A sorted list of dictionaries of filtered results
