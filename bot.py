#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
import requests
from bs4 import BeautifulSoup as bs
import wget
import os


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Instagram Story Downloader Bot.\nPlease note that this is still on beta stage.\n\nPlease leave a feedback on @NandiyaThings Support Caht.", parse_mode=telegram.ParseMode.HTML)


def help(update, context):
    update.message.reply_text('Send /stories [username]')


@run_async
def stories(update, context):

    query = update.message.text.replace("/stories ", "")

    url = f"https://www.insta-stories.com/en/stories/{query}"
    r = requests.get(url).text

    soup = bs(r, "lxml")

    if soup.find("div", class_="msg msg-user-not-found"):
        update.message.reply_text(
            "This username doesn't exist. Please try with another one.")

    else:
        if soup.find("div", class_="msg msg-no-stories"):
            update.message.reply_text(
                "No stories available. Please try again later.")

        else:
            try:
                profile = soup.find(
                    "div", class_="user-name").text.replace("\n", "")
                update.message.reply_text(f"Downloading stories by {profile}")
                for items in soup:
                    image = soup.find("img", class_="story-image")
                    img_url = image["src"]
                    video = soup.find("video", class_="story-video")
                    vid_url = video["src"]

                context.bot.send_video(
                    chat_id=update.message.chat_id, video=vid_url)
                context.bot.send_photo(
                    chat_id=update.message.chat_id, photo=img_url)

            except:
                update.message.reply_text(
                    "Something went wrong. Please try again later.")

def echo(update, context):
    update.message.reply_text('read /help')


def main():
    updater = Updater("TOKEN", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("stories", stories))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
