import json
import sagemaker
import base64
from sagemaker.predictor import Predictor

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classifier-ep'

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    # Instantiate a Predictor
    predictor = Predictor(ENDPOINT)

    # Make a prediction:
    inferences = predictor.predict(image, initial_args={'ContentType':'image/png'})  # inferences = b'[0.3, 0.7]
    inferences = inferences.decode()[1:-1]              # now '0.3, 0.7'
    classes = inferences.split(',')                     # now ['0.3', '0.7']
    inferences = [float(classes[0]), float(classes[1])] # now [0.3, 0.7]

    # We return the data back to the Step Function    
    event = dict()
    event["inferences"] = inferences
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }