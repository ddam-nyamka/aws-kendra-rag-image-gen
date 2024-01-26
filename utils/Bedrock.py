import boto3
import json

import dotenv
dotenv.load_dotenv()

class Bedrock:
    client =  boto3.client(service_name='bedrock-runtime')
    
    model_id = 'anthropic.claude-instant-v1'
    available_models = ['anthropic.claude-v1', 'anthropic.claude-instant-v1']
    
    def __init__(self):
        pass
    
    def answer(self, history, assistant):
        body = self.format_history(history, assistant)
        return self.client.invoke_model_with_response_stream(
            body=body,
            modelId=self.model_id,
        )
        
    def format_history(self, history, assistant):
        return json.dumps({
            "prompt": f"\n\n{history}\n\nAssistant:{assistant}",
            "max_tokens_to_sample": 3000,
            "temperature": 0.5,
            "top_p": 0.9,
        })