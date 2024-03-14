import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat

class multidata():
    def __init__(self, datadict):
        self.datas = datadict
        self.names = [i for i in datadict]


    # Acessar os dataframes por índice
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.datas[self.names[key]]
        else:
            return self.datas[key]

    
    # Formatação para printar os nomes dos dataframes
    def __str__(self):
        return f'{" | ".join(self.names)}'
    

    def plotall(self, index, tamanho=(8,8), amount=0):
        # Decorações
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#949997')
        plt.rcParams["figure.figsize"] = tamanho
        plt.minorticks_on()
        df = self[index]
        ax.set_prop_cycle('color', plt.cm.nipy_spectral(np.linspace(0, 1, amount)))

        # Selecionando as colunas a plotar
        if not amount:
            amount = len(df.columns.values)
        pick = df.copy(deep=True)
        pick.pop('ANO')
        medians = pick.median()
        median = medians.median()
        offsets = medians.apply(lambda x: abs(x - median))
        offsets.sort_values(ascending=True, inplace=True)
        pick = offsets.index.values[:amount]

        # Plotando
        for i in df.columns:
            if i in pick:
                print(i)
                print(df[i])
                print(df['ANO'])
                x = df[i]
                y = df['ANO']
                plt.plot(df['ANO'], df[i], label=i) # Tá quebrado
        if isinstance(index, int):
            plt.title(f'{self.names[index].replace("_", " ")}')
        else:
            plt.title(f'{index.replace("_", " ")}')
        plt.legend(bbox_to_anchor=(1.1,0.9))
        plt.grid(which='both', alpha=0.5)
        plt.show()
