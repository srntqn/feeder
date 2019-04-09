FROM  python:3.7
RUN pip install docker kubernetes
WORKDIR /app
COPY *.py ./
ENTRYPOINT ["python", "-u", "flow.py", "--privateRegistry"]