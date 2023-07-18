VK-post-from-Telegram

This code is for a Telegram bot that fetches the latest posts from a VK (VKontakte) group and sends them to its subscribed Telegram users. The bot is built using the aiogram library, which is an asynchronous framework for Telegram Bot API.

Here's a step-by-step explanation of the code:

1 Importing Libraries: The code begins by importing the necessary libraries, including asyncio, aiogram, sqlite3, vk_api, os, and requests. These libraries are used for asynchronous programming, working with Telegram and VK APIs, handling the SQLite database, and making HTTP requests.

2 Defining Tokens and IDs: The code defines several constants such as vk_token, group_id, and telegram_token. You need to replace 'YOUR VK TOKEN', 'YOUR ID GROUP', and 'YOUR TG TOKEN' with actual VK and Telegram bot tokens and VK group ID.

3 Creating Telegram Bot: The code creates a Telegram bot using the provided telegram_token.

4 Dispatcher and Handlers: The Dispatcher class is used to register message handlers. The bot responds to the /start command, which adds the user's ID to the SQLite database and welcomes them.

5 SQLite Database Operations: The code defines functions to create a SQLite database if it doesn't exist, add a user to the database, delete a user from the database, and get a list of all users in the database.

6 Fetching VK Group Posts: The function get_last_posts fetches the latest posts from the VK group using VK API. It retrieves the post text and photo URLs for each post and returns them in a list.

7 Sending Data to Users: The send_data_to_users coroutine runs in the background (every 2 hours). It fetches the latest VK group posts, retrieves the list of subscribed users from the database, and sends the posts to each user via Telegram messages. If a user is no longer accessible (e.g., blocked the bot), they are removed from the database.

8 Starting the Bot: The on_startup function is called when the bot starts. It creates the SQLite database, starts the send_data_to_users coroutine, and initiates the bot polling process.

9 Main Block: The main block of the code initiates the event loop, creates the database, starts the send_data_to_users coroutine, and starts the bot polling process using executor.start_polling.

Please note that for this code to work properly, you need to replace 'YOUR VK TOKEN', 'YOUR ID GROUP', and 'YOUR TG TOKEN' with the actual VK and Telegram bot tokens and VK group ID.
