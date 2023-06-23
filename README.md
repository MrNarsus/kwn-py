# kwn-py
Python application to query the Kaspa blockchain's public REST server and notify the designated wallet holder that their balance has changed via Discord text channel notifications.


### Software requirements

Make sure python3 and pip3 are installed on your system, then run:

`pip3 install --user -r requirements.txt`

### setup
Open `.env` file using any editor to edit its configurations:

`WEBHOOKURL=`
 
Follow this:
https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

To create a webhook in the Discord channel you'd like to send messages to, then put the webhook url in `WEBHOOKURL` variable, after `=` sign.
 
`MINUTES=`

The default value is five minutes, if you want to change it you can.

`MAIN_KASPA_WALLET_ADDRESS=`

put here the address of the your wallet, this wallet.

`THE_RECEIVE_WALLET=`

Put the address's receive wallet if you want to use receive wallet.

### Starting the Application

`python3 main.py`
