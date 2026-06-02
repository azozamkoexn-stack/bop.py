from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# الإعدادات - ضع مفتاحك هنا مباشرة لتجنب مشاكل Secrets
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.5-flash')
TOKEN = "8914538504:AAEg6qyggd3_l4WepVBZ3y0QsJF58JOytN4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["المساعد الذكي 🤖"], ["قسم FiveM 🚗", "قسم تقنية المعلومات 🖥️"], ["حساباتي 📱"]]
    await update.message.reply_text("أهلاً عزوز! اختر قسماً:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # 1. قائمة الأزرار (هنا لا نستخدم الذكاء الاصطناعي عشان ما يعلّق)
    if text == "/start" or text == "رجوع 🔙":
        await start(update, context)
        
    elif text == "قسم FiveM 🚗":
        await update.message.reply_text("اختر:", reply_markup=ReplyKeyboardMarkup([["إنشاء سيرفر بملفات جاهزة 📂", "إنشاء سيرفر بملفات غير جاهزة 🛠️"], ["رجوع 🔙"]], resize_keyboard=True))
    
    elif text == "قسم تقنية المعلومات 🖥️":
        await update.message.reply_text("اختر لغة:", reply_markup=ReplyKeyboardMarkup([["Python 🐍", "JavaScript 🌐"], ["رجوع 🔙"]], resize_keyboard=True))
    
    elif text == "حساباتي 📱":
        await update.message.reply_text("سنابي: https://snapchat.com/t/yURnwelI", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))

    # 2. إذا ضغط على "المساعد الذكي"، نطلب منه السؤال
    elif text == "المساعد الذكي 🤖":
        await update.message.reply_text("أنا جاهز، اسألني أي شيء:", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
        context.user_data['chatting'] = True

    # 3. فقط إذا كان المستخدم في وضع المحادثة، نرسل للذكاء الاصطناعي
    elif context.user_data.get('chatting'):
        try:
            response = model.generate_content(text)
            await update.message.reply_text(response.text, reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))
        except:
            await update.message.reply_text("حدث خطأ في الاتصال، حاول مرة أخرى.")
    
    else:
        await update.message.reply_text("اختر قسماً من القائمة:", reply_markup=ReplyKeyboardMarkup([["رجوع 🔙"]], resize_keyboard=True))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("البوت يعمل!")
    app.run_polling()
