"""
This module is the main script of initial setup handler
"""
import os
import json
import logging
import time
import boto3
from botocore.exceptions import ClientError
import cfnresponse

msg_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(format=msg_format, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("handler_logger")
logger.setLevel(logging.INFO)

# aws api client
batch = boto3.client('batch')
ecr = boto3.client('ecr')

# load Environment Variables
ecr_image = os.environ["EcrImageId"]


def cfnresponse_handler(cur_event, cur_context, **status):
    """
    Response handler for custom resources << Do not modify code here >>

    @input: event body, context body, boolean of running status
    @output: None (send request to CloudFormation to complete the execution of custom resource)
    """
    response_value = cur_event['ResourceProperties']['StackName']
    response_data = {}
    response_data['Data'] = response_value
    if status["normal"]:
        cfnresponse.send(
            cur_event,
            cur_context,
            cfnresponse.SUCCESS,
            response_data,
            "CustomResourcePhysicalID"
        )
    else:
        cfnresponse.send(
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
            # Get all Parameters of Initial Batch Job
            queue = event['ResourceProperties']['JobQueue']
            definition = event['ResourceProperties']['JobDefinitionArn']

            # Run Initial Batch Job
            logger.info(">>>> start to load initial Batch job")
            run_initial_batch(queue, definition)

            cfnresponse_handler(event, context, normal=True)

        elif event['RequestType'] == "Delete":
            # clean up resources before stack deletion
            stack_deletion()
            cfnresponse_handler(event, context, normal=True)

        elif event['RequestType'] == "BatchJobTrigger":
            # execute when triggered by finish initial setup Batch job

            for job_defs in event["ResourceProperties"]:
                defs = dict(filter(lambda x: x, job_defs.items()))
                # generate dictionary and assign parameters to create Batch job
                new_def_name, new_def_arn = batch_job_creation(ecr_image, config=defs)

                logger.info(f"Successfully create Batch Job")
                logger.info(f"jobDefinitionName: {new_def_name}")
                logger.info(f"job Arn: {new_def_arn}")

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


def batch_job_creation(image_id, **job):
    """
    Create Batch job

    @input: prefix name, image id in ECR, job configuration
    @output: job definition name, job definition arn
    """
    job_name = job["config"]["Name"]
    description = job["config"]["Description"]
    cmd = job["config"]["Command"]
    envs = job["config"]["EnvironmentVariables"]

    logger.info(f"\n <{description}> \n Job Name: {job_name}")
    logger.info(f"Job Command: {cmd} \n Environment Variables: {envs}")

    try:
        response = batch.register_job_definition(
            jobDefinitionName=job_name,
            type="container",
            containerProperties={
                "image": image_id,
                "vcpus": 2,
                "memory": 2000,
                "command": cmd,
                "environment": envs
            },
            retryStrategy={
                "attempts": 1
            }
        )
        logger.info(response)

        return response["jobDefinitionName"], response["jobDefinitionArn"]

    except ClientError as error:
        logger.error("The error occurred when creating new Batch job")
        logger.exception(error)
        raise error


def run_initial_batch(job_queue, job_definition):
    """
    Run initial Batch job to put docker image to ECR

    @input: prefix name, the name of public job queue, job definition arn
    @output: None
    """
    # run initial setup task
    try:
        response = batch.submit_job(
            jobName="container_builder",
            jobQueue=job_queue,
            jobDefinition=job_definition
        )
        logger.info(f"batch job submitting response:\n{response}")
        logger.info(">> Successfully to run initial Batch job")

    except ClientError as error:
        logger.error("The error occurred when running initial Batch job")
        logger.exception(error)
        raise error



def stack_deletion():
    """
    The action of stack deletion

    @input: None
    @output: None
    """
    # execute when CloudFormation being deleted
    logger.info(">> start to delete the custom resources")

    try:

        # delete Batch job definition created by Lambda
        get_def = batch.describe_job_definitions(status='ACTIVE')
        get_def = list(
            filter(lambda x: "Lab" in x["jobDefinitionName"], get_def["jobDefinitions"])
        )
        for dfn in get_def:
            if "Lab" in dfn["jobDefinitionName"]:
                arn = dfn["jobDefinitionArn"]
                logger.info(f"delete Arn => {arn}")
                batch.deregister_job_definition(jobDefinition=arn)

        # delete image in ECR
        ecr_repo_name = ecr_image.split("/")[1].split(":")[0]
        get_image = ecr.batch_get_image(
            repositoryName=ecr_repo_name,
            imageIds=[{'imageTag': 'latest'}]
        )

        if len(get_image["images"]) > 0:
            ecr.batch_delete_image(
                repositoryName=ecr_repo_name,
                imageIds=[{'imageTag': 'latest'}]
            )
            logger.info(f"delete the image from ECR repository <{ecr_repo_name}>")


    except ClientError as error:
        logger.error("The error occurred when deleting resources")
        logger.exception(error)
        raise error
