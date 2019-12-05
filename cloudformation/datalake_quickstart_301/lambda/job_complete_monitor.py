"""
This module is the main script to ensure all tasks have been completed
"""
import os
import json
import logging
from time import sleep
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger("job_handler")
logger.setLevel(logging.INFO)
logger.info('Loading function')

emr = boto3.client('emr')
s3 = boto3.client('s3')
glue = boto3.client('glue')
sns = boto3.client('sns')

s3_data_repo = os.environ["S3DataRepoName"]
crawler_name = os.environ["GlueCrawlerName"]
sns_topic = os.environ['SnsTopic']

def lambda_handler(event, context):
    """
    check if EMR job is completed
    """
    logger.info(event["emrInfo"])

    try:
        # check the step status
        status = is_step_done(
            event["emrInfo"]["cluster_id"],
            event["emrInfo"]["step_list"]
        )

        if status["failed"]:
            logger.info("EMR step run FAILED")
            return "FAILED"

        if status["completed"]:
            logger.info("EMR step is COMPLETED")
        else:
            logger.info("EMR step is still RUNNING")
            return "RUNNING"

        # check the EMR cluster status
        emr_status = get_cluster_status(event["emrInfo"]["cluster_id"])

        if emr_status == "WAITING":
            logger.info("Cluster run finished")
            if get_datalake():
                start = False
                # wait until the crawler finish crawling
                while not run_crawler(crawler_name, start):
                    start = True
                    sleep(1)
                logger.info("Success to run Glue crawler to create Glue tables")
            # terminate the cluster and EMR workload
            emr.terminate_job_flows(
                JobFlowIds=[event["emrInfo"]["jobFlowId"]]
            )
            logger.info("Terminate the EMR jobflow")

            output = "OK"

        elif emr_status == "RUNNING":
            logger.info("Cluster is still running")
            output = emr_status

        else:
            logger.info(f"EMR job FAILED while running")
            message = "EMR job FAILED while running"
            sns.publish(Message=message, TopicArn=sns_topic)
            output = "FAILED"

        return output

    except ClientError as err:
        logger.error("The error occurred when getting the status of EMR cluster")
        logger.exception(err)


def get_datalake():
    """
    check the number of the folder in S3 data lake
    """
    data_exists = False
    res = s3.list_objects_v2(Bucket=s3_data_repo)
    target = list(map(lambda x: x['Key'].split("/")[0], res['Contents']))
    folder_list = list(dict.fromkeys(target))
    logger.info(f"List all the folder in S3 data repository\n{folder_list}")

    if len(folder_list) in [2, 3]:
        data_exists = True

    return data_exists

def run_crawler(glue_crawler, start):
    """
    control the state of Glue crawler

    @input: crawler name, False
    @output: boolean of crawler state
    """
    logger.info("request to run crawler")

    try:
        if not start and glue.get_crawler(Name=glue_crawler)["Crawler"]["State"] == "READY":
            logger.info("Crawer haven't start")
            glue.start_crawler(
                Name=glue_crawler
            )
            while glue.get_crawler(Name=glue_crawler)["Crawler"]["State"] == "READY":
                sleep(1)

        else:
            logger.info("Crawler is running")

        crawler_state = glue.get_crawler(Name=glue_crawler)["Crawler"]["State"]

        logger.info(f"Status: {crawler_state}")

    except ClientError as error:
        logger.error("The error occurred when running Glue crawler")
        logger.exception(error)
        raise error

    return crawler_state == "READY"

def is_step_done(cluster_id, step_id_list):
    """
    get the step status from EMR jobflow
    """
    status_queue = []
    status_table = {
        "completed": False,
        "failed": False
    }

    for step_id in step_id_list:
        res = emr.describe_step(
            ClusterId=cluster_id,
            StepId=step_id
        )

        status_queue.append(
            {
                "stepId": step_id,
                "status": res["Step"]["Status"]["State"]
            }
        )

    check_completed = list(filter(lambda x: x["status"] == "COMPLETED", status_queue))
    check_failed = list(filter(lambda x: x["status"] == "FAILED", status_queue))

    if len(check_completed) == 3:
        status_table["completed"] = True
        logger.info("All EMR step is COMPLETED")
        logger.info("EMR step is still running")
    else:
        logger.info("EMR step is still running")

    if len(check_failed) > 0:
        status_table["failed"] = True

    return status_table

def get_cluster_status(emr_cluster_id):
    """
    get the status of EMR cluster
    """

    response = emr.describe_cluster(ClusterId=emr_cluster_id)
    logger.info(f"Response: \n{response}")

    cluster_state = response['Cluster']['Status']['State']

    return cluster_state
