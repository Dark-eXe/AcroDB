<img src="https://github.com/user-attachments/assets/579013a3-4f3d-4c89-8e1e-7482dbda29cd">

# AcroDB

Chat-queried NoSQL database for gymnasts and parkour practitioners.

[![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)](https://aws.amazon.com/dynamodb/) [![Amazon S3](https://img.shields.io/badge/Amazon%20S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/) [![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/) <br>
[![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://react.dev/)

<img src="https://github.com/user-attachments/assets/c2b2d071-127e-4fc8-a959-a2ae59b65138" width="100%" height="100%">

## Flow

<img src="https://github.com/user-attachments/assets/60e1dac7-9eda-47d6-a905-bd6dcf898a52" width="48%" height="48%"> $\rightarrow$
<img src="https://github.com/user-attachments/assets/f3b377f8-28cc-41ce-8d5b-b9833304dc66" width="48%" height="48%">

## File Directory Structure

```
AcroDB
├── demo
│   ├── basic_query.ipynb
│   ├── chat_query.ipynb
│   └── chat_query.py
├── src
│   ├── AcroDB
│   │   ├── AcroDB.py
│   │   ├── ChatCache.py
│   │   ├── ChatDB.py
│   │   └── prompts
│   │       └── main.txt
│   ├── backend
│   │   ├── api
│   │   │   └── routes.py
│   │   ├── core
│   │   │   ├── cache.py
│   │   │   ├── config.py
│   │   │   └── session.py
│   │   ├── main.py
│   │   ├── models
│   │   │   └── request.py
│   │   └── services
│   │       └── query_handler.py
│   └── react-app
│       ├── package.json
│       └── src
│           ├── App.css
│           └── App.js
└── tests
    ├── conftest.py
    └── test_AcroDB.py
```
