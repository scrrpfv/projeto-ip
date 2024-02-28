import basedosdados as bd
import pandas as pd

# Para carregar o dado direto no pandas
df = bd.read_table(dataset_id='br_seeg_emissoes',
table_id='brasil',
billing_project_id="hazel-logic-415517")

df.to_csv('emissoes_co2')
