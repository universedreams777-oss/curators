import telebot
import re
import os

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

# === ВОССТАНОВЛЕНИЕ ПРОШЛЫХ УЧЕНИКОВ ===
if os.path.exists("processed.txt"):
    with open("processed.txt", "r", encoding="utf-8") as f:
        for line in f:
            assigned_texts.add(line.strip())

# === СОЗДАНИЕ БОТА ===
bot = telebot.TeleBot(API_TOKEN)


# === УДАЛЕНИЕ СООБЩЕНИЙ С "прошло 20 часов" ===
@bot.channel_post_handler(func=lambda m: m.text and m.text.lower().startswith("прошло 20 часов"))
def delete_old_messages(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        print(f"🧹 Удалено сообщение: {message.text[:40]}")
    except Exception as e:
        print(f"❌ Ошибка при удалении: {e}")


# === ОБРАБОТЧИК СООБЩЕНИЙ "Наталия" ===
@bot.channel_post_handler(func=lambda message: message.text and message.text.lower().startswith("наталия"))
def handle_message(message):
    global last_index

    text = message.text.strip()

    # Пропустить, если уже было
    if text in assigned_texts:
        print("⏩ Уже обработано, пропускаем.")
        return
    assigned_texts.add(text)

    # Сохранить обработанное сообщение
    with open("processed.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

    # Назначение куратора по кругу
    last_index = (last_index + 1) % len(curators)
    curator = curators[last_index]

    # Извлечение данных
    name_match = re.search(r"Пользователь\s+(.+)", text)
    email_match = re.search(r"Почта\s+([^\s]+)", text)
    link_match = re.search(r"https?://[^\s\]]+", text)

    student_name = name_match.group(1).strip() if name_match else "Не найдено"
    student_link = link_match.group(0).strip() if link_match else "Не найдено"

    # Финальный текст
    final_text = (
        f"*🧠🥰 Твой ученик, проверь его пожалуйста {curator}*\n\n"
        f"*{student_name}*\n\n"
        f"*🔗 Ссылка на ученика:* {student_link}"
    )

    bot.send_message(CHANNEL_ID, final_text, parse_mode="Markdown")
    print(f"✅ Отправлено куратору {curator}: {student_name}")


# === ЗАПУСК ===
print("Бот запущен...")
# === ЗАПУСК ===
import time

while True:
    try:
        print("Бот запущен...")
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=30)
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        time.sleep(5)

