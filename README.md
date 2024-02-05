
# AWS Serverless Text to Speech Service (Python)

[![license](https://img.shields.io/github/license/ran-isenberg/aws-text-to-speech)](https://github.com/ran-isenberg/aws-text-to-speech/blob/master/LICENSE)
![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.11&color=blue?style=flat-square&logo=python)
![version](https://img.shields.io/github/v/release/ran-isenberg/aws-text-to-speech)
![github-star-badge](https://img.shields.io/github/stars/ran-isenberg/aws-text-to-speech.svg?style=social)
![issues](https://img.shields.io/github/issues/ran-isenberg/aws-text-to-speech)

![alt text](https://github.com/ran-isenberg/aws-text-to-speech/blob/main/banner.png?raw=true)

**[Blogs website](https://www.ranthebuilder.cloud)**
> **Contact details | ran.isenberg@ranthebuilder.cloud**



### **Features**

- A Serverless service that takes text files uploaded to a bucket, converts them to an MP3 and sends the output to an email address
- Uses Amazon Polly
- Python Serverless service with a recommended file structure.
- CI/CD pipelines based on Github actions with python linters, static code analysis, complexity checks and style formatters.
- Unit, integration and E2E test folders ready for implementation.

This is not a production ready code but more of an advanced POC.

I use it to convert my blog's text to audio for accessibility reasons.

It uploads any text file in the /text folder to S3, turns them into .mp3 files and sends them back to an email address.

The email address is hardcoded in the service/logic/email.py file and can be changed.

Here's a deep dive into the design: https://www.ranthebuilder.cloud/post/serverless-empowers-accessibility-convert-text-to-speech-with-amazon-polly

Important: make sure you enable SES to send emails to the email address you choose https://docs.aws.amazon.com/ses/latest/dg/creating-identities.html

### Who gave me this Idea?

I was inspired to design a solution for myself after seeing [this](https://www.youtube.com/watch?v=k-U_YJiuLGs) excellent YouTube video by Johannes Koch and Jimmy Dahlqvist.

### Design

For the service design and further information checkout my blog post [here](https://www.ranthebuilder.cloud/post/serverless-empowers-accessibility-convert-text-to-speech-with-amazon-polly).

### Architecture

![alt text](https://github.com/ran-isenberg/aws-text-to-speech/blob/main/hld.png?raw=true)

Flow of events:
- Text file is uploaded to S3
- A Lambda function is triggered with a 'create object' event.
- The Lambda function reads the text file, and uses [AWS Polly wrapper](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/polly#code-examples) to start a polly text to speech task that will save the output the origin bucket as an .mp3 file
- The Lambda function waits for the task to complete by polling the task status
- Once completed, the function downloads the file and sends it as an email attachment to an email address of your choice

### Design Considerations
1. Why do I use Lambda function? Why not a step function?

That's definitely an improvement, but this was just a quick POC to automate my personal needs and provide a code example for a blog post.

In a production code, you should use a step function state machine that waits until the task is completed.

2. Why do I send the file via email, as it is already on the bucket?

For my needs, I want to upload the mp3 file to my website and remove it from my personal AWS account. You can alter the behavior as you wish.
## Getting started
### **Prerequisites**

* **Docker** - install [Docker](https://www.docker.com/). Required for the Lambda layer packaging process.
* **[AWS CDK](cdk.md)** - Required for synth & deploying the AWS Cloudformation stack.
* Python 10
* [poetry](https://pypi.org/project/poetry/) - Make sure to run ``poetry config --local virtualenvs.in-project true`` so all dependencies are installed in the project '.venv' folder.
* For Windows based machines, use the Makefile_windows version (rename to Makefile). Default Makefile is for Mac/Linux.

### **Creating a Developer Environment**

1. Run ``make dev``
2. Run ``poetry install``

#### **Deploy CDK**

Create a cloudformation stack by running ``make deploy``.

### **Deleting the stack**

CDK destroy can be run with ``make destroy``.

### **Preparing Code for PR**

Run ``make pr``. This command will run all the required checks, pre commit hooks, linters, code formats, flake8 and tests, so you can be sure GitHub's pipeline will pass.

The command auto fixes errors in the code for you.

If there's an error in the pre-commit stage, it gets auto fixed. However, are required to run ``make pr`` again so it continues to the next stages.

Be sure to commit all the changes that ``make pr`` does for you.

### **Building dev/lambda_requirements.txt**

#### lambda_requirements.txt

CDK requires a requirements.txt in order to create a zip file with the Lambda layer dependencies. It's based on the project's poetry.lock file.

``make deploy` command will generate it automatically for you.

#### dev_requirements.txt

This file is used during GitHub CI to install all the required Python libraries without using poetry.

File contents are created out of the Pipfile.lock.

``make deploy`` ``make deps`` commands generate it automatically.

 ### ** How to turn a text file to turn into speech?

Put a text file (.txt) into the /text folder. Deploy the CDK  stack with 'make deploy' command.

It will be uploaded into an S3 bucket and turned into an mp3 file sent to you via email.

The email address is hardcoded and can be found at service/logic/email.py file.

When you add a new file: you can either upload to directly to the bucket or add them to the /text folder and run 'make deploy'.

## Code Contributions
Code contributions are welcomed. Read this [guide.](https://github.com/ran-isenberg/aws-lambda-handler-cookbook/blob/main/CONTRIBUTING.md)

## Code of Conduct
Read our code of conduct [here.](https://github.com/ran-isenberg/aws-lambda-handler-cookbook/blob/main/CODE_OF_CONDUCT.md)

## Connect
* Email: [ran.isenberg@ranthebuilder.cloud](mailto:ran.isenberg@ranthebuilder.cloud)
* Blog Website [RanTheBuilder](https://www.ranthebuilder.cloud)
* LinkedIn: [ranisenberg](https://www.linkedin.com/in/ranisenberg/)
* Twitter: [IsenbergRan](https://twitter.com/IsenbergRan)

## Credits
* [AWS Polly wrapper examples (Python)](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/polly#code-examples)

## License
This library is licensed under the MIT License. See the [LICENSE](https://github.com/ran-isenberg/aws-lambda-handler-cookbook/blob/main/LICENSE) file.
