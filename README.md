# 🤸‍♂️ AcroDB 🤸 
Chat-queried NoSQL database for gymnastics & parkour skills using AWS DynamoDB and OpenAI. [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## 🧠 Tech Stack 🤖
- AWS NoSQL (DynamoDB, S3) with Boto3
- Python with OpenAI
- *TBD*: Web UI or GUI, currently CLI
## 🗄️ Database Contents 🗄️
Requires AWS client permissions for access (closed to public for now).<br><br>
DynamoDB: MAG Code of Points, WAG Code of Points (to be joined), Parkour dictionary
> partition key: 'mvtId'

S3: Multimedia for movement demonstrations
> key: '<dynamodb_table>/mvtId-\<mvtId\>.\<multimedia_extension\>'

## 👷‍♂️ Progress 👷‍♀️
#### Command-Line Interface
Uses ```ChatDB.loop()```
![image](https://github.com/user-attachments/assets/dcad7bb3-b835-4881-9680-c821f3d8d694)
