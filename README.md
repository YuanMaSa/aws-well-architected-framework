
# Prominent data platform design with AWS well-architected framework
![data_lake.jpg](/img/data_lake.jpg)

The passage will elucidate how to combine AWS Well-Architected Framework concept with data platform design

***

## Introduction to AWS well-architected framework

Building an application is not difficult

![sdlc.jpg](/img/sdlc.jpg)

When you reviewing the system, can you answer the question: **"Are you Well-Architected?"**

***

The AWS Well-Architected Framework is based on five pillars — operational
excellence, security, reliability, performance efficiency, and cost optimization

![pillars.png](/img/pillars.png)

Name                       | Description  |
---------------------------|:------------|
Operational Excellence     | The ability to run and monitor systems to deliver business value and to continually improve supporting processes and procedures. |
Security                   | The ability to protect information, systems, and assets while delivering business value through risk assessments and mitigation strategies. |
Reliability                | The ability of a system to recover from infrastructure or service disruptions dynamically acquire computing resources to meet demand, and mitigate disruptions such as misconfigurations or transient network issues. | 
Performance Efficiency     | The ability to use computing resources efficiently to meet system requirements, and to maintain that efficiency as demand changes and technologies evolve. |
Cost Optimization          | The ability to run systems to deliver business value at the lowest price point. |

### General Design Principals

***

#### <span style="color:#009FCC">Stop guessing your capacity needs</span>

Eliminate guessing about your infrastructure capacity needs. When you make a capacity decision before you deploy a system, you might end up sitting on expensive idle resources or dealing with the performance implications of limited capacity. With cloud computing, these problems can go away. You can use as much or as little capacity as you need, and scale up and down automatically. 

#### <span style="color:#009FCC">Test systems at production scale</span>

In the cloud, you can create a production-scale test environment on demand, complete your testing, and then decommission the resources. Because you only pay for the test environment when it's running, you can simulate your live environment for a fraction of the cost of testing on premises.

#### <span style="color:#009FCC">Automate to make architectural experimentation easier</span>

Automation allows you to create and replicate your systems at low cost and avoid the expense of manual effort. You can track changes to your automation, audit the impact, and revert to previous parameters when necessary. 

#### <span style="color:#009FCC">Allow for evolutionary architectures</span>

Allow for evolutionary architectures. In a traditional environment, architectural decisions are often implemented as static, one-time events, with a few major versions of a system during its lifetime. As a business and its context continue to change, these initial decisions might hinder the system's ability to deliver changing business requirements. In the cloud, the capability to automate and test on demand lowers the risk of impact from design changes. This allows systems to evolve over time so that businesses can take advantage of innovations as a standard practice. 

#### <span style="color:#009FCC">Drive architectures using data</span>

In the cloud you can collect data on how your architectural choices affect the behavior of your workload. This lets you make fact-based decisions on how to improve your workload. Your cloud infrastructure is code, so you can use that data to inform your architecture choices and improvements over time.

#### <span style="color:#009FCC">Improve through game days</span>

Test how your architecture and processes perform by regularly scheduling game days to simulate events in production. This will help you understand where improvements can be made and can help develop organizational experience in dealing with events.

***
### <span style="color:#E63F00"> <em>Operational Excellence</em> </span>

#### <span style="color:#1E90FF"> Design Principals </span>

* **Perform operations as code**

    In the cloud, you can apply the same engineering discipline that you use for application code to your entire environment. You can define your entire workload (applications, infrastructure) as code and update it with code. You can implement your operations procedures as code and automate their execution by triggering them in response to events. By performing operations as code, you limit human error and enable consistent responses to events.

* **Annotate documentation**

    In an on-premises environment, documentation is created by hand, used by people, and hard to keep in sync with the pace of change. In the cloud, you can automate the creation of annotated documentation after every build (or automatically annotate hand-crafted documentation). Annotated documentation can be used by people and systems. Use annotations as an input to your operations code.

* **Make frequent, small, reversible changes**

    Design workloads to allow components to be updated regularly. Make changes in small increments that can be reversed if they fail (without affecting customers when possible).

* **Refine operations procedures frequently**

    As you use operations procedures, look for opportunities to improve them. As you evolve your workload, evolve your procedures appropriately. Set up regular game days to review and validate that all procedures are effective and that teams are familiar with them.

* **Anticipate failure**

    Perform “pre-mortem” exercises to identify potential sources of failure so that they can be removed or mitigated. Test your failure scenarios and validate your understanding of their impact. Test your response procedures to ensure that they are effective, and that teams are familiar with their execution. Setup regular game days to test workloads and team responses to simulated events.

