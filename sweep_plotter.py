import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import glob
import math
import pandas as pd

import csv_platform


DATA = 1

SENSOR_ID = 5
KEY = 6


class PassSweepPicker :
    def __init__(self, calc_result_file_name) :
        self.calc_result = csv_platform.csv_file(calc_result_file_name)
        self.calc_result.remove_index()

        self.result_list = []

    def Pick(self, file_list) :
        for file in file_list :
            csv = pd.read_csv(file, nrows=2)
            # csv['GlobalTime'][DATA] : 스윕의 글로벌타임.
            # 일단 센서id를 찾는다.
            # 그다음 글로벌아이디 일치하는것 찾는다. 정확성을 위해 둘다 일치하는 것을 조건으로 하자.
            # 만약 둘다 일치한다면 결과 파일 리스트에 넣는다.
            


class XYSweepPlotter :
    def __init__(self) :
        # 인풋 파일 리스트
        self.log1_file_list
        self.log2_file_list

        # 이너조인 결과물
        self.inner_joined_list

        # 최종 결과물
        self.log1_selected_file_list
        self.log2_selected_file_list

        # log1, log2의 calculation 결과물
        self.log1_calc_result = csv_platform.csv_file("~.csv")
        self.log2_calc_result = csv_platform.csv_file("~.csv")

        self.log1_calc_result.remove_index()
        self.log2_calc_result.remove_index()

    def GetTestLogs(self, log1_file_list, log2_file_list) :
        log1_sensor_id_list = [i.split('_')[SENSOR_ID] for i in sorted(log1_file_list)]
        log2_sensor_id_list = [i.split('_')[SENSOR_ID] for i in sorted(log2_file_list)]

        self.log1_file_list = pd.DataFrame(zip(sorted(log1_file_list), log1_sensor_id_list), columns=['log1_file_name', 'sensor_id'])
        self.log2_file_list = pd.DataFrame(zip(sorted(log1_file_list), log2_sensor_id_list), columns=['log2_file_name', 'sensor_id'])

        self.log1_file_list.drop_duplicates(['sensor_id'], keep='last', inplace=True, ignore_index=True)
        self.log2_file_list.drop_duplicates(['sensor_id'], keep='last', inplace=True, ignore_index=True)

        self.inner_joined_list = pd.merge(self.log1_file_list, self.log2_file_list, left_on = 'sensor_id', right_on = 'sensor_id', how = 'inner')

        self.log1_selected_file_list = self.inner_joined_list['log1_file_name'].to_list()
        self.log2_selected_file_list = self.inner_joined_list['log2_file_name'].to_list()


def DrawPlots(log1_file_list, log2_file_list, pdf_name) : 
    pdf = PdfPages(pdf_name+".pdf")
    file_num = 1

    for log1_file in log1_file_list :
        for log2_file in log2_file_list :
            if log1_file.split('_')[SENSOR_ID] != log2_file.split('_')[SENSOR_ID] : continue

            log1_df = pd.read_csv(log1_file)
            log2_df = pd.read_csv(log2_file)
            
            # ...calculation....




if __name__ == "__main__" :

    log1 = glob.glob("./~~.csv")
    log2 = glob.glob("./~~~.csv")

    plotter = XYSweepPlotter()
    plotter.GetTestLogs(log1, log2)