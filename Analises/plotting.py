import matplotlib.pyplot as plt
import numpy as np
from datatable import DataTable

class Plotting:
    def __init__(self, df_dict) -> None:
        self.data = df_dict
    
    def autoplot(self, index, tamanho=(8,8), n=0):
        df = self.data[index]
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

    def plot_selection(self, df, pick=[], decorado=False):
        if len(pick) == 0:
            pick = df.columns.values
        
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
        