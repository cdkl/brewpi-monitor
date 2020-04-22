# Where is your brewpi web interface? By default, this script runs on the same host
piHost="http://127.0.0.1"
# Which Pid is your beer measurement Pid? This is configuration dependent.
# You can inspect the json directly with
#   curl -d "messageType=getControlVariables" "http://127.0.0.1/socketmessage.php"
beerPidIndex = 3
# These two variables should be set to your pid name and target name
# So that if config or output ever changes, you'll get a warning
beerName = 'beer1'
beerTargetName = 'beer1set'

# Alert if temperature goes outside of these bounds.
tempMin = 1.5
tempMax = 21.0

# Email address to send alerts to.
emailTo = None

# Email account setup. This is tuned to Gmail for now.
# If you are using gmail, you should define an app password that can send email but can't
# log into your account. See https://support.google.com/mail/answer/185833?hl=en
smtpSender = None
smtpPasswd = None
smtpServer = 'smtp.gmail.com'
smtpPort = 587


