# Project ERP UK v1 - Secondary Cron

## Overview

The **ERP UK v1 - Secondary Cron** project is aimed at overcoming the limitations of the cron functionality in Odoo 7. In Odoo 7, cron execution and its execution time are not guaranteed, which can lead to unpredictable behavior in scheduled tasks. To address this issue, we have developed this project, which provides a more reliable and flexible way to schedule and execute tasks.

## Project Architecture

### Version 2 (Current)

The current version (v2) of the project utilizes AWS Lambda and EventBridge rules to manage cron-like functionality. This architecture offers several advantages over the previous version (v1) and traditional cron jobs:

- **Flexibility**: AWS Lambda allows us to run the script whenever required, ensuring precise execution timing.
- **Cost-Efficiency**: By moving to AWS Lambda, we can reduce infrastructure costs associated with maintaining EC2 instances or Docker environments like ECS.
- **Reduced Complexity**: We no longer rely on the Python library apscheduler, simplifying the programming model.

### Version 1 (Legacy)

The previous version (v1) of the project was built using the Python library apscheduler. While functional, it had some drawbacks:

- **Dependency on EC2 or Computing Instances**: v1 required an EC2 instance or a computing environment like Docker (ECS) to run scheduled tasks.
- **Less Precise Timing**: The timing of task execution was less predictable compared to the current AWS Lambda-based architecture.

## Reasons for Version 2 (v2)

The decision to create version 2 (v2) of this project was driven by several key factors:

1. **Improved Reliability**: AWS Lambda and EventBridge provide a highly reliable and serverless execution environment, ensuring that tasks run when needed without the risk of server downtime.

2. **Reduced Operational Overhead**: With AWS Lambda, there's no need to manage and maintain EC2 instances or Docker containers. This significantly reduces operational overhead and infrastructure costs.

3. **Precision and Scalability**: AWS Lambda offers precise execution timing, making it suitable for critical tasks. It also scales automatically to handle increased workloads.

4. **Cost Optimization**: By moving to AWS Lambda, we can optimize costs by paying only for the actual execution time of the tasks, rather than maintaining constantly running instances.

5. **Simplified Architecture**: The transition to AWS Lambda simplifies the architecture, eliminating the need for external libraries like apscheduler. This results in cleaner and more maintainable code.

## Getting Started

### Prerequisites

Before you can build, run locally, or deploy this application, you need to have the following dependencies installed:

1. **AWS CLI**: Install the AWS Command Line Interface (CLI) to manage AWS services.

   ```bash
   # On Linux or macOS
   pip install awscli

   # On Windows
   Download and run the AWS CLI installer from the official AWS website.
   ```

2. **AWS SAM CLI**: Install the AWS Serverless Application Model Command Line Interface (SAM CLI) to build and test serverless applications.

   ```bash
   # On Linux or macOS
   pip install aws-sam-cli

   # On Windows
   Download and run the SAM CLI installer from the official AWS website.
   ```

### Build and Run Locally

To build and run the application locally using AWS SAM, follow these steps:

1. **Clone the Repository**: Clone this repository to your local development environment.

   ```bash
   git clone git@github.com:Chameleon-Codewing-Ltd/erp-uk-v1-secondary-cron.git
   ```

2. **Navigate to Project Directory**: Change your working directory to the project root.

   ```bash
   cd erp-uk-v1-secondary-cron
   ```

3. **Build the Application**: Use AWS SAM to build the application.

   ```bash
   sam build
   ```

4. **Invoke Locally**: You can invoke the AWS Lambda function locally for testing purposes.

   ```bash
   sam local invoke
   ```

### Deploy to AWS

To deploy the application to AWS using AWS SAM, follow these steps:

1. **Configure AWS CLI**: Ensure that your AWS CLI is configured with the necessary AWS credentials and default region.

   ```bash
   aws configure
   ```

2. **Deploy Application**: Use AWS SAM to deploy the application.

   ```bash
   sam deploy --guided
   ```

   Follow the prompts to set deployment options, such as the stack name and AWS region.

3. **Monitor Deployment**: Monitor the deployment process in the AWS CloudFormation console or use the AWS CLI to check the stack status.

### Infrastructure as Code (IAC)

This project leverages AWS CloudFormation as Infrastructure as Code (IAC) to define and manage the AWS resources required for deployment. You can find the CloudFormation templates in the `infra` directory of this repository. To make changes to the infrastructure, modify the appropriate template files and update the stack as needed.

## License

This project is licensed under the **Proprietary and Confidential**.

---

**Note**: This README file provides a general overview of the project, including building and deploying using AWS SAM, dependency installation, and Infrastructure as Code (IAC) with AWS CloudFormation. For more detailed information, please consult the project documentation and specific version documentation (v1 or v2) for implementation details and considerations.