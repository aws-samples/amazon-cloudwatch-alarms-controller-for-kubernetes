FROM python:3.9

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY producer.py producer.py

ENTRYPOINT [ "python" ]
CMD [ "producer.py" ]