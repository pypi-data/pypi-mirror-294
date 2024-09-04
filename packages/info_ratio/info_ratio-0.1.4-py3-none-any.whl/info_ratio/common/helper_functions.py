import loga
import sqlite3
import asyncio
import numpy as np
import pandas as pd
from datetime import datetime
from info_ratio.common.logging import loga
from info_ratio.common.input_output import get_data


@loga.errors
def preprocess_data(self):

    start = pd.Timestamp(self.start_date)
    end = pd.Timestamp(self.end_date)

    # Connect to SQLite database
    with sqlite3.connect(self.db_path) as db:
        db = get_data(db, insert_data=self.insert_data)

        # Fetch data from tabless
        fund_data_df = pd.read_sql_query("SELECT * FROM df_table", db)
        company_data_df = pd.read_sql_query("SELECT * FROM company_table", db)

    fund_data_df['Numeric Date'] = fund_data_df['Port Date'].apply(
        lambda x: datetime.strptime(x, "%d-%b-%Y").strftime("%Y%m")).astype(np.int64)

    # Merge single_fund_df with ace_df_renamed on 'Company ISIN' and 'Numeric Date'
    # Use 'left' join to keep all rows from single_fund_df and fill in 'Price' where matches are found
    merged_df = pd.merge(fund_data_df, company_data_df, on=[
                         'Company ISIN', 'Numeric Date'], how='left')
    merged_df["No Of Shares"] = merged_df["No Of Shares"].replace(
        '--', None, regex=True)

    # Drop rows where 'Price' and 'No of Shares'is missing
    merged_df = merged_df[merged_df['Price'].notna()]
    merged_df = merged_df[merged_df["No Of Shares"].notna()]

    # Convert 'Port Date' to a datetime object
    merged_df['Port Date_'] = pd.to_datetime(merged_df['Port Date'])
    merged_df = merged_df.sort_values(by='Port Date_')

    merged_df["No Of Shares"] = merged_df["No Of Shares"].astype(int)
    merged_df = merged_df.loc[merged_df['Port Date_'].between(start, end)]

    return merged_df

# Create decorator


def run_in_parallel(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped


def calculate_stock_info(input_df, num_wins, num_losses, absolute_gain, absolute_loss):

    stock_df = input_df[input_df['Company Name'] == i]
    stock_df["diff_tmp"] = stock_df["No Of Shares"].diff()
    stock_df["ret_tmp"] = stock_df["Price"] * stock_df["diff_tmp"]
    stock_df['ret_tmp'].iloc[0] = stock_df['Price'].iloc[0] * \
        stock_df['No Of Shares'].iloc[0]

    # We are assuming the the portfolio manager has exited the remaining shares at the end of the analysis period
    last_exit = stock_df['Price'].iloc[-1] * \
        stock_df['No Of Shares'].iloc[-1]

    sum_of_positive_nos = stock_df[stock_df['ret_tmp']
                                   >= 0]['ret_tmp'].sum()

    some_of_negative_nos = np.abs(stock_df[stock_df['ret_tmp'] <= 0]
                                  ['ret_tmp']).sum() + last_exit

    if sum_of_positive_nos < some_of_negative_nos:
        num_wins += 1
        absolute_gain += round((some_of_negative_nos -
                                sum_of_positive_nos), 3)
    else:
        num_losses += 1
        absolute_loss += round((some_of_negative_nos -
                                sum_of_positive_nos), 3)


@loga.errors
def calculate_information_ratio(input_df, fund_info):

    num_wins = 0
    num_losses = 0
    absolute_gain = 0
    absolute_loss = 0

    # Get the breadth of the fund
    stock_list = input_df['Company Name'].unique()
    breadth = len(stock_list)
    if breadth == 0:
        return fund_info, 4
    fund_info.append(breadth)

    # Have a new event loop
    loop = asyncio.get_event_loop()

    looper = asyncio.gather(*[your_function(i, 1)
                            for i in stock_list])  # Run the loop

    results = loop.run_until_complete(looper)

    for i in stock_list:
        stock_df = input_df[input_df['Company Name'] == i]
        stock_df["diff_tmp"] = stock_df["No Of Shares"].diff()
        stock_df["ret_tmp"] = stock_df["Price"] * stock_df["diff_tmp"]
        stock_df['ret_tmp'].iloc[0] = stock_df['Price'].iloc[0] * \
            stock_df['No Of Shares'].iloc[0]

        # We are assuming the the portfolio manager has exited the remaining shares at the end of the analysis period
        last_exit = stock_df['Price'].iloc[-1] * \
            stock_df['No Of Shares'].iloc[-1]

        sum_of_positive_nos = stock_df[stock_df['ret_tmp']
                                       >= 0]['ret_tmp'].sum()

        some_of_negative_nos = np.abs(stock_df[stock_df['ret_tmp'] <= 0]
                                      ['ret_tmp']).sum() + last_exit

        if sum_of_positive_nos < some_of_negative_nos:
            num_wins += 1
            absolute_gain += round((some_of_negative_nos -
                                   sum_of_positive_nos), 3)
        else:
            num_losses += 1
            absolute_loss += round((some_of_negative_nos -
                                   sum_of_positive_nos), 3)

    if num_wins == 0:
        return fund_info, 0
    else:
        average_gain = abs(absolute_gain)/num_wins
    if num_losses == 0:
        return fund_info, 1
    else:
        average_loss = abs(absolute_loss)/num_losses

    fund_info.append(num_wins)
    fund_info.append(num_losses)

    # Pain-to-Gain Ratio
    pain_gain_ratio = abs(absolute_gain/absolute_loss)

    # Calculate the batting average
    batting_average = num_wins/breadth
    fund_info.append(round(batting_average, 3))

    # Calculate the slugging ratio
    slugging_ratio = average_gain/average_loss

    fund_info.append(round(slugging_ratio, 3))

    information_coefficient = 1.6*(batting_average - (1/(1+slugging_ratio)))
    fund_info.append(round(information_coefficient, 3))

    information_ratio = information_coefficient * (np.sqrt(breadth))
    fund_info.append(round(information_ratio, 3))
    fund_info.append(round(pain_gain_ratio, 3))

    return fund_info, 3
