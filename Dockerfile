FROM python:3.8

COPY assets/check.py /opt/resource/check
COPY assets/in.py /opt/resource/in
COPY assets/out.py /opt/resource/out

RUN chmod +x /opt/resource/*