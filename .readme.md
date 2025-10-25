# Building, Deploying and Scaling LLM-Powered Applications

A comprehensive guide to building, containerizing, and deploying LLM applications on AWS using Streamlit, LangChain, and AWS ECS with auto-scaling capabilities.

---

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Local Development Setup](#local-development-setup)
3. [Building the Prediction Pipeline](#building-the-prediction-pipeline)
4. [AWS Configuration](#aws-configuration)
5. [AWS Secrets Manager Setup](#aws-secrets-manager-setup)
6. [Containerization with Docker](#containerization-with-docker)
7. [AWS Elastic Container Registry (ECR)](#aws-elastic-container-registry-ecr)
8. [Deployment to AWS ECS](#deployment-to-aws-ecs)
9. [Understanding Scaling Concepts](#understanding-scaling-concepts)
10. [Implementing Load Balancer and Auto Scaling](#implementing-load-balancer-and-auto-scaling)
11. [Cleanup Resources](#cleanup-resources)

---

## Development Environment Setup

### 1. Installing Development Software

Download and install the following tools:

- **Docker**: [docker.com](https://docker.com)
- **VS Code**: [code.visualstudio.com/download](https://code.visualstudio.com/download)
- **Postman**: [postman.com/downloads](https://postman.com/downloads)
- **Anaconda** (virtual environment): [anaconda.com/download](https://anaconda.com/download)

### 2. Create an AWS Account

Sign up for an AWS account if you don't have one already.

---

## Local Development Setup

### 3. Setting Up Anaconda Virtual Environment

1. Go to Anaconda Navigator
2. Navigate to **Environments**
3. Open terminal
4. List files:
   ```bash
   ls
   ```
5. Create a new virtual environment:
   ```bash
   conda create -n llmapplications
   ```
6. List all virtual environments:
   ```bash
   conda env list
   ```
7. Activate the virtual environment:
   ```bash
   conda activate llmapplications
   ```

### 4. Create Dependencies File

Create a `requirements.txt` file with the following dependencies:

```
langchain
tiktoken
openai
streamlit
boto3
botocore
```

### 5. Install Dependencies

1. Navigate to the project directory in terminal:
   ```bash
   cd project_directory_path
   ```
2. Install all requirements:
   ```bash
   pip3 install -r requirements.txt
   ```

### 6. Configure VS Code Environment

1. Press `Ctrl + Shift + P`
2. Select **Python: Select Interpreter**
3. Choose your virtual environment (`llmapplications`)
4. Open a new terminal

---

## Building the Prediction Pipeline

### 7. Create the Prediction Pipeline

1. Get the OpenAI API key
2. Create `app.py` file
3. Use `chain_type="map_reduce"`:
   - **Example**: To summarize a 500-page book, it first summarizes each page and then summarizes the whole summary

### 8. Secure API Key Injection

Import the `getpass` package to inject the OpenAI API key securely.

### 9. Run the Application

```bash
python3 app.py
```

---

## AWS Configuration

### 10. Installing and Configuring AWS CLI

#### Create IAM User

1. Open **AWS Console**
2. Navigate to **IAM**
3. Click on **Users** (left tab)
4. Click **Create user**
5. Provide a username
6. Check **Provide access to AWS Management Console**
7. Select radio button: **I want to create an IAM user**
8. Set **Console password** → **Custom password**
9. Configure **Set permissions** → **Add user to group**

### 11. Set Access Keys

1. Go to **IAM**
2. Navigate to **Users** → Select your user
3. Go to **Permissions**
4. Navigate to **Security credentials**
5. Click on **Access keys**
6. Select **Command Line Interface**
7. Add description tag

### 12. Install AWS CLI

Follow the installation guide:

- [docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### 13. Configure AWS CLI

Follow the configuration guide:

- [docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)
- Use **Configuring using AWS CLI commands**
- Set up **short term credentials**

---

## AWS Secrets Manager Setup

### 14. Setting Up Secrets Manager

1. Open **AWS Console**
2. Navigate to **Secrets Manager**
3. Click **Store a new secret**
4. Select **Other type of secret** (Radio button)
5. Add **Key value pairs**: `OPENAI_API_KEY`
6. Select **Encryption key**: `aws/secretsmanager`
7. Provide **Secret name and description**: `aws-manager-openai-secret`
8. Set **Configure automatic rotation**: OFF
9. Click **Store**

### 15. Integrate Secret into Application

1. Go to the created secret
2. Navigate to **Sample code** → Select **Python3** (copy code)
3. Click **Retrieve secret value** (button on right) to view the secret value
4. Replace the `getpass` code in `app.py` with the copied sample code

### 16. Feed API Key into Prediction Pipeline

Call the function directly in the LLM: `get_secret()`

---

## Building the Frontend

### 17. Create Streamlit Frontend

Import Streamlit and add UI components:

```python
import streamlit as st
```

Add user input field and button.

### 18. Run the Streamlit App

```bash
streamlit run app.py
```

---

## Containerization with Docker

### 19. Writing Dockerfile

Create a Dockerfile. Note: The Streamlit repo is cloned to get the Streamlit binary in the Docker container.

---

## AWS Elastic Container Registry (ECR)

### 20. Packaging and Storing Application on ECR

1. Open **AWS Console** → **ECR**
2. Click **Create Repository**
3. Select **Private**
4. Repository name: `langchain_streamlit`
5. Navigate to **Amazon ECR** → `langchain_streamlit` → **View push commands**
6. Ensure AWS CLI and Docker Desktop are running
7. Execute the following commands:

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 9897899.dkr.ecr.us-east-1.amazonaws.com

# Build Docker image
docker build -t langchain_streamlit .

# Tag the image
docker tag langchain_streamlit:latest 9897899.dkr.ecr.us-east-1.amazonaws.com/langchain_streamlit:latest

# Push to ECR
docker push 9897899.dkr.ecr.us-east-1.amazonaws.com/langchain_streamlit:latest
```

**Note**: Change `latest` to version tags like `v1`, `v2` for version control.

### 21. Testing Packaged Application Locally

```bash
docker run -p 8501:8501 langchain_streamlit:v1
```

- `8501` (first) = system port
- `8501` (second) = Docker image port

---

## Deployment to AWS ECS

### 22. Modifying Account Permissions for Deployment

Deploy using **Amazon Container Service on AWS Fargate**.

#### Understanding ECS Structure

- First, build a **cluster**
- Each cluster has a **task definition**

#### Create IAM Role for ECS Tasks

1. Navigate to **IAM** → **Roles** → **Create role**
2. Select **Trusted entity**: AWS Service
3. Select **Use case**: Elastic Container Service
4. Choose use case for the specified service: **Elastic Container Service Task**
5. **Role Details** → **Role name**: `ecs-task-execution-role-secret` → **Create role**

#### Add Inline Policy for Secrets Access

1. Go to the created role details screen
2. Click **Add permissions** → **Create inline policy**
3. Switch to **JSON** tab
4. Add the following policy:
   ```json
   {
     "Action": ["secretsmanager:GetSecretValue"],
     "Resource": ["secret-arn"]
   }
   ```
5. Click **Next**
6. **Review and Create** → **Policy name**: `ecs-task-secret`

#### Attach Additional Policy

1. Click **Add one more permission** → **Add permission** → **Attach Policy**
2. Search for: `AmazonECSTaskExecutionRolePolicy`
3. Click **Add Permission**

### 23. Deploying Application on ECS

#### Create ECS Cluster

1. Navigate to **Clusters** → **Create Cluster**
2. **Cluster Name**: `ecs-fargate-cluster`
3. **Infrastructure**: AWS Fargate (Serverless)

#### Create Task Definition

1. Navigate to **Task Definitions** → **Create new task definition**
2. **Task name**: `ecs-fargate-task`
3. **Launch Type**: AWS Fargate
4. **Operating System**: Linux/ARM64
5. **CPU**: 1
6. **Memory**: 3GB
7. **Task execution role**: Select `ecs-task-execution-role-secret` (created above)

#### Configure Container

1. **Container 1 Info**:

   - **Name**: `Container-1`
   - **Image URI**: (Image URI from Elastic Container Registry)
   - **Container port**: Same as Docker expose port (8501)

2. **Environment variables**:

   - **Key**: `openai_key`
   - **Value type**: Value from
   - **Value**: Add ARN of secret

3. **Amazon CloudWatch**:

   - Add log configuration
   - **Key**: `openai_key_test`
   - **Value type**: Value from
   - **Value**: Add secret ARN

4. Click **Create task**

### 24. Testing Application on ECS

#### Run Task

1. Go to **Task definition** → Select the task
2. Click **Deploy** button on top → Select **Run task**
3. **Existing Cluster**: `ecs-fargate-cluster`
4. **Compute configuration**: Launch type
5. **Launch type**: Fargate
6. **Deployment configuration** → **Application Type**: Task
7. Click **Create** (now ECS task is associated to the cluster)

#### Configure Security Group

1. Navigate to **Cluster** → `ecs-fargate-cluster` → **Task**
2. Go to **Task detail** → **Networking** → **ENI ID** → **Security groups**
3. Click **Edit inbound rules**
4. Add rule:
   - **Port**: 8501
   - **Source**: Anywhere-IPv4
5. **Save rules** (allows traffic from anywhere)

#### Access Application

1. Navigate to **Clusters** → **Cluster** → **Public IP**
2. Access application at: `public_ip:8501`

---

## Understanding Scaling Concepts

### 25. Scaling with Application Load Balancers and Auto Scaling Groups

#### Difference Between Horizontal and Vertical Scaling

**Application Architecture**:

- Your app sits inside a Docker container
- Based on configuration: 1 CPU and 3GB RAM
- This image is then copied over to EC2 machine with same configurations

**System Metrics to Monitor**:

- CPU usage
- Requests/sec
- Memory usage

**Scaling Scenario**:

- With the above configuration, assume the system can handle 70 requests/sec
- If we receive 100 requests, we have 30 extra requests

**Options for Extra Requests**:

- Discard them
- Put them in a queue
- **Note**: The above solutions are not viable, which is why we need to scale our application

#### Scaling Options

**Option 1: Vertical Scaling** (Not Recommended)

- Choose a bigger machine
- This machine will always be running
- In scenarios when we don't get that level of requests, we will still be charged

**Option 2: Horizontal Scaling** (Recommended)

- Add more similar-sized machines
- Make replicas of the same system
- Each machine has the application
- Install a **Load Balancer** in front of these machines (attached to each machine)
- The load balancer IP address is exposed to the user
- When a user sends a request, the load balancer checks which machine has capacity to handle that request
- The load balancer sends the request to that machine using an algorithm (like round robin)

---

## Implementing Load Balancer and Auto Scaling

### 26. Cleanup Previous Task

Before implementing auto-scaling, clean up the previous simple deployment:

1. Navigate to **Tasks** → Select task → **Actions** → **Deregister**
2. Go to **Cluster** → **Task** → Select task → **Actions** → **Stop all**
3. Navigate to **Clusters** → **Cluster** → **Delete cluster**

### 27. Adding Load Balancer and Auto Scaling

#### Create Scalable Cluster

1. Go to **AWS Console** → **Elastic Container Service** → **Clusters** → **Create cluster**
2. **Cluster name**: `ecs-scalable-cluster`

#### Create Scalable Task Definition

1. Navigate to **Task Definitions** → **Create new task definition**
2. **Task name**: `ecs-scalable-task`
3. **Launch Type**: AWS Fargate
4. **Operating system**: Linux/ARM64
5. **CPU**: 1
6. **Memory**: 3GB
7. **Task role - Task execution role**: `ecs-task-execution-role-secret`

#### Configure Container

1. **Container 1**:

   - **Name**: `container-1`
   - **Image URI**: (Image URI from ECR)
   - **Port**: 8501

2. **Add environment variable**:

   - **Key**: `openai_key`
   - **Value type**: Value from
   - **Value**: ARN of secret manager

3. **Logs**:

   - **Key**: `openai_key_test`
   - **Value type**: Value from
   - **Value**: Secret ARN

4. Click **Create**

#### Create Service with Load Balancer

1. Navigate to **AWS ECS** → **Task Definitions** → Select task → **Deploy** → **Create Service**

2. **Environment**:

   - **Existing cluster**: `ecs-scalable-cluster`
   - **Compute options**: Launch Type

3. **Deployment configuration**:

   - **Service name**: `demo-service`
   - **Service type**: Replica
   - **Deployment type**: Rolling update

4. **Load Balancing**:

   - **Load balancer type**: Application load balancer
   - **Application load balancer**: Create a new
   - **Load balancer name**: `test-load-balancer`
   - **Health check grace period**: 30 seconds
     - This checks the image health after every 30 seconds. If the image is not working properly, the load balancer will remove that image and create a new replica and re-initialize it.

5. **Listener**:

   - **Create new listener**
   - **Port**: 8501

6. **Target group**:
   - **Create new target group**: `test-target-group`

#### Configure Service Auto Scaling

**Service auto scaling** enables automatic scale-up and scale-down based on workload:

1. **Enable auto scaling groups**
2. **Minimum number of tasks**: 1
3. **Maximum number of tasks**: 2
4. **Scaling policy type**: Target tracking
5. **Policy name**: `scaling-policy`
6. **ECS service metric**: `ALBRequestCountPerTarget`
7. **Target value**: 70
8. **Scale-out cool down period**: 300 seconds
   - After 300 seconds, the load balancer starts to add more containers
9. **Scale-in cool down period**: 300 seconds
10. Click **Create**

### 28. Exposing and Testing the Service

#### Configure Security Group

1. Navigate to **AWS ECS** → **Cluster** → Select the cluster you created → **Task**
2. Go to **Task detail** → **Networking** → **ENI-ID detail** → **Security groups**
3. Click **Edit inbound rules**
4. **Add rule**:
   - **Type**: Custom TCP
   - **Port**: 8501
   - **Source**: Anywhere IPv4
5. **Save rules**

#### Access Application

1. Go back to **Networking** → Copy **Public IP**
2. Access application at: `public_ip:8501`

---

## Cleanup Resources

### Final Cleanup Steps

To avoid ongoing charges, clean up all resources:

1. Go to **Home page** → **EC2** → **Load Balancers**

   - **Actions** → **Delete load balancer**

2. Navigate to **Elastic Container Service** → **Task Definitions**

   - **Action** → **Deregister**

3. Go to **Cluster** → **Service**

   - **Delete service**

4. Navigate to **Cluster** → **Task**

   - **Stop all**

5. Finally, **Delete cluster**

---

## Summary

This guide covered:

- ✅ Local development setup with Anaconda and dependencies
- ✅ Building LLM prediction pipeline with LangChain
- ✅ Securing API keys with AWS Secrets Manager
- ✅ Creating Streamlit frontend
- ✅ Containerizing with Docker
- ✅ Storing images in AWS ECR
- ✅ Deploying to AWS ECS Fargate
- ✅ Implementing Load Balancers for traffic distribution
- ✅ Configuring Auto Scaling for handling variable loads
- ✅ Proper cleanup to avoid unnecessary costs

You now have a production-ready, scalable LLM application deployed on AWS!
