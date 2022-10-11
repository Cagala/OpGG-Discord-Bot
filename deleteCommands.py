import requests

headers = {
    "Authorization": "Bot MTAxNDI1OTYwNTE1ODc2MDQ2OA.G6JttU.cqLFMwqXQHetfDGUwN5vz5BCfutA1Umea2dLgo"
}

json = {}

while True:
    print("""
    1: Bot komutları gör
    2: Guild komutları gör
    3: Bot komut sil
    4: Guild komut sil""")
    inp = int(input())

    if inp == 1:
        url = "https://discord.com/api/v10/applications/1014259605158760468/commands"
        r = requests.get(url=url, headers=headers)
        print(r.content)
    if inp == 2:
        url = "https://discord.com/api/v10/applications/1014259605158760468/guilds/964943633361014805/commands"
        r = requests.get(url=url, headers=headers)
        print(r.content)
    if inp == 3:
        url = "https://discord.com/api/v10/applications/1014259605158760468/commands"
        r = requests.put(url=url, headers=headers, json=json)
        print(r)
    if inp == 4:
        url = "https://discord.com/api/v10/applications/1014259605158760468/guilds/964943633361014805/commands"
        r = requests.put(url=url, headers=headers, json=json)
    if inp == 5:
        False