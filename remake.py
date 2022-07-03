from weakref import proxy
import requests
import random
import string
import json
from time import sleep


discordapi = "https://discordapp.com/api/v10/"


useragents = []


proxies = []


def random_proxy():
    return random.choice(proxies)


def random_user_agent():
    return random.choice(useragents)


def gen_random_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(4))


def send_message_no_proxy(token, channelid):
    link = f"https://discord.com/api/channels/{channelid}/messages"
    
    try:
        a = requests.post(link, headers={"Authorization": token, "User-Agent": random_user_agent(), "Content-Type": "application/json"}, data=json.dumps({"content": f"{gen_random_string()}"}))
        print(a.status_code)
    except Exception as e:
        print(e)


def send_message(token, channelid):
    link = f"https://discord.com/api/channels/{channelid}/messages"
    
    theproxy = random_proxy()

    try:
        a = requests.post(link, proxies={"socks5": f"{theproxy}"}, headers={"Authorization": token, "User-Agent": random_user_agent(), "Content-Type": "application/json"}, data=json.dumps({"content": f"{gen_random_string()}"}))
        if(a.status_code == 200):
            print("Message sent OK")
        elif(a.status_code == 403):
            print("Bad proxy remvoing now")
            proxies.remove(theproxy)
        elif(a.status_code == 429):
            print("Server cannot handle the request")
        else:
            print(a.status_code)
    except Exception as e:
        print(e)


def get_proxy():
    print("[!] Getting proxies")
    try:
        sock5prox = input("[!] Name of .txt file contain SOCKS5 proxies? (Need to be SOCKS5) ")
        get_proxies = open(sock5prox, "r")
        for proxi in get_proxies.read().split('\n'):
            proxies.append(proxi)
    except Exception as e:
        print(f"{e} Make sure proxies name is correct")
        main()


def get_user_agent():
    try:
        get_user_agent = open("./useragents.txt", "r")
        for uas in get_user_agent.read().split('\n'):
            useragents.append(uas)
    except Exception as e:
        print(f"{e} Make sure useragents.txt is in same folder as the python script")
        main()


def spammer_no_proxy(delay, messages, to, ch):
    c = 0
    while c > messages:
        send_message_no_proxy(to, ch)
        c+=1
        print(f"[+] Sent message {c}/{messages}")
        sleep(delay)


def spammer_with_proxy(delay, messages, to, ch):
    print("Starting spam")
    c = 0
    while c < messages:
        send_message(to, ch)
        c+=1
        print(f"[+] Sent message {c}/{messages}")
        sleep(delay)



def main():
    print("\x1b[31;40mBy using this script you understand that spamming is against discord TOS and can result in your account being disabled")
    sleep(2)
    to = input("[+] Discord token>: ")
    ch = input("[+] Channel ID to spam the messages to?: ")

    try:
        dela = int(input("[+] The delay bewteen each message being sent?: "))
    except TypeError:
        print("[!] Value must be an integar")

    try:
        amount_of_messages = int(input("[+] How many messages to attempt to send?: "))
    except TypeError:
        print("[!] The value should be an integar")

    print("[+] Getting user agents....")
    get_user_agent()
    print(f"[!] Found {len(useragents)} User Agents")

    useproxy = input("Would you like to use SOCKS5 proxies? You do not have to use proxies but it reduces the chances of being rate limited! (Y/N) ")
    if(useproxy == "y"):
        get_proxy()
        print(f"[+] Found {len(proxies)} Proxies")
        spammer_with_proxy(dela, amount_of_messages, to, ch)
    elif(useproxy == "n"):
        print("[!] Use proxyless mode")
        spammer_no_proxy(dela, amount_of_messages, to, ch)
    else:
        print("[!] Invalid either y or n was expected")


if __name__ == "__main__":
    main()