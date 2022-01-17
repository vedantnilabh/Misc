import requests
url = 'https://www.allsides.com/media-bias/media-bias-ratings'
r = requests.get(url)
print(r.content[:100])
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')
#Our data is located in a table inside a tbody tag further under a tr tag, which is what we need to select
rows = soup.select('tbody tr')
# We now have a list of rows, each contaning 4 cells, source name and link, bias data, agreement buttons, and community data
# Let's start with the first column, the source name and link
row = rows[0]
name = row.select_one('.source-title').text.strip()
print(name)

# selecting title with anchor tag so we can fet the link as well
allsides_page = row.select_one('.source-title a')['href']
allsides_page = 'https://www.allsides.com' + allsides_page
print(allsides_page)

# retrieving the bias rating from the link, because the format is simple, we can just split the string and get the last element
bias = row.select_one('.views-field-field-bias-image a')['href']
bias = bias.split('/')[-1]
print(bias)

# scraping the agree/disagree ratio from the community data
agree = row.select_one('.agree').text
agree = int(agree)

disagree = row.select_one('.disagree').text
disagree = int(disagree)

agree_ratio = agree / disagree

print(f"Agree: {agree}, Disagree: {disagree}, Ratio {agree_ratio:.2f}")

# We can't retrieve the degree of agreement because it is in javascript
print(row.select_one('.community-feedback-rating-page'))
# WE can manually recreate this by by manually finding the logic they are using, and we can then makea function
# to imitate this
def get_agreeance_text(ratio):
    if ratio > 3:
        return "absolutely agrees"
    elif 2 < ratio <= 3:
        return "strongly agrees"
    elif 1.5 < ratio <= 2:
        return "agrees"
    elif 1 < ratio <= 1.5:
        return "somewhat agrees"
    elif ratio == 1:
        return "neutral"
    elif 0.67 < ratio < 1:
        return "somewhat disagrees"
    elif 0.5 < ratio <= 0.67:
        return "disagrees"
    elif 0.33 < ratio <= 0.5:
        return "strongly disagrees"
    elif ratio <= 0.33:
        return "absolutely disagrees"
    else:
        return None


print(get_agreeance_text(2.5))

# creating a loop that gets data from every row on the first page
data = []
for row in rows:
    d = {}
    d['name'] = row.select_one('.source-title').text.strip()
    d['allsides_page'] = 'https://www.allsides.com' + row.select_one('.source-title a')['href']
    d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]
    d['agree'] = int(row.select_one('.agree').text)
    d['disagree'] = int(row.select_one('.disagree').text)
    d['agree_ratio'] = d['agree'] / d['disagree']
    d['agreeance_text'] = get_agreeance_text(d['agree_ratio'])

    data.append(d)
print(data[0])

# requesting multiple pages
pages = [
    'https://www.allsides.com/media-bias/media-bias-ratings',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=1',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=2'
]
# based on the robots.txt file, we need to wait 10 seconds between each request
from time import sleep
data = []

for page in pages:
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('tbody tr')

    for row in rows:
        d = {}
        d['name'] = row.select_one('.source-title').text.strip()
        d['allsides_page'] = 'https://www.allsides.com' + row.select_one('.source-title a')['href']
        d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]
        d['agree'] = int(row.select_one('.agree').text)
        d['disagree'] = int(row.select_one('.disagree').text)
        d['agree_ratio'] = d['agree'] / d['disagree']
        d['agreeance_text'] = get_agreeance_text(d['agree_ratio'])

        data.append(d)

    sleep(10)

# Let's also get the real url to the news source
website = soup.select_one('.www')['href']

# Using a loop to get the urls of all the pages while throwing an error if the page is not found
# Also includes a progress bar, because this will take about 44 minutes to run (10 seconds per page for 256 pages)
from copy import deepcopy
from tqdm import tqdm_notebook

for d in tqdm_notebook(data):
    r = requests.get(d['allsides_page'])
    soup = BeautifulSoup(r.content, 'html.parser')

    try:
        website = soup.select_one('.www')['href']
        d['website'] = website
    except TypeError:
        pass

    sleep(10)

# saving our data
import json
with open('allsides_data.json', 'w') as f:
    json.dump(data, f)

#If we want to load our data
with open('allsides_data.json', 'r') as f:
    data = json.load(f)

# data analysis - using list comprehension to get the sources with absolutely agrees for community feedback
# relative to the bias as per the website
abs_agree = [d for d in data if d['agreeance_text'] == 'absolutely agrees']

print(f"{'Outlet':<20} {'Bias':<20}")
print("-" * 30)

for d in abs_agree:
    print(f"{d['name']:<20} {d['bias']:<20}")

# Let's use pandas to make our lives easier
import pandas as pd
df = pd.read_json('allsides_data.json')
df.set_index('name', inplace=True)
print(df.head())

print(df[df'agreeance_text'] = = 'strongly disagrees']

df['total_votes'] = df['agree'] + df['disagree']
df.sort_values('total_votes', ascending=False, inplace=True)

df.head(10)

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df2 = df.head(25).copy()
print(df2.head())

fig, ax = plt.subplots(figsize=(20, 10))

ax.bar(df2.index, df2['agree'], color='#5DAF83')
ax.bar(df2.index, df2['disagree'], bottom=df2['agree'], color='#AF3B3B')

ax.set_ylabel = 'Total feedback'

plt.yticks(fontsize='x-large')
plt.xticks(rotation=60, ha='right', fontsize='x-large', rotation_mode='anchor')

plt.legend(['Agree', 'Disagree'], fontsize='xx-large')
plt.title('AllSides Bias Rating vs. Community Feedback', fontsize='xx-large')
plt.show()

df3 = df.copy()

fig = plt.figure(figsize=(15, 15))

biases = df3['bias'].unique()

for i, bias in enumerate(biases):
    # Get top 10 news sources for this bias and sort index alphabetically
    temp_df = df3[df3['bias'] == bias].iloc[:10]
    temp_df.sort_index(inplace=True)

    # Get max votes, i.e. the y value for tallest bar in this temp dataframe
    max_votes = temp_df['total_votes'].max()

    # Add a new subplot in the correct grid position
    ax = fig.add_subplot(len(biases) / 2, 2, i + 1)

    # Create the stacked bars
    ax.bar(temp_df.index, temp_df['agree'], color='#5DAF83')
    ax.bar(temp_df.index, temp_df['disagree'], bottom=temp_df['agree'], color='#AF3B3B')

    # Place text for the ratio on top of each bar
    for x, y, ratio in zip(ax.get_xticks(), temp_df['total_votes'], temp_df['agree_ratio']):
        ax.text(x, y + (0.02 * max_votes), f"{ratio:.2f}", ha='center')

    ax.set_ylabel('Total feedback')
    ax.set_title(bias.title())

    # Make y limit larger to compensate for text on bars
    ax.set_ylim(0, max_votes + (0.12 * max_votes))

    # Rotate tick labels so they don't overlap
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

plt.tight_layout(w_pad=3.0, h_pad=1.0)
plt.show()




