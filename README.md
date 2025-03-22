# 🤸‍♂️ AcroDB 🤸 
Chat-queried NoSQL database for gymnastics & parkour skills using AWS and OpenAI.<br><br>
[![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)](https://aws.amazon.com/dynamodb/) [![Amazon S3](https://img.shields.io/badge/Amazon%20S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/) [![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
```
AcroDB
├── demo
│   ├── basic_query.ipynb
│   ├── chat_query.ipynb
│   └── chat_query.py
├── src
│   ├── AcroDB.py
│   ├── ChatDB.py
│   ├── main.py
│   ├── prompts
│   │   └── main.txt
│   └── react-app
│       ├── package.json
│       └── src
│           ├── App.css
│           ├── App.js
└── tests
    ├── conftest.py
    └── test_AcroDB.py
```

## 👷‍♂️ Progress 👷‍♀️
#### Web Interface 
![Snip20250322_4](https://github.com/user-attachments/assets/213a9827-9245-4c49-afa5-b70631d6e132)

#### Command-Line Interface
Uses ```ChatDB.loop()```
![image](https://github.com/user-attachments/assets/dcad7bb3-b835-4881-9680-c821f3d8d694)

## 🧠 Tech Stack 🤖
- AWS NoSQL Database Services with Boto3: DynamoDB, S3 \****requires AWS client permissions for access (closed to public for now)*
- OpenAI with Python SDK \****requires API key for token usage*
- Web UI: React 
  
## 🗄️ Database Contents 🗄️
DynamoDB: MAG Code of Points, WAG Code of Points (to be joined), Parkour dictionary
> partition key: 'mvtId'

S3: Multimedia for movement demonstrations
> key: '<dynamodb_table>/mvtId-\<mvtId\>.\<multimedia_extension\>'

## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
