import discord
from discord.ext import commands

from Commands import opGG

ChampList = ('aatrox', 'ahri', 'akali', 'akshan', 'alistar', 'amumu', 'anivia', 'annie', 'aphelios', 'ashe', 'aurelionsol', 'azir', 'bard', 'belveth', 'blitzcrank', 'brand', 'braum', 'caitlyn', 'camille', 'cassiopeia', 'chogath', 'corki', 'darius', 'diana', 'drmundo', 'draven', 'ekko', 'elise', 'evelynn', 'ezreal', 'fiddlesticks', 'fiora', 'fizz', 'galio', 'gangplank', 'garen', 'gnar', 'gragas', 'graves', 'gwen', 'hecarim', 'heimerdinger', 'illaoi', 'irelia', 'ivern', 'janna', 'jarvaniv', 'jax', 'jayce', 'jhin', 'jinx', 'kaisa', 'kalista', 'karma', 'karthus', 'kassadin', 'katarina', 'kayle', 'kayn', 'kennen', 'khazix', 'kindred', 'kled', 'kogmaw', 'leblanc', 'leesin', 'leona', 'lillia', 'lissandra', 'lucian', 'lulu', 'lux', 'malphite', 'malzahar', 'maokai', 'masteryi', 'missfortune', 'mordekaiser', 'morgana', 'nami', 'nasus', 'nautilus', 'neeko', 'nidalee', 'nilah', 'nocturne', 'nunuvewillump', 'olaf', 'orianna', 'ornn', 'pantheon', 'poppy', 'pyke', 'qiyana', 'quinn', 'rakan', 'rammus', 'reksai', 'rell', 'renataglasc', 'renekton', 'rengar', 'riven', 'rumble', 'ryze', 'samira', 'sejuani', 'senna', 'seraphine', 'sett', 'shaco', 'shen', 'shyvana', 'singed', 'sion', 'sivir', 'skarner', 'sona', 'soraka', 'swain', 'sylas', 'syndra', 'tahmkench', 'taliyah', 'talon', 
'taric', 'teemo', 'thresh', 'tristana', 'trundle', 'tryndamere', 'twistedfate', 'twitch', 'udyr', 'urgot', 'varus', 'vayne', 'veigar', 'velkoz', 'vex', 'vi', 'viego', 'viktor', 'vladimir', 'volibear', 'warwick', 'wukong', 'xayah', 'xerath', 'xinzhao', 'yasuo', 'yone', 'yorick', 'yuumi', 'zac', 'zed', 'zeri', 'ziggs', 'zilean', 'zoe', 'zyra')

EMBED_COLOR = 0x3B920A

bot = commands.Bot(command_prefix="!!", intents=discord.Intents.all(), debug_guild_id=[YOUR_DISCORD_SERVER_ID])

@bot.event
async def on_ready():
    print(f"{bot.user} has logged.")

@bot.slash_command(name="opgg_account", description="Get account info via opGG", name_localizations={"tr" : "opgg_hesap"}, description_localitzations={"tr" : "opGG'den hesap bilgileri alın"})
async def opAccount(ctx: discord.ApplicationContext,
               accountname: discord.Option(str, "Enter account name", requried=True)):
    
    editedAccountName = accountname.replace(" ", "%20")
    await opGG.opGGAccount(ctx, bot, editedAccountName).setup()
 

@bot.slash_command(name="opgg_champ", description="Get champ role info via opGG", name_localizations={"tr" : "opgg_karakter"}, description_localitzations={"tr" : "opGG'den karakter buildlerini alın."})
async def opChamps(ctx: discord.ApplicationContext,
                champ: discord.Option(str, "Choice champion", choices=[], requried=True),
                position: discord.Option(str, "Choice lane", choices=["TOP", "JUNGLE", "MID", "ADC", "SUPPORT"])):

    await opGG.opGGChamps(ctx, bot, champ, position).setup()

bot.run("TOKEN")