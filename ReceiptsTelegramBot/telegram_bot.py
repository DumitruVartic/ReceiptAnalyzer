import logging
from . import receipt_handling as rh
from os import environ
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    filters, 
    MessageHandler, 
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes, 
    CallbackQueryHandler, 
    ConversationHandler
)
Token = environ.get("TOKEN") # Get the token from the environment variables (set in .env file)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Standard Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = "Help yourself now!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bye! I hope we can talk again some day.")
    return -1

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    if query.data == "get_all_time_stats":
        stats = await rh.get_basic_stats(update.effective_chat.id)
        stat_list = [f'{key} : {str(value).replace(".", ",").replace("-", ":")}' for key, value in stats.items()]
        message_text = f"Here are your all time stats:\n{"\n".join(stat_list)}"
        await query.edit_message_text(text=message_text, parse_mode="Markdown")
    elif query.data == "get_stats_by_month":
        stats = await rh.get_stats_grouped_by_month(update.effective_chat.id)
        message_text = f"Here are your stats grouped by month:\n{stats}"
        await query.edit_message_text(text=message_text, parse_mode="Markdown")
    elif query.data == "get_stats_by_year":
        stats = await rh.get_stats_grouped_by_year(update.effective_chat.id)
        message_text = f"Here are your stats grouped by year:\n{stats}"
        await query.edit_message_text(text=message_text, parse_mode="Markdown")
    elif query.data == "get_stats_by_week":
        stats = await rh.get_stats_grouped_by_week(update.effective_chat.id)
        message_text = f"Here are your stats grouped by week:\n{stats}"
        await query.edit_message_text(text=message_text, parse_mode="Markdown")
    elif query.data == "get_stats_by_day":
        stats = await rh.get_stats_grouped_by_day(update.effective_chat.id)
        message_text = f"Here are your stats grouped by day:\n{stats}"
        await query.edit_message_text(text=message_text, parse_mode="Markdown")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Show all time stats", callback_data="get_all_time_stats")],
        [
            InlineKeyboardButton("Show stats by month", callback_data="get_stats_by_month"),
            InlineKeyboardButton("Show stats by year", callback_data="get_stats_by_year")
        ],
        [
            InlineKeyboardButton("Show stats by week", callback_data="get_stats_by_week"),
            InlineKeyboardButton("Show stats by day", callback_data="get_stats_by_day")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = f"Chose what stats to show"
    await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode="MarkdownV2")

# QRCode Handler
async def handle_qrcode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = await rh.handle_qrcode(update.message)
    message_text = f"Here is the link to your receipt on [Sistemul Informațional Automatizat Monitorizarea Electronica a Vânzărilor]({url})"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text, parse_mode="MarkdownV2")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End the conversation."""
    await update.message.reply_text(
        f"Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    
    reply_keyboard = [
        ["a"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"',
        reply_markup=markup,
    )
    return 1

def create_telegram_bot():
    application = ApplicationBuilder().token(Token).concurrent_updates(False).build()

    # Standard Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('cancel', cancel))

    # application.add_handler(ConversationHandler(
    #     entry_points=[CommandHandler('stats', start)],
    #     states={
    #         1: [CommandHandler('choice', choice)]
    #     },
    #     fallbacks=[CommandHandler('done', done)],
    # ))

    application.add_handler(CallbackQueryHandler(buttons_handler))
    application.add_handler(CommandHandler('stats', stats))
    application.add_handler(MessageHandler(filters.PHOTO, handle_qrcode))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    return application

def start_telegram_bot(application):
    application.run_polling()