import base64
import json
import pandas as pd
import random
import streamlit as st
import vanna as vn
from src.train_model import Model
# from src.mistral_model import mistral_call


@st.cache_resource(ttl=3600)
def setup_connexion():
    if 'model_status' not in st.session_state:
        st.session_state.model_status = False

    if "vanna" in st.secrets:
        key =  st.secrets["vanna"]["key"]
        st.session_state.model_name = st.secrets["vanna"]["model_name"]
        print(key,st.session_state.model_name )

        # model object
        model = Model(st.session_state.model_name) 
        api_key = vn.get_api_key(key)
        vn.set_api_key(api_key)

        # model
        vn.set_model(st.session_state.model_name )
        if st.session_state.model_status == False:
            model.train()
            st.session_state.model_status = True
    else:
        raise Exception("No API key found")

title = f"💬 Reporter"
image = open("img/hackbcn24.jpeg", "rb")
contents = image.read()
data_url = base64.b64encode(contents).decode("utf-8")
image.close()

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
        <style>
            section[data-testid="stSidebar"] {
                width: 440px !important; 
            }
        </style>
        """,
    unsafe_allow_html=True,
)

def page_title(title, data_url):
    # Custom CSS style to center the title
    custom_css = """
        <style>
            .centered-title {
                text-align: center;
            }
        </style>
    """

    # Display the custom CSS
    st.sidebar.markdown(custom_css, unsafe_allow_html=True)


    custom_width = 200
    centered_image_html = f"""
        <div style="display: flex; justify-content: center; align-items: flex-start; height: {custom_width/2}px; padding-bottom: 40px;">
            <img src="data:image/png;base64,{data_url}" alt="Centered Image" width="{custom_width}"/>
        </div>
    """
    st.sidebar.markdown(centered_image_html, unsafe_allow_html=True)
    # Centered title using the custom class
    st.sidebar.markdown(f"""
    <div style='padding-top: 20px;'>
        <p style='font-size: 30px;' class='centered-title'>{title}</p>
    </div>
