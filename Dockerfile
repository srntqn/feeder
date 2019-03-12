FROM  python:3.7
RUN pip install docker kubernetes
WORKDIR /app
COPY *.py ./
#COPY static ./static
ENTRYPOINT ["python", "flow.py"]