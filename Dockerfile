# FROM alpine:latest
# FROM python:alpine
# FROM python
FROM rappdw/docker-java-python:latest
# FROM ubuntu:latest

WORKDIR /usr/src/app

# RUN apt-get update -y && apt-get install -y python3-pip python-dev && apt-get clean
# RUN apt-get update -y

# ENV DEBIAN_FRONTEND=noninteractive 
# RUN apt-get install -y default-jre

#Upgrade pip
# RUN pip3 install --upgrade pip

# RUN pip3 install --no-cache-dir torch

#Install python modules and don't cache install files to save space
RUN pip3 install --no-cache-dir flask flask_cors numpy spacy nltk language-tool-python sentence-transformers torch==1.8.1+cpu --find-links https://download.pytorch.org/whl/torch_stable.html

COPY requirements.txt ./ 

RUN pip3 install --no-cache-dir -r requirements.txt --find-links https://download.pytorch.org/whl/torch_stable.html

#Copy the application to the working directory
COPY . ./

RUN python3 -m nltk.downloader stopwords && python3 -m nltk.downloader punkt  && \
  python3 -m nltk.downloader wordnet

RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('bert-base-nli-mean-tokens')"

RUN python3 -c "import language_tool_python; language_tool_python.LanguageTool('en-US')"

# RUN python3 -m spacy download en_core_web_sm

#Start the website
CMD [ "bash", "runserver.sh"]