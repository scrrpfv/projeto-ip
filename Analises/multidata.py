import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat


class MultiData():
    def __init__(self, datadict):
        self.datas = datadict
        self.names = [df for df in datadict]
        self.change_to_DataTable()
        

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
        self.decorate(index, tamanho, n, df=df)
        

        # Selecionando as colunas a plotar
        pick = df.copy(deep=True)
        top = pick.max()
        bot = pick.min()
        offsets = top - bot
        offsets.apply(lambda x: abs(x))
        offsets.sort_values(ascending=True, inplace=True)
        pick = offsets.index.values[:n]
        
        # Plotando
        self.plot_selection(df, pick)


    def plot_selection(self, df, pick):
        for i in df.columns:
            if i in pick:
                plt.plot(df.index.values, df[i], label=i)
        plt.title(f'{df.name.replace("_", " ")}')
        plt.legend(bbox_to_anchor=(1.1,0.9))
        plt.grid(which='both', alpha=0.5)
        plt.show()
    
    
    def decorate(self, index, tamanho, n, df):
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor('#949997')
        plt.minorticks_on()
        plt.rcParams["figure.figsize"] = tamanho
        self.ax.set_prop_cycle('color', plt.cm.nipy_spectral(np.linspace(0, 1, n)))
        
        
    def change_to_DataTable(self):
        for name in self.names:
            self.datas[name] = DataTable(name, data=self.datas[name])


class DataTable(pd.DataFrame):
    def __init__(self, name, data):
        super().__init__(data)
        self.name = name
        self.set_index('ANO', drop=True, inplace=True)

