import os
from info_ratio.common.logging import loga
import pandas as pd
from datetime import datetime
from info_ratio.common.input_output import dfs_tabs
from info_ratio.common.helper_functions import preprocess_data, calculate_information_ratio


pd.options.mode.chained_assignment = None  # default='warn'


@loga
class InfoRatio:
    def __init__(self, input_df, db_path, start_date, end_date, insert_data=False, enable_logging=True):

        if not enable_logging:
            loga.stop()

        self.main_dict = []
        self.only_wins = []
        self.only_losses = []
        self.dont_exist = []

        self.insert_data = insert_data

        self.input_df = input_df

        self.start_date = start_date
        self.end_date = end_date

        self.db_path = db_path

    def run(self):
        processed_df = preprocess_data(self)

        for scheme_name in self.input_df["Scheme Name"]:
            fund_info = [scheme_name]
            scheme_df = processed_df[processed_df["Scheme Name"]
                                     == scheme_name]

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

        return df, only_win_df, only_loss_df, dont_exist_df
