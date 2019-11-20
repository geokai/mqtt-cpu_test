# This file was created on 13/01/17
# Author: George Kaimakis

# ThingSpeak Update Using MQTT
# Copyright 2016, MathWorks, Inc

# This is an example of publishing to multiple fields simultaneously.
# Connnections over standard TCP, websockets or SSL are possible by setting
# the parameters below.
#
# CPU and RAM usage is collected every 20 seconds and published to a
# ThingSpeak channel using an MQTT Publish
#
# This example requires the Paho MQTT client package which
# is available at: http://eclipse.org/paho/clients/python

from __future__ import print_function
import paho.mqtt.publish as publish
import psutil
import credentials
import os
from time import sleep


###   Variables   ###
LOOP_INTERVAL = 28.5    # seconds

###   Start of Channel Settings   ###

#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = credentials.CH_ID

# The Write API Key for the channel
# Replace this with your Write API key
apiKey = credentials.API_ID

#  MQTT Connection Methods

# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system
# resources.
useUnsecuredTCP = False

# Set useUnsecuredWebsockets to True to use MQTT over an unseured websocket on
# port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False

# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resourses, but the
# connection will be secure by SSL.
useSSLWebsockets = True


###   End Of User Configuration   ###


# The Hostname of the ThingSpeak MQTT service
mqttHost = "api.thingspeak.com"

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443

# Create the topic string
topic = "update?" + "api_key=" + apiKey


# Run a loop which calculates the system performance every
#   xx seconds and publishes that to a ThingSpeak channel
#   using MQTT.


def dots(*, interval=0.5, num_of_dots=3, xtr_line=False):
    for i in range(num_of_dots):
        sleep(interval)
        print(".", end='', flush=True)
    if xtr_line:
        print()     # print extra line - leaves dots in place


# clear the screen:
os.system('clear')


try:
    while(True):
        dots()
        # get the system performance data:
        cpuPercent = psutil.cpu_percent(interval=0.5)
        ramPercent = psutil.virtual_memory().percent
        print ("\rCPU usage = {}%".format(cpuPercent),"\tRAM usage = {}%".format(ramPercent))

        # build the payload string:
        tPayload = "&field1=" + str(cpuPercent) + "&field2=" + str(ramPercent)

        # attempt to publish this data to the topic:
        try:
            publish.single(topic, payload=tPayload, hostname=mqttHost) # , \
#                    port=tPort, tls=tTLS, transport=tTransport)
        except:
            print ("There was an error while publishing the data.")
        sleep(LOOP_INTERVAL)
except KeyboardInterrupt:
    print(" :Quitting!")
finally:
    exit()
