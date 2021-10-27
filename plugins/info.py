# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import json
import requests
from .admin import *
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import *


API = "https://api.sumanjay.cf/watch/query="

JOIN_BUTTONS = [
    InlineKeyboardButton(
        text='⚙ Join Updates Channel ⚙',
        url='https://telegram.me/FayasNoushad'
    )
]


@Client.on_message(filters.command(["info", "information"]), group=-1)
async def get_command(bot, update):
    movie = requote_uri(update.text.split(" ", 1)[1])
    username = (await bot.get_me()).username
    keyboard = [
        InlineKeyboardButton(
            text="Click here",
            url=f"https://telegram.me/{username}?start={movie}"
        )
    ]
    await update.reply_text(
        text=f"**Click the button below**",
        reply_markup=InlineKeyboardMarkup([keyboard]),
        disable_web_page_preview=True,
        quote=True
    )


@Client.on_message(filters.private & filters.text & ~filters.via_bot & ~filters.edited)
async def get_movie_name(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.text.startswith("/"):
        return
    await get_movie(bot, update, update.text)


def get_movies(name):
    movie_name = requote_uri(name)
    movie_api = API + movie_name
    r = requests.get(movie_api)
    movies = r.json()
    return movies


async def get_movie(bot, update, name, cb=False):
    movies = get_movies(name)
    number = 0
    keyboard = []
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Select required option"
    for movie in movies:
        photo, description, info = await movie_info(movie, update.from_user.id)
        number += 1
        try:
            movie_text = "movie|" + name + "|" + str(number)
            button = [
                InlineKeyboardButton(
                    text=description,
                    callback_data=movie_text
                )
            ]
            keyboard.append(button)
        except:
            pass
    keyboard.append(JOIN_BUTTONS)
    if cb and not update.message.text:
        await update.message.reply_to_message.reply_text(
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        await update.message.delete()
    elif cb:
        await update.message.edit_text(
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.reply_text(
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )


async def movie_info(movie, user_id):
    try:
        if movie['movie_thumb'] and await db.allow_info(user_id, "photo"):
            photo = movie['movie_thumb']
        else:
            photo = None
    except:
        photo = None
    description_set = []
    if movie['title']:
        description_set.append(movie['title'])
    if movie['type']:
        description_set.append(movie['type'].capitalize())
    if movie['release_year']:
        description_set.append(str(movie['release_year']))
    description = " | ".join(description_set)
    try:
        info = f"**Title:** `{movie['title']}`\n"
    except:
        info = None 
    try:
        if movie['type'] and await db.allow_info(user_id, "type"):
            info += f"**Type:** `{movie['type'].capitalize()}`\n"
    except:
        pass
    try:
        if movie['release_date'] and await db.allow_info(user_id, "release_date"):
            info += f"**Release Date:** `{str(movie['release_date'])}`\n"
    except:
        pass
    try:
        if movie['release_year'] and await db.allow_info(user_id, "release_year"):
            info += f"**Release Year:** `{movie['release_year']}`\n"
    except:
        pass
    try:
        if movie['score'] and await db.allow_info(user_id, "score"):
            scores = movie['score']
            info += "**Score:** "
            score_set = []
            for score in scores:
                score_set.append(f"{score.upper()} - `{str(scores[score])}`")
            info += " | ".join(score_set) + "\n"
    except:
        pass
    try:
        if movie['providers'] and await db.allow_info(user_id, "providers"):
            info += "**Providers:** "
            providers = movie['providers']
            provider_set = []
            for provider in providers:
                provider_set.append(f"<a href={providers[provider]}>{provider.capitalize()}</a>")
            info += " | ".join(provider_set)
    except:
        pass
    return photo, description, info


@Client.on_inline_query()
async def inline_info(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await update.answer(
            results=[],
            switch_pm_text="First start the bot",
            switch_pm_parameter="start"
        )
        return
    query = update.query
    num = None
    if "|" in query:
        set = query.split("|", -1)
        movie_name = set[0]
        num = int(set[1])
    else:
        movie_name = query
    movies = [get_movies(movie_name)[num - 1]] if num else get_movies(movie_name)
    answers = []
    reply_markup = InlineKeyboardMarkup([JOIN_BUTTONS])
    for movie in movies:
        photo, description, info = await movie_info(movie, update.from_user.id)
        if photo is None:
            try:
                answers.append(
                    InlineQueryResultArticle(
                        title=movie['title'],
                        thumb_url=movie['movie_thumb'] if movie['movie_thumb'] else None,
                        description=description,
                        input_message_content=InputTextMessageContent(
                            message_text=info,
                            disable_web_page_preview=True
                        ),
                        reply_markup=reply_markup
                    )
                )
            except Exception as error:
                print(error)
        else:
            try:
                answers.append(
                    InlineQueryResultPhoto(
                        title=movie['title'],
                        photo_url=photo,
                        description=description,
                        caption=info,
                        reply_markup=reply_markup
                    )
                )
            except Exception as error:
                print(error)
    await update.answer(answers)


@Client.on_callback_query(group=11)
async def send_movie_info(bot, update):
    if update.data.startswith("back|") or update.data.startswith("movie|"):
        await update.answer("Processing")
    else:
        return
    if update.data.startswith("back"):
        name = update.data.split("|")[1]
        movie = await get_movie(bot, update, name, cb=True)
    elif update.data.startswith("movie|"):
        callback, name, value = update.data.split("|")
        movie = get_movies(name)[int(value) - 1]
        photo, description, information = await movie_info(movie=movie, user_id=update.from_user.id)
        callback_buttons = [
            InlineKeyboardButton(text="🔙 Back", callback_data=f"back|{name}"),
            InlineKeyboardButton(text="🔄 Refresh", callback_data=update.data),
            InlineKeyboardButton(text="Close ⛔️", callback_data="close")
        ]
        if photo:
            if update.message.reply_to_message:
                await update.message.reply_to_message.reply_photo(
                    photo=photo,
                    caption=information,
                    reply_markup=InlineKeyboardMarkup(
                        [callback_buttons, JOIN_BUTTONS]
                    ),
                    quote=True
                )
            else:
                await update.message.reply_photo(
                    photo=photo,
                    caption=information,
                    reply_markup=InlineKeyboardMarkup(
                        [callback_buttons, JOIN_BUTTONS]
                    ),
                    quote=True
                )
            await update.message.delete()
        else:
            if update.message.media:
                await update.message.reply_to_message.reply_text(
                    text=information,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [callback_buttons, JOIN_BUTTONS]
                    ),
                    quote=True
                )
                await update.message.delete()
            else:
                await update.message.edit_text(
                    text=information,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [callback_buttons, JOIN_BUTTONS]
                    )
                )
