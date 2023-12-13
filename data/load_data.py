from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
from pandas_gbq import to_gbq
import os

project_id = os.getenv("PROJECT_ID")
dataset_name = os.getenv("DATASET_NAME")
table_name = os.getenv("TABLE_NAME")
workdir = os.getenv("WORKDIR")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = workdir + '/data/keyfile.json'
destination_table = f"{project_id}.{dataset_name}.{table_name}"

creds = service_account.Credentials.from_service_account_file(workdir + '/data/keyfile.json')
client = bigquery.Client(credentials=creds, project=project_id)

columns = [
    "ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", 
    "Organic_carbon", "Trihalomethanes", "Turbidity", "Potability"
]
df = pd.read_csv(workdir + '/data/water_potability.csv', usecols=columns)
df = df.rename(columns={'Organic_carbon': 'OrganicCarbon'})
df = df.fillna(df.median())
df = df.map(lambda x: round(x, 2))

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]

to_gbq(df, destination_table=destination_table, project_id=project_id, if_exists='replace')