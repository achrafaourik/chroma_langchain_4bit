###########
# BUILDER #
###########

# pull official base image
FROM python:3.7.5 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get upgrade && apt-get --assume-yes install postgresql postgresql-contrib \
    unixodbc-dev python3-psycopg2 python3-dev gcc netcat vim git-lfs

# install dependencies
RUN pip install transformers
RUN git clone https://github.com/PanQiWei/AutoGPTQ.git && pip install ./AutoGPTQ
RUN git lfs clone https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GPTQ
RUN pip -q install sentencepiece Xformers einops
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


