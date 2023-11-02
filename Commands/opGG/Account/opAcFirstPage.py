import discord
import requests
import json

EMBED_COLOR = 0x3B920A

class opAcFirst():

    def __init__(self, opAccountID: str, headers:dict = None):
        self.accInfApi = f"https://tr.op.gg/api/summoners/tr/{opAccountID}"
        self.headers = headers if headers else {"User-Agent" : "YOUR USER AGENT", "accept" : "application/json"}
        
        self.embed = discord.Embed(color=EMBED_COLOR)

        self.datas = {}

    def get_datas(self):
        r = requests.get(url=self.accInfApi, headers=self.headers)
        dataJson = json.loads(r.content)['data']

        name = dataJson['name']
        profile_image = dataJson['profile_image_url']
        level = dataJson['level']

        soloRankedTier = dataJson['league_stats'][0]['tier_info']['tier'] if dataJson['league_stats'][0]['tier_info']['tier'] else "UNRANKED"
        soloRankedDivision = dataJson['league_stats'][0]['tier_info']['division'] if dataJson['league_stats'][0]['tier_info']['division'] else " "
        soloRankedTierImgUrl = dataJson['league_stats'][0]['tier_info']['tier_image_url']
        soloRankedWin = dataJson['league_stats'][0]['win']
        soloRankedLose = dataJson['league_stats'][0]['lose']
        soloRankedLp = dataJson['league_stats'][0]['tier_info']['lp']
        soloWinRate = format((int(soloRankedWin)*100)/(int(soloRankedWin)+int(soloRankedLose)), ".2f") if not int(soloRankedWin) == 0 or int(soloRankedLose) else "00.00"

        flexRankedTier = dataJson['league_stats'][1]['tier_info']['tier'] if dataJson['league_stats'][1]['tier_info']['tier'] else "UNRANKED"
        flexRankedDivision = dataJson['league_stats'][1]['tier_info']['division'] if dataJson['league_stats'][1]['tier_info']['division'] else " "
        flexRankedTierImgUrl = dataJson['league_stats'][1]['tier_info']['tier_image_url']
        flexRankedWin = dataJson['league_stats'][1]['win']
        flexRankedLose = dataJson['league_stats'][1]['lose']
        flexRankedLp = dataJson['league_stats'][1]['tier_info']['lp']
        flexWinRate = format((int(flexRankedWin)*100)/(int(flexRankedWin)+int(flexRankedLose)), ".2f") if not int(flexRankedWin) == 0 or int(flexRankedLose) else "     00.00"



        self.datas['name'] = name
        self.datas['profile_image'] = profile_image
        self.datas['level'] = level

        self.datas['soloRankedTier'] = soloRankedTier
        self.datas['soloRankedDivision'] = soloRankedDivision
        self.datas['soloRankedUrl'] = soloRankedTierImgUrl
        self.datas['soloRankedWin'] = soloRankedWin
        self.datas['soloRankedLose'] = soloRankedLose
        self.datas['soloRankedWinrate'] = soloWinRate
        self.datas['soloRankedLp'] = soloRankedLp

        self.datas['flexRankedTier'] = flexRankedTier
        self.datas['flexRankedDivision'] = flexRankedDivision
        self.datas['flexRankedUrl'] = flexRankedTierImgUrl
        self.datas['flexRankedWin'] = flexRankedWin
        self.datas['flexRankedLose'] = flexRankedLose
        self.datas['flexRankedWinrate'] = flexWinRate
        self.datas['flexRankedLp'] = flexRankedLp

    def getEmbed(self) -> discord.Embed:
        self.get_datas()
        self.embed.set_author(name=f"{self.datas['name']} - {self.datas['level']} Level")
        self.embed.set_thumbnail(url=self.datas['profile_image'])
        self.embed.add_field(name="Solo Ranked", value=f"`Rank`: {self.datas['soloRankedTier'].capitalize()} {self.datas['soloRankedDivision']}\n`LP`: **{self.datas['soloRankedLp']}**\n`Win`: **{self.datas['soloRankedWin']}**\n`Lose`: **{self.datas['soloRankedLose']}**\n`Winrate`: **%{self.datas['soloRankedWinrate']}**")
        self.embed.add_field(name="Flex Ranked", value=f"`Rank`: {self.datas['flexRankedTier'].capitalize()} {self.datas['flexRankedDivision']}\n`LP`: **{self.datas['flexRankedLp']}**\n`Win`: **{self.datas['flexRankedWin']}**\n`Lose`: **{self.datas['flexRankedLose']}**\n`Winrate`: **%{self.datas['flexRankedWinrate']}**")
        return self.embed