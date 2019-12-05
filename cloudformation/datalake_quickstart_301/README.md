## About this lab

### AWS Data Lake quickstart

This lab using a Cloudformation Stack to generate the following items:
* Data lake storage bucket
* Glue data catalog with metadata definition
* Data transfer instance in VPC private subnet
* Step function as task monitor
* Lambda Function as the handler for Step function

**This lab would take you 30 mins to 40 mins to complete all the components and setting up the resources** 

![DFG-Diagram-datalake_lab.png](./img/DFG-Diagram-datalake_lab.png)

**This lab using the following datasets from Kaggle and NYC gov**
* https://www.kaggle.com/fivethirtyeight/uber-pickups-in-new-york-city

    ![kaggle_uber.png](./img/kaggle_uber.png)
* https://www.kaggle.com/selfishgene/historical-hourly-weather-data#city_attributes.csv

    ![kaggle_weather.png](./img/kaggle_weather.png)
* https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

    ![nyc_gov.png](./img/nyc_gov.png)


### Prerequisites

* You must have an AWS account and an IAM user with sufficient permissions to interact with the AWS Management Console

* Create an EC2 key pair for the bastion if you do not have one in this AWS Region, create it before continuing
    * [How to create EC2 key pairs](https://docs.aws.amazon.com/zh_tw/AWSEC2/latest/UserGuide/ec2-key-pairs.html)

* Download the CloudFormation stack **datalake_qs.yml**

### CloudFormation Deployment

* On the service menu, click **CloudFormation**
* For **Prepare template**, choose **Template is ready**
* For **Specify template**, select **Upload a template file** and select **Choose file**.
* Choose the **datalake_qs.yml**
* Click **Next**
* Enter the values in each Parameters and create the stack.

![param.png](./img/param.png)

*Please follow the instruction to fill in the parameters*

**Prefix Configuration**

Parameters                 | Description  |   Default    |
---------------------------|:-------------|:------------:|
Prefix Name                |       An environment name that will be prefixed to resource names (only contain lowercase letters and numbers or underscore (_))      |       dna_team       |

Enter a unique name to prefixed to the resources

**VPC Configuration**

Parameters     | Description  |   Default    |
---------------|:-------------|:------------:|
VPC CIDR       |       Please enter the IP range (CIDR notation) for the VPC of Lab      |      10.66.89.0/24        |
Public Subnet 1 CIDR       |      Please enter the IP range (CIDR notation) for the public subnet in the first Availability Zone        |       10.66.89.0/28       |
Public Subnet 2 CIDR       |       Please enter the IP range (CIDR notation) for the public subnet in the second Availability Zone       |       10.66.89.32/28       |
Private Subnet 1 CIDR       |       Please enter the IP range (CIDR notation) for the private subnet in the first Availability Zone       |     10.66.89.128/28      |   
Private Subnet 2 CIDR       |       Please enter the IP range (CIDR notation) for the private subnet in the second Availability Zone      |     10.66.89.160/28      |   

For lab quick starter
* Leave all parameters as default

**EC2 Data Transfer Server Configuration**

Parameters                                | Description  |   Default    |
------------------------------------------|:-------------|:------------:|
EC2 Key Pair               |      Choose an existing key pair.      |         |
EC2 Instance Type               |      Select one of the instance types      | t2.micro        |

Select your EC2 Key Pair in **Key Pair Name**

**S3 Data Lake Storage Configuration**

Parameters                 | Description  |   Default    |
---------------------------|:-------------|:------------:|
S3 Data Lake Bucket Name                |       Please enter a **UNIQUE** bucket name to create a data repository for S3      |       datalake-lab-bucket-ver6689       |

Enter a unique name to create the data lake bucket

**SNS Email Target Configuration**

Parameters                 | Description  |   Default    |
---------------------------|:-------------|:------------:|
SNS Email Target                |       Enter the Email address for the target of SNS notification       |      sam@ecloud6689.com        |

Enter your mail address to receive the notification

* After entering all the parameter values, choose **Next**
* On the next screen, enter any required tags, an IAM role, or any advanced options, and then choose **Next**
* Review the details on the final screen, **select I acknowledge that AWS CloudFormation might create IAM resources**, and then choose **Create Stack**

* CloudFormation will start to build all resources (stack creation would take 10 - 20 mins)

### It's Coffee time :))

![latte.jpeg](./img/latte.jpeg)

***

![pending.png](./img/pending.png)

Check the AWS CloudFormation Resources section to see all the components set up by this stack 

![done.png](./img/done.png)

Also, check the output from the stack creation

![output.png](./img/output.png)

Examine the new resources via console

**S3**

![s3.png](./img/s3.png)

**Step Function**

![step_func.png](./img/step_func.png)

**Lambda**

![lambda.png](./img/lambda.png)

**EC2**

![ec2.png](./img/ec2.png)

***
* When CloudFormation complete the creation, a Lambda function will be triggered to execute **Step Function**

* Step Function will use another Lambda function to run a job flow for **EMR ingestion job** with multiple steps which including
    * Setup debugging 
    * Setup copy files
    * Run Spark application

*Monitor the EMR job status with **Step Function** workflow*

![sf_workflow.png](./img/sf_workflow.png)

As illustrated in the preceding diagram, the workflow including

1. **Create EMR Cluster Run Step**

    * Triggered by Lambda function

2. **Wait for EMR to create the cluster**

    ![sf_run.png](./img/sf_run.png)

    * Wait for 300 secs
3. **Check EMR cluster status**

    * Wait for 15 secs if the EMR cluster hasn't run
    * End the EMR job if cluster create failed

4. **Wait for EMR step to complete**

    * Wait for 600 secs (**Spark application will take about 15 - 20 mins**)

    ![spark_cluster.png](./img/spark_cluster.png)
    
5. **Monitor EMR step**
    * End the job if all steps run succeed

    ![sf_succeed.png](./img/sf_succeed.png)

    A Lambda function will be triggered to terminate EMR cluster when the job is done

    ![spark_complete.png](./img/spark_complete.png)

    * End the job if any step run failed
    * Wait for 15 secs if Spark application is still running

***

*The following step introduces how to use **Athena** query the S3 data lake*


### Clean-Up Operation Procedures

* Find the S3 Bucket for Redshift which was created by CloudFormation template.
    * (e.g., datalake-lab-bucket-ver6689)

* Delete all object in the bucket and make sure the bucket is empty

![bucket_deletion.png](./img/bucket_deletion.png)

* On the service menu, click **CloudFormation**
* On AWS CloudFormation console make sure that the region is where you created the stack
* Click **Delete** to remove the stack along with all resources

* **The deletion time will take 10 mins to 20 mins**

### Lab References
* [awslab - amazon-s3-step-functions-ingestion-orchestration](https://github.com/awslabs/amazon-s3-step-functions-ingestion-orchestration)