* **Learn from all operational failures**

    Drive improvement through lessons learned from all operational events and failures. Share what is learned across teams and through the entire organization.

#### <span style="color:#1E90FF"> Best Practices </span>

* Prepare
* Operate
* Evolve

#### <span style="color:#1E90FF"> Key AWS Services </span>

* **Essential**
    * CloudFormation
        * enables you to provision resources in an orderly and consistent fashion from your development through production environments

* **Prepare**
    * AWS Config
        * AWS Config and AWS Config rules can be used to create standards for workloads
* **Operate**
    * CloudWatch
        * monitor the operational health of a workload
* **Evolve**
    * Amazon Elasticsearch Service (ES)
        * analyze your log data to gain actionable insights quickly and securely


***
### <span style="color:#E63F00"> <em>Security</em> </span>

#### <span style="color:#1E90FF"> Design Principals </span>

* **Implement a strong identity foundation**

    Implement the principle of least privilege and enforce separation of duties with appropriate authorization for each interaction with your AWS resources. Centralize privilege management and reduce or even eliminate reliance on long-term credentials.

* **Enable traceability**

    Monitor, alert, and audit actions and changes to your environment in real time. Integrate logs and metrics with systems to automatically respond and take action.

* **Apply security at all layers**

    Rather than just focusing on protection of a single outer layer, apply a defense-in-depth approach with other security controls. Apply to all layers (e.g., edge network, VPC, subnet, load balancer, every instance, operating system, and application).

* **Automate security best practices**

    Automated software-based security mechanisms improve your ability to securely scale more rapidly and cost effectively. Create secure architectures, including the implementation of controls that are defined and managed as code in version-controlled templates.

* **Protect data in transit and at rest**

    Classify your data into sensitivity levels and use mechanisms, such as encryption, tokenization, and access control where appropriate.

* **Keep people away from data**

    Create mechanisms and tools to reduce or eliminate the need for direct access or manual processing of data. This reduces the risk of loss or modification and human error when handling sensitive data.

* **Prepare for security events**

    Prepare for an incident by having an incident management process that aligns to your organizational requirements. Run incident response simulations and use tools with automation to increase your speed for detection, investigation, and recovery

#### <span style="color:#1E90FF"> Best Practices </span>

* Identity and Access Management
* Detective Controls
* Infrastructure Protection
* Data Protection
* Incident Response

#### <span style="color:#1E90FF"> Key AWS Services </span>

![security_key_services.png](/img/security_key_services.png)

* **Data Protection**
    
    Services such as ELB, Amazon Elastic Block Store (Amazon EBS), Amazon S3, and Amazon Relational Database Service (Amazon RDS) include encryption capabilities to protect your data in transit and at rest. Amazon Macie automatically discovers, classifies and protects sensitive data, while AWS Key Management Service (AWS KMS) makes it easy for you to create and control keys used for encryption.

    * ELB
    * EBS
    * S3
    * RDS
    * KMS

* **Identity and Access Management**

    IAM enables you to securely control access to AWS services and resources. MFA adds an additional layer of protection on user access. AWS Organizations lets you centrally manage and enforce policies for multiple AWS accounts.

    * IAM
    * MFA

* **Infrastructure Protection**

    Amazon Virtual Private Cloud (Amazon VPC) enables you to launch AWS resources into a virtual network that you've defined. Amazon CloudFront is a global content delivery network that securely delivers data, videos, applications, and APIs to your viewers which integrates with AWS Shield for DDoS mitigation. AWS WAF is a web application firewall that is deployed on either Amazon CloudFront or Application Load Balancer to help protect your web applications from common web exploits.

    * VPC

* **Detective Control**

    AWS CloudTrail records AWS API calls, AWS Config provides a detailed inventory of your AWS resources and configuration. Amazon GuardDuty is a managed threat detection service that continuously monitors for malicious or unauthorized behavior. Amazon CloudWatch is a monitoring service for AWS resources which can trigger CloudWatch Events to automate security responses.

    * CloudWatch
    * CloudTrail

* **Incident Response**

    IAM should be used to grant appropriate authorization to incident response teams and response tools. AWS CloudFormation can be used to create a trusted environment or clean room for conducting investigations. Amazon CloudWatch Events allows you to create rules that trigger automated responses including AWS Lambda.

    * CloudWatch Events
    * Lambda

***
### <span style="color:#E63F00"> <em>Reliability</em> </span>

