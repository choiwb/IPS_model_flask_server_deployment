

import pickle
import psycopg2 as pg2
import torch
import numpy as np
import scipy as sp
from transformers import AutoTokenizer
from transformers import pipeline, AutoTokenizer
import shap


SERVER_IP = 'SERVER IP'
PORT = 17171 # local


# 절대 경로
IPS_text_model_path = 'MODEL DIR !!!!!!!'
IPS_total_model_path =  'MODEL DIR !!!!!!!'

IPS_text_explainer_path = 'MODEL DIR !!!!!!!'
IPS_total_explainer_path = 'MODEL DIR !!!!!!!'

IPS_pytorch_bert_model_path = 'MODEL DIR !!!!!!!'
# IPS_pytorch_bert_explainer_path = 'MODEL DIR !!!!!!!'


IPS_text_model = pickle.load(open(IPS_text_model_path, 'rb'))
IPS_total_model = pickle.load(open(IPS_total_model_path, 'rb'))

# IPS_text_explainer = pickle.load(open(IPS_text_explainer_path, 'rb'))

# 학습데이터 경로
ips_training_data = 'TRAINING DATA DIR !!!!!'

new_sql_query = """
    
    SELECT
   
        IF(INT(RLIKE(payload, 'VCAvY2dpLWJpbi9waHA0') )>0
        OR INT(RLIKE(payload, 'L2NnaS1iaW4v') )>0
        OR INT(RLIKE(payload, 'IC9jZ2ktYmlu') )>0
        OR INT(RLIKE(payload, 'UE9TVCAvY2dpLWJpbi9waHA/') )>0
        OR INT(RLIKE(payload, 'VCAvY2dpLWJpbi9w') )>0
        OR INT(RLIKE(payload, 'ZGllKEBtZDU=') )>0
        OR INT(RLIKE(payload, 'L2FueWZvcm0yL3VwZGF0ZS9hbnlmb3JtMi5pbmk=') )>0
        OR INT(RLIKE(payload, 'Ly5iYXNoX2hpc3Rvcnk=') )>0
        OR INT(RLIKE(payload, 'L2V0Yy9wYXNzd2Q=') )>0
        OR INT(RLIKE(payload, 'QUFBQUFBQUFBQQ==') )>0
        OR INT(RLIKE(payload, 'IG1hc3NjYW4vMS4w') )>0
        OR INT(RLIKE(payload, 'd2dldA==') )>0
        OR INT(RLIKE(payload, 'MjB3YWl0Zm9yJTIwZGVsYXklMjAn') )>0
        OR INT(RLIKE(payload, 'V0FJVEZPUiBERUxBWQ==') )>0
        OR INT(RLIKE(payload, 'ZXhlYw==') )>0
        OR INT(RLIKE(payload, 'Tm9uZQ==') )>0
        OR INT(RLIKE(payload, 'OyB3Z2V0') )>0
        OR INT(RLIKE(payload, 'VXNlci1BZ2VudDogRGlyQnVzdGVy') )>0
        OR INT(RLIKE(payload, 'cGhwIGRpZShAbWQ1') )>0
        OR INT(RLIKE(payload, 'JTI4U0VMRUNUJTIw') )>0
                ,1, 0) AS ips_00001_payload_base64,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'select(.*?)from') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'select(.*?)count') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'select(.*?)distinct') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'union(.*?)select') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'select(.*?)extractvalue(.*?)xmltype') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'from(.*?)generate(.*?)series') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'from(.*?)group(.*?)by') )>0
                ,1, 0) AS ips_00001_payload_sql_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'case(.*?)when') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'then(.*?)else') )>0
                ,1, 0) AS ips_00001_payload_sql_comb_02,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'waitfor(.*?)delay') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'db(.*?)sql(.*?)server') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cast(.*?)chr') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'like(.*?)http/1.') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'upper(.*?)xmltype') )>0
                ,1, 0) AS ips_00001_payload_sql_comb_03,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'script(.*?)alert') )>0
                ,1, 0) AS ips_00001_payload_xss_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wget(.*?)ttp') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'chmod(.*?)777') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'rm(.*?)rf') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cd(.*?)tmp') )>0
                ,1, 0) AS ips_00001_payload_cmd_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'jndi(.*?)dap') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '),'jndi(.*?)dns') )>0
                ,1, 0) AS ips_00001_payload_log4j_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'etc(.*?)passwd') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)createelement') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cgi(.*?)bin') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)forms') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)location') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'fckeditor(.*?)filemanager') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'manager(.*?)html') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'current_config(.*?)passwd') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'currentsetting(.*?)htm') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'well(.*?)known') )>0
                ,1, 0) AS ips_00001_payload_word_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'bash(.*?)history') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'apache(.*?)struts') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)open') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'backup(.*?)sql') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'robots(.*?)txt') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'sqlexec(.*?)php') )>0
        OR INT(RLIKE(LOWER(payload), 'exec') )>0
        OR INT(RLIKE(LOWER(payload), 'htaccess') )>0
        OR INT(RLIKE(LOWER(payload), 'htpasswd') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cgi(.*?)cgi') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'api(.*?)ping') )>0
                ,1, 0) AS ips_00001_payload_word_comb_02,

        IF(INT(RLIKE(LOWER(payload), 'aaaaaaaaaa') )>0
        OR INT(RLIKE(LOWER(payload), 'cacacacaca') )>0
        OR INT(RLIKE(LOWER(payload), 'mozi[\\.]') )>0
        OR INT(RLIKE(LOWER(payload), 'bingbot') )>0
        OR INT(RLIKE(LOWER(payload), 'md5') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'jpg(.*?)http(.*?)1.1') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'count(.*?)cgi(.*?)http') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'this(.*?)program(.*?)can') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'sleep(.*?)sleep') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'and(.*?)sleep') )>0
        OR INT(RLIKE(LOWER(payload), 'delete'))>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'get(.*?)ping') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'msadc(.*?)dll(.*?)http') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'filename(.*?)asp') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'filename(.*?)jsp') )>0
        OR INT(RLIKE(LOWER(payload), 'powershell'))>0
        OR INT(RLIKE(LOWER(payload), '[\\.]env'))>0
                ,1, 0) AS ips_00001_payload_word_comb_03,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp(.*?)login') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp(.*?)content') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp(.*?)include') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp(.*?)config') )>0
                ,1, 0) AS ips_00001_payload_wp_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cmd(.*?)open') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'echo(.*?)shellshock') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'php(.*?)echo') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'admin(.*?)php') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'script(.*?)setup(.*?)php') )>0
        OR INT(RLIKE(LOWER(payload), 'phpinfo') )>0
        OR INT(RLIKE(LOWER(payload), 'administrator') )>0
        OR INT(RLIKE(LOWER(payload), 'phpmyadmin') )>0
        OR INT(RLIKE(LOWER(payload), 'access') )>0
        OR INT(RLIKE(LOWER(payload), 'eval') )>0
        OR INT(RLIKE(LOWER(payload), 'mdb') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wise(.*?)survey(.*?)admin') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'admin(.*?)serv(.*?)admpw') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'php(.*?)create(.*?)function') )>0
                ,1, 0) AS ips_00001_payload_word_comb_04,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)zgrab') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)nmap') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)dirbuster') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)ahrefsbot') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)baiduspider') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)mj12bot') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)petalbot') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)semrushbot') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)curl/') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)masscan') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)sqlmap') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'user-agent(.*?)urlgrabber(.*?)yum') )>0
                ,1, 0) AS ips_00001_payload_useragent_comb,
                
        (SIZE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'get(.*?)http/1.')) -1)
            + (SIZE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'post(.*?)http/1.')) -1)
        + (SIZE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'head(.*?)http/1.')) -1)
        + (SIZE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'option(.*?)http/1.')) -1)
        AS ips_00001_payload_whitelist
    FROM table
    
"""



