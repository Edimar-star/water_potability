from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from google.oauth2 import service_account
from google.cloud import bigquery
import joblib
import os

project_id = os.getenv("PROJECT_ID")
dataset_name = os.getenv("DATASET_NAME")
table_name = os.getenv("TABLE_NAME")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keyfile.json'
destination_table = f"{project_id}.{dataset_name}.{table_name}"

creds = service_account.Credentials.from_service_account_file('keyfile.json')
client = bigquery.Client(credentials=creds, project=project_id)

sql = f"SELECT * FROM {destination_table}"
df_data = client.query(sql).result().to_dataframe()

inputs = ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "OrganicCarbon", "Trihalomethanes", "Turbidity"]
output = "Potability"
X = df_data[inputs].values.astype(float)
y = df_data[output].values

random_state = 10
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3, random_state=random_state)

model = DecisionTreeClassifier(random_state=random_state)
model.fit(Xtrain, ytrain)

y_pred = model.predict(Xtest)
score = model.score(Xtest, ytest)

# Imprimir métricas de rendimiento
NP, P = 0, 1
print(f"P: {list(ytrain).count(P)}")
print(f"NP: {list(ytrain).count(NP)}")
print(f"Valores P: {list(ytest).count(P)}")
print(f"Predicciones P: {list(y_pred).count(P)}")
print(f"Valores NP: {list(ytest).count(NP)}")
print(f"Predicciones NP: {list(y_pred).count(NP)}")
print(f'Score: {score}')

joblib.dump(model,'../server/models/model_potability.joblib')