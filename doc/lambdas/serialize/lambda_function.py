# This cell will write the function to your local machine. Note the name of the file and the name of the function. 
# Compare this to the 'Handler' parameter. 

import json
import base64
import os
import boto3


# Lambda Event Structure
#{
#    "inferences": [], # Output of predictor.predict
#    "s3_key": "", # Source data S3 key
#    "s3_bucket": "", # Source data S3 bucket
#    "image_data": ""  # base64 encoded string containing the image data
#}

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    s3 = boto3.client('s3')

    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']
    
    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, '/tmp/image.png')
    
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }