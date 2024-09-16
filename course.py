from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

## Function To get response from LLAma 2 model

def get_course(input_text):
    
    ### LLama2 model
    llm=CTransformers(model='llama-2-7b-chat.Q2_K.gguf',
                      model_type='llama',
                      config={'max_new_tokens':512,
                              'temperature':0.01})
    
   ## Prompt Template

    template="""
    [INST] 
    <<SYS>>Generate a deep explication of the following:<</SYS>>
    {input_text} [/INST]
            """
    prompt=PromptTemplate(input_variables=["input_text"],
                          template=template)
    
    ## Generate the ressponse from the LLama 2 model
    response=llm(prompt.format(input_text=input_text))
    print(response)
    return response







