FROM python:3.7

COPY ./main.py /lab_scripts/

RUN pip install boto3 && pip install awscli

CMD [ "python", "./lab_scripts/main.py" ]
