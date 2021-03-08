import unittest
import os
from subscriber import generate_feedback_message, lambda_handler,DENIAL_MESSAGE_LOWER, DENIAL_MESSAGE_UPPER, ALLOWANCE_MESSAGE
from unittest import TestCase


class TestSubscriber(TestCase):

    def test_generate_feedback_message_allows_message_in_case_lower_than_upper_limit(self):
        message = {
            "price": 30000000,
            "name": 'シーガルズグランドガーデン(架空)',
            "message": '適切なマンションポエムをここに入れる'
        }

        os.environ['PRICE_UPPER_LIMIT'] = '30000000'
        result = generate_feedback_message(message)

        self.assertEqual(result, ALLOWANCE_MESSAGE.format(message.get('name')))
        del os.environ['PRICE_UPPER_LIMIT']

    def test_generate_feedback_message_denies_message_in_case_more_than_upper_limit(self):
        message = {
            "price": 30000001,
            "name": 'シーガルズグランドガーデン(架空)',
            "message": '適切なマンションポエムをここに入れる'
        }

        os.environ['PRICE_UPPER_LIMIT'] = '30000000'
        result = generate_feedback_message(message)
        self.assertEqual(result,
                         DENIAL_MESSAGE_UPPER.format(message.get('name'),
                                                     message.get('price'),
                                                     os.environ.get('PRICE_UPPER_LIMIT')))
        del os.environ['PRICE_UPPER_LIMIT']

    def test_generate_feedback_message_denies_message_in_case_lower_than_lower_limit(self):
        message = {
            "price": 99999999,
            "name": 'シーガルズグランドガーデン(架空)',
            "message": '適切なマンションポエムをここに入れる'
        }
        os.environ['PRICE_LOWER_LIMIT'] = '100000000'
        result = generate_feedback_message(message)
        self.assertEqual(result,
                         DENIAL_MESSAGE_LOWER.format(message.get('name'),
                                                     message.get('price'),
                                                     os.environ.get('PRICE_LOWER_LIMIT')))
        del os.environ['PRICE_LOWER_LIMIT']

    def test_generate_feedback_message_allows_message_in_case_more_than_equal_lower_limit(self):
        message = {
            "price": 100000000,
            "name": 'シーガルズグランドガーデン(架空)',
            "message": '適切なマンションポエムをここに入れる'
        }
        os.environ['PRICE_LOWER_LIMIT'] = '100000000'
        result = generate_feedback_message(message)
        self.assertEqual(result, ALLOWANCE_MESSAGE.format(message.get('name')))

        del os.environ['PRICE_LOWER_LIMIT']

    # テスト実行の際には事前にAWSの認証情報および、バケットの名前をセットアップしておくこと
    # e.g. export FEEDBACK_UPLOAD_BUCKET=advertisement-feedback-agerag
    def test_lambda_handler(self):
        event = {
            'Records': [
                {
                    'messageId': '40886b30-b88d-496a-be40-be9417f9e9b6',
                    'receiptHandle': 'AQEBa0uGT1hacqAzfBrLKAUicFyIedg5xV5Z074uMpc4lsWfM0xSLhUteh3OvKbKk79tFHz1SjsErEyy5a8KVhpHEwnAJGJ4/B4zTIzsZr8ngFQu1QzrT0iVCWkkYIosGIQL+uk+KQ4hBceO8QXHvhy0wfWS1HeGCqqgmzcEDRfxBqxXL/5xwWjLVBN1z6/dmlVNc58VvPr5f+DtvRoPgPwo1KrwzGrmDHSB1jz5ElBpwd4QSfBPT8E+Rl7JGOk4uvPUKZpmcXoCnxwD1Sw5ZYyR8HCfA+cXPXL+2zwYbappruuTj5H9EYTawoR+4CAMti04spfAhBUOakgMOWC2NqIxVRYhkSvSJoRC/HZBx+Bspgbh3HKgqrVFJDDGyYlsVr8Cy4TQOqaWpExMwOV3CPKopCHroV8D62oAa+DCbuAB9b8=',
                    'body': '{\n  "Type" : "Notification",\n  "MessageId" : "198b74d7-8b7e-5d63-a232-2c6c64914c58",\n  "TopicArn" : "arn:aws:sns:ap-northeast-1:354384904427:advertisement-destribution-topic",\n  "Subject" : "sample-message",\n  "Message" : "{\\n  \\"price\\": 25000000,\\n   \\"name\\": \\"シーガルズグランドガーデン(架空)\\",\\n \\t\\"message\\": \\"適切なマンションポエムをここに入れる\\"  \\n}",\n  "Timestamp" : "2021-03-05T08:37:03.334Z",\n  "SignatureVersion" : "1",\n  "Signature" : "kHR94W5bP6HT8N+hM72I4VEKgev0IvtbIJUJl26JBM7EqzhuTb0P8Ba5yrZ/Bo0oyLtjPH4fpiTJ44I3CJoCG3uAsLvx+UvfHwBC+bcG3yt5YjbTbOMxSDGB4g2xCSTKg+um21fzNmCJp46F12NT15oIQy8P7T4JhxhRN3lmed1KXex3Iw/uqnHSYtTTynoAnZsnkfwCKsYU4ho0UChP1gZ8h7QqLAQXwKfoFEUgd3Ruqq30PxDTviUCKJw9k2W/xfKZZCEhPPQDQfbMSLVAt07OZ9/jJzpe3HbYg/DI87cIPyZpLqCX7YD9j+5hM1Hs8lYAXv+Cb5f6nkKhXwa7fg==",\n  "SigningCertURL" : "https://sns.ap-northeast-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",\n  "UnsubscribeURL" : "https://sns.ap-northeast-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:ap-northeast-1:354384904427:advertisement-destribution-topic:c38449ff-9a09-43cc-aa26-0dcc66f45e3d"\n}',
                    'attributes': {
                        'ApproximateReceiveCount': '2', 'SentTimestamp': '1614933423396',
                        'SenderId': 'AIDAIERWYNSNBY7YRB6SY',
                        'ApproximateFirstReceiveTimestamp': '1614933661442'
                    },
                    'messageAttributes': {},
                    'md5OfBody': '0a1f3f8f25ec8cfc77d92fec505b2704',
                    'eventSource': 'aws:sqs',
                    'eventSourceARN': 'arn:aws:sqs:ap-northeast-1:354384904427:subscriber-a-queue',
                    'awsRegion': 'ap-northeast-1'}
            ]
        }
        result = lambda_handler(event, None)
        print(result)
        self.assertEqual(200, result.get('statusCode'))


if __name__ == '__main__':
    unittest.main()