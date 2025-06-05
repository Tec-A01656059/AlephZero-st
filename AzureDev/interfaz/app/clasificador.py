import pickle
import json
import pandas as pd
# Dummy classifier for demonstration

class Requester:
    def __init__(self, path_to_model):
        # Load the pickle model
        self.model = None
        with open(path_to_model, 'rb') as file:
            self.model = pickle.load(file)

    def post(self, data, scoring_uri = None, headers=None):
        input_json = json.loads(data)
        df = pd.DataFrame(input_json["data"])

        # Simulate a POST request to the model
        output = self.model.predict(df)
        return json.dumps({
            'result': output.tolist()
        })
        
class GuestProfileClassifier:
    def __init__(self, path_to_model):
        self.requester = Requester(path_to_model)

    def classify(self, data, muestra=10):
        input_data = data
        if 'cluster' in input_data.columns:
            input_data = input_data.drop(columns=['cluster'])
        input_data = input_data.drop(columns=['LocalCurrencyAmount'])
        
        # Serialize
        input_data = input_data.to_json(orient='records')
        input_data = {
            'data': json.loads(input_data)
        }
        model_input = json.dumps(input_data)
        headers = {'Content-Type': 'application/json'}
        scoring_uri = None
        
        # Call the model
        response = self.requester.post(model_input, scoring_uri, headers)
        
        # Deserialize
        response = json.loads(response)
        outputs = response['result'][:muestra] if muestra > 0 else response['result']
        return outputs

if __name__ == "__main__":
    # Initialize the classifier
    classifier = GuestProfileClassifier(path_to_model='AzureDev/interfaz/app/model.pkl')
    # Classify the data
    outputs = classifier.classify(data_path='AzureDev/interfaz/app/Validation_Data.csv', muestra = 10)
    # Print the outputs
    print(outputs)
    