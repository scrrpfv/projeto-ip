import pandas as pd


class DataTable(pd.DataFrame):
    def __init__(self, name='Noname', last_year=2023, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        if self.index.name != 'ANO' and ('ANO' in self.columns):
            self['ANO'] = pd.to_datetime(self['ANO'], format='%Y')
            self.set_index('ANO', drop=True, inplace=True)
        else:
            self.index = pd.to_datetime(pd.Series([ano for ano in range(1970, last_year)]), format='%Y')
            self.index.name='ANO'
