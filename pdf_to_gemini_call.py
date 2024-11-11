# %%
import requests
from pdf_parsing_with_image_section import StructuredDocument
import cv2
import google.generativeai as genai
import os
from uuid import uuid4

genai.configure(api_key=os.environ["GEMINI_KEY"])

# %%
doc = StructuredDocument("1706.03762.pdf")

# %%
if not os.path.exists("tmp_data"):
    os.makedirs("tmp_data")

def prompt_generation(doc, query):
    images = []
    myfiles = []

    for page in doc.cropped_images.values():
       for i in page:
          filename = str(uuid4()) + ".png"
          cv2.imwrite(os.path.join("tmp_data", filename), i)
          myfiles.append(genai.upload_file(f"tmp_data/{filename}"))
          images.append(filename)

    texts = doc.markdown_text.split('<!-- image -->')
    prompt = []
    for i, text in enumerate(texts[:-1]):
        prompt.append(text)
        prompt.append("\n\n")
        prompt.append(myfiles[i])
        prompt.append("\n\n")
    prompt.append(texts[-1])
    prompt.append(query)

    for file in images:
        os.remove(f"tmp_data/{file}")
    return prompt

model = genai.GenerativeModel("gemini-1.5-flash")
result = model.generate_content(
    prompt_generation(
        doc,
        "Explain the figure 1 from the paper in detail write mermaid script that displays similar flowchart to the one showed in this figure"
    ),
    generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=["x"],
        max_output_tokens=1000,
        temperature=0.5,
    )
)
print(f"{result.text}")
