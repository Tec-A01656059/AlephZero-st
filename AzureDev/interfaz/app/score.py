import json
import joblib
import pandas as pd
import pickle
import numpy as np

from azureml.core.model import Model

def init():
    global model
    # Cargar el modelo que incluye el pipeline con preprocesamiento
    model_path = Model.get_model_path('classifier')  # nombre registrado en Azure
    # Load from a pickle file
    
    model = joblib.load(model_path)

def run(raw_data):
    try:
        # Convertir JSON a DataFrame
        input_json = json.loads(raw_data)

        # Asegura que 'data' exista y sea una lista
        if isinstance(input_json, dict) and "data" in input_json:
            df = pd.DataFrame(input_json["data"])
        else:
            return json.dumps({"error": "Input must be a JSON with a 'data' key containing a list of records."})
        # Checar si tiene o no las columnas de cluster y LocalCurrencyAmount para quitarlas, sino pues no lo haga
        if 'cluster' in df.columns:
            df = df.drop(columns=['cluster'])
        if 'LocalCurrencyAmount' in df.columns:
            df = df.drop(columns=['LocalCurrencyAmount'])
        X = df
        # Hacer predicción con el pipeline cargado
        predictions = model.predict(X)

        # Retornar los resultados como JSON
        return json.dumps({"result": predictions.tolist()})["result"]
    
    except Exception as e:
        return json.dumps({"error": str(e)})


# if __name__ == "__main__":
#     # Inicializar el modelo
#     init()
#     print ("Model initialized.")
#     input_data = pd.read_csv("Validation_Data.csv")
#     # Serialize the first 5 rows of the DataFrame to JSON
#     input_data = input_data.head(5).to_json(orient="records")
#     input_data = {
#         "data": json.loads(input_data)  # Asegúrate de que sea una lista de registros
#     }
#     # Llamar a la función run con los datos simulados
#     result = run(json.dumps(input_data))
#     # Imprimir el resultado
#     print(result)