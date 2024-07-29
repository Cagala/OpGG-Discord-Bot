![Build Example](http://drive.google.com/uc?export=view&id=1PbxEFbRBQXqiTEZwpTLpyEMbPlrCuupn)

This project allows quick access to any League of Legends champion's current item and skill build information without using an extra web browser tab via a Discord bot. It is best suited for those playing LoL with friends on Discord and for users with low to mid-range computers.

**Important:** This version is outdated and should not be used for new projects. The method that used with get data via opGG API is no longer working.

# OpGG Discord Bot
The bot accesses [op.gg](https://www.op.gg) with character and lane input, then retrieves all character information via op.gg's internal API, obtained by scraping the web network. In fact, op.gg doesn't have an API for end users, but it uses an internal API to provide these types of information for its service. Riot Games (the publisher and developer of the game) offers an API, but to use those APIs, you need higher budget projects to get detailed APIs.

Also, the API doesn't contain ready-to-use build templates. It provides information on which runes and items are bought. So, the bot gets the IDs of the items and runes, finds their PNG files from op.gg, puts them into a template, and finally creates the build image.

Most of the time, you just need this information for the moment. Discord embedding only accepts the URL of the image. So, the created image should be in a CDN service, but based on the scale of the project, there is no storage and upload service. Therefore, the bot sends a message to the Discord user, copies the CDN URL that Discord provides, puts it into a Discord embed, and then deletes the message. This approach saves budget and project scale by preventing unnecessary storage usage.

The Discord Bot API and Discord Embeds don't contain a changeable embed list component. This feature is built from scratch too. You can use the arrow buttons to change the current page and delete the message with the "⛔" sign from the server.
