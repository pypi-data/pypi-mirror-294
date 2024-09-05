from typing import Any, Dict, Optional

import boto3

from .sentieo_aws_base import SentieoAWSBase


class SentieoSQSConnection(SentieoAWSBase):
    """
    Class to connect to SQS service.

    Attributes:
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.
        local (bool): LocalService.

    """

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        local: bool = False,
    ) -> None:
        super(SentieoSQSConnection, self).__init__(
            "sqs", aws_access_key_id, aws_secret_access_key, local
        )

    def get_queue(self, queue_name) -> Optional[boto3.resource]:
        """
        Get an sqs Queue
        Args:
            queue_name (str): name of the sqs queue
        Returns:
            queue_object
        """
        try:
            queue = self.aws_resource.get_queue_by_name(QueueName=queue_name)
        except Exception:
            queue = None

        return queue

    def send_message(self, queue_name, message_body) -> Dict[str, Any]:
        """
        Send a message to the specified sqs Queue
        Args:
            queue_name (str): name of the sqs queue
            message_body (str): message being sent to the queue
        Returns:
            JSON response consisting of request details & response
        """
        queue = self.get_queue(queue_name)

        return queue.send_message(MessageBody=message_body)

    def read_message(self, queue_name) -> Dict[str, Any]:
        """
        Reads a message from specified queue
        Args:
            queue_name (str): name of the sqs queue
        Returns:
            JSON response consisting of message details
        """
        queue = self.get_queue(queue_name)

        return self.aws_client.receive_message(
            QueueUrl=queue.url, MaxNumberOfMessages=1, AttributeNames=["All"]
        )

    def delete_message(self, queue_name, receipt_handle) -> Dict[str, Any]:
        """
        Deletes the specified message from specified queue
        Args:
            queue_name (str): name of the sqs queue
            receipt_handle (str): receipt_handle of the message to be deleted
        Returns:
            JSON response consisting of request & response details
        """
        queue = self.get_queue(queue_name)

        return self.aws_client.delete_message(
            QueueUrl=queue.url, ReceiptHandle=receipt_handle
        )
