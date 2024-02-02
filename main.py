import ReceiptsTelegramBot.telegram_bot

if __name__ == '__main__':
    application = ReceiptsTelegramBot.telegram_bot.create_telegram_bot()
    ReceiptsTelegramBot.telegram_bot.start_telegram_bot(application)