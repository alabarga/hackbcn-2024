import os
import sys
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage



api_key = os.environ["MISTRAL_API_KEY"]

client = MistralClient(api_key=api_key)
fine_tuned_model = 'ft:open-mistral-7b:953eb039:20240629:e98cba77'
def mistral_call(input):
    chat_response = client.chat(
    model=fine_tuned_model,
    messages=[ChatMessage(role='user', 
                          content=input
                          )
                ]
    )

    return chat_response.choices[0].message.content

input = 'SINTOMA : temperatura corporal normal| SINTOMA : colección pancreática| SINTOMA : colección pancreática| SINTOMA : trastorno de compartimiento retroperitoneal| SINTOMA : cultivo microbiológico positivo (hallazgo)| SINTOMA : balance de líquidos de drenaje - hallazgo| SINTOMA : deterioro general de la salud| SINTOMA : fiebre| SINTOMA : colección intrabdominal| SINTOMA : fiebre'
print(mistral_call(input))