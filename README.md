# Manga Library Bot
## A Discord bot that can manage manga to read
### Disclaimer
**This project is built for personal use and demonstrates my understanding of API interactions. It is not intended for commercial use, and I do not claim ownership of the data used from the API. It does not involve any redistribution or modification of content.**

### Overview
This Discord bot provides real-time notifications for manga series updates using the MangaDex API. Users can subscribe to their favorite manga series and receive alerts when new chapters are released.

### Usage
- Subscribe: Use the `.sub` command followed by the title of the manga series to subscribe. Example: `.sub Mobile Suit Gundam Thunderbolt`
- Unsubscribe: Use the `.unsub` command followed by the title of the manga series to unsubscribe. Example: `.unsub Mobile Suit Gundam Thunderbolt`
- List Subscriptions: Use the `.list` command to list all the manga series you are currently following.

### Notices
- This is just code for a Discord bot, not the bot itself. You'll have to make your own bot, get started at the [Discord Developer Portal](https://discord.com/developers)
- The bot, by default, sends notifications to a channel called `manga-updates`. You might want to modify the code to send it elsewhere (line 129), or create a channel on your server
- It's important to specify as much as possible when subscribing to a series, the API finds the closest title with what you give it
