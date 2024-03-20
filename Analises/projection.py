import pandas as pd
import statsmodels.api as sm
import numpy as np
from datatable import DataTable


class Projection:
    def __init__(self, multidata_object):
        self.data = multidata_object
    

    def VAR(self, last_year_projected: int, columns: list, title='esqueceu o titulo kkkkkk', plot=True):
         # Criando um dataframe com as colunas que o usuário escolheu
        chosen_n_analysis = round(((pd.to_datetime(last_year_projected, format='%Y') - self.data[0].first_valid_index()).days/365))
        max_n_analysis = round(((self.data[0].last_valid_index() - self.data[0].first_valid_index())).days/365)
        training_years = min(chosen_n_analysis, max_n_analysis)
        df = pd.DataFrame()
        for column in columns:
            df = pd.concat([df, self.data[column[0]][column[1]]], axis=1)

        training_data = df[:training_years + 1] ## splicing do dataframe
        
        k = 0
        if last_year_projected > 2022:
            k = 1

        # Código de projeção
        model = sm.tsa.VAR(np.asarray(training_data, dtype='float'))
        model_fit = model.fit()
        prediction = pd.DataFrame(model_fit.forecast(model.endog, steps=(max(chosen_n_analysis, max_n_analysis) - (training_years + k)))) ## gerado o dataframe com a projeção dos próximos anos
        prediction.index = [training_data.index[-1] + pd.offsets.DateOffset(years=(i + 1)) for i in range(len(prediction))]
        prediction.rename(columns={i: name for i, name in enumerate(df.columns.values)}, inplace=True)
        forecast = pd.concat([training_data, prediction])
        forecast.rename(columns={name: (name + ' projetado') for name in forecast.columns.values}, inplace=True)
        
        result = pd.concat([forecast, df], axis=1)
        result_cols = self.intercalate_cols(df=result) # Intercalando as colunas para legibilidade do gráfico/
        result = DataTable(data=result[result_cols], name=title, last_year=max(last_year_projected, 2023))
        return result


    def intercalate_cols(self, df):
        cols = df.columns.values
        number_of_forecasts = int(len(cols)/2)
        forecast_cols = cols[:number_of_forecasts]
        data_cols = cols[number_of_forecasts:]
        result_cols = []
        for i in range(number_of_forecasts):
            result_cols.append(forecast_cols[i])
            result_cols.append(data_cols[i])
        return result_cols


    def errordiff(self, result_a, result_b):
        result_a = self.data[result_a]
        result_b = self.data[result_b]
        errors = []
        columns_a, columns_b = result_a.columns.values, result_b.columns.values
        size_a, size_b = len(columns_a), len(columns_b)
        for i in range(1, size_a, 2):
            if columns_a[i] in columns_b:
                error_a = sm.tools.eval_measures.mse(result_a[columns_a[i]], result_a[columns_a[i] + ' projetado'], axis=0)
                error_b = sm.tools.eval_measures.mse(result_b[columns_a[i]], result_b[columns_a[i] + ' projetado'], axis=0)
                if error_a > error_b:
                    diff = f'Modelo 2 é {error_a/error_b} vezes mais preciso'
                else:
                    diff = f'Modelo 1 é {error_b/error_a} vezes mais preciso'
                errors.append(columns_a[i] + ': ' +  diff)
        return errors
