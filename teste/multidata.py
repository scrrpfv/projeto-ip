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
        return self.datas[self.names[key]]

    
    # Formatação para printar os nomes dos dataframes
    def __str__(self):
        return f'{" | ".join(self.names)}'
    

    def plotall(self, index, tamanho=(8,8)):
        fig, ax = plt.subplots()
        plt.rcParams["figure.figsize"] = tamanho
        plt.minorticks_on()
        df = self[index]
        n = len(df.columns.values) - 1
        ax.set_prop_cycle('color', plt.cm.nipy_spectral(np.linspace(0,1,n)))
        for i in df.columns:
            if i != 'ANO':
                plt.plot(df['ANO'], df[i], label=i)
        plt.legend(bbox_to_anchor=(1.1,0.9))
        plt.grid(which='both', alpha=0.5)
        plt.show()

