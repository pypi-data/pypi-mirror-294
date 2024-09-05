from typing import Any, Dict, List, Optional

from .sentieo_aws_base import SentieoAWSBase


class SentieoSNSConnection(SentieoAWSBase):
    """
    Class to connect to SNS service.

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
        super(SentieoSNSConnection, self).__init__(
            "sns", aws_access_key_id, aws_secret_access_key, local
        )

    def get_all_topics(self) -> List[str]:
        """
        Get all SNS topics
        Args:
            None
        Returns:
            returns a list of all topic names
        """
        resp = self.aws_client.list_topics()

        return [topic["TopicArn"] for topic in resp["Topics"]]

    def get_topic_arn(self, topic_name) -> Optional[str]:
        """
        Get the topic ARN
        Args:
            topic_name (str): name of the sns topic
        Returns:
            ARN of the topic
        """
        if "arn:aws:sns" in topic_name:
            return topic_name

        for topic in self.get_all_topics():
            if topic_name in topic:
                return topic

        return None

    def create_topic(self, topic_name) -> Dict[str, Any]:
        """
        Creates an SNS topic
        Args:
            topic_name (str): name of the sns topic
        Returns:
            JSON response consisting of created topic details
        """
        return self.aws_client.create_topic(Name=topic_name)

    def publish(self, msg, topic_name) -> Dict[str, Any]:
        """
        Publishes a message to the specified sns topic
        Args:
            topic_name (str): name of the sns topic to which msg is being published
            msg (str): message which is being published to the specified sns topic
        Returns:
            JSON response consisting of published message details
        """
        topic_arn = self.get_topic_arn(topic_name)

        return self.aws_client.publish(Message=msg, TopicArn=topic_arn)

    def subscribe(self, topic_name, protocol, endpoint) -> Dict[str, Any]:
        """
        Subscribes to the specified topic, with the desired protocol & endpoint
        Args:
            topic_name (str): name of the sns topic which is being subscribed to
            protocol (str): email, phone etc
            endpoint (str): email value, phone number etc
        Returns:
            JSON response consisting of subscription details
        """
        topic_arn = self.get_topic_arn(topic_name)

        return self.aws_client.subscribe(
            TopicArn=topic_arn, Protocol=protocol, Endpoint=endpoint
        )

    def subscribe_sqs_queue(self, topic_name, endpoint) -> Dict[str, Any]:
        """
        Subscribes an sqs queue to topic_name
        Args:
            topic_name (str): name of the sns topic which is being subscribed to
            endpoint (str): ARN or URL of the sqs queue
        Returns:
            JSON response consiting of subscription details
        """
        topic_arn = self.get_topic_arn(topic_name)

        return self.subscribe(topic_arn, "sqs", endpoint)
