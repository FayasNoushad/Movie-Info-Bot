# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .info import *
from .admin import *

START_TEXT = """Hello {}  😌
I am a movie information finder bot.

> `I can find information of all movies.`

Made by @FayasNoushad"""

HELP_TEXT = """**Hey, Follow these steps:**

➠ Just send a movie name for information.
➠ I will send the information of movie.

**Available Commands**

/start - Checking Bot Online
/help - For more help
/about - For more about me
/status - For bot status
/settings - For bot settings
/reset - For reset bot settings

Made by @FayasNoushad"""

ABOUT_TEXT = """--**About Me 😎**--

🤖 **Name :** [Movie Info Bot](https://telegram.me/{})

👨‍💻 **Developer :** [GitHub](https://github.com/FayasNoushad) | [Telegram](https://telegram.me/FayasNoushad)

👥 **Group :** [Developer Team](https://telegram.me/TheDeveloperTeam)

🌐 **Source :** [👉 Click here](https://github.com/FayasNoushad/Movie-Info-Bot)

📝 **Language :** [Python3](https://python.org)

🧰 **Framework :** [Pyrogram](https://pyrogram.org)"""

SETTINGS_TEXT = "**Settings**"

RESET_TEXT = "**Are you sure for reset.**"

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Help', callback_data='help'),
        InlineKeyboardButton('About 🔰', callback_data='about'),
        InlineKeyboardButton('Close ⛔️', callback_data='close')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('📹 Video Tutorial', url='https://www.youtube.com/watch?v=qjMRZlzhCVo')
        ],[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('About 🔰', callback_data='about')
        ],[
        InlineKeyboardButton('⚒ Settings', callback_data='settings'),
        InlineKeyboardButton('Close ⛔️', callback_data='close')
        ]]
    )

ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('Help ⚙', callback_data='help')
        ],[
        InlineKeyboardButton('Close ⛔️', callback_data='close')
        ]]
    )

SETTINGS_BUTTONS = [
    [
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('Help ⚙', callback_data='help')
    ],
    [
        InlineKeyboardButton('🔄 Reset', callback_data='reset'),
        InlineKeyboardButton('Close ⛔️', callback_data='close')
    ]
]

RESET_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="Yes ✅", callback_data="confirm_reset"),
        InlineKeyboardButton(text="No ❌", callback_data="cancel_reset")
        ]]
    )

JOIN_BUTTONS = [
    InlineKeyboardButton(
        text='⚙ Join Updates Channel ⚙',
        url='https://telegram.me/FayasNoushad'
    )
]

BUTTONS = InlineKeyboardMarkup(
    [JOIN_BUTTONS]
)

@Client.on_message(filters.private & filters.command(["start"]), group=1)
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.text == "/start":
        await update.reply_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )
    else:
        movie = update.text.split(" ", 1)[1]
        await get_movie(bot, update, movie)

@Client.on_message(filters.private & filters.command(["help"]), group=2)
async def help(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS,
        quote=True
    )

@Client.on_message(filters.private & filters.command(["about"]), group=3)
async def about(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS,
        quote=True
    )

@Client.on_message(filters.private & filters.command(["reset"]), group=4)
async def reset(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=RESET_TEXT,
        disable_web_page_preview=True,
        reply_markup=RESET_BUTTONS,
        quote=True
    )

@Client.on_message(filters.private & filters.command(["status"]), group=5)
async def status(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )

@Client.on_message(filters.private & filters.command(["settings"]), group=6)
async def settings(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await display_settings(bot, update, db)

async def display_settings(bot, update, db, cb=False):
    chat_id = update.from_user.id
    text = SETTINGS_TEXT
    buttons = []
    if await db.allow_info(chat_id, info="photo"):
        buttons.append(InlineKeyboardButton(text="Photo ✅", callback_data="set+photo"))
    else:
        buttons.append(InlineKeyboardButton(text="Photo ❌", callback_data="set+photo"))
    if await db.allow_info(chat_id, info="type"):
        buttons.append(InlineKeyboardButton(text="Type ✅", callback_data="set+type"))
    else:
        buttons.append(InlineKeyboardButton(text="Type ❌", callback_data="set+type"))
    if await db.allow_info(chat_id, info="release_date"):
        buttons.append(InlineKeyboardButton(text="Release Date ✅", callback_data="set+release_date"))
    else:
        buttons.append(InlineKeyboardButton(text="Release Date ❌", callback_data="set+release_date"))
    if await db.allow_info(chat_id, info="release_year"):
        buttons.append(InlineKeyboardButton(text="Release Year ✅", callback_data="set+release_year"))
    else:
        buttons.append(InlineKeyboardButton(text="Release Year ❌", callback_data="set+release_year"))
    if await db.allow_info(chat_id, info="score"):
        buttons.append(InlineKeyboardButton(text="Score ✅", callback_data="set+score"))
    else:
        buttons.append(InlineKeyboardButton(text="Score ❌", callback_data="set+score"))
    if await db.allow_info(chat_id, info="providers"):
        buttons.append(InlineKeyboardButton(text="Providers ✅", callback_data="set+providers"))
    else:
        buttons.append(InlineKeyboardButton(text="Providers ❌", callback_data="set+providers"))
    keyboard = []
    for button in buttons:
        if len(keyboard) == 0 or len(keyboard[-1]) >= 1:
            keyboard.append([button])
        else:
            keyboard[-1].append(button)
    for setting_button in SETTINGS_BUTTONS:
        keyboard.append(setting_button)
    if cb:
        await update.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )
    else:
        await update.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True,
            quote=True
        )
