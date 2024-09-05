from typing import Any, Dict, Optional, Tuple, Union

import json
import os
import pathlib
import tempfile

import boto3
import brotli
import magic
from botocore.exceptions import ClientError

from .constants import MODE_TYPE_MAP
from .sentieo_aws_base import SentieoAWSBase


class SentieoS3Connection(SentieoAWSBase):
    """
    Class to connect to the S3 service.

    Attributes:
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.
        s3_config (str): S3 Config.
        local (bool): LocalService.

    """

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        s3_config: Optional[Dict[Any, Any]] = None,
        local: bool = False,
    ) -> None:
        super(SentieoS3Connection, self).__init__(
            "s3", aws_access_key_id, aws_secret_access_key, local
        )
        self.s3_config = s3_config

    def get_bucket(self, bucket_name: str) -> boto3.resource:
        """
        Get the S3 bucket
        Args:
            bucket_name (str): The name of the bucket.
        Returns:
            boto3.resource: The boto3 s3 bucket resource.
        """
        return self.aws_resource.Bucket(bucket_name)

    def get_object(self, bucket_name: str, object_name: str) -> boto3.resource:
        """
        Get the S3 object
        Args:
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.
        Returns:
            boto3.resource: The boto3 s3 object resource.
        """
        return self.get_bucket(bucket_name).Object(object_name)

    def get_object_content(self, bucket_name: str, object_name: str) -> Tuple[str, str]:
        """
        Get the S3 object content
        Args:
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.
        Returns:
            Tuple[str, str]: The content of the object.
        Raises:
            Exception: If the object does not exist.
        """
        try:
            s3_obj = self.get_object(bucket_name, object_name)
            content = s3_obj.get().get("Body").read()
            content_type = s3_obj.get().get("ContentType")
        except Exception as e:
            content, content_type = "", ""
            print(e)
        return content, content_type

    def put_object_content(
        self,
        bucket_name: str,
        object_name: str,
        content: Union[str, Dict[Any, Any]],
        content_type: str,
    ) -> bool:
        """
        Put the S3 object content
        Args:
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.
            content (Union[str, dict]): The content of the object.
            content_type (str): The content type of the object.
        Returns:
            bool: True if the object was created.
        """
        try:
            s3_obj = self.get_object(bucket_name, object_name)
            if isinstance(content, dict):
                content = json.dumps(content)
            s3_obj.put(Body=content, ContentType=content_type)
            status = True
        except Exception as e:
            status = False
            print(e)
        return status

    def upload_file(
        self,
        bucket_name: str,
        object_name: str,
        file_path: str,
        compress: bool,
        make_public: bool = True,
        acl: str = "private",
    ) -> None:
        """
        Upload a file to S3
        Args:
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.
            file_path (str): The path to the file.
            compress (bool): Whether to compress the file.
            make_public (bool): Whether to make the file public.
        Returns:
            None
        """
        mime = magic.Magic(mime=True)
        file_type = pathlib.Path(file_path).suffix
        extra_kwargs = {"ContentType": mime.from_file(file_path)}
        extra_kwargs.update(
            {"ACL": "public-read"}
        ) if make_public else extra_kwargs.update({"ACL": acl})

        bucket = self.get_bucket(bucket_name)
        if not compress:
            bucket.upload_file(file_path, object_name, ExtraArgs=extra_kwargs)
        else:
            tmp_file = tempfile.NamedTemporaryFile(
                mode="wb", suffix=".br", delete=False
            )
            with open(file_path, "rb") as f_in:
                file_content = f_in.read()
            if "font.css" in file_path:
                mode = brotli.MODE_FONT
            else:
                mode = MODE_TYPE_MAP.get(file_type, brotli.MODE_GENERIC)
            compressed_content = brotli.compress(file_content, mode=mode)
            with open(tmp_file.name, "wb") as c_file:
                c_file.write(compressed_content)
            extra_kwargs.update({"ContentEncoding": "br"})
            bucket.upload_file(tmp_file.name, object_name, ExtraArgs=extra_kwargs)
            os.unlink(tmp_file.name)

    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> bool:
        """
        Download a file from S3
        Args:
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.
            file_path (str): The path to the file.
        Returns:
            bool: True if the file was downloaded.
        """
        try:
            path = pathlib.Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            self.get_object(bucket_name, object_name).download_file(file_path)
        except ClientError as e:
            print("AWS S3 Client Error", e)
            return False
        except FileNotFoundError as e:
            print("File Not Found", e)
            return False
        return True

    def get_pre_signed_url(
        self, bucket_name: str, object_name: str, expiration: int = 3600
    ) -> Any:
        """
        Generate a pre-signed url to share an S3 object
        Args:
            bucket_name (str): The name of the bucket
            object_name (str): The name of the object
            expiration (int): Time in seconds for the presigned URL to remain valid
        Returns:
            str: Presigned URL as string. If error, returns None.

        """
        try:
            response = self.aws_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_name},
                ExpiresIn=expiration,
            )
        except ClientError as e:
            print("Error creating the pre signed url ", e)
            return None
        return response
