import openai
import os
import streamlit as st
from  langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.documents import Document
from langchain import OpenAI
import json
import base64
import getpass

# print('Please Enter the OpenAI API key: ')
# api_key = getpass.getpass("Enter your OpenAI API key: ")
# print("OpenAI API key Initialised ")

def get_secret():
    secret_name = 'aws_managed_secret'
    region_name = 'us-east-1'

    #create a secret manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        print(get_secret_value_response)
    except Exception as e:
        raise e

    #Decrypt the secret using the associated KMS key
    secret = get_secret_value_response['SecretString']

    secret = json.loads(secret)
    return str(secret['OPENAI_API_KEY'])

api_key = get_secret()
print("OpenAI API key Initialised ", api_key)

def prediction_pipeline(text):

    print("insude prediction pipeline")
    text_splitter = CharacterTextSplitter(seperate='\n',chunk_size=1000, chunk_overlap=20)

    text_chunks = text_splitter.split_text(text)

    print(len(text_chunks))

    # llm = OpenAI(openai_api_key=api_key)
    llm = OpenAI(openai_api_key=get_secret())

    docs = [Document(page_content=t) for t in text_chunks]

    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)

    summary = chain.run(docs)

    return summary

# text = ""
# prediction_pipeline(text)
user_input = st.text_area("Enter text to summarize:")
button = st.button('Generate Summary')

if user_input and button:
    summary = prediction_pipeline(user_input)
    st.write("Summary: ", summary)
