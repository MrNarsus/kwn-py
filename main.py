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
receive_Wallet_Address = getenv("THE_RECEIVE_WALLET")
minutes = getenv("MINUTES")

url = 'https://api.kaspa.org'

# The cache balance of wallets
cachedBalance = 0
rwcachedBalance = 0


def sendDiscordChannelMessage(message):
    discord = Discord(url=f"{webhookurl}")
    discord.post(content=message)

def checkf():
    site = get(f"{url}/addresses/{kaspa_wallet_address}/balance")
    if site.status_code != 200:
        print("Error occured when querying wallet address!")
        sys.exit(1)
    else: global result; result = loads(site.text)["balance"] / 100000000

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
def check_Receive_Wallet():
    b = get(f"{url}/addresses/{receive_Wallet_Address}/balance")
    if b.status_code == 200:
        pass
    else:
        print("Error occured when querying receive wallet address!")
        sys.exit(1)

def receive_wallet_function():
    global result
    global rwcachedBalance
    print(f"Current KAS balance: {result}")
    site = get(f"{url}/addresses/{receive_Wallet_Address}/balance")
    if loads(site.text)["balance"] != 0:
        global rwbalance
        rwbalance = loads(site.text)["balance"] / 100000000
        #here the block mined ant transactions occurred...
        blockReward = get(f"{url}/info/blockreward?stringOnly=true")
        if rwcachedBalance != 0 and cachedBalance != rwbalance:
            total = result + rwbalance
            differenceInKAS = rwbalance - rwcachedBalance
            firstp = 'Block mined!' if differenceInKAS == blockReward else 'Transaction occurred!'
            secondp = " Wallet balance modified by "
            TRANSACTION_OCCURED_MSG = firstp + secondp + str(differenceInKAS) + "\n" + "Current KAS balance: " + str(total)
            sendDiscordChannelMessage(TRANSACTION_OCCURED_MSG)
            print(f"Your Balance is: {total}\nPlease Compound it!")
    else:
        print("No changes occurred on your balance...")

# Start The Application
while True:
    print('''Select an option:
    1. Main Wallet (The address of 'this wallet')
    2. Receive Wallet (another address)''')
    selection = input("Enter a Number: ")
    match selection:
        case '1'|'01':
            print('Querying wallet...')
            checkf()
            mainfunction()
            cachedBalance = currentBalance
            print("Please wait a minute..." if minutes == 1 or minutes == "1" else f"Please wait for {minutes} minutes...")
            sleep(int(minutes) * 60)
        case '2'|'02':
            checkf()
            check_Receive_Wallet()
            receive_wallet_function()
            rwcachedBalance = rwbalance
            print("Please wait a minute..." if minutes == 1 or minutes == "1" else f"Please wait for {minutes} minutes...")
            sleep(int(minutes) * 60)
        case _:
            print("No match found!\n\n\n")
