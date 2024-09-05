from typing import List, Optional
import google.generativeai as genai

def init_gemini(api_key):
    genai.configure(api_key=api_key)

def get_gemini_embedding(text: str, model="models/text-embedding-004", tesk_type="", title="") -> List[float]:
    text = text.replace("\n", " ")
    response = genai.embed_content(
        model=model,
        content=[text],
        task_type=tesk_type,
        title=title
    )

    return response['embedding'][0]




def get_gemini_embeddings(
    list_of_text: List[str], model="text-embedding-3-small", tesk_type="", title=""
) -> List[List[float]]:
    assert len(list_of_text) <= 2048, "The batch size should not be larger than 2048."
    list_of_text = [text.replace("\n", " ") for text in list_of_text]

    response = genai.embed_content(
        model=model,
        content=list_of_text,
        task_type=tesk_type,
        title=title
    )
    return response['embedding']