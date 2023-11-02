import requests
from bs4 import BeautifulSoup
import html5lib
import json

class GetOPID():

    def __init__(self, account:str, header:dict = None) -> None:
        self.accountName = account
        self.url = "https://tr.op.gg/summoners/tr/{}".format(self.accountName)
        self.headers = header if header else {"User-Agent" : "YOUR USER AGENT"}
        

    def getId(self) -> str:
        r = requests.get(url=self.url, headers=self.headers)

        soup = BeautifulSoup(r.content, "html5lib")
        data = json.loads(soup.find(id="__NEXT_DATA__", type='application/json').text)
        ID = data['props']['pageProps']['data']['summoner_id']
        return ID

