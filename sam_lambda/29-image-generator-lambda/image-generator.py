import base64
import boto3
import json
import os
import random
import logging

# Setter opp logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setter opp AWS-klienter
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
s3_client = boto3.client("s3")

def lambda_handler(event, context):
    # Leser bucket-navnet fra miljøvariabelen
    bucket_name = os.environ.get("BUCKET_NAME")
    if not bucket_name:
        logger.error("BUCKET_NAME environment variable is not set.")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Server configuration error"})
        }
    
    # Leser prompt fra forespørselen og valider den
    try:
        body = json.loads(event["body"])
        prompt = body.get("prompt")
        if not prompt:
            logger.warning("No prompt provided in the request body.")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'prompt' in request body"})
            }
        logger.info("Generating image with prompt: %s", prompt)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse request body as JSON: %s", e)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in request body"})
        }

    # Genererer et unikt filnavn
    seed = random.randint(0, 2147483647)
    s3_image_path = f"29/generated_images/titan_{seed}.png"

    # Konfigurerer forespørsel til Bedrock
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

    # Kaller Bedrock-modellen og håndter feil
    try:
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-image-generator-v1", 
            body=json.dumps(native_request)
        )
        model_response = json.loads(response["body"].read())
        base64_image_data = model_response["images"][0]
        image_data = base64.b64decode(base64_image_data)
        logger.info("Image generated successfully.")
    except Exception as e:
        logger.error("Failed to generate image with Bedrock: %s", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to generate image"})
        }

    # Laster opp bildet til S3 og håndterer feil
    try:
        s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)
        logger.info("Image uploaded to S3 at path: %s", s3_image_path)
    except Exception as e:
        logger.error("Failed to upload image to S3: %s", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to upload image to S3"})
        }

    # Returnerer suksessrespons
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Image generated and stored", "path": s3_image_path}),
    }
