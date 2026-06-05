import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# الإعدادات: تأكد من إضافة GEMINI_API_KEY و TOKEN في Railway Variables
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')
TOKEN = os.getenv('TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["المساعد الذكي 🤖"], ["قسم FiveM 🚗", "قسم تقنية المعلومات 🖥️"], ["حساباتي 📱"]]
    await update.message.reply_text("أهلاً عزوز! اختر قسماً:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "/start" or text == "رجوع 🔙":
        context.user_data['chatting'] = False
        await start(update, context)

    # --- قسم FiveM ---
    elif text == "قسم FiveM 🚗":
        keyboard = [["ملفات جاهزة 📂", "ملفات غير جاهزة 🛠️"], ["تعليم برمجة FiveM 💻"], ["رجوع 🔙"]]
        await update.message.reply_text("قسم FiveM، اختر ما تريد:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    
    elif text == "ملفات جاهزة 📂":
        await update.message.reply_text("شرح السيرفر بملفات جاهزة:\nhttps://youtu.be/OTMCjJC39ig?si=p12653YWJJmAh4O0", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
    
    elif text == "ملفات غير جاهزة 🛠️":
        await update.message.reply_text("شرح إنشاء سيرفر من الصفر:\nhttps://youtu.be/JRCMn4s4mX4?si=UJj7hulSczbCx8E8", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
    
    elif text == "تعليم برمجة FiveM 💻":
        await update.message.reply_text("تعليم برمجة سكربتات FiveM:\nhttps://youtu.be/-VrETs6osNI?si=UC-2IThRv1HsJ2F5", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))

    # --- قسم التقنية ---
    elif text == "قسم تقنية المعلومات 🖥️":
        keyboard = [["Python 🐍", "JavaScript 🌐"], ["C++ ⚙️", "Lua 🌙"], ["رجوع 🔙"]]
        await update.message.reply_text("اختر اللغة:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    
    elif text == "Python 🐍":
        await update.message.reply_text("لغة بايثون: ممتازة للذكاء الاصطناعي والأتمتة.\nشرح: https://youtu.be/kqtD5dpn9C8", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
    elif text == "JavaScript 🌐":
        await update.message.reply_text("لغة جافا سكريبت: أساس برمجة الويب.\nشرح: https://youtu.be/B7wHpQ0eg-s", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
    elif text == "C++ ⚙️":
        await update.message.reply_text("لغة C++: قوية جداً في الأداء والألعاب.\nشرح: https://youtu.be/rVp09sltqmc", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
    elif text == "Lua 🌙":
        await update.message.reply_text("لغة Lua: هي اللغة المستخدمة في برمجة سكربتات FiveM.\nشرح: https://youtu.be/iMacBhPWn5g", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))

    # --- قسم الحسابات ---
    elif text == "حساباتي 📱":
        await update.message.reply_text("حسابات عزوز:\nتيك توك: https://www.tiktok.com/@.5q6\nسناب: https://snapchat.com/t/yURnwelI", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))

    # --- الذكاء الاصطناعي ---
    elif text == "المساعد الذكي 🤖":
        await update.message.reply_text("أنا معك، اكتب سؤالك:", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
        context.user_data['chatting'] = True

    elif context.user_data.get('chatting'):
        try:
            response = model.generate_content(text)
            await update.message.reply_text(response.text, reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
        except Exception as e:
            await update.message.reply_text("حدث خطأ في الاتصال بالذكاء الاصطناعي، تأكد من مفتاح الـ API في Railway.")
    
    else:
        await start(update, context)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
