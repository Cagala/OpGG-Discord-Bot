import requests
from bs4 import BeautifulSoup
import html5lib
import json

class Get_NEXTID():

    def __init__(self, champName:str, header:dict = None) -> None:
        self.champName = champName
        self.url = "https://www.op.gg/champions/{}/top/build?region=global&tier=platinum_plus".format(self.champName)
        self.headers = header if header else {"User-Agent" : "YOUR USER AGENT"}
        

    def get_NEXTId(self) -> str:
        r = requests.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(r.content, "html5lib")
        dataJson = json.loads(soup.find(id="__NEXT_DATA__", type='application/json').text)
        _NEXTID = dataJson["buildId"]
        return _NEXTID
