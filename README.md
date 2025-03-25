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
│           └── App.js
└── tests
    ├── conftest.py
    └── test_AcroDB.py
```

## 👷‍♂️ Progress 👷‍♀️
#### Web Interface 	
[![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://react.dev/)
![Snip20250323_34](https://github.com/user-attachments/assets/1b3a4d37-ee99-4307-af37-a0c1dbfab4d6)
<br>
![Snip20250325_20](https://github.com/user-attachments/assets/15a106e3-4364-4876-8585-68c043c0f6b3)





#### Command-Line Interface
Uses ```ChatDB.loop()```
![image](https://github.com/user-attachments/assets/dcad7bb3-b835-4881-9680-c821f3d8d694)

## 🧠 Tech Stack 🤖
- AWS NoSQL Database Services with Boto3: DynamoDB, S3 \****requires AWS client permissions for access (closed to public for now)*
- OpenAI with Python SDK \****requires API key for token usage*
  
## 🗄️ Database Contents 🗄️
DynamoDB: MAG Code of Points, WAG Code of Points (to be joined), Parkour dictionary
> partition key: 'mvtId'

S3: Multimedia for movement demonstrations
> key: '<dynamodb_table>/mvtId-\<mvtId\>.\<multimedia_extension\>'

## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
