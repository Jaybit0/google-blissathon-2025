from google import genai
from google.genai import types

from . import constants


def convert_scene_to_image_description(text=):
    client = genai.Client(
        vertexai=True,
        project=constants.GCP_PROJECT_ID,
        location="global",
    )

    si_text1 = """make an english description of an image matching this scene description. black and white, rough sketch, cartoonish style. only answer with the description. no other text."""

    model = "gemini-2.0-flash-001"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=text)],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"
            ),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        system_instruction=[types.Part.from_text(text=si_text1)],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
