import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import glob
import math
import pandas as pd

import csv_platform


DATA = 0

SENSOR_ID = 5
KEY = 6


class PassSweepPicker :
    def __init__(self, calc_result_file_name) :
        self.calc_result = csv_platform.csv_file(calc_result_file_name)
        self.calc_result.remove_index()
        self.calc_result.data = self.calc_result.data.where(self.calc_result.data['result'] == '1').dropna(subset=['result'])
        self.calc_result.data_sort("GlobalTime")
        self.calc_result.data_duplicate("sensorID")

        self.result_list = []

    def Pick(self, file_list) :
        for sweep_file in file_list :
            sweep = pd.read_csv(sweep_file, nrows=2)
            if len(self.calc_result.data.where((self.calc_result.data['sensorID'] == sweep_file.split('_')[SENSOR_ID]) & (self.calc_result.data['GlobalTime'] == sweep.loc[DATA]['GlobalTime']))) != 0 :
                self.result_list.append(sweep_file)

        return self.result_list


class XYSweepPlotter :
    def __init__(self) :
        # 인풋 파일 리스트
        #self.log1_file_list
        #self.log2_file_list

        # 이너조인 결과물
        #self.inner_joined_list

        # 패스 필터링 전 결과물
        #self.log1_selected_file_list
        #elf.log2_selected_file_list

        # PASS 스윕 픽커. 
        self.log1_pass_sweep_picker = PassSweepPicker("log1_calculation_result.csv")
        self.log2_pass_sweep_picker = PassSweepPicker("log2_calculation_result.csv")
        
        # 패스 필터링 된 결과물
        #self.log1_pass_sweep_file_list
        #self.log2_pass_sweep_file_list

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

        self.log1_pass_sweep_file_list = self.log1_pass_sweep_picker.Pick(self.log1_selected_file_list)
        self.log2_pass_sweep_file_list = self.log2_pass_sweep_picker.Pick(self.log2_selected_file_list)



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