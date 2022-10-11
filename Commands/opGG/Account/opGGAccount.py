import discord
from discord.ui import Button, View
from datetime import datetime
from shutil import rmtree
from os import path

from ..Embeds.EmbedList import EmbedList
from .opAcFirstPage import opAcFirst
from .opAcGames import opAcGames
from ..getID import GetOPID


class opGGAccount(View):
        def __init__(self, ctx, bot, accountName) -> None:
            super().__init__(timeout=None)#View options (discord.ui.View)

            self.ctx = ctx #The message when bot reply to us and crate a message
            self.bot = bot
            self.accountName = accountName

            self.EmbedList = EmbedList()
            self.selfID = id(self)

            self.current_page = 0
            self.Embeds = self.EmbedList.embedPages
            self.EmbedsLen = 0

            self.want_delete = False

        async def asyncDeleteMessage(self):
            waiting = await self.bot.wait_for('interaction', check=lambda i: i == self.ctx, timeout=7)
            if waiting:
                return True
            else:
                await self.ctx.edit_message("f")

        #First Page Button
        @discord.ui.button(emoji="⏪", style=discord.ButtonStyle.secondary)
        async def firstPage_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.current_page = 0
            self.want_delete = False

            self.children[2].label = "" #Delete button
            self.children[2].style = discord.ButtonStyle.success

            button.disabled = True #Self button disabled
            self.children[1].disabled = True #Previous Page Button disabled
            self.children[3].disabled = False #Next Page Button enable, if you press next btn it stay disabled if you in last page
            self.children[4].disabled = False #Last Page Button

            self.Embeds[self.current_page].set_footer(text=f"{self.Embeds.index(self.Embeds[self.current_page])+1}/{self.EmbedsLen}")
            await interaction.response.edit_message(embed=self.Embeds[self.current_page],view=self)

        #Previous Page Button
        @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
        async def prePage_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.current_page -= 1
            self.want_delete = False

            self.children[2].label = "" #Delete button
            self.children[2].style = discord.ButtonStyle.success

            if self.current_page == 0:
                button.disabled = True
                self.children[0].disabled = True
            
            self.children[3].disabled = False
            self.children[4].disabled = False

            self.Embeds[self.current_page].set_footer(text=f"{self.Embeds.index(self.Embeds[self.current_page])+1}/{self.EmbedsLen}")
            await interaction.response.edit_message(embed=self.Embeds[self.current_page], view=self)

        
        #Null button, doesn't effect
        @discord.ui.button(emoji="⛔", style=discord.ButtonStyle.success)
        async def deleteButton_callback(self, button, interaction):
            
            if self.want_delete == True:
                rmtree(path.dirname(__file__) + r"\Runes\%s"%self.selfID)

                await interaction.message.delete()
            else:
                self.want_delete = True
                button.style = discord.ButtonStyle.danger
                button.label = "Eminseniz Tıklayın."
                await interaction.response.edit_message(view=self)

        #Next Page Button
        @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
        async def nextPage_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.current_page += 1
            self.want_delete = False

            self.children[2].label = "" #Delete button
            self.children[2].style = discord.ButtonStyle.success
            
            if self.current_page == self.EmbedsLen-1:
                button.disabled = True
                self.children[4].disabled = True

            self.children[0].disabled = False
            self.children[1].disabled = False
            
            self.Embeds[self.current_page].set_footer(text=f"{self.Embeds.index(self.Embeds[self.current_page])+1}/{self.EmbedsLen}")
            await interaction.response.edit_message(embed=self.Embeds[self.current_page], view=self)

        #Last Page Button
        @discord.ui.button(emoji="⏩", style=discord.ButtonStyle.secondary)
        async def lastPage_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.current_page = self.EmbedsLen - 1
            self.want_delete = False

            self.children[2].label = "" #Delete button
            self.children[2].style = discord.ButtonStyle.success

            button.disabled = True #Self
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[3].disabled = True

            self.Embeds[self.current_page].set_footer(text=f"{self.Embeds.index(self.Embeds[self.current_page])+1}/{self.EmbedsLen}")
            await interaction.response.edit_message(embed=self.Embeds[self.current_page], view=self)

        async def setup(self):
            await self.ctx.defer()
            self.children[0].disabled = True
            self.children[1].disabled = True

            accountId = GetOPID(self.accountName).getId()
            print(f"ID Alındı ({self}): {datetime.now().strftime('%H:%M:%S')} {accountId}")
            games = await opAcGames(ctx=self.ctx, opAccountID=accountId, requestSelfID=self.selfID).getEmbedList()
            firstPage = opAcFirst(opAccountID=accountId).getEmbed()

            self.EmbedList.add_embeds(firstPage)
            self.EmbedList.add_embeds(*games)
            self.EmbedsLen = len(self.Embeds)

            if self.EmbedsLen == 1:
                self.children[3].disabled = True
                self.children[4].disabled = True

            self.Embeds[self.current_page].timestamp = datetime.utcnow()
            self.Embeds[self.current_page].set_footer(text=f"{self.Embeds.index(self.Embeds[self.current_page])+1}/{self.EmbedsLen}")
            
            await self.ctx.respond(content=self.ctx.author.mention, embed=self.Embeds[self.current_page], view=self)
            await self.asyncDeleteMessage()
