"""
This module is the main script to add EMR step
"""
import os
import json
import logging
import time
import boto3
from botocore.exceptions import ClientError

msg_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(format=msg_format, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("handler_logger")
logger.setLevel(logging.INFO)

# aws api client
s3 = boto3.client('s3')
emr = boto3.client('emr')

# load Environment Variables
prefix_name = os.environ["Prefix"]
s3_data_repo = os.environ["S3DataRepoName"]
sns_topic = os.environ["SnsTopic"]
subnet_id = os.environ["SubnetId"]
master_sg = os.environ['MasterSg']
slave_sg = os.environ['SlaveSg']
service_access_sg = os.environ['ServiceAccessSg']
log_uri = os.environ["LogUri"]
lab_bucket = os.environ["LabBucket"]


def lambda_handler(event, context):
    """
    Main function
    """

    total_start_time = time.time()
    logger.info(f"event:\n{event}")

    res = emr_run_spark()
    outer_info = fetch_emr_info(res["ClusterArn"])
    logger.info("fetch all the required values")

    logger.info(
        "total running time of function : --- %s seconds ---"
        %(time.time() - total_start_time)
    )

    event["job_status"] = "start to run EMR step"

    return {
        'statusCode': 200,
        'jobFlowId': res["JobFlowId"],
        'clusterArn': res["ClusterArn"],
        'cluster_id': outer_info["cluster_id"],
        "step_list": outer_info["step_list"]
    }

def emr_run_spark():
    """
    EMR run pyspark script
    """

    try:
        response = emr.run_job_flow(
            Name="Lab Spark Cluster",
            LogUri=log_uri,
            ReleaseLabel='emr-5.28.0',
            Instances={
                'MasterInstanceType': 'm5.xlarge',
                'SlaveInstanceType': 'r5.2xlarge',
                'InstanceCount': 4,
                'KeepJobFlowAliveWhenNoSteps': True,
                'TerminationProtected': False,
                'Ec2SubnetId': subnet_id,
                'EmrManagedMasterSecurityGroup': master_sg,
                'EmrManagedSlaveSecurityGroup': slave_sg,
                'ServiceAccessSecurityGroup': service_access_sg
            },
            Applications=[
                {
                    'Name': 'Spark'
                }
            ],
            BootstrapActions=[
                {
                    'Name': 'Maximize Spark Default Config',
                    'ScriptBootstrapAction': {
                        'Path': 's3://support.elasticmapreduce/spark/maximize-spark-default-config',
                    }
                },
                {
                    'Name': 'Install boto3',
                    'ScriptBootstrapAction': {
                        'Path': f's3://{lab_bucket}/spark/conf/install_python_modules.sh',
                    }
                }
            ],
            Steps=[
                {
                    'Name': 'Setup Debugging',
                    'ActionOnFailure': 'TERMINATE_CLUSTER',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['state-pusher-script']
                    }
                },
                {
                    'Name': 'setup - copy files',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['aws', 's3', 'cp', f's3://{lab_bucket}/spark/main.py', '/home/hadoop/']
                    }
                },
                {
                    'Name': 'Run Spark',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['spark-submit', '/home/hadoop/main.py', lab_bucket, s3_data_repo]
                    }
                }
            ],
            Configurations=[
                {
                    'Classification': 'spark-env',
                    "Configurations": [
                        {
                            "Classification": "export",
                            "Properties": {
                                "PYSPARK_PYTHON": "/usr/bin/python3"
                            }
                        }
                    ]
                }
            ],
            VisibleToAllUsers=True,
            JobFlowRole='EMR_EC2_DefaultRole',
            ServiceRole='EMR_DefaultRole',
            Tags=[
                {
                    'Key': 'Project',
                    'Value': 'Data Lake Quickstart'
                },
                {
                    'Key': 'Prefix',
                    'Value': prefix_name
                }
            ]
        )

        return response

    except ClientError as error:
        logger.error("The error occurred when configure emr to run spark")
        logger.exception(error)

def fetch_emr_info(cluster_arn):
    """
    fetch all required info from EMR
    """
    for cluster in emr.list_clusters()["Clusters"]:
        if cluster["ClusterArn"] == cluster_arn:
            cluster_id = cluster["Id"]

    res = emr.list_steps(ClusterId=cluster_id)
    step_list = list(map(lambda x: x["Id"], res["Steps"]))

    return {
        "cluster_id": cluster_id,
        "step_list": step_list
    }
