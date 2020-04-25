#!/usr/bin/env python3

import urllib.request
import json
import smtplib
import sys

# You will need to copy config-sample.py to config.py and provide variable information there.
import config

piUrl=config.piHost + "/socketmessage.php"

mailContent = ''

testEmail = False
if len(sys.argv) > 1 and sys.argv[1] == "-testemail":
    testEmail = True
    mailContent = "This is a test email from brewpi-monitor."

if not testEmail:
    try:
        req = urllib.request.Request(piUrl, "messageType=refreshControlVariables&message=".encode('utf-8'))
        with urllib.request.urlopen(req) as response:
           the_page = response.read()

        req = urllib.request.Request(piUrl, "messageType=getControlVariables".encode('utf-8'))
        with urllib.request.urlopen(req) as response:
           ret = response.read()

        piData = json.loads(ret.decode('utf-8'))

        currentName = piData["pids"][config.beerPidIndex]["input"]["sensor"]["name"]
        targetName = piData["pids"][config.beerPidIndex]["input"]["setPoint"]["name"]

        if currentName != config.beerName or targetName != config.beerTargetName:
            mailContent += "BrewPi Data problem. Couldn't recognize configuration\n."

        currentTemp = piData["pids"][config.beerPidIndex]["input"]["sensor"]["delegate"]["value"]
        targetTemp= piData["pids"][config.beerPidIndex]["input"]["setPoint"]["value"]

        if currentTemp < config.tempMin:
            mailContent += "BrewPi Temperature problem. Temp too low: " + str(currentTemp) + "\n"

        if currentTemp > config.tempMax:
            mailContent += "BrewPi Temperature problem. Temp too high: " + str(currentTemp) + "\n"

    except Exception as e:
        mailContent += 'Serious error: ' + str(e) + "\n"

if not mailContent:
    exit()

print(mailContent)

TO = config.emailTo
if testEmail:
    SUBJECT = 'Brewpi Monitor test'
else:
    SUBJECT = 'BREWPI NEEDS HALP!!'

TEXT = mailContent

server = smtplib.SMTP(config.smtpServer, config.smtpPort)
server.ehlo()
server.starttls()
server.login(config.smtpSender, config.smtpPasswd)

BODY = '\r\n'.join(['To: %s' % TO,
        'From: %s' % config.smtpSender,
        'Subject: %s' % SUBJECT,
        '', TEXT])

try:
        server.sendmail(config.smtpSender, [TO], BODY)
        print ('email sent')
except:
        print ('error sending mail')

server.quit()


