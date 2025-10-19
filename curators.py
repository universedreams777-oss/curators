import telebot
import re

# === НАСТРОЙКИ ===
API_TOKEN = '8053472683:AAHhlg9q26TXeF2GvmOghUiWL2fXltE3I9U'
CHANNEL_ID = -1002704063181  # ID канала (без кавычек)

curators = [
    "@neurogury",
    "@Good_zee_calligraphy",
    "@vscpnoy",
    "@Olga_Lukashina_Vocal"
]

# === ВРЕМЕННОЕ СОСТОЯНИЕ ===
last_index = -1
assigned_texts = set()

# === СОЗДАНИЕ БОТА ===
bot = telebot.TeleBot(API_TOKEN)

# === ОБРАБОТЧИК СООБЩЕНИЙ В КАНАЛЕ ===
@bot.channel_post_handler(func=lambda message: message.text and message.text.lower().startswith("наталия"))
def handle_message(message):
    global last_index

    text = message.text.strip()

    # Пропустить, если уже было
    if text in assigned_texts:
        return
    assigned_texts.add(text)

    # Назначение куратора по кругу
    last_index = (last_index + 1) % len(curators)
    curator = curators[last_index]

    # Извлечение данных
    name_match = re.search(r"Пользователь\s+(.+)", text)
    email_match = re.search(r"Почта\s+([^\s]+)", text)
    link_match = re.search(r"https?://[^\s\]]+", text)

    student_name = name_match.group(1).strip() if name_match else "Не найдено"
    student_email = email_match.group(1).strip() if email_match else "Не найдено"
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
