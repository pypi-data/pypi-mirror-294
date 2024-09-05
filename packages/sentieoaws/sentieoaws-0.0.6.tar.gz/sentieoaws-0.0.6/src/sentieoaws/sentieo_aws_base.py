from typing import Optional

import boto3
import localstack_client.session as local_boto3
from botocore.client import Config
from botocore.exceptions import ClientError


class SentieoAWSBase:
    """
    Class to connect to the AWS service(s).

    Attributes:
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.
        local (bool): LocalService.

    """

    def __init__(
        self,
        aws_service: str,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        local: bool = False,
    ) -> None:
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.local = local
        self.aws_service = aws_service
        self.aws_client = self.get_client()
        self.aws_resource = self.get_resource()

    def get_client(self) -> boto3.client:
        """
        Get the boto3 client for the S3 service.
        Returns:
            boto3.client: The boto3 client for the AWS service.
        Raises:
            Exception: If the client could not be created.
        """
        try:
            if self.local:
                aws_client = local_boto3.client(self.aws_service)
            elif self.aws_access_key_id and self.aws_secret_access_key:
                aws_client = boto3.client(
                    self.aws_service,
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                )
            else:
                if self.aws_service == "s3":
                    aws_client = boto3.client(
                        self.aws_service, config=Config(signature_version="s3v4")
                    )
                else:
                    aws_client = boto3.client(self.aws_service)
        except ClientError as e:
            print(f"Exception occurred : {e}")
            aws_client = None
        return aws_client

    def get_resource(self) -> boto3.resource:
        """
        Get the boto3 resource for the AWS service.
        Returns:
            boto3.resource: The boto3 resource for the AWS service.
        Raises:
            Exception: If the resource could not be created.
        """
        try:
            if self.local:
                aws_resource = local_boto3.resource(self.aws_service)
            elif self.aws_access_key_id and self.aws_secret_access_key:
                aws_resource = boto3.resource(
                    self.aws_service,
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                )
            else:
                if self.aws_service == "s3":
                    aws_resource = boto3.resource(
                        self.aws_service, config=Config(signature_version="s3v4")
                    )
                else:
                    aws_resource = boto3.resource(self.aws_service)
        except ClientError as e:
            print(f"Exception occurred : {e}")
            aws_resource = None

        return aws_resource
