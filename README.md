<img src="https://github.com/user-attachments/assets/0d4bf9f3-7125-490a-9790-9a68be751489">

# AcroDB

Chat-queried NoSQL database for gymnasts and parkour practitioners.

[![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)](https://aws.amazon.com/dynamodb/) [![Amazon S3](https://img.shields.io/badge/Amazon%20S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/) [![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/) <br>
[![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://react.dev/)

<img src="https://github.com/user-attachments/assets/c2b2d071-127e-4fc8-a959-a2ae59b65138" width="100%" height="100%">

## Web User Interface

<img src="https://github.com/user-attachments/assets/691c4348-1556-46c4-8984-078b21f2f9aa" width="75%" height="75%"> <br/> $\rightarrow$ <br/>
<img src="https://github.com/user-attachments/assets/7bc3b2e0-c9a7-419d-bbfa-5010a7cf2f14" width="75%" height="75%"> <br/> $\rightarrow$ <br/>
<img src="https://github.com/user-attachments/assets/7da9223b-b963-402f-9d5a-8d36c11eae8b" width="75%" height="75%">

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
│   │   │   ├── rate_limit.py
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
