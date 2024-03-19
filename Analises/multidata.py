import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat
import copy
import statsmodels.api as sm


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
        
        
    def projection_var(self, last_year_projected: int, columns: list, title='esqueceu o titulo kkkkkk', plot=True): # Forecasting exclusivam
        # Criando um dataframe com as colunas que o usuário escolheu
        chosen_n_analysis = round(((pd.to_datetime(last_year_projected, format='%Y')-self[0].first_valid_index()).days/365))
        max_n_analysis = round(((self[0].last_valid_index()-self[0].first_valid_index())).days/365)
        training_years = min(chosen_n_analysis, max_n_analysis)
        df = pd.DataFrame()
        for column in columns:
            df = pd.concat([df, self[column[0]][column[1]]], axis=1)

        training_data = df[:training_years + 1] ## splicing do dataframe
        
        # Código de projeção
        model = sm.tsa.VAR(np.asarray(training_data, dtype='float'))
        model_fit = model.fit()
        prediction = pd.DataFrame(model_fit.forecast(model.endog, steps=(max(chosen_n_analysis, max_n_analysis) - training_years))) ## gerado o dataframe com a projeção dos próximos anos
        prediction.index = [training_data.index[-1] + pd.offsets.DateOffset(years=(i+1)) for i in range(len(prediction))]
        prediction.rename(columns={i: name for i, name in enumerate(df.columns.values)}, inplace=True)
        forecast = pd.concat([training_data, prediction])
        forecast.rename(columns={name: (name + ' projetado') for name in forecast.columns.values}, inplace=True)
        
        labels = forecast.columns.values
        for i in range(len(columns)):
            df.insert((i*2)+1, labels[i], forecast[labels[i]])
        df = self.change_to_DataTable(df, title, last_year=max(last_year_projected, 2023))

        if plot:
            self.plot_selection(df=df)
        return df


    def periodic_proj(self, columns, title='esqueceu o titulo', period=5):
        df = pd.DataFrame()
        for column in columns:
            df = pd.concat([df, self[column[0]][column[1]]], axis=1)
        n_projections = int(period/columns)
        for p in len(1, n_projections + 1):
            training_size = p*period
            training_data = df[:training_size + 1]
            model = sm.tsa.VAR(np.asarray(training_data, dtype='float'))
            model_fit = model.fit()
            prediction = pd.DataFrame(model_fit.forecast(model.endog, steps=period))
            prediction.rename(columns={i: name for i, name in enumerate(df.columns.values)}, inplace=True)
            forecast = pd.concat([training_data, prediction])
            forecast.rename(columns={name: (name + ' projetado') for name in forecast.columns.values}, inplace=True)
        


    def add_dataframe(self, df, name):
        i = 0 
        while name in self.names:
            i += 1
            name = f'{name}_{i}'
        dt = self.change_to_DataTable(df, name=name)
        self.datas[name] = dt
        self.names.append(name)

    def change_to_DataTable(self, df, name, last_year=2023):
        df_copy = DataTable(columns = df.columns, data = copy.deepcopy(df.values), name=name, last_year=last_year)
        return df_copy
    

    
class DataTable(pd.DataFrame):
    def __init__(self, name, last_year=2023, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        if self.index.name != 'ANO' and ('ANO' in self.columns):
            self['ANO'] = pd.to_datetime(self['ANO'], format='%Y')
            self.set_index('ANO', drop=True, inplace=True)
        else:
            self.index = pd.to_datetime(pd.Series([ano for ano in range(1970, last_year)]), format='%Y')
            self.index.name='ANO'

