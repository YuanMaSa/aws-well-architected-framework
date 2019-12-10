"""
This module is the main script of initial setup handler
"""
import os
import json
import logging
import time
import boto3
import requests
from botocore.exceptions import ClientError

msg_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(format=msg_format, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("handler_logger")
logger.setLevel(logging.INFO)

# aws api client
s3 = boto3.client('s3')
s3r = boto3.resource('s3')
sfn = boto3.client('stepfunctions')

# load Environment Variables
prefix_name = os.environ["Prefix"]
s3_data_repo = os.environ["S3DataRepoName"]
sns_topic = os.environ["SnsTopic"]
sm_arn = os.environ["StateMachineArn"]

class cfnresponse():
    """
    response handler
    """
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    def send(self, event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
        """
        send response to cloudformation client
        """
        responseUrl = event['ResponseURL']

        print(responseUrl)

        responseBody = {}
        responseBody['Status'] = responseStatus
        responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + \
            context.log_stream_name
        responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
        responseBody['StackId'] = event['StackId']
        responseBody['RequestId'] = event['RequestId']
        responseBody['LogicalResourceId'] = event['LogicalResourceId']
        responseBody['NoEcho'] = noEcho
        responseBody['Data'] = responseData

        json_responseBody = json.dumps(responseBody)

        print("Response body:\n" + json_responseBody)

        headers = {
            'content-type': '',
            'content-length': str(len(json_responseBody))
        }

        try:
            response = requests.put(
                responseUrl,
                data=json_responseBody,
                headers=headers
            )
            print("Status code: " + response.reason)
        except Exception as err:
            print("send(..) failed executing requests.put(..): " + str(err))


def cfnresponse_handler(cur_event, cur_context, **status):
    """
    Response handler for custom resources << Do not modify code here >>

    @input: event body, context body, boolean of running status
    @output: None (send request to CloudFormation to complete the execution of custom resource)
    """
    cfn_hdr = cfnresponse()
    response_value = cur_event['ResourceProperties']['StackName']
    response_data = {}
    response_data['Data'] = response_value

    if status["normal"]:
        cfn_hdr.send(
            cur_event,
            cur_context,
            cfnresponse.SUCCESS,
            response_data,
            "CustomResourcePhysicalID"
        )
    else:
        cfn_hdr.send(
            cur_event,
            cur_context,
            cfnresponse.FAILED,
            response_data,
            "CustomResourcePhysicalID"
        )

def lambda_handler(event, context):
    """
    Main function
    """

    total_start_time = time.time()
    logger.info(f"event:\n{event}")

    try:
        if event['RequestType'] == "Create":
            # execute when CloudFormation being created
            # get all Parameters from custom resources
            stack_name = event['ResourceProperties']['StackName']
            logger.info(f"trigger by the custom resource from {stack_name} stack")
            # run state machine
            run_sfn()

            cfnresponse_handler(event, context, normal=True)

        elif event['RequestType'] == "Delete":
            # remove all the object from data lake
            folder_list = ["Green", "Yellow", "Weather"]
            for folder in folder_list:
                remove_s3_folder(folder, s3_data_repo)

            cfnresponse_handler(event, context, normal=True)


    except ClientError as error:
        cfnresponse_handler(event, context, normal=True)
        logger.error("The error occurred in main function")
        logger.exception(error)

    logger.info(
        "total running time of function : --- %s seconds ---"
        %(time.time() - total_start_time)
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def run_sfn():
    """
    execute state machine
    """
    res = sfn.start_execution(
        stateMachineArn=sm_arn,
        name='emr_step_job_flow',
        input="{\"job_status\" : \"start\"}"
    )
    exec_arn = res["executionArn"]
    logger.info(f"Execution Arn: {exec_arn}")

def remove_s3_folder(folder, bucket_name):
    """
    remove external location folder of Athena table <delete previous data>

    @input: new table name in the query (same as the folder name in s3)
    @output: None
    """
    try:
        bucket = s3r.Bucket(bucket_name)
        waiter = s3.get_waiter('object_not_exists')

        # delete the folder and all objects from inside
        bucket.objects.filter(Prefix=f"{folder}/").delete()
        # wait to check if folder have been removed successfully
        waiter.wait(Bucket=bucket_name, Key=f"{folder}/")
        logger.info(f"remove the folder <{folder}/> in bucket <{bucket_name}>")

    except ClientError as error:
        logger.error("The error occurred when removing s3 folder")
        logger.exception(error)
        raise error
