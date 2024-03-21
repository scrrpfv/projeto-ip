import pandas as pd
import numpy as np
import copy
from datatable import DataTable
from projection import Projection
from plotting import Plotting


class MultiData():
    def __init__(self, datadict):
        self.datas = copy.deepcopy(datadict)
        self.names = [df for df in datadict]
        for name in self.names:
            self.datas[name] = DataTable(data=self.datas[name], name=name, last_year=pd.to_datetime(self.datas[name].last_valid_index()).year+1)
        self.Projection = Projection(self)
        self.Plotting = Plotting(self)


    # Acessar os dataframes por índice
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.datas[self.names[key]]
        else:
            return self.datas[key]
        
    # Formatação para printar os nomes dos dataframes
    def __str__(self):
        return f'{" | ".join(self.names)}'
    
    # Função que adiciona um novo dataframe ao MultiData
    def add_dataframe(self, df, name):
        i = 0 
        while name in self.names:
            i += 1
            name = f'{name}_{i}'
        dt = DataTable(data=df, name=name, last_year=2023)
        self.datas[name] = dt
        self.names.append(name) # Atualização do self.names com o novo nome de DataTable
        self.Projection = Projection(self) # Atualização do self.Projection
        self.Plotting = Plotting(self) # Atualização do self.Plotting
        