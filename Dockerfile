FROM python:3.9
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
