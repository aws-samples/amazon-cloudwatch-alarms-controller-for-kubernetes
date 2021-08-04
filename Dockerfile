FROM python:3.7

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY cwoperator cwoperator

CMD kopf run --standalone -v cwoperator/operator_handler.py