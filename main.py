from json import loads
from os import getenv
from dotenv import load_dotenv
from requests import get
from discordwebhook import Discord
import sys
from time import sleep

# The Variables
load_dotenv()
webhookurl = getenv('WEBHOOKURL')
kaspa_wallet_address = getenv('MAIN_KASPA_WALLET_ADDRESS')
minutes = getenv("MINUTES")

url = 'https://api.kaspa.org'
cachedBalance = 0


def sendDiscordChannelMessage(message):
    discord = Discord(url=f"{webhookurl}")
    discord.post(content=message)

def checkf():
    global result 
    site = get(f"{url}/addresses/{kaspa_wallet_address}/balance")
    result = loads(site.text)["balance"] / 100000000
    if site.status_code == 200: pass
    else:
        print("Error occured when querying wallet address!")
        sys.exit(1)


cachedBalance = 0
def mainfunction():
    global cachedBalance
    global currentBalance
    currentBalance = result
    print(f"Current KAS balance: {currentBalance}")
    blockReward = get(f"{url}/info/blockreward?stringOnly=true")
    if cachedBalance != 0 and cachedBalance != currentBalance:
        differenceInKAS = currentBalance - cachedBalance
        firstp = 'Block mined!' if differenceInKAS == blockReward else 'Transaction occurred!'
        secondp = " Wallet balance modified by "
        thirdp = "+" if differenceInKAS > 0 else "-"
        TRANSACTION_OCCURED_MSG = firstp + secondp + thirdp + str(differenceInKAS) + "\n" + "Current KAS balance: " + str(currentBalance)
        sendDiscordChannelMessage(TRANSACTION_OCCURED_MSG)
        print(TRANSACTION_OCCURED_MSG)


# Start The Application
while True:
    print('Querying wallet...')
    checkf()
    mainfunction()
    cachedBalance = currentBalance
    print("Please wait a minute..." if minutes == 1 or minutes == "1" else f"Please wait for {minutes} minutes...")
    sleep(int(minutes) * 60)