""",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f"<p style='font-size: 11px; color: #808080;' class='centered-title'>powered by<p>",
        unsafe_allow_html=True,
    )

def cs_sidebar():
    """
    setup_connexion()
    st.session_state.model_name = st.secrets["vanna"]["model_name"]
    model = Model(model_name=st.session_state.model_name)"""
    caption_placeholder = st.sidebar.empty()
    caption_html = """
    <div style="display: flex; justify-content: center;">
        <p style="font-size: 20px;">🚀 Mistral AI</p>
    </div>
    """

    caption_placeholder.markdown(caption_html, unsafe_allow_html=True)
    with st.sidebar.form(key='sidebar_form'):
        user_name = st.text_input("Please enter your name:")
        user_avatar = st.radio("Please choose an avatar:", ["🐶", "🐼", "👾", "⭐","🦄","🌈"], 
                                index=0,
                                horizontal=True,)
        button_pressed = st.form_submit_button(label='Start Chat')
        if button_pressed:
            st.session_state.chat_reset = True

        st.session_state.user_name = user_name
        st.session_state.user_avatar = user_avatar


        if user_name:
            st.sidebar.markdown("## Examples")
            st.sidebar.write("*Por favor, recupera el expediente médico del paciente 35*")
            st.sidebar.write("*Indica cuántos pacientes han sido diagnosticados con diabetes entre los años 2020 y 2024*")  

def handle_chat(model):
    if st.session_state.user_name:
        caption_html = f"""
        <div style="font-size: 18px; color: grey;">
            Hi {st.session_state.user_avatar} {st.session_state.user_name}! Welcome to {title}!
        </div>
    """
        st.markdown(caption_html, unsafe_allow_html=True)
        
        # Initialize the explanation status if it doesn't exist
        if "explanation_status" not in st.session_state:
            st.session_state.explanation_status = False

        # Initialize the chat messages history
        if "messages" not in st.session_state.keys(): # TODO
            # Initialize messages list with an assistant message
            st.session_state.messages = [
                {"role": "assistant", "content": "Ask me a question and I can answer you with a SQL Query!", "avatar": "🤖"}
            ]
        
        # Initialize the prompt status if it doesn't exist
        if prompt := st.chat_input("Your question"): 
            st.session_state.messages.append({"role": "user", "content": prompt, "avatar": st.session_state.user_avatar})
        
        # Display the prior chat messages
        for message in st.session_state.messages: 
            with st.chat_message(message["role"], avatar=st.session_state.user_avatar):
                st.write(message["content"])
        
        # Add training.json
        data = load_jsonl()

        if "messages" in data and len(data["messages"]) > 1:
            # If last message is not from assistant, generate a new response
            if st.session_state.messages[-1]["role"] != "assistant":
                with st.spinner("Thinking..."):
                    # ask the model
                    response = model.ask(st.session_state.messages[-1]["content"]) # SQL
                    # update the explanation status
                    st.session_state.explanation_status = True
                    # update the last message
                    st.session_state.last_message = response

                # Print the response as a new message from the assistant
                chatbot_message_response = st.chat_message("assistant", avatar="🤖")
                chatbot_message_response.code(response, language="sql", line_numbers=True)
                message =  {"role": "assistant", "content": response, "avatar": "🤖"}
                # Add response to message history
                st.session_state.messages.append(message) 
                sql_res = data["messages"][0]["content"]
                if response != "No SELECT statement could be found in the SQL code":
                    df = create_df(sql_res)
                    st.dataframe(df.head(3)) # df

                with st.form(key='user_form'):
                    query = st.form_submit_button(label='Do you want an explanation of the query?')    
                    if st.session_state.explanation_status and query:
                        with st.spinner("Thinking..."):
                            # ask the model for an explanation of the last query
                            explanation = model.explain(st.session_state.last_message)
                            st.write(explanation)
                            # print the explanation as a new message from the assistant
                            explanation_message_response = st.chat_message("assistant", avatar="🤖")
                            explanation_message_response.write(explanation)
                            # add explanation to message history
                            explanation_message = {"role": "assistant", "content": explanation}
                            st.session_state.messages.append(explanation_message)
                
                st.text_area("Report:", value=data["messages"][1]["content"])
        else:
            st.write("No messages found or insufficient data.")

def add_buttons(model, data, query, report):
    if report:
        st.text("You clicked Button 1!")
        st.text_area(" ", value=data["messages"][1]["content"])
    
    if st.session_state.explanation_status and query:
        with st.spinner("Thinking..."):
            # ask the model for an explanation of the last query
            explanation = model.explain(st.session_state.last_message)
            # print the explanation as a new message from the assistant
            explanation_message_response = st.chat_message("assistant", avatar="🤖")
            explanation_message_response.write(explanation)
            # add explanation to message history
            explanation_message = {"role": "assistant", "content": explanation}
            st.session_state.messages.append(explanation_message)

def load_jsonl():
    data = []
    with open("notebooks/training_file.jsonl", 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line.strip()))
    return random.choice(data)

def create_df(input_str):
    # Split the input string into items
    items = input_str.split('|')

    # Initialize lists to store data
    enfermedades = []
    sintomas = []
    procedimientos = []

    # Parse the items and categorize them
    for item in items:
        item = item.strip()
        if item.startswith('ENFERMEDAD'):
            enfermedades.append(item.replace('ENFERMEDAD : ', '').strip())
        elif item.startswith('SINTOMA'):
            sintomas.append(item.replace('SINTOMA : ', '').strip())
        elif item.startswith('PROCEDIMIENTO'):
            procedimientos.append(item.replace('PROCEDIMIENTO : ', '').strip())

    # Create a DataFrame with lists of different lengths
    max_length = max(len(enfermedades), len(sintomas), len(procedimientos))
    data = {
        'ENFERMEDAD': enfermedades + [None] * (max_length - len(enfermedades)),
        'SINTOMA': sintomas + [None] * (max_length - len(sintomas)),
        'PROCEDIMIENTO': procedimientos + [None] * (max_length - len(procedimientos))
    }
    return pd.DataFrame(data)

def main():
    page_title(title, data_url)
    setup_connexion()
    st.session_state.model_name = st.secrets["vanna"]["model_name"]
    model = Model(model_name=st.session_state.model_name)
    cs_sidebar()
    handle_chat(model)


if __name__ == "__main__":
    main()
    
