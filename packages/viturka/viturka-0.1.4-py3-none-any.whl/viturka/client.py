import requests
import pickle
import base64

class ModelUploader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.server_url = "https://viturka.com/upload_model"

    def upload_model(self, local_model, model_type):
        # Serialize the local model
        model_data = pickle.dumps(local_model)

        # Send the model to the server and receive the global model
        response = requests.post(
            f'{self.server_url}',
            files={'model': ('model.pkl', model_data)},
            data={'api_key': self.api_key, 'model_type': model_type}
        )


        if response.status_code == 200:
            # Deserialize the received global model
            data = response.json()
            #print(data)
            if data['model'] == 200:
                global_model = local_model
            else:

                # Decode the base64 encoded string back to bytes

                pickled_model = base64.b64decode(data['model'])

                # Unpickle the model
                global_model = pickle.loads(pickled_model)

            # Perform local aggregation
                local_model.w0_ += global_model.w0_
                local_model.w_ += global_model.w_
                local_model.V_ += global_model.V_
                local_model.w0_ /= 2
                local_model.w_ /= 2
                local_model.V_ /= 2
            print("Model uploaded and aggregated successfully.")
        else:
            print(f"Failed to upload model: {response.content.decode()}")

