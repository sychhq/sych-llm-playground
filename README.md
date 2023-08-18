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

## Features

**Sych LLM Playground** offers a streamlined experience for managing and interacting with language models in the cloud. Its capabilities include:

### Deploy Models

- Easily deploy various language models to supported cloud platforms.

### List Resources

- Get an overview of all the deployed resources, including models and endpoints.

### Interact with Models

- Utilize a simple interface to communicate with deployed models, sending queries and receiving responses.

### Cleanup Resources

- Safely remove deployed models and endpoints to manage costs and maintain a clean environment.

### Configure Cloud Credentials

- A guided setup to input and securely store credentials for your preferred cloud platforms.

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

- **Amazon Web Services (AWS) SageMaker**

Other popular cloud platforms are on our roadmap and will be supported soon. Stay tuned for updates, and don't hesitate to contribute or request support for your preferred platforms.

## Requirements

- **Python Version**: 3.10 or higher. Ensure that Python is properly installed on your system.

- **Cloud Account**: Appropriate configuration and permissions to deploy and manage models on your chosen cloud platform:
  - AWS
    - AWS IAM User Access Key
    - AWS IAM User Secret Key
    - AWS IAM User has `AmazonSageMakerFullAccess` permission policy assigned.
    - AWS IAM Role ARN
    - AWS IAM Role has `AmazonSageMakerFullAccess` permission policy assigned.

## Installation

You can install _Sych LLM Playground_ via [pip] from [PyPI]:

```console
$ pip install sych-llm-playground
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [Apache 2.0 license][license],
_Sych LLM Playground_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

[pypi]: https://pypi.org/
[file an issue]: https://github.com/sychhq/sych-llm-playground/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/sychhq/sych-llm-playground/blob/main/LICENSE
[contributor guide]: https://github.com/sychhq/sych-llm-playground/blob/main/CONTRIBUTING.md
[command-line reference]: https://sych-llm-playground.readthedocs.io/en/latest/usage.html
