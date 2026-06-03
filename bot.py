import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# إعداد الربط
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')
TOKEN = os.getenv('TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["المساعد الذكي 🤖"], ["قسم FiveM 🚗", "قسم تقنية المعلومات 🖥️"], ["حساباتي 📱", "المقاطع 🎥"]]
    await update.message.reply_text("أهلاً عزوز! اختر قسماً:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "/start" or text == "رجوع 🔙":
        context.user_data['chatting'] = False
        await start(update, context)
        
    elif text == "حساباتي 📱":
        await update.message.reply_text("سنابي: https://snapchat.com/t/yURnwelI", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
    
    elif text == "المقاطع 🎥":
        # هنا تقدر تحط روابط المقاطع اللي اختفت
        await update.message.reply_text("قائمة مقاطعي:\nرابط 1: ...\nرابط 2: ...", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))

    elif text == "المساعد الذكي 🤖":
        await update.message.reply_text("أنا جاهز، اسألني:", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
        context.user_data['chatting'] = True

    elif context.user_data.get('chatting'):
        try:
            response = model.generate_content(text)
            await update.message.reply_text(response.text, reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
        except Exception as e:
            await update.message.reply_text("عذراً، تأكد من أن مفتاح Gemini (GEMINI_API_KEY) صحيح في إعدادات Railway.")

    else:
        await update.message.reply_text("اختر من القائمة:", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
