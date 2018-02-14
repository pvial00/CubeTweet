from CubeTweet import CubeTweet
import sys

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

def usage():
    sys.stdout.write("python cubetweet.py <mode> <key>\n")
    sys.stdout.write("\nModes:\n")
    sys.stdout.write("update_status\nuser_timeline\ndirect_message\n")
    sys.exit(1)

nonce_length = 8
try:
    mode = sys.argv[1]
except IndexError as i:
    usage()

try:
    key = sys.argv[2]
except IndexError as i:
    usage()

ct = CubeTweet(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, key, nonce_length)
if mode == "update_status":
    msg = raw_input("Enter text to post to your status: ")
    ct.update_status(msg)
elif mode == "user_timeline":
    user = raw_input("Enter username: ")
    tweets = ct.user_timeline(user, 100)
    for tweet in tweets:
        sys.stdout.write(tweet+"\n")
elif mode == "send_direct_message":
    user = raw_input("Enter username: ")
    msg = raw_input("Enter text to send: ")
    ct.send_direct_message(user, msg)
