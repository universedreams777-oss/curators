import telebot
import re

# === НАСТРОЙКИ ===
API_TOKEN = '8053472683:AAHhlg9q26TXeF2GvmOghUiWL2fXltE3I9U'
CHANNEL_ID = -1002704063181  # ID канала

curators = [
    "@neurogury",
    "@Good_zee_calligraphy",
    "@vscpnoy",
    "@Olga_Lukashina_Vocal"
]

# === СОСТОЯНИЕ ===
last_index = -1
assigned_texts = set()

# === СОЗДАНИЕ БОТА ===
bot = telebot.TeleBot(API_TOKEN)

# === ОБРАБОТКА СООБЩЕНИЙ ===
@bot.channel_post_handler(func=lambda m: m.text and m.text.lower().startswith("наталия"))
def handle_message(message):
    global last_index

    text = message.text.strip()
    if text in assigned_texts:
        return
    assigned_texts.add(text)

    last_index = (last_index + 1) % len(curators)
    curator = curators[last_index]

    name_match = re.search(r"Пользователь\s+(.+)", text)
    link_match = re.search(r"https?://[^\s\]]+", text)

    student_name = name_match.group(1).strip() if name_match else "Не найдено"
    student_link = link_match.group(0).strip() if link_match else "Не найдено"

    final_text = (
        f"*🧠🥰 Твой ученик, проверь его пожалуйста {curator}*\n\n"
        f"*{student_name}*\n\n"
        f"*🔗 Ссылка на ученика:* {student_link}"
    )

    bot.send_message(CHANNEL_ID, final_text, parse_mode="Markdown")

# === ЗАПУСК ===
print("Бот запущен...")
bot.polling(none_stop=True)
