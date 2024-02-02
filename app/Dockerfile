FROM python:latest
WORKDIR /code
ADD requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
# CMD ["uvicorn", "main:app", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
