from typing import Dict, Union
import uuid
import boto3
import os
import json


DENIAL_MESSAGE_UPPER = """ご連絡ありがとうございます。
申し訳ないのですが、ご連絡頂いた商品({})の価格({}円)では、
当方の予算({}円)を超過しております。
できれば今後は当方の要件にあった情報をお渡しいただきたく思います。
"""

DENIAL_MESSAGE_LOWER = """ご連絡ありがとうございます。
ご連絡頂いた商品({})の価格({}円)では、
当方の希望する価格({}円以上)よりも安価に過ぎます。
もっと付加価値の伴ったものを提案いただきたく考えています。
"""

ALLOWANCE_MESSAGE = """ご連絡ありがとうございます。
ご連絡頂いた商品({})ですが、
当方の希望する価格とマッチしており、
より詳細な話をお聞きしたく考えています。
"""


def lambda_handler(event: dict, context):
    s3 = boto3.resource('s3')
    feedback_upload_bucket = os.environ.get("FEEDBACK_UPLOAD_BUCKET")
    records = event.get('Records')
    for record in records:
        try:
            body = json.loads(record.get('body'))
            message = json.loads(body.get('Message'))
        except Exception as e:
            print(e)
            exit(1)

        try:
            result = generate_feedback_message(message)
            obj = s3.Object(feedback_upload_bucket, str(uuid.uuid4()))
            obj.put(Body=json.dumps(message, ensure_ascii=False))
        except Exception as e:
            print(e)
            exit(1)

    return {
        'statusCode': 200
    }


def generate_feedback_message(message: Dict[str, Union[int, str]]) -> str:
    v = os.environ.get("PRICE_UPPER_LIMIT")
    price_upper_limit = int(v) if v is not None else None
    v = os.environ.get("PRICE_LOWER_LIMIT")
    price_lower_limit = int(v) if v is not None else None

    price = int(message.get('price'))
    name = message.get('name')

    if price_upper_limit is not None and price > price_upper_limit:
        return DENIAL_MESSAGE_UPPER.format(name, price, price_upper_limit)

    if price_lower_limit is not None and price < price_lower_limit:
        return DENIAL_MESSAGE_LOWER.format(name, price, price_lower_limit)

    return ALLOWANCE_MESSAGE.format(name)


if __name__ == '__main__':
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

    lambda_handler(event, None)
