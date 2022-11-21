import discord
from discord.ext import commands
from discord.ui import View, Button

from Commands import opGG

ChampList = ['aatrox', 'ahri', 'akali', 'akshan', 'alistar', 'amumu', 'anivia', 'annie', 'aphelios', 'ashe', 'aurelionsol', 'azir', 'bard', 'belveth', 'blitzcrank', 'brand', 'braum', 'caitlyn', 'camille', 'cassiopeia', 'chogath', 'corki', 'darius', 'diana', 'drmundo', 'draven', 'ekko', 'elise', 'evelynn', 'ezreal', 'fiddlesticks', 'fiora', 'fizz', 'galio', 'gangplank', 'garen', 'gnar', 'gragas', 'graves', 'gwen', 'hecarim', 'heimerdinger', 'illaoi', 'irelia', 'ivern', 'janna', 'jarvaniv', 'jax', 'jayce', 'jhin', 'jinx', 'kaisa', 'kalista', 'karma', 'karthus', 'kassadin', 'katarina', 'kayle', 'kayn', 'kennen', 'khazix', 'kindred', 'kled', 'kogmaw', 'leblanc', 'leesin', 'leona', 'lillia', 'lissandra', 'lucian', 'lulu', 'lux', 'malphite', 'malzahar', 'maokai', 'masteryi', 'missfortune', 'mordekaiser', 'morgana', 'nami', 'nasus', 'nautilus', 'neeko', 'nidalee', 'nilah', 'nocturne', 'nunuvewillump', 'olaf', 'orianna', 'ornn', 'pantheon', 'poppy', 'pyke', 'qiyana', 'quinn', 'rakan', 'rammus', 'reksai', 'rell', 'renataglasc', 'renekton', 'rengar', 'riven', 'rumble', 'ryze', 'samira', 'sejuani', 'senna', 'seraphine', 'sett', 'shaco', 'shen', 'shyvana', 'singed', 'sion', 'sivir', 'skarner', 'sona', 'soraka', 'swain', 'sylas', 'syndra', 'tahmkench', 'taliyah', 'talon', 
'taric', 'teemo', 'thresh', 'tristana', 'trundle', 'tryndamere', 'twistedfate', 'twitch', 'udyr', 'urgot', 'varus', 'vayne', 'veigar', 'velkoz', 'vex', 'vi', 'viego', 'viktor', 'vladimir', 'volibear', 'warwick', 'wukong', 'xayah', 'xerath', 'xinzhao', 'yasuo', 'yone', 'yorick', 'yuumi', 'zac', 'zed', 'zeri', 'ziggs', 'zilean', 'zoe', 'zyra']

EMBED_COLOR = 0x3B920A

bot = commands.Bot(command_prefix="!!", intents=discord.Intents.all(), debug_guild_id=[964943633361014805])

@bot.event
async def on_ready():
    print(f"{bot.user} has logged.")


@bot.command
async def test(ctx, *args):
    ctx.send(*args)


@bot.command()
async def image(ctx):
    with open('rune.png', 'rb') as f:
        picture = discord.File(f)
        s = await ctx.author.send(content=f"Hey{bot.latency}", file=picture)
        print(s.attachments[0].url)
        await s.delete()

        d = discord.Embed(title="G")
        d.set_author(name="Rengar", url="https://opgg-static.akamaized.net/images/profile_icons/profileIcon949.jpg?image=q_auto")
        d.set_thumbnail(url="https://opgg-static.akamaized.net/images/lol/champion/Rengar.png")
        d.set_image(url=s.attachments[0].url)
        
        await ctx.send(embed=d)


@bot.slash_command(name="opgg_account", description="Get account info via opGG", name_localizations={"tr" : "opgg_hesap"}, description_localitzations={"tr" : "opGG'den hesap bilgileri alın"})
async def opAccount(ctx: discord.ApplicationContext,
               accountname: discord.Option(str, "Hesap adını girin", requried=True)):
    
    editedAccountName = accountname.replace(" ", "%20")
    await opGG.opGGAccount(ctx, bot, editedAccountName).setup()
 

@bot.slash_command(name="opgg_champ", description="Get champ roel info via opGG", name_localizations={"tr" : "opgg_karakter"}, description_localitzations={"tr" : "opGG'den karakter buildlerini alın."})
async def opChamps(ctx: discord.ApplicationContext,
                champ: discord.Option(str, "Karakter seçin", choices=[], requried=True),
                position: discord.Option(str, "Koridor seçin", choices=["TOP", "JUNGLE", "MID", "ADC", "SUPPORT"])):

    await opGG.opGGChamps(ctx, bot, champ, position).setup()

@bot.slash_command(name="senpai_champ", description="Get champ roel info via Senpai", name_localizations={"tr" : "senpai_karakter"}, description_localitzations={"tr" : "Senpai'den karakter buildlerini alın."})
async def opChamps(ctx: discord.ApplicationContext,
                champ: discord.Option(str, "Karakter seçin", choices=[], requried=True),
                position: discord.Option(str, "Koridor seçin", choices=["TOP", "JUNGLE", "MID", "ADC", "SUPPORT"])):

    pass

bot.run("MTAxNDI1OTYwNTE1ODc2MDQ2OA.G6JttU.cqLFMwqXQHetfDGUwN5vz5BCfutA1Umea2dLgo")