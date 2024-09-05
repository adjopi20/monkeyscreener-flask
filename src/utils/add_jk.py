import pandas as pd
import os

current_file_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_file_dir, '../../assets/stocklist.xlsx')
path = os.path.abspath(relative_path)

#alternative way manual
def addJK():
    dataframe = pd.read_excel(path)
    symbol_arr = []

    if 'Kode' in dataframe.columns:
        for symbol in dataframe['Kode']:
            modified_symbol = symbol + '.JK' #add .JK to symbol
            symbol_arr.append(modified_symbol) #add the symbol to the array
            # print(f"Symbols added to symbol_arr: {symbol_arr}")
    else:
        print('Kode not found in dataframe')


