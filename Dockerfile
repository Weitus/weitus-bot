FROM python:3.9.15
WORKDIR /rasa

ADD . ./

RUN pip3 install -U pip
RUN pip3 install rasa
RUN rasa train


EXPOSE 5005

CMD ["rasa", "run", "--enable-api", "--cors", "\"*\""]
