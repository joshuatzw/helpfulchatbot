# Want to build a telegram bot that:
# Responds to questions by answering questions by pulling chatgpt api

# Webscrapes to build context for articles 
# summarises these articles using chatGPT 


# importing openAI dependencies 
import os 
import openai 
# importing Telegram dependencies 
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

from polish import polish_text


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )


# configurations
openai.organization = "org-zwbK7Hjjr1HNheSeCU32ptT7"
openai.api_key = "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"


# Polish text takes the "Update" object from Telegram API, isolates the update > message > text item
# then drops the  / command in the beginning of the sentence. 

# Basic ChatGPT Function: calling openAI api
def speak_to_chat_gpt(update):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role" : "user", "content" : polish_text(update) }
        ]
    )
    final_answer = completion["choices"][0]["message"]["content"]
    return (final_answer)


def translate_chat_gpt(update):
    # Identifying what the ISO 639-1 Language Code is
    text = polish_text(update)
    text_prefix = "Read through the text and identify its language. Return only the iso 639-1 language code:"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role" : "user", "content" : text_prefix + text }
        ]
    )
    
    language_code = completion["choices"][0]["message"]["content"]
    print(language_code)
    if language_code != "en":
        final_translation_prefix = "Translate the following to English please:"
    elif language_code == "en":
        final_translation_prefix = "Translate the following to Chinese please:"

    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": final_translation_prefix + text}
            ]
        )
    
    final_answer = completion["choices"][0]["message"]["content"]
    print (final_answer)
    return (final_answer)

    


async def start (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, and thanks for using ZW's Helpful chatbot! 🤖 \n\nHere's a list of commands to get you started: \n/start: Recalls this list of instructions \n/ask: Interact with ChatGPT to get ChatGPT to do anything you'd like!\n/translate: Translates all languages to English, and English to Chinese. More language support coming shortly. \n\n⚡ Upcoming Features ⚡: \n1. Currency Conversion \n2. Weather Forecast \n"
    )

async def ask (update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("ask command triggered.")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=speak_to_chat_gpt(update)
    )

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("translate command triggered")
    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=translate_chat_gpt(update)
    )


# Starting the main prog:
# 1. building the application/bot
# 2. building the command handler 
# 3. running the app 
if __name__ == '__main__':
    application = ApplicationBuilder().token('6216896704:AAESUnIO3Tlm4GYcWUg9nzaITgpLGS-Qm2E').build()

    # Tell the bot to know how to handle /start command
    start_handler = CommandHandler('start', start)
    ask_handler = CommandHandler('ask', ask)
    translate_handler = CommandHandler('translate', translate)
    # ask_gpt_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), ask_gpt)
    
    # Running the handlers in the actual program
    application.add_handler(start_handler)
    application.add_handler(ask_handler)
    application.add_handler(translate_handler)

    application.run_polling()