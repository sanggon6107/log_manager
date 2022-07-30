from mimetypes import init
import pandas as pd

class CsvFile :
    def __init__(self, file_name) :
        self.data = pd.read_csv(file_name)

    def print_out(self) :
        print(self.data)
    
    # merge된 로그에서 인덱스 행 모두 제거
    def pre_process(self) :
        drop_list = []
        for i in range(len(self.data)) :
            if(self.data.iloc[i][0] == self.data.columns[0]) :
                drop_list.append(i)
        
        self.data.drop(drop_list, axis = 0, inplace = True)
        self.data.reset_index(drop = True, inplace = True)
    
    # 인덱스 기준으로 정렬
    def data_sort(self, idx) :
        self.data.sort_values(by = [idx], inplace = True, ascending = True, kind = 'quicksort', ignore_index = True)

    def data_duplicate(self, idx) :
        self.data.drop_duplicates(subset = idx, inplace = True, keep = "first", ignore_index = True)

if __name__ == "__main__" :
    data = CsvFile("input.csv")
    data.pre_process()
    data.print_out()
    data.data_sort("globalTime")
    data.print_out()
    data.data_duplicate("sensorID")
    data.print_out()
