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

Endpoint name: sych-llm-pg-meta-textgeneration-llama-2-7b-e-1692399247

Deployment successful!

```

### List Resources

- Get an overview of all the deployed resources, including models and endpoints.

```
> sych-llm-playground list

[?] Please choose a provider:: AWS
 > AWS

✓ Cloud Credentials validated.

✓ Cloud Credentials loaded.

Deployed Models:
sych-llm-pg-meta-textgeneration-llama-2-7b-f-m-1692383398

Deployed Endpoints:
sych-llm-pg-meta-textgeneration-llama-2-7b-f-e-1692383398

```

### Interact with Models

- Utilize a simple interface to communicate with deployed models, sending queries and receiving responses.

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

### Cleanup Resources

- Safely remove deployed models and endpoints to manage costs and maintain a clean environment.

```
> sych-llm-playground cleanup

[?] Please choose a provider:: AWS
 > AWS

✓ Cloud Credentials validated.

✓ Cloud Credentials loaded.

[?] What would you like to cleanup?: Endpoint
  Model
> Endpoint

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

Amazon SageMaker is a managed service that provides developers and data scientists with the ability to build, train, and deploy machine learning (ML) models quickly. Key concepts include:

- **Model**: A trained machine learning model that you can deploy to an endpoint.
- **Endpoint**: A hosted deployment of your model, which enables real-time predictions. Names of Endpoints and Models deployed by this Playground are in the format: `"sych-llm-pg-{model_id}-m-{timestamp}"`. The timestamp will allow you to match endpoints with their corresponding models when two or models exists with the same id.

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

- Registered AWS Account
- AWS IAM User Access Key
- AWS IAM User Secret Key
- AWS IAM User must have `AmazonSageMakerFullAccess` permission policy assigned.
- AWS IAM Role ARN
- AWS IAM Role must have `AmazonSageMakerFullAccess` permission policy assigned.

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
