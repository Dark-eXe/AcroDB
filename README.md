# AcroDB
Chat-queried NoSQL database for gymnastics & parkour skills using AWS DynamoDB and OpenAI.
## Tech Stack
- AWS (DynamoDB, S3, Lambda *maybe*, CloudWatch *maybe*) with Boto3
- Python with openai *probably*
- *TBD*: Web UI or GUI, currently CLI
## Database Contents
Requires AWS client permissions for access (closed to public for now).<br><br>
DynamoDB: MAG Code of Points, WAG Code of Points (to be joined), Parkour dictionary (to be joined)
> partition key: 'mvtId'

S3: Multimedia for movement demonstrations
> key: '<dynamodb_table>/mvtId-\<mvtId\>.\<multimedia_extension\>'
