
## Overview of the App
The app is a chat bot that utilizes various functionalities such as Kendra RAG, Generate image, and Opensearch RAG. These functionalities allow users to interact with the chat bot in different ways.
- Chat bot with Kendra RAG
- Generate image
- Chat bot with Opensearch RAG
## Config .env

To configure the app, you need to set the following environment variables in the `.env` file:

- `KENDRA_INDEX_ID`: This variable should be set to the ID of the Kendra index that you want to use for the Kendra RAG functionality.
- `AWS_PROFILE`: This variable should be set to the AWS profile that you want to use for authentication and authorization with AWS services.

Make sure to provide the appropriate values for these variables before running the app.
## Run it locally

```sh
python3 -m venv env
source .env/bin/activate
pip install -r requirements.txt
streamlit run RAG.py
```
