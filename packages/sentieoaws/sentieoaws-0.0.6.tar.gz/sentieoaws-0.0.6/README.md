# Sentieo AWS 

[![Python Version](https://img.shields.io/pypi/pyversions/sentieos3)][python version]

[![Tests](https://github.com/ShubhamBansal1997/sentieos3/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/ShubhamBansal1997/sentieos3/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]


[python version]: https://pypi.org/project/sentieos3
[tests]: https://github.com/ShubhamBansal1997/sentieos3/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/ShubhamBansal1997/sentieos3
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Installation

You can install _SentieoAWS_ via [pip] from [PyPI]:

```console
$ pip install --extra-index-url https://api.packagr.app/PLesWotlL sentieoaws==0.0.1
```
## Documentation
Sentieoaws is a wrapper around the current [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) packages for various aws services
including [S3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html), [SNS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html), [SQS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html) etc.

## Usage

### For AWS Base Client

```python
from sentieoaws.sentieo_aws_base import SentieoAWSBase
aws_client = SentieoAWSBase("s3", local=True).get_client()
aws_resouce = SentieoAWSBase("s3", local=True).get_resource()
```
### For S3
```python
from sentieoaws.s3api import SentieoS3Connection
s3_obj = SentieoS3Connection(local=True)

BUCKET_NAME = "test_bucket"
OBJECT_KEY = "test_object"

bucket = s3_obj.get_bucket(BUCKET_NAME) # returns bucket object
object = s3_obj.get_object(BUCKET_NAME, OBJECT_KEY) # returns s3 object
content, content_type = s3_obj.get_object_content(BUCKET_NAME, OBJECT_KEY) # returns content, content_type 
uploaded = s3_obj.put_object_content(BUCKET_NAME, OBJECT_KEY, "content", "content_type") # return True / False
s3_obj.upload_file(BUCKET_NAME, OBJECT_KEY, file_path, is_compress, is_public) # uploads file
s3_obj.download_file(BUCKET_NAME, OBJECT_KEY, file_path) # downloads file

```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.10+
* Create a virtual environment and install the dependencies

```sh
make poetry-download
```

* Activate the virtual environment

```sh
make env
```

### Testing

```sh
make test
```


### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---



## Contributing

Contributions are very welcome.
