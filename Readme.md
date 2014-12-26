This script converts your tweet archive to [Day One](http://dayoneapp.com) entries. Tweets from the same day are grouped into the same entry.

First, you need Day One tha app, and its [command line tool](http://dayoneapp.com/downloads/dayone-cli.pkg) installed.

Assuming you unziped the tweet archive from Twitter at TWEETPATH, simply run:

        python3 tweet_archive_to_dayone.py TWEETPATH/data/js/tweets/ 

Your method of running Python 3 environment may vary.
