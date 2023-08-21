import gradio as gr
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
import re


os.environ["OPENAI_API_KEY"] = "YOUR OPENAI API KEY !!!!!!!"
    
doc_reader = PdfReader('SAMPLE PDF PATH !!!!!!!')

template = """You are a cyber security analyst. about user question, answering specifically in korean.
            Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer. 
            Use three sentences maximum and keep the answer as concise as possible. 
            {context}
            question: {question}
            answer: """
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template)

#PDF에서 텍스트를 읽어서 raw_text변수에 저장
raw_text = ''

for i, page in enumerate(doc_reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text


#임베딩을 위해 문서를 작은 chunk로 분리해서 texts라는 변수에 나누어서 저장, chunk_overlap은 앞 chunk의 뒤에서 200까지 내용을 다시 읽어와서 저장, 즉 새 text는 800이고 200은 앞의 내용이 들어가게 됨, 숫자 바꿔서 문서에 따라 변경
text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)

texts = text_splitter.split_text(raw_text)

embeddings = OpenAIEmbeddings()

################################################################################
# 임베딩 벡터 DB 저장 & 호출
db_save_path = "DB SAVE PATH !!!!!!!"

# docsearch = FAISS.from_texts(texts, embeddings)
# docsearch.embedding_function
# docsearch.save_local(os.path.join(db_save_path, "cmd_injection_index"))

new_docsearch = FAISS.load_local(os.path.join(db_save_path, 'cmd_injection_index'), embeddings)
retriever = new_docsearch.as_retriever(search_type="similarity", search_kwargs={"k":4})
################################################################################

conversation_history = []
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7, max_tokens=512)

def query_chain(question):
    
    # 질문을 대화 기록에 추가
    conversation_history.append(("latest question: ", question))

    # 대화 맥락 형식화: 가장 최근의 대화만 latest question, latest answer로 나머지는 priorr question, prior answer로 표시
    if len(conversation_history) == 1:
        print('대화 시작 !!!!!!!')
        formatted_conversation_history = f"latest question: {question}"
    else:
        formatted_conversation_history = "\n".join([f"prior answer: {text}" if sender == "latest answer: " else f"prior question: {text}" for sender, text in conversation_history])
        
        # formatted_conversation_history의 마지막 prior question은 아래 코드 에서 정의한 latest question과 동일하므로 일단 제거 필요
        lines = formatted_conversation_history.split('\n')
        if lines[-1].startswith("prior question:"):
            lines.pop()
        formatted_conversation_history = '\n'.join(lines)
        
        formatted_conversation_history += f"\nlatest question: {question}"
    print('전체 대화 맥락 기반 질문: ', formatted_conversation_history)

    qa_chain = RetrievalQA.from_chain_type(llm,
                                          retriever=retriever, 
                                          return_source_documents=True,
                                          chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
                                           )

    result = qa_chain({"query": formatted_conversation_history})
    
    # 답변을 대화 기록에 추가
    conversation_history.append(("latest answer: ", result["result"]))

    return result["result"]



def generate_text(history):
    generated_history = history.copy()

    def callback_func(reply):
        nonlocal generated_history
        
        stop_re = re.compile(r'^(latest question|latest answer|prior question|prior answer):', re.MULTILINE)
        
        if re.search(stop_re, reply):
            reply = ''.join(reply.split('\n')[:-1])
            generated_history[-1][1] = reply.strip()
            return generated_history
        
        generated_history[-1][1] = reply.strip()
        return generated_history
 
    # respomse는 최신 답변만 해당 !!!!!!!!!
    response = query_chain(generated_history[-1][0])  # Assuming the user message is the last one in history    
    
    # Call the callback function with the bot response
    generated_history = callback_func(response)

    return generated_history


            
with gr.Blocks(css="#chatbot .overflow-y-auto{height:5000px} footer {visibility: hidden;}") as gradio_interface:

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
            msg = gr.Textbox(value="SQL Injection 공격에 대응하는 방법을 알려주세요.", placeholder="질문을 입력해주세요.")

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

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        # generate_text 함수의 경우, 대화의 history 를 나타냄.
        generate_text, inputs=[
            chatbot
        ], outputs=[chatbot],
    ).then(fix_history, chatbot)

    clear.click(lambda: None, None, chatbot, queue=False)



# gradio_interface.launch()
gradio_interface.launch(debug=True, server_name="127.0.0.1", share=True, enable_queue=True)
