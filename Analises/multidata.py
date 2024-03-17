import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat
import copy


class MultiData():
    def __init__(self, datadict):
        self.datas = copy.deepcopy(datadict)
        self.names = [df for df in datadict]
        for name in self.names:
            self.datas[name] = self.change_to_DataTable(self.datas[name], name)
        

    # Acessar os dataframes por índice
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.datas[self.names[key]]
        else:
            return self.datas[key]

    
    # Formatação para printar os nomes dos dataframes
    def __str__(self):
        return f'{" | ".join(self.names)}'
            

    def autoplot(self, index, tamanho=(8,8), n=0):
        df = self[index]
        if not n:
            n = len(df.columns.values)
        # Decorações
        self.decorate(n=n, tamanho=tamanho)
        decorado = True
        

        # Selecionando as colunas a plotar
        pick = df.copy(deep=True)
        top = pick.max()
        bot = pick.min()
        offsets = top - bot
        offsets.apply(lambda x: abs(x))
        offsets.sort_values(ascending=True, inplace=True)
        pick = offsets.index.values[:n]
        
        # Plotando
        self.plot_selection(df, pick, decorado)


    def plot_selection(self, df, pick, decorado=False):
        if not decorado:
            self.decorate(n=len(pick))
        for i in df.columns:
            if i in pick:
                plt.plot(df.index.values, df[i], label=i)
        plt.title(f'{df.name.replace("_", " ")}')
        plt.legend(bbox_to_anchor=(1.1,0.9))
        plt.grid(which='both', alpha=0.5)
        plt.show()
    
    
    def decorate(self, n, tamanho=(8,8)):
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor('#949997')
        plt.minorticks_on()
        plt.rcParams["figure.figsize"] = tamanho
        self.ax.set_prop_cycle('color', plt.cm.nipy_spectral(np.linspace(0, 1, n)))
        
        
    def change_to_DataTable(self, df, name):
        df_copy = DataTable(columns = df.columns, data = copy.deepcopy(df.values), name=name)
        return df_copy

class DataTable(pd.DataFrame):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self['ANO'] = pd.to_datetime(self['ANO'], format='%Y')
        if self.index.name != 'ANO' and ('ANO' in self.columns):
            self.set_index('ANO', drop=True, inplace=True)
        else:
            self.index = pd.to_datetime(pd.Series([ano for ano in range(1970, 2023)]))
            self.index.name='ANO'

