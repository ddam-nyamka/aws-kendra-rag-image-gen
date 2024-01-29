## App Overview

The simple app is a chat bot that incorporates two main functionalities: Kendra RAG and Generate Image with Bedrock (Stable Diffusion, Titan Image Generator).

### Kendra RAG

The chat bot utilizes Kendra RAG, which stands for Retrieval-Augmented Generation.

### Generate Image

The app also includes a feature to generate images. It uses the Bedrock model, specifically the Stable Diffusion and Titan Image Generator. This functionality allows users to generate images based on specific inputs or prompts.

## Configuring the App

To configure the app, you need to set the following environment variables in the `.env` file:

- `KENDRA_INDEX_ID`: This variable should be set to the ID of the Kendra index that you want to use for the Kendra RAG functionality. To create an index on the AWS Kendra service, please refer to the documentation [here](https://docs.aws.amazon.com/kendra/latest/dg/create-index.html).
- `MODEL_REGION`: This variable allows you to select the AWS Bedrock available region. For example: us-west-2.
- `AWS_PROFILE`: This variable should be set to the AWS profile that you want to use for authentication and authorization with AWS services.

Make sure to provide the appropriate values for these variables before running the app.

## Running the App Locally

To run the app locally, follow these steps:

1. Create a virtual environment:

```sh
python3 -m venv env
```

2. Activate the virtual environment:

```sh
source .env/bin/activate
```

3. Install the required dependencies:

```sh
pip install -r requirements.txt
```

4. Run the app:

```sh
streamlit run RAG.py
```

## Screenshots

Here are some screenshots of the app in action:
![Generate Image](docs/image-screenshot.png)

![RAG Chat with Kendra](docs/rag-screenshot.png)
