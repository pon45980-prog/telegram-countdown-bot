import asyncio
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError

# ===== НАСТРОЙКИ (ЗАМЕНИ НА СВОИ!) =====
BOT_TOKEN = "8319150880:AAG1AYR8othCsR2FSoFyRN2AIg000advjPM"  # Токен от @BotFather
CHANNEL_ID = "-1003177549317"  # ID канала (например: -1001234567890)
TARGET_DATE = datetime(2024, 12, 8, 0, 0, 0)  # 8 декабря 2024, 00:00:00
UPDATE_INTERVAL = 5  # Обновлять каждые 5 секунд

# ===== КОД БОТА (НЕ ТРОГАЙ!) =====
async def calculate_countdown():
    """Вычисляет оставшееся время"""
    now = datetime.now()
    delta = TARGET_DATE - now
    
    if delta.total_seconds() <= 0:
        return "⏰ ЧЕЛЛЕНДЖ ЗАВЕРШЁН! 🎉"
    
    total_seconds = int(delta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    # Анимированный индикатор (меняется каждую секунду)
    indicators = ["⏳", "⌛"]
    indicator = indicators[seconds % 2]
    
    return f"{indicator} Конец чего?:\n{hours:03d}:{minutes:02d}:{seconds:02d}"

async def run_countdown():
    """Основная функция бота"""
    bot = Bot(token=BOT_TOKEN)
    message_id = None
    
    print("🚀 Бот запущен! Таймер обновляется каждые", UPDATE_INTERVAL, "секунд")
    print(f"📅 Цель: {TARGET_DATE.strftime('%d.%m.%Y %H:%M:%S')}")
    print("❌ Для остановки нажми Ctrl+C\n")
    
    try:
        while True:
            countdown_text = await calculate_countdown()
            
            try:
                if message_id is None:
                    # Первая публикация
                    msg = await bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=countdown_text,
                        parse_mode='Markdown'
                    )
                    message_id = msg.message_id
                    print(f"✅ Пост создан! ID: {message_id}")
                else:
                    # Обновление существующего поста
                    await bot.edit_message_text(
                        chat_id=CHANNEL_ID,
                        message_id=message_id,
                        text=countdown_text,
                        parse_mode='Markdown'
                    )
                    print(f"🔄 Обновлено: {countdown_text.split('**')[1]}")
                
            except TelegramError as e:
                if "message is not modified" in str(e).lower():
                    print("⏭️ Текст не изменился, пропускаем...")
                else:
                    print(f"❌ Ошибка: {e}")
            
            await asyncio.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n⏹️ Бот остановлен!")

if name == "main":
    asyncio.run(run_countdown())
