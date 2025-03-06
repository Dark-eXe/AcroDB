# AcroDB
Chat-queried NoSQL database for gymnastics & parkour elements using AWS DynamoDB and OpenAI.
## Tech Stack
- AWS (DynamoDB, S3, Lambda *maybe*, CloudWatch *maybe*) with Boto3
- Python with openai *probably*
- *TBD*: Web UI or GUI, currently CLI
## Database Contents
Requires AWS client permissions for access (closed to public for now).
- DynamoDB ('mvtId' partition key): MAG Code of Points, WAG Code of Points (to be joined), Parkour dictionary (to be joined)
- S3 ('<dynamodb_table>/mvtId-<mvtId>' key): Multimedia for movement demonstrations
