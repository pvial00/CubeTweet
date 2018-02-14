import tweepy
from pycube256 import Cube, CubeRandom, CubeKDF
import binascii, base64

class CubeTweet:
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, key, nonce_length=8):
        self.key = key
        self.nonce_length = nonce_length
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(self.auth)

    def decrypt_tweets(self, tweets):
       msgs = []
       key = CubeKDF().genkey(self.key)
       for tweet in tweets:
           nonce = tweet[:self.nonce_length]
           msg = tweet[self.nonce_length:]
           msg = Cube(key, nonce).decrypt(msg)
           msgs.append(msg)
       return msgs

    def encrypt_tweet(self, msg):
        key = CubeKDF().genkey(self.key)
        nonce = CubeRandom().random(self.nonce_length)
        msg = Cube(key, nonce).encrypt(msg)
        return base64.b64encode(nonce+msg)

    def user_timeline(self, user, count):
       tweet_msgs = self.api.user_timeline(screen_name = user, count= count)
       encrypted_tweets = []
       tweets_for_csv = [tweet.text for tweet in tweet_msgs]
       for t in tweets_for_csv:
          try:
             b = base64.b64decode(str(t))
          except (TypeError, UnicodeEncodeError) as i:
             pass
          else:
             encrypted_tweets.append(b)

       tweets = self.decrypt_tweets(encrypted_tweets)
       return tweets

    def update_status(self, msg):
        tweet = self.encrypt_tweet(msg)
        self.api.update_status(tweet)

    def send_direct_message(self, user, msg):
        tweet = self.encrypt_tweet(msg)
        self.api.send_direct_message(user, text = tweet)
