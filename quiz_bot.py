

import telebot
from telebot import types


BOT_TOKEN = "8339772715:AAErZ2V55mLDcKO7imcxrb-ci6QrkBpZzbA"

bot = telebot.TeleBot(BOT_TOKEN)


questions = {
    1: {
        "question": "Python da print ning vazifasi nima?",
        "options": ["Matnni ekranga chiqaradi", "O‘zgaruvchi yaratadi", "Faylni o‘qiydi", "Ma’lumotni saqlaydi"],
        "answer": "Matnni ekranga chiqaradi"
    },
    2: {
        "question": "HTML ning to‘liq nomi nima?",
        "options": ["Hyper Text Markup Language", "High Transfer Markup Language", "Home Tool Markup Language", "Hyper Text Machine Language"],
        "answer": "Hyper Text Markup Language"
    },
    3: {
        "question": "Python-da ro‘yxatni qanday belgilaymiz?",
        "options": ["{}", "[]", "()", "<>"],
        "answer": "[]"
    }
}


user_scores = {}
user_states = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id

    
    bot.send_message(
        user_id,
        "👋 Assalomu alaykum!\nBotga xush kelibsiz!\n\nQuizzni boshlash uchun quyidagi tugmani bosing 👇"
    )


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("▶️ Savollarni boshlash")
    markup.add(start_button)
    bot.send_message(user_id, "Tayyor bo‘lsangiz boshlaymiz!", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "▶️ Savollarni boshlash")
def start_quiz(message):
    user_id = message.chat.id
    user_states[user_id] = 1
    user_scores[user_id] = 0
    send_question(user_id, 1)


def send_question(chat_id, q_id):
    if q_id not in questions:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("▶️ Savollarni boshlash"))
        bot.send_message(
            chat_id,
            f"🎉 Test tugadi!\nSizning natijangiz: {user_scores[chat_id]} / {len(questions)}",
            reply_markup=markup
        )
        return

    q = questions[q_id]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for opt in q["options"]:
        markup.add(types.KeyboardButton(opt))
    
    bot.send_message(chat_id, f"❓ {q['question']}", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def check_answer(message):
    user_id = message.chat.id

    
    if user_id not in user_states:
        bot.send_message(user_id, "Boshlash uchun /start buyrug‘ini bosing.")
        return

    q_id = user_states[user_id]
    if q_id not in questions:
        bot.send_message(user_id, "Test tugagan. Qayta boshlash uchun '▶️ Savollarni boshlash' bosing.")
        return

    q = questions[q_id]
    correct = q["answer"]

    if message.text == correct:
        bot.send_message(user_id, "✅ To‘g‘ri javob!")
        user_scores[user_id] += 1
    else:
        bot.send_message(user_id, f"❌ Noto‘g‘ri. To‘g‘ri javob: {correct}")

    user_states[user_id] += 1
    send_question(user_id, user_states[user_id])


bot.polling()
