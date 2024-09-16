
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import PyPDF2
import re
import requests
import os

def get_summary(data,is_concatenated_summary=False):
    llm = CTransformers(model='llama-2-7b-chat.Q2_K.gguf',
                        model_type='llama',
                        config={'max_new_tokens': 512,
                                'temperature': 0.01})
    
    if is_concatenated_summary:

        template = """ 
         [INST] <<SYS>>Please merge the following phrases into a coherent and concise paragraph,
         minimize word count while preserving key information :<</SYS>>
        {data} [/INST]. """

    else:

        template =""" [INST] <<SYS>>Write a concise summary of the following, 
        return your responses with only 1 phrase that cover the key points of the following:<</SYS>>
        {data} [/INST]"""

    prompt = PromptTemplate(input_variables=["data"],template=template)

    response = llm(prompt.format(data=data))

    return response


    
    
#extracting text from pdf 
    
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            full_page_text = re.sub(r'\s{2,}', ' ', page.extract_text())
            text += full_page_text
    return text



#spliting the pdf text in mini text that can be manipulated by the model 
def split_text(text):
    mini_texts = []
    start_index = 0
    while start_index < len(text):
        end_index = min(start_index + 1125, len(text))
        if end_index == len(text):
            mini_texts.append(text[start_index:].strip())
            break
        last_period = text.rfind('.', start_index, end_index)
        if last_period == -1:
            mini_texts.append(text[start_index:end_index].strip())
            start_index = end_index
        else:
            mini_texts.append(text[start_index:last_period + 1].strip())
            start_index = last_period + 1
    return mini_texts




def text_into_mini_summary(text):

    mini_texts = split_text(text)
    mini_summaries = []
    
    for mini_text in mini_texts:
        mini_summary = get_summary(mini_text,is_concatenated_summary=False)
        mini_summaries.append(mini_summary)

    concatenated_mini_summary = ' '.join(mini_summaries)
       
    # Check if concatenated mini summary exceeded 512 tokens (512 tokens = 1125 word)
    if len(concatenated_mini_summary) > 1125:
        # Recursively summarize until within token limit
        return text_into_mini_summary(concatenated_mini_summary)
    else: 
        return concatenated_mini_summary
    





def get_pdf(url):

    text=extract_text_from_pdf(url)

    concatenated_mini_summary=text_into_mini_summary(text)
    
    result = get_summary(concatenated_mini_summary,is_concatenated_summary=True)

    return result
    
