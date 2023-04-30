from mimetypes import init
import pandas as pd

class CsvFile :
    def __init__(self, file_name, no_header=False) :
        if no_header : self.data = pd.read_csv(file_name, header=None)
        else : self.data = pd.read_csv(file_name)

    def print_out(self) :
        print(self.data)
    
    # merge된 로그에서 인덱스 행 모두 제거
    def remove_index(self) :
        drop_list = []
        for i in range(len(self.data)) :
            if(self.data.iloc[i][0] == self.data.columns[0]) :
                drop_list.append(i)
        
        self.data.drop(drop_list, axis = 0, inplace = True)
        self.data.reset_index(drop = True, inplace = True)
    
    # 컬럼 기준으로 정렬
    def data_sort(self, idx) :
        self.data.sort_values(by = [idx], inplace = True, ascending = True, kind = 'quicksort', ignore_index = True)

    # 컬럼 기준으로 중복 제거. 시간순 정렬은 되어있다고 가정한다.
    def data_duplicate(self, idx) :
        try :
            self.data.drop_duplicates(subset = idx, inplace = True, keep = "first", ignore_index = True)
        
        except :
            print("error")
    
    def data_to_csv(self, filename) :
        self.data.to_csv(filename, index = None)

    # header=None 인 데이터에 대하여 특정 범위의 행만 추출
    def split_csv(self, row_begin, row_end) -> pd.DataFrame :
        ret_temp = self.data.iloc[row_begin:row_end,:]
        ret_temp.rename(columns=ret_temp.iloc[0], inplace=True)
        ret_temp.drop(ret_temp.index[0], inplace=True)
        ret_temp.reset_index(drop = True, inplace = True)
        ret_temp.dropna(how='all', axis='columns', inplace=True)

        return ret_temp



class LogRefiner :
    def __init__(self, data_name, nvm_name) :
        self.data = CsvFile(data_name)
        self.nvm = CsvFile(nvm_name)
    
    # 초검 데이터만 추출
    def refine(self) :
        self.data.remove_index()
        self.data.data_sort("globalTime")
        self.data.data_duplicate("sensorID")

        self.nvm.remove_index()
        self.nvm.data_sort("globalTime")
        self.nvm.data_duplicate("sensorID")

        # self.data에서 self.nvm 데이터 sensorID에 존재하는 sensorID만 추출한다.
        sensorID_list = self.nvm.data["sensorID"].values.tolist()
        drop_list = []

        for i in range(len(self.data.data)) :
            if(not (self.data.data.loc[i]["sensorID"] in sensorID_list)) :
                drop_list.append(i)
        
        self.data.data.drop(drop_list, axis = 0, inplace = True)
        self.data.data.reset_index(drop = True, inplace = True)


class ColumnIntegrator :
    def __init__(self, file_name) :
        self.log = CsvFile(file_name, no_header=True)
        self.__df_list = []

    def execute(self) :
        try :
            split_start = 0
            for row in range(1, len(self.log.data)) :
                if self.log.data.iloc[row][0] != self.log.data.iloc[0][0] : continue
                self.__df_list.append(self.log.split_csv(row_begin=split_start, row_end=row))
                split_start = row
            self.__df_list.append(self.log.split_csv(row_begin=split_start, row_end=len(self.log.data)))

            self.__df_list.sort(key=lambda x : len(x.columns), reverse=True)
            result = pd.concat(self.__df_list, ignore_index=True)

            result.to_csv("Result.csv", index=None)

        except Exception as e :
            print("Exception : ", e)

if __name__ == "__main__" :
    #log = log_refiner("input.csv", "nvm.csv")
    #log.refine()
    # a = pd.read_csv("input.csv", header=None)


    a = ColumnIntegrator("input.csv")
    a.execute()