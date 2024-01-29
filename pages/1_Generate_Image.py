import json
import base64
from PIL import Image
from io import BytesIO
import streamlit as st
from utils.Bedrock import Bedrock
import random

bedrock = Bedrock()

st.title('Generate image')
st.subheader("Powered by Amazon Bedrock")

col1, col2 = st.columns(2)

images = []


def base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image


with col1:
    with st.form("image_generate_form"):
        model_id = st.selectbox(
            'Image Generation Models',
            (
                'stability.stable-diffusion-xl-v0',
                'stability.stable-diffusion-xl-v1',
                'amazon.titan-image-generator-v1'
            )
        )

        style_preset = st.selectbox(
            'Styles',
            (
                None,
                '3d-model',
                'analog-film',
                'anime',
                'cinematic',
                'comic-book',
                'digital-art',
                'enhance',
                'fantasy-art',
                'isometric',
                'line-art',
                'low-poly',
                'modeling-compound',
                'neon-punk',
                'origami',
                'photographic',
                'pixel-art',
                'tile-texture'
            )
        )

        seed = st.slider('Seed', 0, 4294967295, 0)
        image_number = st.slider('Number of Image', 0, 7, 0) or 1
        cfg_scale = st.slider('CFG Scale', 0, 30, 0)
        step = st.slider('Step', 0, 150, 0)
        image_strength = st.slider('Image Strength', 0.0, 1.0, 0.0)

        prompt = st.text_input(
            "Prompt",
            label_visibility="visible",
            placeholder="Prompt",
        )
        negative_prompt = st.text_input(
            "Negative Prompt",
            label_visibility="visible",
            placeholder="Negative Prompt",
        )
        submitted = st.form_submit_button("Generate", type="primary")

        if submitted:
            for i in range(image_number):
                image_form = {
                    "style_preset": style_preset or '',
                    "seed": int(random.random() * 4294967295),
                    "step": int(step) or 50,
                    "cfg_scale": int(cfg_scale) or 7,
                    "image_strength": float(image_strength) or 0.35,
                    "text_prompt": [
                        {
                            "text": prompt or '',
                            "weight": 1
                        }, {
                            "text": negative_prompt or '',
                            "weight": -1
                        }
                    ],
                }
                image = bedrock.generate_image(model_id, image_form)
                images.append(image)
                print("Generating...", len(images))
with col2:
    for i in images:
        for j in i:
            tmp = json.loads(j)
            if model_id == "amazon.titan-image-generator-v1":
                for artifact in tmp["images"]:
                    try:
                        image = base64_to_image(artifact)
                        st.image(image, use_column_width=True)
                    except Exception as e:
                        st.error(
                            "Error converting base64 to image: {}".format(str(e)))
            else:
                for artifact in tmp["artifacts"]:
                    try:
                        image = base64_to_image(artifact['base64'])
                        st.image(image, use_column_width=True)
                    except Exception as e:
                        st.error(
                            "Error converting base64 to image: {}".format(str(e)))
