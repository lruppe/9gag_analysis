import random
from collections import defaultdict
from typing import Generator

import pandas as pd
from waybackpy import WaybackMachineCDXServerAPI


# response = requests.get('http://archive.org/wayback/available?url=http://9gag.com/&timestamp=201900602021852').json()
# print(response['url'])
# print(response)
# post_url = response['archived_snapshots']['closest']['url']
#
#
# response = requests.get(post_url).content
# pprint.pprint(response)

def get_snapshots(url: str, start, end) -> Generator:
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    cdx = WaybackMachineCDXServerAPI(url, user_agent, start_timestamp=start, end_timestamp=end)
    return cdx.snapshots()

def get_snapshot_for_year(url: str, year) -> list:
    return list(get_snapshots(url=url, start=year, end=year))

def print_stats(snapshots: list, title : str):
    snaps_per_day = defaultdict(int)
    for item in snapshots:
        key = item.datetime_timestamp.date()
        snaps_per_day[key] += 1
    total_snapshots = sum(snaps_per_day.values())
    total_days = len(snaps_per_day.keys())
    avg = total_snapshots / total_days if total_days > 0 else 0
    print(title)
    print(f'Total snapshots: {total_snapshots}')
    print(f'Nr of days: {total_days}')
    print(f'Average snaps per day: {avg}')
    print('#############################################')


def get_samples(snapshots : list, sample_size: int) -> list:
    snaps_by_date = defaultdict(list)
    for snap in snapshots:
        date = snap.datetime_timestamp.date()
        snaps_by_date[date].append(snap)

    samples = []
    for date, entries in snaps_by_date.items():
        nr_samples = min(sample_size, len(entries))
        current_samples = random.sample(entries, nr_samples)
        for sample in current_samples:
            samples.append(sample)
    return samples

if __name__ == '__main__':
    url = "http://9gag.com/"
    nr_of_samples = 2
    snapshots = []
    for year in range(2014, 2026):
        snapshots_per_year = get_snapshot_for_year(url, year)
        print_stats(snapshots_per_year, 'Total Snaps')
        snapshots_per_year = [snap for snap in snapshots_per_year if snap.statuscode == '200']
        sampled_snaps = get_samples(snapshots_per_year, nr_of_samples)
        print_stats(sampled_snaps, '2 Snaps per day')
        sampled_snaps = [(sample.timestamp,sample.archive_url) for sample in sampled_snaps]
        snapshots.extend(sampled_snaps)

    df = pd.DataFrame(snapshots, columns=['Timestamp', 'URL'])
    df.to_csv('url_per_day.csv', index=False)


