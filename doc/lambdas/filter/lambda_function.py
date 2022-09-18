import json

THRESHOLD = .93


def lambda_handler(event, context):

    # Grab the inferences from the event
    json_string = event['body']
    json_object = json.loads(json_string)
    inferences = json_object['inferences']
    

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = [1.0*(cls > THRESHOLD) for cls in inferences] 

    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    event = dict()
    if sum(meets_threshold):
        event["inferences"] = meets_threshold      
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")
    return {
        'statusCode': 200,
        'body': event #json.dumps(event)
    }