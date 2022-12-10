import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import glob
import math
import pandas as pd

SENSOR_ID = 5
KEY = 6
class XYSweepPlotter :
    def __init__(self) :
        self.log1_file_list
        self.log2_file_list

        self.log1_selected_file_list
        self.log2_selected_file_list

        self.inner_joined_list

    def GetTestLogs(self, log1_file_list, log2_file_list) :
        log1_sensor_id_list = [i.split('_')[SENSOR_ID] for i in sorted(log1_file_list)]
        log2_sensor_id_list = [i.split('_')[SENSOR_ID] for i in sorted(log2_file_list)]

        self.log1_file_list = pd.DataFrame(zip(sorted(log1_file_list), log1_sensor_id_list), columns=['log1_file_name', 'sensor_id'])
        self.log2_file_list = pd.DataFrame(zip(sorted(log1_file_list), log2_sensor_id_list), columns=['log2_file_name', 'sensor_id'])

        self.log1_file_list.drop_duplicates


if __name__ == "__main__" :

    log1 = glob.glob("./~~.csv")
    log2 = glob.glob("./~~~.csv")

    plotter = XYSweepPlotter()
    plotter.GetTestLogs(log1, log2)