import discord

import requests
import json

from PIL import Image
import io
import os

from datetime import datetime

EMBED_COLOR = 0x3B920A

class opChampBuilds:
    def __init__(self, ctx:discord.ApplicationContext, champName:str = None, position:str = "TOP", selfRequsestID:int = None, _NEXT:str = None, headers:dict = None):
        self.champName = champName
        self.position = position

        self.lang = "tr_TR"
        self.buildsApi = f"https://www.op.gg/_next/data/{_NEXT}/champions/{self.champName}/top/build.json?region=global&tier=diamond&champion={self.champName}&position={self.position}?hl={self.lang}"
        self.headers = headers if headers else {"User-Agent" : "YOUR USE AGENT HERE", "accept" : "application/json"}
        self.ctx = ctx
        self.ID = selfRequsestID

        self.embedList = []

        self.datas = {}
        self.path = os.path.dirname(__file__) + r"\Runes\%s"%self.ID 

    async def prepareSystem(self):
        print(f"Preparing and the first page are being made - {datetime.now().strftime('%H:%M:%S')}")
        await self.ctx.edit(content="Data is being fetched...")
        r = requests.get(url=self.buildsApi, headers=self.headers)
        
        self.dataJson = json.loads(r.content)
        
        try:
            champPositionsData = self.dataJson['pageProps']['data']['summary']['summary']['positions']
        except:
            errorEmbed = discord.Embed(title="Error!", description=f"We couldn't find chosen champion! Make sure that champion name was entered correctly.\n\n`The entered name`: **{self.champName}**", color=EMBED_COLOR)
            errorEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1014259605158760468/1ae34e5436c31387ae5f75f1a9e32ce9.webp")
            
            self.embedList.append(errorEmbed)
            return self.embedList

        champPositions = []
        for roleNumber in range(len(champPositionsData)):
            champPositions.append(champPositionsData[roleNumber]['name'])

        if self.position not in champPositions:
            errorEmbed = discord.Embed(title="Error!", description=f"The chosen champion hasn't been played in the chosen lane. Please choose common lane.\n\n`Common lanes for {self.champName}: `: {' '.join(str(x) for x in champPositions)}", color=EMBED_COLOR)
            errorEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1014259605158760468/1ae34e5436c31387ae5f75f1a9e32ce9.webp")
            
            self.embedList.append(errorEmbed)
            return self.embedList
        else:
            champPositionIndex = champPositions.index(self.position) 

        self.champPosInf = champPositionsData[champPositionIndex]
        
        self.WR = format(self.champPosInf['stats']['win_rate']*100, ".2f")
        self.RoleRate = format(self.champPosInf['stats']['role_rate']*100, ".2f")
        self.KDA = format(self.champPosInf['stats']['kda'], ".2f")


        self.champMeta = self.dataJson['pageProps']['data']['summary']['meta']

        self.tips = self.champMeta['ally_tips']
        self.champName = self.champMeta['name']
        self.champImageUrl = self.champMeta['image_url']

        self.tipsList = []
        for i in self.tips:
            self.tipsList.append(f"**⋆** {i}")
        if self.tipsList == []:
            self.tipsList.append("**⋆** Data is not found.")

        firstPageEmbed = discord.Embed(title=f"{self.champName} - {self.position}", color=EMBED_COLOR)
        
        firstPageEmbed.add_field(name="Win Rate", value=f"%{self.WR}", inline=True)
        firstPageEmbed.add_field(name="KDA", value=f"{self.KDA}", inline=True)
        firstPageEmbed.add_field(name="Role Rate", value=f"%{self.RoleRate}", inline=True)
        
        firstPageEmbed.add_field(name="Gameplay Tips", value="\n".join(map(str, self.tipsList)), inline=False)
        firstPageEmbed.set_thumbnail(url=self.champImageUrl)

        self.embedList.append(firstPageEmbed)
        await self.getBuilds()

    async def getBuilds(self):
        print(f"Buildler alınıyor - {datetime.now().strftime('%H:%M:%S')}")
        runeDatas = self.dataJson['pageProps']['data']['runes']
        statDatas = self.dataJson['pageProps']['data']

        skillsOrder = statDatas['skills'][0]['order'] if len(statDatas['skills']) else "Veri alınamadı"

        summonerHashMap = {1: 'SummonerBoost', 3: 'SummonerExhaust', 4: 'SummonerFlash', 6: 'SummonerHaste', 7: 'SummonerHeal', 11: 'SummonerSmite', 12: 'SummonerTeleport', 13: 'SummonerMana', 14: 'SummonerDot', 21: 'SummonerBarrier', 30: 'SummonerPoroRecall', 31: 'SummonerPoroThrow', 32: 'SummonerSnowball', 39: 'SummonerSnowURFSnowball_Mark', 54: 'Summoner_UltBookPlaceholder', 55: 'Summoner_UltBookSmitePlaceholder'}
        
        itemsUrl = "https://opgg-static.akamaized.net/images/lol/item/"
        spellsUrl = "https://opgg-static.akamaized.net/images/lol/spell/"
        
        urlRune = "https://opgg-static.akamaized.net/images/lol/perk/"
        urlStats = "https://opgg-static.akamaized.net/images/lol/perkShard/"

        Line = Image.open(io.BytesIO(requests.get("https://i.ibb.co/L65yDD8/line-divider-transparent-9.png").content)).resize((126,83))
        trinket = Image.open(io.BytesIO(requests.get("https://opgg-static.akamaized.net/images/lol/item/3361.png").content)).resize((24, 24))
        try:
            for buildListNumber in range(3):
                summonerMainRunes = runeDatas[buildListNumber]['primary_rune_ids']
                summonerSecondRunes = runeDatas[buildListNumber]['secondary_rune_ids']
                summonerStatsRune = runeDatas[buildListNumber]['stat_mod_ids']

                im = Image.new("RGBA", (326, 120), (255, 0, 0, 0))
                for m in range(9):
                    if m == 0:
                        mainRune = Image.open(io.BytesIO(requests.get(urlRune + str(summonerMainRunes[0]) + ".png").content)).resize((100, 96))
                        im.paste(mainRune, (0, 0))
                    elif m == 1:
                        secondRune = Image.open(io.BytesIO(requests.get(urlRune + str(summonerMainRunes[1]) + ".png").content)).resize((24, 24))
                        im.paste(secondRune, (96, 0))
                    elif m == 2:
                        thirdRune = Image.open(io.BytesIO(requests.get(urlRune + str(summonerMainRunes[2]) + ".png").content)).resize((24, 24))
                        im.paste(thirdRune, (96, 30))
                    elif m == 3:
                        fourthRune = Image.open(io.BytesIO(requests.get(urlRune + str(summonerMainRunes[3]) + ".png").content)).resize((24, 24))
                        im.paste(fourthRune, (96, 60))
                    elif m == 4:
                        secondPageRune1 = Image.open(io.BytesIO(requests.get(urlRune + str(summonerSecondRunes[0]) + ".png").content)).resize((24, 24))
                        im.paste(secondPageRune1,(24, 92))
                    elif m == 5:
                        secondPageRune2 = Image.open(io.BytesIO(requests.get(urlRune + str(summonerSecondRunes[1]) + ".png").content)).resize((24, 24))
                        im.paste(secondPageRune2, (53, 92))
                    elif m == 6:
                        firstStatRune = Image.open(io.BytesIO(requests.get(urlStats + str(summonerStatsRune[0]) + ".png").content)).resize((24, 24))
                        im.paste(firstStatRune, (163, 92))
                    elif m == 7:
                        secondStatRune = Image.open(io.BytesIO(requests.get(urlStats + str(summonerStatsRune[1]) + ".png").content)).resize((24, 24))
                        im.paste(secondStatRune, (197, 92))
                        pass
                    elif m == 8:
                        thirdStatRune = Image.open(io.BytesIO(requests.get(urlStats + str(summonerStatsRune[2]) + ".png").content)).resize((24, 24))
                        im.paste(thirdStatRune, (230, 92))
                        pass
                    
                im.paste(Line, (99, 123))

                starterItems, sItemsLen = statDatas['starter_items'][buildListNumber], len(statDatas['starter_items'][buildListNumber]['ids'])
                coreItems = statDatas['core_items'][buildListNumber]
                summonerSpells = statDatas['summoner_spells'][0]
                
                if sItemsLen == 2:
                    for startItemImage in range(2):
                        if startItemImage == 0:
                            sItemOne = Image.open(io.BytesIO(requests.get(itemsUrl + str(starterItems['ids'][0]) + ".png").content)).resize((24, 24))
                            im.paste(sItemOne, (180, 20))
                        elif startItemImage == 1:
                            sItemSecond = Image.open(io.BytesIO(requests.get(itemsUrl + str(starterItems['ids'][1]) + ".png").content)).resize((24, 24))
                            im.paste(sItemSecond, (213, 20))
                
                if sItemsLen == 3:
                    for startItemImage in range(3):
                        if startItemImage == 0:
                            sItemOne = Image.open(io.BytesIO(requests.get(itemsUrl + str(starterItems['ids'][0]) + ".png").content)).resize((24, 24))
                            im.paste(sItemOne, (163, 20))
                        elif startItemImage == 1:
                            sItemSecond = Image.open(io.BytesIO(requests.get(itemsUrl + str(starterItems['ids'][1]) + ".png").content)).resize((24, 24))
                            im.paste(sItemSecond, (197, 20))
                        elif startItemImage == 2:
                            sItemThird  = Image.open(io.BytesIO(requests.get(itemsUrl + str(starterItems['ids'][2]) + ".png").content)).resize((24, 24))
                            im.paste(sItemThird, (230, 20))

                for coreItemImage in range(3):
                        if coreItemImage == 0:
                            cItemOne = Image.open(io.BytesIO(requests.get(itemsUrl + str(coreItems['ids'][0]) + ".png").content)).resize((24, 24))
                            im.paste(cItemOne, (163, 56))
                        elif coreItemImage == 1:
                            cItemSecond = Image.open(io.BytesIO(requests.get(itemsUrl + str(coreItems['ids'][1]) + ".png").content)).resize((24, 24))
                            im.paste(cItemSecond, (197, 56))
                        elif coreItemImage == 2:
                            cItemThird = Image.open(io.BytesIO(requests.get(itemsUrl + str(coreItems['ids'][2]) + ".png").content)).resize((24, 24))
                            im.paste(cItemThird, (230, 56))



                for spellsImage in range(2):
                        if spellsImage == 0:
                            spellOne = Image.open(io.BytesIO(requests.get(spellsUrl + str(summonerHashMap[summonerSpells['ids'][0]]) + ".png").content)).resize((24, 24))
                            im.paste(spellOne, (277, 20))
                        elif spellsImage == 1:
                            spellTwo = Image.open(io.BytesIO(requests.get(spellsUrl + str(summonerHashMap[summonerSpells['ids'][1]]) + ".png").content)).resize((24, 24))
                            im.paste(spellTwo, (277, 56))
                
                im.paste(trinket, (277, 92))
                

                if os.path.exists(self.path):
                    pass
                else:
                    os.mkdir(self.path)
                
                im.save(r"%s\%s.png"%(self.path, buildListNumber))
                print(f"The image have been created #{buildListNumber} - {id(self)} - {datetime.now().strftime('%H:%M:%S')}")  
                await self.ctx.edit(content=f"Build have been created #{buildListNumber+1}")

                buildWR = format(int(coreItems['win']*100)/int(coreItems['play']), ".2f") if int(coreItems['win']) > 1 else 00.00
                buildPickRate = format(coreItems['pick_rate']*100, ".2f") if int(coreItems['win']) > 1 else 00.00

                buildEmbed = discord.Embed(title=f"{self.champName} - {self.position} Build #{buildListNumber+1}")
                buildEmbed.add_field(name="Build Win Rate", value=f"%{buildWR}", inline=True)
                buildEmbed.add_field(name="Build Pick Rate", value=f"%{buildPickRate}", inline=True)
                buildEmbed.add_field(name="Skill Order", value=' > '.join(map(str,skillsOrder)), inline=False)
                buildEmbed.set_thumbnail(url=self.champImageUrl)

                with open(self.path+r"\%s.png"%buildListNumber, 'rb') as f:
                    picture = discord.File(f)
                    """Embeds don't work with image files. I send to the generated image to
                        myself via bot and then copy that url of the image. So, I use Discord
                        as cloud service."""
                    mes = await self.ctx.guild.get_member("YOUR DISCORD ID").send(file=picture)
                    runeEmbedUrl = mes.attachments[0].url
                    await mes.delete()
                buildEmbed.set_image(url=runeEmbedUrl)
                self.embedList.append(buildEmbed)
        except IndexError:
            pass


    async def getBuildEmbedList(self):
        await self.prepareSystem()
        print(f"The embeds are ready. The embeds is being sent - {datetime.now().strftime('%H:%M:%S')}")
        return self.embedList
