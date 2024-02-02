import os, datetime
from . import opencv_qr_decode as qr, scrapper as sc
from ReceiptStatsAnalyzer import receipts_analyzer as stats_analyzer
from telegram import Update

async def create_user_folders(chat_id: int) -> tuple[str, str]:
    '''Creates a folders for the user to store their images and receipts'''
    base_path = f"./ReceiptsData/users/{chat_id}"
    image_path = f"{base_path}/chats"
    receipt_path = f"{base_path}/receipts"
    os.makedirs(image_path, exist_ok=True)
    os.makedirs(receipt_path, exist_ok=True)
    return image_path, receipt_path

async def save_receipts_photo(message : Update.MESSAGE) -> str:
    '''Saves the images in the message to the user's directory and returns the paths'''
    image_path, receipt_path = await create_user_folders(message.chat_id)
    image_path = f"{image_path}/{message.message_id}.jpg"
    receipt_path = f"{receipt_path}/{message.message_id}.json"
    photo_file = await message.photo[-1].get_file()
    await photo_file.download_to_drive(image_path)

    return image_path, receipt_path

async def handle_qrcode(message : Update.MESSAGE) -> str:
    '''Handles the qr code in the message and returns the url of the receipt'''
    image_path, receipt_path = await save_receipts_photo(message)
    url = await qr.decode(image_path)
    await sc.scrape_receipt(url, receipt_path)
    return url

async def get_stats_by_time_period(chat_id: int, start: datetime, end: datetime) -> dict:
    '''Returns the stats of the user's receipts by the given time frame'''
    return await stats_analyzer.get_stats_by_time_period(chat_id, start, end)

async def get_stats_grouped_by_month(chat_id: int) -> list[dict]:
    '''Returns the stats of the user's receipts grouped by month'''
    return await stats_analyzer.get_stats_grouped_by_month(chat_id)

async def get_stats_grouped_by_year(chat_id: int) -> list[dict]:
    '''Returns the stats of the user's receipts grouped by year'''
    return await stats_analyzer.get_stats_grouped_by_year(chat_id)

async def get_stats_grouped_by_week(chat_id: int) -> list[dict]:
    '''Returns the stats of the user's receipts grouped by week'''
    return await stats_analyzer.get_stats_grouped_by_week(chat_id)

async def get_stats_grouped_by_day(chat_id: int) -> list[dict]:
    '''Returns the stats of the user's receipts grouped by day'''
    return await stats_analyzer.get_stats_grouped_by_day(chat_id)

async def get_basic_stats(chat_id: int): # check if they exist , raise a custom exception , no stats
    '''Returns the basic stats of the user's receipts'''
    return await stats_analyzer.get_all_stats(chat_id)