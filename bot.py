#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.


from io import BytesIO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from instaloader import Instaloader, Profile, Post
import sys
import shutil
import glob
import os
import telegram
from itertools import islice
from math import ceil

bot_token = ""


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="<b>Hi There! 👋</b>\nI can download all posts (pictures + videos) in a profile, IGTV Videos & Stories from Instagram.\nPlease read /help before use.", parse_mode=telegram.ParseMode.HTML)


def help(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="This bot can help you to download Stories from Instagram without leaving Telegram. Simply send /stories with a Instagram username (handle) without '@'.\n\n<b>Example :</b>\n/stories rashmika_mandanna\n\n<b>How to find the username?</b>\nOpen Instagram app & then go to the profile that you want to download. Username must be on the top.\nIn case you are using Instagram on a browser you can find it in the Address bar.\n<b>Example : </b>Username for instagram.com/rashmika_mandanna & @rashmika_mandanna is 'rashmika_mandanna' 😉", parse_mode=telegram.ParseMode.HTML)


def about(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='''Made with ❤️ + python-telegram-bot & Instaloader.\nSource Code : <a href="https://github.com/NandiyaLive/xIGDLBot">GitHub</a>\n\n<b>Readme File : https://bit.ly/xIGDLBot''', parse_mode=telegram.ParseMode.HTML)


def contact(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Please contact me on @NandiyaX Chat.In case you want to PM please use @NandiyaBot.", parse_mode=telegram.ParseMode.HTML)


def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="You have to send a command with an username.\nRead /help before use.", parse_mode=telegram.ParseMode.HTML)


@run_async
def login(update, context):

    L = Instaloader()
    USER = ""
    PASSWORD = ""

    try:
        L.login(USER, PASSWORD)
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text="<b>API ERROR:</b>\n"+str(
            e), parse_mode=telegram.ParseMode.HTML)
        return


@run_async
def stories(update, context):

    query = update.message.text.replace("/stories ", "")

    L = Instaloader(dirname_pattern=query, download_comments=False,
                    download_video_thumbnails=False, save_metadata=False)

    try:
        profile = L.check_profile_id(query)
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text="<b>API ERROR:</b>\n"+str(
            e), parse_mode=telegram.ParseMode.HTML)
        return

    update.message.reply_text(
        "Searching for stories of : " + query + "\nInstagram ID : "+str(profile.userid))

    try:
        L.download_stories(userids=[profile.userid])
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text="<b>ERROR ò_ô</b>\n"+str(
            e), parse_mode=telegram.ParseMode.HTML)
        return

    src_dir = query

    for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
        context.bot.send_photo(
            chat_id=update.message.chat_id, photo=open(jpgfile, 'rb'))

    for vidfile in glob.iglob(os.path.join(src_dir, "*.mp4")):
        context.bot.send_video(
            chat_id=update.message.chat_id, video=open(vidfile, 'rb'))

    try:
        shutil.rmtree(query)
    except Exception:
        pass


def main():

    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("login", login))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(CommandHandler("about", about))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
