from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import Application
import telegram.ext
import main as m
import threading
import time
import logging

fw = open("urls.txt", "r")
interval = 120


def read_from_file():
    for url in fw:
        urls.append(url)

urls = []

read_from_file()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def addurl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.text.replace("/addurl ", "")
    urls.append(msg)
    if(main.check_url(msg)):
        f = open("urls.txt", "a")
        f.write(msg + "\n")
        f.close()
    else:
        logging.info("Inserted URL is not correct")

async def listurl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Current URLS:")
    for url in urls:
        await update.message.reply_text(url)

def check_sites_thread_fun():
    m.check_sites(urls)


async def check_sites(context: ContextTypes.DEFAULT_TYPE): 
    if(len(urls) > 0):
        check_sites_thread = threading.Thread(target=check_sites_thread_fun)
        check_sites_thread.start()


def main():
    application = telegram.ext.ApplicationBuilder().token("7030039868:AAGIchRX3qnUjLV157ETzdyFgTdhpiTQfKk").build()
    job_queue = application.job_queue
    job_queue.run_repeating(check_sites, interval=240, first=5)
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addurl", addurl))
    application.add_handler(CommandHandler("listurl", listurl)) 
    application.run_polling()


if __name__ == '__main__':
    main()