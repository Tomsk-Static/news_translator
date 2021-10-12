FROM ubuntu:20.04
COPY new_translator ./new_translator
SHELL ["/bin/bash", "-c"] #switch sh on bash because in sh 'source' doesnt work 
RUN apt update
RUN apt install -y python3.9
RUN apt install -y python3-pip
RUN pip3 install -r ./new_translator/requirements.txt
CMD ["uvicorn", "new_translator.main:app"]
