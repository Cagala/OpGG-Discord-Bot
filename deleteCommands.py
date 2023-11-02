import requests

headers = {
    "Authorization": "API AUTH"
}

json = {}

while True:
    print("""
    1: View bot commands
    2: View guild commands
    3: Delete bot command
    4: Delete guild command""")
    inp = int(input())

    if inp == 1:
        url = "https://discord.com/api/v10/applications/YOUR SERVER ID/commands"
        r = requests.get(url=url, headers=headers)
        print(r.content)
    if inp == 2:
        url = "https://discord.com/api/v10/applications/YOUR DC DEVELOPER APP ID/guilds/YOUR SERVER ID/commands"
        r = requests.get(url=url, headers=headers)
        print(r.content)
    if inp == 3:
        url = "https://discord.com/api/v10/applications/YOUR DC DEVELOPER APP ID/commands"
        r = requests.put(url=url, headers=headers, json=json)
        print(r)
    if inp == 4:
        url = "https://discord.com/api/v10/applications/YOUR DC DEVELOPER APP ID/guilds/YOUR SERVER ID/commands"
        r = requests.put(url=url, headers=headers, json=json)
    if inp == 5:
        False