import pandas as pd
from telethon.sync import TelegramClient

api_id =  # Ваш api id
api_hash = '' # Ваш api hash
phone_number = '' # Ваш номер телефона в формате +12345678
password = ''  # Ваш пароль от 2FA

client = TelegramClient('session_1', api_id, api_hash)

async def main():
    print("Запуск клиента...")
    await client.connect()

    if not await client.is_user_authorized():
        print("Требуется авторизация...")
        await client.send_code_request(phone_number)  # Запрашиваем код
        code = input("Введите код из Telegram: ")  # Вручную вводим код
        try:
            await client.sign_in(phone_number, code)
        except Exception as e:
            print(f"Требуется пароль 2FA: {e}")
            await client.sign_in(password=password)  # Вводим пароль 2FA

    print("Клиент авторизован!")

    # Получаем канал
    channel = await client.get_entity('https://t.me/physics_lib')
    print(f"Получен канал: {channel.title}")

    # Загружаем последние 100 сообщений
    messages = await client.get_messages(channel, limit=100)
    print(f"Получено {len(messages)} сообщений!")

    data = []

    for message in messages:
        text = message.text or "" # Берем текст
        links = [entity.url for entity in message.entities or [] if hasattr(entity, 'url')] # Ищем ссылки

        # Добавляем данные в список
        data.append({"Сообщение": text, "Ссылки": ", ".join(links)})

    # Создаем DataFrame и сохраняем в CSV
    df = pd.DataFrame(data)
    df.to_csv("telegram_physics_lib_100_last_message.csv", index=False, encoding="utf-8-sig")
    print('Данные сохранены в telegram_physics_lib_100_last_message.csv!')

with client:
    client.loop.run_until_complete(main())