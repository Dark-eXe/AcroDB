# 🤸‍♂️ AcroDB 🤸

Chat-queried NoSQL database for gymnasts and parkour practitioners.<br><br>
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
│   ├── ChatCache.py
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

## Web Interface

[![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://react.dev/)
![demo](https://github.com/user-attachments/assets/3ca1c32b-cab8-4441-a7c4-a6673c46fb1c)

## 🏛️ Ecosystem  🏛️
![Flowchart](https://github.com/user-attachments/assets/c2b2d071-127e-4fc8-a959-a2ae59b65138)

## Command-Line Interface

Uses `ChatDB.loop()`<br>
See `demo/chat_query.ipynb`
![image](https://github.com/user-attachments/assets/dcad7bb3-b835-4881-9680-c821f3d8d694)

## 🔒 Access 🔒
Frameworks/tools: Python (`requirements.txt`), [React](https://www.freecodecamp.org/news/how-to-install-react-a-step-by-step-guide/) (Node.js, npm, [Bootstrap](https://getbootstrap.com/docs/3.4/getting-started/))<br><Br>
AWS: login/signup through AWS Cognito in web browser <br>
OpenAI: enter API key in web browser<br><br>

If in admin mode and running CLI, [set up AWS CLI configuration](https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-configure.html) in terminal and paste OpenAI API key in a new directory `secrets/API_KEY` (or edit line $27$ in `demo/chat_query.py` or cell $6$ in `demo/chat_query.ipynb`).<br><br>
*Note: you still will not be able to access resources unless you are in my user pool in Cognito... or you are me, so you would need to launch the web page on localhost (run `npm start` on `src/react-app`) and sign up with Cognito... by that point, you should just use the web page since you are obviously not an admin*

## Steps
1. Install tools and ensure proper configuration from above
2. From `src/` run `uvicorn main:app --reload` to launch FastAPI server
3. From `src/react-app/` run `npm start` to launch web server
4. Go to localhost:3000 in web browser

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
