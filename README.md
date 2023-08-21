# Sych LLM Playground

[![PyPI](https://img.shields.io/pypi/v/sych-llm-playground.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/sych-llm-playground.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/sych-llm-playground)][python version]
[![License](https://img.shields.io/pypi/l/sych-llm-playground)][license]

[![Read the documentation at https://sych-llm-playground.readthedocs.io/](https://img.shields.io/readthedocs/sych-llm-playground/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/sychhq/sych-llm-playground/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/sychhq/sych-llm-playground/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/sych-llm-playground/
[status]: https://pypi.org/project/sych-llm-playground/
[python version]: https://pypi.org/project/sych-llm-playground
[read the docs]: https://sych-llm-playground.readthedocs.io/
[tests]: https://github.com/sychhq/sych-llm-playground/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/sychhq/sych-llm-playground
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Requirements

- **Python Version**: 3.10 or higher. Ensure that Python is properly installed on your system.

## Installation

You can install _Sych LLM Playground_ via [pip] from [PyPI]:

```console
$ pip install sych-llm-playground
```

## Usage

Please see the [Command-line Reference] for details.

## Features

**Sych LLM Playground** offers a streamlined experience for managing and interacting with language models in the cloud. Its capabilities include:

### Configure Cloud Credentials

- A guided setup to input and securely store credentials for your preferred cloud platforms.

```
> sych-llm-playground configure

                 ******
            *******  ******
        *******          *******
      ****,      *****       *****
      ***    **************    ***   @@@@@@@@@                    @@@
      ***    ***       ****    ***   @@@       @@@   @@@  @@@@@@@ @@@@@@@@
      ***    ***       ****    ***    @@@@@@@@  @@@ @@@  @@@      @@@   @@@
      **     *****    *****    ***  @&     @@@   @@@@@   @@@      @@@   @@@
          **************       ***   @@@@@@@      @@@      @@@@@@ @@@   @@@
      *******              *******               @@@
          *******      ******
               **********
                   **

Welcome to the Sych LLM Playground CLI.
This tool is part of our efforts to contribute to the open-source community.
Explore more at https://sych.io

For detailed documentation, visit https://sych-llm-playground.readthedocs.io

Let's begin with the configuration.

[?] Please choose a provider:: AWS
 > AWS

Please Provide your AWS Access Key: xxxxxxxx
Please provide your AWS Secret Key: xxxxx
Please provide your ARN of the IAM role for SageMaker: xxxxxx
Please provide the AWS Region you want to deploy in [us-west-2]:
Configuration successful!

```

### Deploy Models

- Easily deploy various language models to supported cloud platforms.

```
> sych-llm-playground deploy

[?] Please choose a provider:: AWS
 > AWS

✓ Cloud Credentials validated.

✓ Cloud Credentials loaded.

[?] Select a model id to deploy:: Llama-2-7b - v2.0.0
 > Llama-2-7b - v2.0.0
   Llama-2-7b-chat - v1.1.0
   Llama-2-13b - v2.0.0
   Llama-2-13b-chat - v1.1.0
   Llama-2-70b - v1.1.0
   Llama-2-70b-chat v1.1.0

Deploying... Why not grab a cup of coffee? /|\

✓ Model and Endpoint Deployed

Endpoint name: sych-llm-pg-meta-textgeneration-llama-2-7b-e-1692399247

✓ Created REST API

✓ Fetched REST API

✓ Created API resources

✓ Created a POST method

✓ Created API Integration with SageMaker endpoint

✓ API Deployed

Public API HTTP (POST) URL: https://dhdb1mu9w1.execute-api.us-west-2.amazonaws.com/prod/predict

Deployment successful!
```

### List Resources

- Get an overview of all the deployed resources, including models, endpoints, and API Gateways.

```
> sych-llm-playground list

[?] Please choose a provider:: AWS
 > AWS

✓ Cloud Credentials validated.

✓ Cloud Credentials loaded.

Deployed Models:
{'name': 'sych-llm-pg-meta-textgeneration-llama-2-7b-f-m-1692586488'}

Deployed Endpoints:
{'name': 'sych-llm-pg-meta-textgeneration-llama-2-7b-f-e-1692586488', 'url': 'https://runtime.sagemaker.us-west-2.amazonaws.com/endpoints/sych-llm-pg-meta-textgeneration-llama-2-7b-f-e-1692586488/invocations'}

Deployed API Gateways:
{'name': 'sych-llm-pg-api-sych-llm-pg-meta-textgeneration-llama-2-7b-f-e-1692558825', 'id': 'dhdb1mu9w1', 'method': 'POST', 'url': 'https://dhdb1mu9w1.execute-api.us-west-2.amazonaws.com/prod/predict'}

```

### Interact with Models

- Utilize a simple interface to communicate with deployed models, sending queries and receiving responses including a chat interface with conversation history for chat models:

```
> sych-llm-playground interact

[?] Please choose a provider:: AWS
 > AWS

✓ Cloud Credentials validated.

✓ Cloud Credentials loaded.

[?] Select an endpoint to interact with:: sych-llm-pg-meta-textgeneration-llama-2-7b-f-e-1692383398
 > sych-llm-pg-meta-textgeneration-llama-2-7b-f-e-1692383398

Provide a system instruction to guide the model's behavior (optional, e.g., 'Please talk in riddles.'): Be professional
Your desired Max new tokens? (default 256): 70
Your desired top_p? (default 0.9):
Your desired Temperature? (default 0.6) :

Type 'exit' to end the chat.

You: Hi my name is Ryan

Model:  Hello Ryan,

It's a pleasure to meet you. How are you today?

You: What is my name?

Model:  Ryan, it's nice to meet you. How are you today?

You: exit
Exiting chat...
Chat ended.

```

- Interact via Public HTTP API

```
curl -X POST \
    -H 'Content-Type: application/json' \
    -H 'custom_attributes: accept_eula=true' \
    -d '{"inputs": [[{"role": "system", "content": "Talk profession"}, {"role": "user", "content": "Hi my name is Ryan"}]], "parameters": {"max_new_tokens": 256, "top_p": 0.9, "temperature": 0.6}}' \
    'https://valauuhvic.execute-api.us-west-2.amazonaws.com/prod/predict'

[
  {
    "generation":{
      "role":"assistant",
      "content":" Hello Ryan, it's a pleasure to meet you. How may I assist you today? Is there something specific you need help with or would you like to discuss a particular topic? I'm here to listen and provide guidance to the best of my abilities. Please feel free to ask me anything."
    }
  }
]%

```

### Cleanup Resources

- Safely remove deployed models, endpoints and API Gateways to manage costs and maintain a clean environment.

```
> sych-llm-playground cleanup

[?] Please choose a provider:: AWS
 > AWS

✓ Cloud Credentials validated.

✓ Cloud Credentials loaded.

[?] What would you like to cleanup?: Endpoint
  Model
> Endpoint
  API Gateway

[?] Select a endpoint to cleanup:: sych-llm-pg-meta-textgeneration-llama-2-7b-f-e-1692383398
 > sych-llm-pg-meta-textgeneration-llama-2-7b-f-e-1692383398

Endpoint sych-llm-pg-meta-textgeneration-llama-2-7b-f-e-1692383398 cleaned up successfully.

```

## Coming Soon

- **Fine-tuning via CLI**: Direct fine-tuning of models using the CLI will be available soon.

- **Interaction via GUI**: Playround will soon support interaction via a graphical user interface.

- **Local Playground** Downloading and interacting selected models will soon be available.

## Supported Models

**Sych LLM Playground** currently supports the following language models, with more to be added soon:

### Llama Models

- **Llama-2-7b**: Version 2.0.0
- **Llama-2-7b-chat**: Version 1.1.0
- **Llama-2-13b**: Version 2.0.0
- **Llama-2-13b-chat**: Version 1.1.0
- **Llama-2-70b**: Version 1.1.0
- **Llama-2-70b-chat**: Version 1.1.0

Stay tuned for updates as we expand support to include additional language models.

## Supported Cloud Platforms

Playground currently supports the following platforms:

### [Amazon Web Services (AWS) SageMaker](https://aws.amazon.com)

Amazon SageMaker is a managed service that provides developers and data scientists with the ability to build, train, and deploy machine learning (ML) models quickly and easily. Here are some key concepts to understand:

- **Model**: A trained machine learning model that can be deployed to an endpoint for making predictions.
- **Endpoint**: A hosted deployment of your model, facilitating real-time predictions.
- **API Gateway**: A gateway that allows you to call your endpoints. In the context of this tool, it enables interaction with models via a publicly accessible HTTP URL. This tool automatically creates a publicly available POST API endpoint upon successful deployment.

The naming conventions for Models, Endpoints, and API Gateways deployed by this Playground follow these formats:

- Model: `"sych-llm-pg-{model_id}-m-{timestamp}"`
- Endpoint: `sych-llm-pg-{model_id}-e-{timestamp}`
- API Gateway: `"sych-llm-pg-api-{endpoint_name}"`

The timestamp in the naming convention helps in matching endpoints with their corresponding models, especially when two or more models exist with the same ID.

#### AWS SageMaker Instance Types and Cloud Costs

AWS SageMaker allows running models on specific hardware instance types, such as `ml.g5.2xlarge`. It's essential to be aware of the associated costs and quotas:

- It is common to have an applied default quota value of 0 for specific instance types on AWS.

- To enable them, you need to:

  1. Go to your AWS Console > Service Quotas.
  2. Navigate to AWS Services -> Amazon SageMaker -> Apply Quotas for specific instance types.
  3. Apply for the required quota. Please note, it can sometimes take over 1 day to get a quota approved.

- [Here's a link](https://docs.aws.amazon.com/sagemaker/latest/dg/instance-types-az.html) to search for specific instance types used by a model, which you can apply quotas for. If you can't find the instance type for your model, and do not have a quota assigned, the CLI will display an error message with the exact instance type that needs an assigned quota value.

- For more information about the costs associated with SageMaker and the specific instance types, you can refer to the [AWS SageMaker Pricing Page](https://aws.amazon.com/sagemaker/pricing/).

#### Requirements

##### 1. **Register for an AWS Account**

If you don't have one already, you can create an AWS account [here](https://aws.amazon.com).

##### 2. **Create an IAM Role for SageMaker and API Gateway**

Follow these steps to set up the role:

a. **Create a New IAM Role**: Navigate to IAM in the AWS Console, and create a new role.

b. **Add Trust Policy**: Use the following custom trust policy to allow SageMaker and API Gateway to assume this role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": ["sagemaker.amazonaws.com", "apigateway.amazonaws.com"]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

c. **Attach Permission Policy**: Under the newly created role, attach the `AmazonSageMakerFullAccess` managed policy.

##### 3. **Create an IAM User with Necessary Permissions**

Here's how to create the user:

a. **Create IAM User**: In the IAM section of the AWS Console, create a new user.

b. **Attach Managed Policies**: Attach the `AmazonSageMakerFullAccess` and `AmazonAPIGatewayAdministrator` managed policies to the user.

c. **Add Custom Inline Policy**: Add the following custom inline policy, replacing `YOUR_IAM_ROLE_ARN` with the ARN of the IAM role you created earlier:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "YOUR_IAM_ROLE_ARN"
    }
  ]
}
```

d. **Create an Access Key**: In the user's security credentials tab, create a new access key. Be sure to store the generated Access Key ID and Secret Access Key in a safe place.

##### 4. **Configure the CLI**

Use the Access Key ID, Secret Access Key and your IAM role ARN to configure the CLI as shown in the examples above.

### Other Cloud Providers

Other popular cloud platforms are on our roadmap and will be supported soon. Stay tuned for updates, and don't hesitate to contribute or request support for your preferred platforms.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [Apache 2.0 license][license],
_Sych LLM Playground_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

[pypi]: https://pypi.org/
[file an issue]: https://github.com/sychhq/sych-llm-playground/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/sychhq/sych-llm-playground/blob/main/LICENSE
[contributor guide]: https://github.com/sychhq/sych-llm-playground/blob/main/CONTRIBUTING.md
[command-line reference]: https://sych-llm-playground.readthedocs.io/en/latest/usage.html