#### <span style="color:#1E90FF"> Design Principals </span>

* **Test recovery procedures**

    In an on-premises environment, testing is often conducted to prove the system works in a particular scenario. Testing is not typically used to validate recovery strategies. In the cloud, you can test how your system fails, and you can validate your recovery procedures. You can use automation to simulate different failures or to recreate scenarios that led to failures before. This exposes failure pathways that you can test and rectify before a real failure scenario, reducing the risk of components failing that have not been tested before.

* **Automatically recover from failure**

    By monitoring a system for key performance indicators (KPIs), you can trigger automation when a threshold is breached. This allows for automatic notification and tracking of failures, and for automated recovery processes that work around or repair the failure. With more sophisticated automation, it's possible to anticipate and remediate failures before they occur.

* **Scale horizontally to increase aggregate system availability:**

    Replace one large resource with multiple small resources to reduce the impact of a single failure on the overall system. Distribute requests across multiple, smaller resources to ensure that they don't share a common point of failure.

* **Stop guessing capacity**

    A common cause of failure in on-premises systems is resource saturation, when the demands placed on a system exceed the capacity of that system (this is often the objective of denial of service attacks). In the cloud, you can monitor demand and system utilization, and automate the addition or removal of resources to maintain the optimal level to satisfy demand without overor under- provisioning.

* **Manage change in automation**

    Changes to your infrastructure should be done using automation. The changes that need to be managed are changes to the automation.

#### <span style="color:#1E90FF"> Best Practices </span>

* Foundations
* Change Management
* Failure Management

#### <span style="color:#1E90FF"> Key AWS Services </span>

![reliability_key_services.png](/img/reliability_key_services.png)

* **Foundations**

    AWS IAM enables you to securely control access to AWS services and resources. Amazon VPC lets you provision a private, isolated section of the AWS Cloud where you can launch AWS resources in a virtual network. AWS Trusted Advisor provides visibility into service limits. AWS Shield is a managed Distributed Denial of Service (DDoS) protection service that safeguards web applications running on AWS.

    * IAM
    * VPC

* **Change Management**

    AWS CloudTrail records AWS API calls for your account and delivers log files to you for auditing. AWS Config provides a detailed inventory of your AWS resources and configuration, and continuously records configuration changes. Amazon Auto Scaling is a service that will provide an automated demand management for a deployed workload. Amazon CloudWatch provides the ability to alert on metrics, including custom metrics. Amazon CloudWatch also has a logging feature that can be used to aggregate log files from your resources.

    * Amazon Auto Scaling
    * CloudTrail
    * CloudWatch

* **Failure Management**

    AWS CloudFormation provides templates for the creation of AWS resources and provisions them in an orderly and predictable fashion. Amazon S3 provides a highly durable service to keep backups. Amazon Glacier provides highly durable archives. AWS KMS provides a reliable key management system that integrates with many AWS services.

    * CloudFormation
        * rollback

    * S3
        * backup


***
### <span style="color:#E63F00"> <em>Performance Efficiency</em> </span>

#### <span style="color:#1E90FF"> Design Principals </span>

* **Democratize advanced technologies**

    Technologies that are difficult to implement can become easier to consume by pushing that knowledge and complexity into the cloud vendor's domain. Rather than having your IT team learn how to host and run a new technology,  they can simply consume it as a service. For example, NoSQL databases, media transcoding, and machine learning are all technologies that require expertise that is not evenly dispersed across the technical community. In the cloud, these technologies become services that your team can consume while focusing on product development rather than resource provisioning and management.

* **Go global in minutes**

    Easily deploy your system in multiple Regions around the world with just a few clicks. This allows you to provide lower latency and a better experience for your customers at minimal cost.

* **Use serverless architectures**

    In the cloud, serverless architectures remove the need for you to run and maintain servers to carry out traditional compute activities. For example, storage services can act as static websites, removing the need for web servers, and event services can host your code for you. This not only removes the operational burden of managing these servers, but also can lower transactional costs because these managed services operate at cloud scale.

* **Experiment more often**

    With virtual and automatable resources, you can quickly carry out comparative testing using different types of instances, storage, or configurations.

* **Mechanical sympathy**

    Use the technology approach that aligns best to what you are trying to achieve. For example, consider data access patterns when selecting database or storage approaches.

#### <span style="color:#1E90FF"> Best Practices </span>

* Selection
* Review
* Monitoring
* Tradeoffs


#### <span style="color:#1E90FF"> Key AWS Services </span>

