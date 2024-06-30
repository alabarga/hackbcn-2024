import streamlit as st
import vanna as vn
from train_model import Model
import time,json

SIMULATION_MODE = True



def load_json_file(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def format_conditions(conditions):
    formatted_conditions = []
    for i, condition in enumerate(conditions, 1):
        start_date = condition['condition_start_date']
        end_date = condition['condition_end_date']
        concept_name = condition['concept_name']
        formatted_conditions.append(f"{i}. {concept_name} ({start_date}, {end_date})")
    return "\n".join(formatted_conditions)

def get_easy_response(data, question, response_sql=True):
    for item in data:
        if item['question'] == question:
            if response_sql == True:
                return format_conditions(conditions=item['response_sql']) 
            else:
                return item['response_easy_language']
    return "I dont have information about this patient in the database.Please contact the hospital for more information."


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


if SIMULATION_MODE==True:
        data = load_json_file("data/response.json")
else:
        data = []

def main():
    model = ""

    col1, col2, col3 = st.columns([1,2,1])
    col2.image('img/doclingo_logo.png',  use_column_width='always',width=10)

    caption_placeholder = st.empty()

    # Initialize the user name if it doesn't exist
    if "user_name" not in st.session_state or not st.session_state.user_name:
        caption_placeholder.caption("🚀 A streamlit chatbot powered by Vanna-AI/Mistral")
        with st.form(key='user_form'):
            user_name = st.text_input("Please enter your name:")
            user_avatar = st.radio("Please choose an avatar:", ["🐼",  "🦊","🦄","🌸","⭐","🌈"], 
                                    index=0,
                                    horizontal=True,)
            submit_button = st.form_submit_button(label='Start Chat')
        if submit_button and user_name:
            st.session_state.user_name = user_name
            st.session_state.user_avatar = user_avatar
            caption_placeholder.caption(f"🚀 Hi {st.session_state.user_avatar} {st.session_state.user_name}, welcome to the chatbot powered by Vanna-AI")
            handle_chat(model=model)
    else:
        handle_chat(model=model)
    

def handle_chat(model=""):
    caption_placeholder = st.empty()
    caption_placeholder.caption(f"Hi {st.session_state.user_avatar} {st.session_state.user_name}, welcome to the Doclingo powered by Vanna-AI/Mistral")
    
    # Initialize the explanation status if it doesn't exist
    if "explanation_status" not in st.session_state:
        st.session_state.explanation_status = False

    # Initialize the chat messages history
    if "messages" not in st.session_state.keys(): 
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

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.spinner("Thinking..."):
            # ask the model
            st.session_state.question = st.session_state.messages[-1]["content"]
            time.sleep(2)
            response = get_easy_response(data, st.session_state.question, response_sql=True) 
            # update the explanation status
            st.session_state.explanation_status = True
            # update the last message
            st.session_state.last_message = response

        # Print the response as a new message from the assistant
        chatbot_message_response = st.chat_message("assistant", avatar="🤖")
        chatbot_message_response.code(response, language="sql", line_numbers=True)
        message =  {"role": "assistant", "content": response}

        # Add response to message history
        st.session_state.messages.append(message) 

    if st.session_state.explanation_status:
        if st.button('Do you want an explanation of the query?'):
            with st.spinner("Thinking..."):
                # ask the model for an explanation of the last query
                question = st.session_state.question# st.session_state.last_message
                time.sleep(6)
                explanation = response = get_easy_response(data, question, response_sql=False) #model.explain(st.session_state.last_message)
                
                # print the explanation as a new message from the assistant
                explanation_message_response = st.chat_message("assistant", avatar="🤖")
                explanation_message_response.write(explanation)

                # add explanation to message history
                explanation_message = {"role": "assistant", "content": explanation}
                st.session_state.messages.append(explanation_message)


if __name__ == "__main__":
    main()