FROM python:3.7

RUN pip install pymongo

COPY assets/check.py /opt/resource/check
COPY assets/in.py /opt/resource/in
COPY assets/out.py /opt/resource/out
COPY assets/common.py /opt/resource/common.py

RUN chmod +x /opt/resource/*