# new_sql_query의 ips_00001_payload_base64 부터 ips_00001_payload_useragent_comb 까지 추출
# re.S의 경우, 줄바꿈 문자열 까지 매치 !!!!!!!
attack_new_sql_query = re.findall(r'ips_00001_payload_base64.*?ips_00001_payload_useragent_comb', new_sql_query, re.S)[0]
# attack_new_sql_query '\\n|\\r|\\t', ' ' 는 제거, 단 regex = False
attack_new_sql_query = attack_new_sql_query.replace('\\n|\\r|\\t', '').replace(' ', '')

# new_sql_query의 '' 안에 있는 문자열들을 추출하여 리스트 생성, 
ai_field = re.findall(r'\'(.*?)\'', attack_new_sql_query)
# ai_field에서 'remove_string' 는 제거
ai_field = [x for x in ai_field if x != '']


# attack_new_sql_query 에서 'AS' 를 기준으로 분할
attack_new_sql_query_split = attack_new_sql_query.split('AS')

sql_1 = attack_new_sql_query_split[0]
sql_2 = attack_new_sql_query_split[1]
sql_3 = attack_new_sql_query_split[2]
xss = attack_new_sql_query_split[3]
cmd = attack_new_sql_query_split[4]
log4j = attack_new_sql_query_split[5]
word_1 = attack_new_sql_query_split[6]
word_2 = attack_new_sql_query_split[7]
word_3 = attack_new_sql_query_split[8]
wp = attack_new_sql_query_split[9]
word_4 = attack_new_sql_query_split[10]
user_agent = attack_new_sql_query_split[11]

