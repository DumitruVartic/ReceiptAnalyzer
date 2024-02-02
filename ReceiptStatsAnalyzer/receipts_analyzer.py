import pandas as pd
try:
    from . import utils
except:
    import utils
import datetime

def get_data(path='receipts.json'):
    ''' 
        Returns the receipts and products dataframes
        ----------
        * receipts_df: The receipts dataframe
        * products: The products dataframe
    '''
    receipts_df = pd.read_json(path)
    products = pd.concat([pd.json_normalize(row) for row in receipts_df["products"]], ignore_index=True)
    return receipts_df, products

def get_stats_df(chat_id : int):
    ''' 
        Returns the receipts and products dataframes
        ----------
        If the receipts.json not found, it will create it and return the dataframes
        * receipts_df: The receipts dataframe
        * products: The products dataframe
    '''
    utils.create_user_receipts_json(f"./ReceiptsData/users/{chat_id}/")
    path = f"./ReceiptsData/users/{chat_id}/receipts.json"
    return get_data(path)

def get_stats_from_dataframe(receipts_df: pd.DataFrame, products: pd.DataFrame = None):
    '''Returns the basic stats of the receipts'''
    average_total_price_by_receipt = receipts_df["total_price"].mean().round(4)
    total_money_spent = receipts_df["total_price"].sum()
    first_date = receipts_df["date"].min()
    last_date = receipts_df["date"].max()
    stats = {"Total Money Spent": total_money_spent, "Average total price by receipt": average_total_price_by_receipt, "First Receipt Date" : first_date, "Last Receipt Date" : last_date}
    stats = {key: str(value).replace("00:00:00", "").replace(" - ", " > ") for key, value in stats.items()}
    return stats

async def get_all_stats(chat_id : int) -> dict[str, str]:
    '''Returns the basic stats of the receipts'''
    receipts_df, products = get_stats_df(chat_id)
    return get_stats_from_dataframe(receipts_df, products)

async def get_stats_by_time_period(chat_id: int, start: datetime, end: datetime) -> dict[str, str]:
    '''Returns the stats of the user's receipts by the given time frame'''
    receipts_df, products = get_stats_df(chat_id)
    stats_in_time_frame = receipts_df[(receipts_df["date"] > start) & (receipts_df["date"] <= end)]
    return get_stats_from_dataframe(stats_in_time_frame, products)

async def get_stats_grouped_by_month(chat_id: int) -> list[dict]:
    receipts_df, products = get_stats_df(chat_id)
    receipts_df["month"] = receipts_df["date"].dt.to_period('M')
    stats_grouped_by_month = receipts_df.groupby("month").apply(get_stats_from_dataframe, products)
    return stats_grouped_by_month.to_list()

async def get_stats_grouped_by_year(chat_id: int) -> list[dict]:
    receipts_df, products = get_stats_df(chat_id)
    receipts_df["year"] = receipts_df["date"].dt.to_period('Y')
    stats_grouped_by_year = receipts_df.groupby("year").apply(get_stats_from_dataframe, products)
    return stats_grouped_by_year.to_list()

async def get_stats_grouped_by_day(chat_id: int) -> list[dict]:
    receipts_df, products = get_stats_df(chat_id)
    stats_grouped_by_day = receipts_df.groupby("date").apply(get_stats_from_dataframe, products)
    return stats_grouped_by_day.to_list()

async def get_stats_grouped_by_week(chat_id: int) -> list[dict]:
    receipts_df, products = get_stats_df(chat_id)
    receipts_df["week"] = receipts_df["date"].dt.to_period('W')
    stats_grouped_by_week = receipts_df.groupby("week").apply(get_stats_from_dataframe, products)
    return stats_grouped_by_week.to_list()

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)