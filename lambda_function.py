# -------------------------------------   PLEASE READ   ------------------------------------------
# PURPOSE: This Python script is intended to be used as a AWS Lambda function with
# Runtime Version Python3.9. When integrated with AWS S3 Bucket and SNS Topic. It read the text file
# and send the email with number of words in uploaded text file.
# VERY IMPORTANT - REPLACE THE TEXT ENCLOSED IN BRACKETS <> on line#43 WITH YOUR SNS ARN
#
# Please feel free to update script as per your usage and it is highly recommended that user READ
# and UNDERSTAND the script and its purpose prior to the execution.
# ------------------------------------------------------------------------------------------------

import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    eventname = event['Records'][0]['eventName']
    sns_message = str("The word count in the file " + key + " is ")
    try:
        print(eventname)
        response = s3.get_object(Bucket=bucket, Key=key)
        mes = str(response['Body'].read())
        sns_message += str(len(mes.split()))
        print("CONTENT TYPE: " + response['ContentType'])
        print(str(sns_message))
        sns_response = sns.publish(
        TargetArn='<REPLACE THIS WITH YOUR SNS ARN>',
        Message= str(sns_message),
        Subject= str("Word Count Result")
        )
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