sql_1 = re.findall(r'\'(.*?)\'', sql_1)
sql_1 = [x for x in sql_1 if x != '']

sql_2 = re.findall(r'\'(.*?)\'', sql_2)
sql_2 = [x for x in sql_2 if x != '']

sql_3 = re.findall(r'\'(.*?)\'', sql_3)
sql_3 = [x for x in sql_3 if x != '']

xss = re.findall(r'\'(.*?)\'', xss)
xss = [x for x in xss if x != '']

cmd = re.findall(r'\'(.*?)\'', cmd)
cmd = [x for x in cmd if x != '']

log4j = re.findall(r'\'(.*?)\'', log4j)
log4j = [x for x in log4j if x != '']

word_1 = re.findall(r'\'(.*?)\'', word_1)
word_1 = [x for x in word_1 if x != '']

word_2 = re.findall(r'\'(.*?)\'', word_2)
word_2 = [x for x in word_2 if x != '']

word_3 = re.findall(r'\'(.*?)\'', word_3)
word_3 = [x for x in word_3 if x != '']

wp = re.findall(r'\'(.*?)\'', wp)
wp = [x for x in wp if x != '']

word_4 = re.findall(r'\'(.*?)\'', word_4)
word_4 = [x for x in word_4 if x != '']

user_agent = re.findall(r'\'(.*?)\'', user_agent)
user_agent = [x for x in user_agent if x != '']

# device = torch.device('mps')
# device = torch.device('cpu')
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

IPS_pytorch_bert_model = torch.load(IPS_pytorch_bert_model_path, map_location = device)
# IPS_pytorch_bert_explainer = torch.load(IPS_pytorch_bert_explainer_path)

model_checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

print('BERT 전이학습 모델 평가: ', IPS_pytorch_bert_model.eval())



# define a prediction function
def bert_predict(x):
    tv = torch.tensor([tokenizer.encode(v, padding='max_length', max_length=100, truncation=True) for v in x]).to(device)

    #outputs = model(tv)[0].detach().cpu().numpy()
    outputs = IPS_pytorch_bert_model(tv)[0].detach().cpu().numpy()

    scores = (np.exp(outputs).T / np.exp(outputs).sum(-1)).T
    val = sp.special.logit(scores[:,1]) # use one vs rest logit units
    # val = shap_logit(val)
    
    return val

bert_pipe = pipeline(task = "text-classification",
                model = IPS_pytorch_bert_model,
                tokenizer = tokenizer
                )

bert_pipe.device = device
bert_pipe.model.to(device)





# PostgreSQL - Payload 예측 DB 연동
conn = pg2.connect('''host = ?? 
                    dbname = ?? 
                    user = ?? 
                    password = ?? 
                    port = ??''')

