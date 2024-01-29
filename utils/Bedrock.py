import boto3
import json
import os

import dotenv
dotenv.load_dotenv()


class Bedrock:
    client = boto3.client(service_name='bedrock-runtime',
                          region_name=os.getenv('MODEL_REGION'))

    def answer(self, history, assistant, model_id):
        body = self.format_history(history, assistant)

        return self.client.invoke_model_with_response_stream(
            body=body,
            modelId=model_id,
        )

    def format_history(self, history, assistant):
        return json.dumps({
            "prompt": f"\n\n{history}\n\n {assistant} Assistant:",
            "max_tokens_to_sample": 3000,
            "temperature": 0.5,
            "top_p": 0.9,
        })

    def generate_image(self, model, params):
        model_params = self.createBodyImage(model, params)
        res = self.client.invoke_model(
            body=model_params,
            modelId=model,
            accept="application/json",
            contentType="application/json"
        )
        body = res['body']
        return body.readlines()

    def createBodyImage(self, model, params):
        modelConfig = self.image_controller(model)
        return modelConfig['createBodyImage'](params)

    def image_controller(self, model):
        BEDROCK_IMAGE_GEN_MODELS = {
            'stability.stable-diffusion-xl-v0': {
                'createBodyImage': self.create_body_image_stable_diffusion,
            },
            'stability.stable-diffusion-xl-v1': {
                'createBodyImage': self.create_body_image_stable_diffusion,
            },
            'amazon.titan-image-generator-v1': {
                'createBodyImage': self.create_body_image_titan_image,
            }
        }
        return BEDROCK_IMAGE_GEN_MODELS[model]

    def create_body_image_stable_diffusion(self, params):
        body = {
            'text_prompts': params['text_prompt'],
            'cfg_scale': params['cfg_scale'],
            'style_preset': params['style_preset'] or None,
            'seed': params['seed'],
            'steps': params['step'],
            'image_strength': params['image_strength']
        }
        return json.dumps(body)

    def create_body_image_titan_image(self, params):
        image_generation_config = {
            'numberOfImages': 1,
            'quality': 'standard',
            'height': 512,
            'width': 512,
            'cfgScale': params['cfg_scale'],
            'seed': params['seed'] % 214783648
        }
        body = {
            'taskType': 'TEXT_IMAGE',
            'textToImageParams': {
                'text': (
                    next(
                        (x['text'] for x in params['text_prompt']
                         if x['weight'] > 0), '') + ', ' + params['style_preset']
                ),
                'negativeText': next(
                    (x['text'] for x in params['text_prompt'] if x['weight'] < 0), '')
            },
            'imageGenerationConfig': image_generation_config
        }
        return json.dumps(body)
