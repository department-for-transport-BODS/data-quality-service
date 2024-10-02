import boto3

class SESHelper:
    def __init__(self, source_email, recipient_email):
        self.client = boto3.client("ses", region_name="eu-west-2")
        self.source_email = source_email
        self.recipient_email = recipient_email

    def send_email(self, subject, body):
        try:
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [self.recipient_email]
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': body,
                        }
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': subject,
                    },
                },
                Source=self.source_email
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")
