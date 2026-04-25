import csv
import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_html(url: str):
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Attempt failed for URL: {url} with error: {e}")



def extract_data_from_new_format(url: str) -> list:
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the embedded script data
    script_tag = soup.find('script', text=re.compile(r'data\s*=\s*\{'))
    script_content = script_tag.string if script_tag else ''

    # Use regex to extract JSON data
    data_match = re.search(r'data\s*=\s*(\{.*?\});', script_content, re.DOTALL)
    data_json = json.loads(data_match.group(1)) if data_match else {}

    posts_data = data_json.get('posts', [])

    # Extract required fields
    posts_info = []

    for post in posts_data:
        post_info = {
            'url': f"https://9gag.com/gag/{post['id']}",
            'likes': post.get('upVoteCount', 0),
            'comments': post.get('commentsCount', 0),
            'nsfw': bool(post.get('nsfw', 0))
        }
        posts_info.append(post_info)

    # Print extracted data
    for post in posts_info:
        print(post)


def extract_data_from_old_format(url: str) -> list:
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article')
    print(f'Posts: {len(articles)} for URL: {url}')
    article_data = []

    for article in articles:
        data_entry_id = article.get('data-entry-id')
        data_entry_url = article.get('data-entry-url')
        data_entry_votes = article.get('data-entry-votes')
        data_entry_comments = article.get('data-entry-comments')

        # Check for NSFW indicator
        nsfw_indicator = bool(article.find('div', class_='nsfw-post'))

        article_info = {
            'data-entry-id': data_entry_id,
            'data-entry-url': data_entry_url,
            'data-entry-votes': data_entry_votes,
            'data-entry-comments': data_entry_comments,
            'nsfw_indicator': nsfw_indicator
        }

        article_data.append(article_info)
    return article_data

def append_posts_to_csv(posts: list):
    posts_df = pd.DataFrame(posts)
    posts_df.to_csv('posts/posts.csv', index=False, mode='a', header=False, quoting=csv.QUOTE_ALL)

def save_finished_urls(urls: list):
    with open('posts/finished_urls.txt', 'a') as f:
        for url in urls:
            f.write(url + '\n')
def read_urls_to_list(file_path: str) -> list:
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f]
    return urls


if __name__ == '__main__':
    extract_data_from_new_format("https://web.archive.org/web/20171222070220/https://9gag.com/")

    # df = pd.read_csv("snapshots/url_per_day.csv")
    # sleep_amount = 80
    # request_amount = 10
    # posts = []
    # finished_urls = []
    # previous_urls = read_urls_to_list('posts/finished_urls.txt')
    # requests_count = 0
    #
    #
    #
    # for index, row in df.iterrows():
    #     url = row['URL']
    #     timestamp = row['Timestamp']
    #
    #     if url in previous_urls:
    #         print(f"Skipping URL {url} as it has already been processed.")
    #         continue
    #
    #     if requests_count >= request_amount:
    #         print(f"Pausing code execution. Sleeping for {sleep_amount} seconds.")
    #         append_posts_to_csv(posts)
    #         save_finished_urls(finished_urls)
    #         posts = []
    #         finished_urls = []
    #         time.sleep(sleep_amount)
    #         requests_count = 0
    #
    #     try:
    #         posts_per_day = extract_data_from_old_format(url)
    #         requests_count += 1
    #         for post in posts_per_day:
    #             post['timestamp'] = timestamp
    #         posts.extend(posts_per_day)
    #         finished_urls.append(url)
    #     except Exception as e:
    #         print(f"Failed to process URL {url}: {e}")
    #         print(f"Rate limit reached. Sleeping for additional {sleep_amount} seconds.")
    #         time.sleep(sleep_amount)
    #
    # append_posts_to_csv(posts)

