
import os
import re
import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import Html2TextTransformer
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.document_loaders import AsyncHtmlLoader
from langchain.chains import create_extraction_chain
from langchain.chains import LLMChain, RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
import time
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain.retrievers import ContextualCompressionRetriever


template = """You are a cyber security analyst. about user question, answering specifically in korean.
            Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer. 
            For questions, related to Mitre Att&ck, in the case of the relationship between Tactics ID and T-ID (Techniques ID), please find T-ID (Techniques ID) based on Tactics ID.
            Tactics ID's like start 'TA' before 4 number.
            T-ID (Techniques ID) like start 'T' before 4 number.
            Tactics ID is a major category of T-ID (Techniques ID), and has an n to n relationship.
            Respond don't know to questions not related to cyber security.
            Use three sentences maximum and keep the answer as concise as possible. 
            {context}
            question: {question}
            answer: """


QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template)

# (회사) 유료 API 키!!!!!!!!
# 20230904_AIR	
os.environ['OPENAI_API_KEY'] = "YOUR OPENAI API KEY !!!!!!!"

callbacks = [StreamingStdOutCallbackHandler()]

scraping_llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0, max_tokens=8192,
                  callbacks=callbacks, streaming=True)

# chat_llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0, max_tokens=512,
#                   callbacks=callbacks, streaming=True)
chat_llm = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=0, max_tokens=512,
                  callbacks=callbacks, streaming=True)

tactics_url = "https://attack.mitre.org/tactics/enterprise/"

ta0001_url = "https://attack.mitre.org/tactics/TA0001/"
ta0002_url = "https://attack.mitre.org/tactics/TA0002/"
ta0003_url = "https://attack.mitre.org/tactics/TA0003/"
ta0004_url = "https://attack.mitre.org/tactics/TA0004/"
ta0005_url = "https://attack.mitre.org/tactics/TA0005/"
ta0006_url = "https://attack.mitre.org/tactics/TA0006/"
ta0007_url = "https://attack.mitre.org/tactics/TA0007/"
ta0008_url = "https://attack.mitre.org/tactics/TA0008/"
ta0009_url = "https://attack.mitre.org/tactics/TA0009/"
ta0010_url = "https://attack.mitre.org/tactics/TA0010/"
ta0011_url = "https://attack.mitre.org/tactics/TA0011/"
ta0040_url = "https://attack.mitre.org/tactics/TA0040/"
ta0042_url = "https://attack.mitre.org/tactics/TA0042/"
ta0043_url = "https://attack.mitre.org/tactics/TA0043/"

# Function Calling
# web scraping 진행 시, 결과에 대한 검증 방법 연구 필요해 보임 !!!!!!!!!!!!!!
tactics_schema = {
    "properties": {
        "tactics_id": {"type": "string"},
        "tactics_name": {"type": "string"},
        "tactics_description": {"type": "string"}
    },
    "required": ["tactics_id", "tactics_name", "tactics_description"],
}

specific_tactics_schema = {
    "properties": {
        "tactics_name": {"type": "string"},
        "techniques_id": {"type": "string"},
        "techniques_name": {"type": "string"},
        "techniques_description": {"type": "string"}
    },
    "required": ["tactics_name", "techniques_id", "techniques_name", "techniques_description"],
}

def extract(content: str, schema: dict):
    extracted_content = create_extraction_chain(schema=schema, llm=scraping_llm).run(content)
    return extracted_content


text_splitter = CharacterTextSplitter(        
    # 표기준의 경우 '|' 기준 split, 그대신 tactics id가 제대로 분할 안됨 !!!!!!!!
    separator = "\|\n",
    chunk_size = 30000, 
    chunk_overlap  = 0,
    length_function = len,
    is_separator_regex=True
)
'''현재 지속적인 api 요청이 아닌 1번만 취합 후 요청하는 형태라 잘려서 DB에 저장됨 !!!!!!!!!!!
예) TA0005의 경우, T-ID가 42개라 특정 T-ID만 호출되어 저장 됨.'''

# 임베딩 벡터 DB 저장 & 호출
db_save_path = "DB SAVE PATH !!!!!!!"

html2text = Html2TextTransformer()

# OpenAI VS HuggingFace
embeddings = OpenAIEmbeddings()

def web_scraping_faiss_save(url0, *urls):
    
    loader = AsyncHtmlLoader(url0)
    docs = loader.load()

    docs = html2text.transform_documents(docs)  
    docs = text_splitter.split_documents(docs)

    extracted_content = extract(
            schema=tactics_schema, content=docs[0].page_content
        )
    
    total_content = extracted_content
    
    for url in urls:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        loader = AsyncHtmlLoader(url)
        docs = loader.load()
        docs = html2text.transform_documents(docs)  
        docs = text_splitter.split_documents(docs)

        extracted_content = extract(
            schema=specific_tactics_schema, content=docs[0].page_content
        )
        print(extracted_content)
        total_content += extracted_content
    
    # # Convert list of dictionaries to strings
    total_content = [str(item) for item in total_content]
                    
    # docsearch = FAISS.from_documents(total_content, embeddings)
    docsearch = FAISS.from_texts(total_content, embeddings)

    docsearch.embedding_function
    docsearch.save_local(os.path.join(db_save_path, "mitre_attack_20231005_index"))


