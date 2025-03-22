# 🤸‍♂️ AcroDB 🤸 
Chat-queried NoSQL database for gymnastics & parkour skills using AWS DynamoDB and OpenAI.<br><br>
![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white) ![Amazon S3](https://img.shields.io/badge/Amazon%20S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white) ![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
```
AcroDB
├── demo
│   ├── basic_query.ipynb
│   ├── chat_query.ipynb
│   └── chat_query.py
├── src
│   ├── AcroDB.py
│   ├── ChatDB.py
│   └── prompts
│       └── main.txt
└── tests
    ├── conftest.py
    └── test_AcroDB.py
```

## 👷‍♂️ Progress 👷‍♀️
#### Command-Line Interface
Uses ```ChatDB.loop()```
![image](https://github.com/user-attachments/assets/dcad7bb3-b835-4881-9680-c821f3d8d694)

## 🧠 Tech Stack 🤖
- AWS NoSQL (DynamoDB, S3) with Boto3
- Python with OpenAI \****requires API key for token usage*
- *TBD*: Web UI or GUI, currently CLI
  
## 🗄️ Database Contents 🗄️
\****requires AWS client permissions for access (closed to public for now)*<br><br>
DynamoDB: MAG Code of Points, WAG Code of Points (to be joined), Parkour dictionary
> partition key: 'mvtId'

S3: Multimedia for movement demonstrations
> key: '<dynamodb_table>/mvtId-\<mvtId\>.\<multimedia_extension\>'

## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