![performance_efficiency_key_services.png](/img/performance_efficiency_key_services.png)

* **Selection**
    * **Compute** 
    
        Auto Scaling is key to ensuring that you have enough instances to meet demand and maintain responsiveness.

        * Amazon Auto Scaling

    * **Storage**

        ![storage_comparison.png](/img/storage_comparison.png)
    
        Amazon EBS provides a wide range of storage options (such as SSD and provisioned input/output operations per second (PIOPS)) that allow you to optimize for your use case. Amazon S3 provides serverless content delivery, and Amazon S3 transfer acceleration enables fast, easy, and secure transfers of files over long distances.

        * S3
        * EBS

    * **Database**

        ![database_comparison.png](/img/database_comparison.png)

        Amazon RDS provides a wide range of database features (such as PIOPS and read replicas) that allow you to optimize for your use case. Amazon DynamoDB provides single-digit millisecond latency at any scale.

        * RDS
        * DynamoDB

    * **Network**

        Amazon Route 53 provides latency-based routing. Amazon VPC endpoints and AWS Direct Connect can reduce network distance or jitter.

        * VPC
        * Route 53
        * Direct Connect

* **Review**

    The AWS Blog and the What's New section on the AWS website are resources for learning about newly launched features and services.

* **Monitoring**

    Amazon CloudWatch provides metrics, alarms, and notifications that you can integrate with your existing monitoring solution, and that you can use with AWS Lambda to trigger actions.

    * CloudWatch
    * Lambda


* **Tradeoffs**

    Amazon ElastiCache, Amazon CloudFront, and AWS Snowball are services that allow you to improve performance. Read replicas in Amazon RDS can allow you to scale read-heavy workloads.
    

***

### <span style="color:#E63F00"> <em>Cost Optimization</em> </span>


#### <span style="color:#1E90FF"> Design Principals </span>

* **Adopt a consumption model**

    Pay only for the computing resources that you require and increase or decrease usage depending on business requirements, not by using elaborate forecasting. For example, development and test environments are typically only used for eight hours a day during the work week. You can stop these resources when they are not in use for a potential cost savings of 75% (40 hours versus 168 hours).

* **Measure overall efficiency**

    Measure the business output of the workload and the costs associated with delivering it. Use this measure to know the gains you make from increasing output and reducing costs.

* **Stop spending money on data center operations**

    AWS does the heavy lifting of racking, stacking, and powering servers, so you can focus on your customers and organization projects rather than on IT infrastructure.

* **Analyze and attribute expenditure**

    The cloud makes it easier to accurately identify the usage and cost of systems, which then allows transparent attribution of IT costs to individual workload owners. This helps measure return on investment (ROI) and gives workload owners an opportunity to optimize their resources and reduce costs.

* **Use managed and application level services to reduce cost of ownership**

    In the cloud, managed and application level services remove the operational burden of maintaining servers for tasks such as sending email or managing databases. As managed services operate at cloud scale, they can offer a lower cost per transaction or service.

#### <span style="color:#1E90FF"> Best Practices </span>

* Expenditure Awareness
* Cost-Effective Resources
* Matching supply and demand
* Optimizing Over Time


#### <span style="color:#1E90FF"> Key AWS Services </span>

![cost_optimization_key_services.png](/img/cost_optimization_key_services.png)

* **Expenditure Awareness**

    AWS Cost Explorer allows you to view and track your usage in detail. AWS Budgets notify you if your usage or spend exceeds actual or forecast budgeted amounts

    * AWS Cost Explorer

* **Cost-Effective Resources**

    You can use Cost Explorer for Reserved Instance recommendations, and see patterns in how much you spend on AWS resources over time. Use Amazon CloudWatch and Trusted Advisor to help right size your resources. You can use Amazon Aurora on RDS to remove database licensing costs. AWS Direct Connect and Amazon CloudFront can be used to optimize data transfer.

* **Matching supply and demand**

    Auto Scaling allows you to add or remove resources to match demand without overspending.

    * Amazon Auto Scaling

* **Optimizing Over Time**

    The AWS News Blog and the What's New section on the AWS website are resources for learning about newly launched features and services. AWS Trusted Advisor inspects your AWS environment and finds opportunities to save you money by eliminating unused or idle resources or committing to Reserved Instance capacity.

    * AWS Trusted Advisor

***
## Take well-architected concept into the data platform design




## Real scenario and case study





## Summary





## Appendix: CloudFormation


    {"CloudFormation": "Infrastructure as code"}