# start = time.time()
# total_content = web_scraping_faiss_save(tactics_url, ta0001_url, ta0002_url, ta0003_url, ta0004_url, ta0005_url, ta0006_url,
#                                         ta0007_url, ta0008_url, ta0009_url, ta0010_url, ta0011_url, ta0040_url, ta0042_url, ta0043_url
#                                         )
# end = time.time()
# print('임베딩 완료 시간: %.2f (초)' %(end-start))


new_docsearch = FAISS.load_local(os.path.join(db_save_path, 'mitre_attack_20231005_index'), embeddings)

retriever = new_docsearch.as_retriever(search_type="similarity", search_kwargs={"k":5})

# 유사도 0.7 이상만 추출
embeddings_filter = EmbeddingsFilter(embeddings = embeddings, similarity_threshold = 0.7)

# 압축 검색기 생성
compression_retriever = ContextualCompressionRetriever(base_compressor = embeddings_filter,
                                                        base_retriever = retriever)


retrieval_qa_chain = RetrievalQA.from_chain_type(chat_llm,
                                        retriever=compression_retriever, 
                                        return_source_documents=True,
                                        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
                                        chain_type='stuff'
                                        )
# qa_llmchain = LLMChain(llm=chat_llm, prompt=QA_CHAIN_PROMPT)

conversation_history = []

def query_chain(question):
    
    # 질문을 대화 기록에 추가
    conversation_history.append(("latest question: ", question))

    # 대화 맥락 형식화: 가장 최근의 대화만 latest question, latest answer로 나머지는 priorr question, prior answer로 표시
    if len(conversation_history) == 1:
        # print('대화 시작 !!!!!!!')
        formatted_conversation_history = f"latest question: {question}"
    else:
        formatted_conversation_history = "\n".join([f"prior answer: {text}" if sender == "latest answer: " else f"prior question: {text}" for sender, text in conversation_history])
        
        # formatted_conversation_history의 마지막 prior question은 아래 코드 에서 정의한 latest question과 동일하므로 일단 제거 필요
        lines = formatted_conversation_history.split('\n')
        if lines[-1].startswith("prior question:"):
            lines.pop()
        formatted_conversation_history = '\n'.join(lines)
        
        formatted_conversation_history += f"\nlatest question: {question}"
    # print('전체 대화 맥락 기반 질문: ', formatted_conversation_history)

    result = retrieval_qa_chain({"query": formatted_conversation_history}) 
    
    print('답변에 대한 참조 문서')
    # print(source_documents)
    # for i in range(len(result['source_documents'])):
    #     print('!!!!!!!!!!!!!!!!!!!!!!')
    #     print(result['source_documents'][i].page_content)
    #     docs_and_scores = new_docsearch.similarity_search_with_score(formatted_conversation_history)
    #     '''
    #     IndexError: list index out of range
    #     '''
    #     print('유사도 점수: ', docs_and_scores[i][1])
    
    ###############################################################################################################
    
    docs_and_scores = new_docsearch.similarity_search_with_score(formatted_conversation_history, k=1, fetch_k=5)
    for doc, score in docs_and_scores:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(f"Content: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")
    

    # result = qa_llmchain({"context": source_documents, "question": formatted_conversation_history})
    # 답변을 대화 기록에 추가 => 추 후, AIR 적용 시, DB 화 필요 함!!!!!
    conversation_history.append(("latest answer: ", result["result"]))
    # conversation_history.append(("latest answer: ", result["text"]))

    return result["result"]
    # return result["text"]



def generate_text(history):
    generated_history = history.copy()

    stop_re = re.compile(r'(question:)', re.MULTILINE)
 
    # respomse는 최신 답변만 해당 !!!!!!!!!
    response = query_chain(generated_history[-1][0])  # Assuming the user message is the last one in history    
    
    if re.findall(stop_re, response):
        response = ''.join(response.split('\n')[0])

    history[-1][1] = ""
    for character in response:
        generated_history[-1][1] += str(character)
        time.sleep(0.03)
        yield generated_history

            
with gr.Blocks(title= 'IGLOO AiR ChatBot', css="#chatbot .overflow-y-auto{height:5000px} footer {visibility: hidden;}") as gradio_interface:

    with gr.Row():
        gr.HTML(
        """<div style="text-align: center; max-width: 2000px; margin: 0 auto; max-height: 5000px; overflow-y: hidden;">
            <div>
                <h1>IGLOO AiR ChatBot</h1>
            </div>
        </div>"""

        )

    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot()
            # msg = gr.Textbox(value="SQL Injection 공격에 대응하는 방법을 알려주세요.", placeholder="질문을 입력해주세요.")
            msg = gr.Textbox(value="Mitre Att&ck에 대해서 설명해주세요.", placeholder="질문을 입력해주세요.")

            with gr.Row():
                clear = gr.Button("Clear")



    def user(user_message, history):
        # user_message 에 \n, \r, \t, "가 있는 경우, ' ' 처리
        user_message = user_message.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('"', ' ')

        return "", history + [[user_message, None]]
    
    def fix_history(history):
        update_history = False
        for i, (user, bot) in enumerate(history):
            if bot is None:
                update_history = True
                history[i][1] = "_silence_"
        if update_history:
            chatbot.update(history) 

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=True).then(
        # generate_text 함수의 경우, 대화의 history 를 나타냄.
        generate_text, inputs=[
            chatbot
        ], outputs=[chatbot],
    ).then(fix_history, chatbot)

    clear.click(lambda: None, None, chatbot, queue=True)

gradio_interface.queue().launch(debug=True, server_name="127.0.0.1", share=True)
