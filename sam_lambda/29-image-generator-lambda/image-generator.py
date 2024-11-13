import base64
import boto3
import json
import os
import random

# Sett opp AWS-klienter
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
s3_client = boto3.client("s3")

def lambda_handler(event, context):
    # Les prompt fra forespørselen
    body = json.loads(event["body"])
    prompt = body.get("prompt", "Default prompt")  # "Default prompt" hvis prompt mangler

    # Generer et unikt filnavn
    seed = random.randint(0, 2147483647)
    s3_image_path = f"29/generated_images/titan_{seed}.png"

    # Konfigurer forespørsel til Bedrock
    native_request = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {"text": prompt},
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "quality": "standard",
            "cfgScale": 8.0,
            "height": 1024,
            "width": 1024,
            "seed": seed,
        }
    }

    # Kall Bedrock-modellen
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-image-generator-v1", body=json.dumps(native_request)
    )
    model_response = json.loads(response["body"].read())

    # Dekode bildet fra Base64
    base64_image_data = model_response["images"][0]
    image_data = base64.b64decode(base64_image_data)

    # Last opp bildet til S3
    bucket_name = os.environ.get("BUCKET_NAME")
    s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)

    # Returner suksessrespons
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Image generated and stored", "path": s3_image_path}),
    }
