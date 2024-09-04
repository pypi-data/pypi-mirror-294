import os
from info_ratio.common.logging import loga
import pandas as pd
from datetime import datetime
from info_ratio.common.input_output import dfs_tabs
from info_ratio.common.helper_functions import preprocess_data, calculate_information_ratio


pd.options.mode.chained_assignment = None  # default='warn'


@loga
class InfoRatio:
    def __init__(self, funds_for_analysis_path, output_path, db_path, start_date, end_date, insert_data=False, enable_logging=True):

        if not enable_logging:
            loga.stop()

        self.main_dict = []
        self.only_wins = []
        self.only_losses = []
        self.dont_exist = []

        self.insert_data = insert_data

        self.start_date = start_date
        self.end_date = end_date

        self.funds_for_analysis_path = funds_for_analysis_path
        self.output_path = output_path
        self.db_path = db_path

    def run(self):
        input_df = preprocess_data(self)

        funds_df = pd.read_excel(
            self.funds_for_analysis_path, sheet_name='Enter Funds', engine="openpyxl")

        for scheme_name in funds_df['Funds']:
            fund_info = [scheme_name]
            scheme_df = input_df[input_df['Scheme Name'] == scheme_name]
            scheme_df.to_excel("MergedDf.xlsx")

            fund_info, type_ = calculate_information_ratio(
                scheme_df, fund_info)
            if type_ == 0:
                self.only_losses.append(fund_info)
            elif type_ == 1:
                self.only_wins.append(fund_info)
            elif type_ == 4:
                self.dont_exist.append(fund_info)
            else:
                self.main_dict.append(fund_info)

        df = pd.DataFrame(self.main_dict, columns=['Fund Name', 'Breadth', 'Wins', 'Loss', "Batting Average",
                          "Slugging Ratio", "Information Coefficient", "Information Ratio", "Pain/Gain Ratio"])
        only_win_df = pd.DataFrame(self.only_wins, columns=[
                                   'Fund Name', 'Breadth'])
        only_loss_df = pd.DataFrame(self.only_losses, columns=[
                                    'Fund Name', 'Breadth'])
        dont_exist_df = pd.DataFrame(self.dont_exist, columns=['Fund Name'])

        # list of dataframes and sheet names
        dfs = [df, only_win_df, only_loss_df, dont_exist_df]
        sheets = ['Main', 'Only Wins', 'Only Losses', "Don't Exist"]

        name = self.output_path + datetime.now().strftime("%Y-%m-%d")+".xlsx"
        # run function
        dfs_tabs(dfs, sheets, name)
