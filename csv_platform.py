from mimetypes import init
import pandas as pd

class CsvFile :
    def __init__(self, file_name) :
        self.data = pd.read_csv(file_name)

    def print_out(self) :
        print(self.data)
    
    def pre_process(self) :
        drop_list = []
        for i in range(len(self.data)) :
            if(self.data.iloc[i][0] == self.data.columns[0]) :
                drop_list.append(i)
        
        self.data.drop(drop_list, axis = 0, inplace = True)

if __name__ == "__main__" :
    data = CsvFile("input.csv")
    data.pre_process()
    data.print_out()