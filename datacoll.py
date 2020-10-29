import csv
import tweepy
import re

class Main:
    def data_collection(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
        # create authentication for accessing Twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # initialize Tweepy API
        api = tweepy.API(auth)

        # get the name of the spreadsheet we will write to
        fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))

        with open('%s.csv' % ('tdata'), 'w',encoding="utf-8") as file:
            w = csv.writer(file)

            w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count'])

            for tweet in tweepy.Cursor(api.search, q=hashtag_phrase + ' -filter:retweets', \
                                       lang="en", tweet_mode='extended').items(100):
                w.writerow([tweet.created_at, tweet.full_text.replace('\n', ' ').encode('utf-8'),
                            tweet.user.screen_name.encode('utf-8'),
                            [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])


    consumer_key = "s4sywQCAw6zR4GH4slrO4bbU8"
    consumer_secret = "TD1sjKj8xk2lWPooaUlAnNxAKfyxNRRLOWbduZeyXkny5p6DZr"
    access_token = "855052793366761474-l8A3izx4whw06PqQmdYiFRH9M19fncq"
    access_token_secret = "5wUU1axw3zwhzbxw0ofuThzAUxVeJ5iQGbh1atHEGKmdr"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    hashtag_phrase = input('Hashtag Phrase ')
    if __name__ == '__main__':
        data_collection(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)
if __name__ == '__main__':
    Main()