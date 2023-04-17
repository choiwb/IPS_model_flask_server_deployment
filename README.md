# Cyber_Security_XAI_GAI_web_service

IPS & WAF Detection - attack / normal  
WEB Log Detection - SQL Injection, Command Injection, XSS, normal
-----
- Data: IPS & WAF Payload, WEB Log
- Feature create: PySpark (Spark SQL)
- Algorithm: LightGBM
- XAI: Shapley value based R&D
- Deployment: Flask & Docker
- Domain Signature pattern and AI feature highlighting after pattern method matching
- WAF & WEB LOG (APACHE or NGINX or IIS) Parsing
- WEB LOG based user-agent application, normal_bot_crawler, bad_bot_crawler classification (referenced https://user-agents.net/, https://github.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker/blob/master/_generator_lists/bad-user-agents.list)
-----
- DistilBERT Transfer Learning (adding cyber security domain word)
- DistilBERT (task: question-answering) based fine tuning like SQUAD dataset format
- DistilBART based text-summarization
- OpenAI API (gpt-3.5-turbo & gpt-4) based XAI analysis
-----
- TO DO: OpenAI GPT (https://huggingface.co/openai-gpt) based cyber security Chatbot R&D

