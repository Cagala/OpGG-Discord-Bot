from arrow import now
import discord
import requests
import json
from PIL import Image
import io
import os
from datetime import datetime

EMBED_COLOR = 0x3B920A

class opAcGames():

    def __init__(self, ctx, opAccountID:str, requestSelfID:int, headers:dict = None):
        self.gamesInfApi = f"https://op.gg/api/v1.0/internal/bypass/games/tr/summoners/{opAccountID}?&limit=10&hl=tr_TR&game_type=total"
        self.headers = headers if headers else {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.54", "accept" : "application/json"}
        self.ctx = ctx
        self.ID = requestSelfID

        self.embedList = []

        self.datas = {}
        self.path = os.path.dirname(__file__) + r"\Runes\%s"%self.ID

    def get_builds(self):
        r = requests.get(url=self.gamesInfApi, headers=self.headers)

        dataJson = json.loads(r.content)['data']
        for i in range(10):
            gameId = dataJson[i]['id']
            gameCreated_At = dataJson[i]['created_at'].replace(":","%3A").replace("+", "%2B")
            participant_id = dataJson[i]['myData']['participant_id']

            runeUrl = f"https://op.gg/api/v1.0/internal/bypass/games/tr/analysis/{gameId}?created_at={gameCreated_At}"

            runeRequest = requests.get(url=runeUrl, headers=self.headers)
            runeDataJson = json.loads(runeRequest.content)['data']['participants']

            for j in range(len(runeDataJson)):

                if runeDataJson[j]['participant_id'] == participant_id:
                    summonerRuneBuild = runeDataJson[j]['rune_build']
                else:
                    pass
            
            summonerMainRunes = summonerRuneBuild['primary_rune_ids']
            summonerSecondRunes = summonerRuneBuild['secondary_rune_ids']
            urlRune = "https://opgg-static.akamaized.net/images/lol/perk/"

            im = Image.new("RGBA", (326, 120), (255, 0, 0, 0))
            for m in range(6):
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
            
            if os.path.exists(self.path):
                pass
            else:
                os.mkdir(self.path)
            
            im.save(r"%s\%s.png"%(self.path, i))
            print(f"Resim oluşturuldu #{i} - {self} - {datetime.now().strftime('%H:%M:%S')}")        
        

    def get_datas(self):
        r = requests.get(url=self.gamesInfApi, headers=self.headers)

        dataJson = json.loads(r.content)['data']

        for i in range(10):
            print(f"Veriler alınıyor - {datetime.now().strftime('%H:%M:%S')}")
            gameData = dataJson[i]
            summonerData = gameData['myData']

            gameMap = "Sihirdar Vadisi" if gameData['game_map'] == "SUMMONERS_RIFT" else "ARAM"

            champAPIData = json.loads(requests.get(url=f"https://op.gg/api/v1.0/internal/bypass/meta/champions/{summonerData['champion_id']}?hl=tr_TR", headers=self.headers).content)
            championName = champAPIData['data']['name']
            championUrl = champAPIData['data']['image_url']
           
            summonerPosition = summonerData['position']
            summonerItems = summonerData['items']
            summonerTotemItem = summonerData['trinket_item']
            
            #Hasar Verme
            summonerTotalDealt = summonerData['stats']['total_damage_dealt']
            summonerDealtToPlayer = summonerData['stats']['total_damage_dealt_to_champions']
            summonerDealtToObj = summonerData['stats']['damage_dealt_to_objectives']
            summonerDealtToTurrets = summonerData['stats']['damage_dealt_to_turrets']

            #Hasar Tanklama
            summonerTotalTaken = summonerData['stats']['total_damage_taken']
            summonerMitigated = summonerData['stats']['damage_self_mitigated']

            #İşlevesllik
            summonerVisionScore = summonerData['stats']['vision_score']
            summonerVisionBought = summonerData['stats']['vision_wards_bought_in_game']
            summonerWardKill = summonerData['stats']['ward_kill']
            summonerWardPlace = summonerData['stats']['ward_place']
            summonerTurretKill = summonerData['stats']['turret_kill']
            summonerEarnedGold = summonerData['stats']['gold_earned']

            #Stats
            summonerChampLevel = summonerData['stats']['champion_level']
            summonerKill = summonerData['stats']['kill']
            summonerDeath = summonerData['stats']['death']
            summonerAssist = summonerData['stats']['assist']
            summonerCS = int(summonerData['stats']['minion_kill']) + int(summonerData['stats']['neutral_minion_kill'])
            print(f"Veriler alındı. Veriler tanımlanıyor {datetime.now().strftime('%H:%M:%S')}")

            self.datas[f'{i}.gameMap'] = gameMap
            self.datas[f'{i}.championName'] = championName
            self.datas[f'{i}.championUrl'] = championUrl
            self.datas[f'{i}.summonerPosition'] = summonerPosition
            self.datas[f'{i}.summonerTotalDealt'] = summonerTotalDealt
            self.datas[f'{i}.summonerItems'] = summonerItems
            self.datas[f'{i}.summonerTotemItem'] = summonerTotemItem
            self.datas[f'{i}.summonerDealtToPlayer'] = summonerDealtToPlayer
            self.datas[f'{i}.summonerDealtToObj'] = summonerDealtToObj
            self.datas[f'{i}.summonerDealtToTurrets'] = summonerDealtToTurrets
            self.datas[f'{i}.summonerTotalTaken'] = summonerTotalTaken
            self.datas[f'{i}.summonerMitigated'] = summonerMitigated
            self.datas[f'{i}.summonerVisionScore'] = summonerVisionScore
            self.datas[f'{i}.summonerVisionBought'] = summonerVisionBought
            self.datas[f'{i}.summonerWardKill'] = summonerWardKill
            self.datas[f'{i}.summonerWardPlace'] = summonerWardPlace
            self.datas[f'{i}.summonerTurretKill'] = summonerTurretKill
            self.datas[f'{i}.summonerEarnedGold'] = summonerEarnedGold
            self.datas[f'{i}.summonerChampLevel'] = summonerChampLevel
            self.datas[f'{i}.summonerKill'] = summonerKill
            self.datas[f'{i}.summonerDeath'] = summonerDeath
            self.datas[f'{i}.summonerAssist'] = summonerAssist
            self.datas[f'{i}.summonerCS'] = summonerCS
            print(f"Veriler tanımlandı. {datetime.now().strftime('%H:%M:%S')}")



    async def getEmbedList(self):
        self.get_builds()
        self.get_datas()
        print(f"Embedler hazırlanıyor. {datetime.now().strftime('%H:%M:%S')}")
        for i in range(10):
            embed = discord.Embed(title=f"{self.datas[f'{i}.gameMap']} - {self.datas[f'{i}.championName']} #{i+1}", color=EMBED_COLOR)
            embed.set_thumbnail(url=self.datas[f'{i}.championUrl'])
            
            embed.add_field(name="Atanan Rol", value=f'{self.datas[f"{i}.summonerPosition"]}', inline=False)
            embed.add_field(name="Verilen Hasarlar", value=f"`Toplam Hasar`: {self.datas[f'{i}.summonerTotalDealt']}\n`Oyunculara Karşı`: **{self.datas[f'{i}.summonerDealtToPlayer']}**\n`Objektiflere Karşı`: **{self.datas[f'{i}.summonerDealtToObj']}**\n`Kulelere Karşı`: **{self.datas[f'{i}.summonerDealtToTurrets']}**")
            embed.add_field(name="Alınan Hasarlar", value=f"`Toplam Hasar`: {self.datas[f'{i}.summonerTotalTaken']}\n`Azaltılan Hasar`: **{self.datas[f'{i}.summonerMitigated']}**\n")

            with open(self.path+r"\%s.png"%i, 'rb') as f:
                picture = discord.File(f)
                mes = await self.ctx.guild.get_member(335088129134297088).send(file=picture)
                runeEmbedUrl = mes.attachments[0].url
                await mes.delete()
            embed.set_image(url=runeEmbedUrl)

            self.embedList.append(embed)
            print(f"#{i} Embed hazırlandı. {datetime.now().strftime('%H:%M:%S')}")
        return self.embedList