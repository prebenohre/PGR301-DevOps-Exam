import base64
import boto3
import json
import os
import random
import logging

# Sett opp logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sett opp AWS-klienter
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
s3_client = boto3.client("s3")

# Konstante variabler
MODEL_ID = "amazon.titan-image-generator-v1"

def lambda_handler(event, context):
    # Les bucket-navnet fra miljøvariabelen
    bucket_name = os.environ.get("BUCKET_NAME")
    if not bucket_name:
        logger.error("BUCKET_NAME environment variable is not set.")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Server configuration error"})
        }

    # Iterer gjennom alle SQS-meldinger i eventet
    for record in event.get("Records", []):
        prompt = record["body"]
        logger.info("Processing prompt from SQS message: %s", prompt)

        # Generer et unikt filnavn i mappen "29/sqs_generated_images/"
        seed = random.randint(0, 2147483647)
        s3_image_path = f"29/sqs_generated_images/titan_{seed}.png"

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
            },
        }

        # Kall Bedrock-modellen og håndter feil
        try:
            response = bedrock_client.invoke_model(
                modelId=MODEL_ID,
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

        # Last opp bildet til S3 i mappen "29/sqs_generated_images/"
        try:
            s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)
            logger.info("Image uploaded to S3 at path: %s", s3_image_path)
        except Exception as e:
            logger.error("Failed to upload image to S3: %s", e)
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to upload image to S3"})
            }

    # Returner suksessrespons
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Images processed successfully"})
    }
