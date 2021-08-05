FROM python:3.9

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY consumer.py consumer.py

ENTRYPOINT [ "python" ]
CMD [ "consumer.py" ]