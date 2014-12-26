#!/usr/bin/env python

import json
import sys
import os
from datetime import datetime
import re

def organize_by_date(raw_data):
    entries = {} # by date
    for tweet in raw_data:
        date = tweet['created_at'].split()[0]
        entries[date] = entries.get(date, [])
        entries[date].append(tweet)
    return entries

def format_tweet(rawTweet):
    components = []
    text = rawTweet['text']
    # add URL to mentions
    mentionPattern = re.compile('@[\w]+')
    match = mentionPattern.search(text)
    while match:
        text = text[:match.start()] + '[{}](http://twitter.com/{})'.format(match.group(), match.group()[1:]) + text[match.end():]
        match = mentionPattern.match(text)
    # add timestamp
    userId = rawTweet['user']['screen_name']
    time = datetime.strptime(rawTweet['created_at'], '%Y-%m-%d %H:%M:%S %z')
    timestamp = "[[{}](https://twitter.com/{}/status/{})]".format(time.strftime('%H:%M:%S'), userId, rawTweet['id_str'])
    components = [timestamp, text]
    if 'in_replay_to_status_id_str' in rawTweet:
        previous_tweet = "[[Previous](https://twitter.com/{}/status/{})]".format(rawTweet['in_reply_to_screen_name'], rawTweet['in_replay_to_status_id_str'])
        components.append(previous_tweet)
    if 'retweeted_status' in rawTweet:
        original_tweet = "[[original](https://twitter.com/{}/status/{})]".format(rawTweet['retweeted_status']['user']['screen_name'], rawTweet['retweeted_status']['id_str'])
        components.append(original_tweet)
    return " ".join(components)



def generate_entry_content(list_of_tweet, date_string):
    return '## tweets\n### Posts on {}\n\n{}\n\n(#social #twitter)'.format(
        date_string, 
        '\n'.join(['* {}'.format(format_tweet(t)).replace('\n', '\n  ') for t in list_of_tweet])
        )

if __name__ == '__main__':
    from tempfile import NamedTemporaryFile
    for tweet_file in [f for f in os.listdir(sys.argv[1]) if f.endswith('.js')]:
        raw = json.loads('\n'.join(open(tweet_file).read().split('\n')[1:]))
        for (date, tweets) in organize_by_date(raw).items():
            entry = generate_entry_content(tweets, date)
            with NamedTemporaryFile('w') as f:
                f.write(entry)
                f.flush()
                os.system("dayone -d='{}' new < {}".format(date, f.name))


