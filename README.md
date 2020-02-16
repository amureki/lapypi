# lapypi

"Serverless" PyPI (Python Package Index) served via AWS Lambda.

## Installation

```bash
$ pip install -r requirements.txt
```

## Usage

1. Deploy Lambda via [Chalice](https://github.com/aws/chalice)

```bash
$ chalice deploy

Creating deployment package.
Creating IAM role: lapypi-dev-api_handler
Creating lambda function: lapypi-dev
Updating rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:{REGION}:{ACCOUNT_ID}:function:lapypi-dev
  - Rest API URL: {LAMBDA_API_URL}
```

2. Upload package to your S3 bucket. This step will be automated later.
3. Set your Lambda domain as a main or extra index (in requirements.txt):

```
--index-url {LAMBDA_API_URL}
// or if you still want to use https://pypi.org/
--extra-index-url {LAMBDA_API_URL}

my-own-package
```

4. Download the package

```bash
$ pip install -r requirements.txt

Looking in indexes: {LAMBDA_API_URL}
Collecting my-own-package
...
Installing collected packages: my-own-package
Successfully installed my-own-package-1.0.0
```

## Development

```bash
$ pip install -r requirements.txt
$ chalice local

Found credentials in shared credentials file: ~/.aws/credentials
Serving on http://127.0.0.1:8000
```

## Features (what already works)
1. AWS Lambda that (almost fully) complies with [PEP 503](https://www.python.org/dev/peps/pep-0503/)
2. S3 as storage allows to install packages via pip

## TODO

1. Handle package uploads
2. How to cache?
3. Authentication layer
