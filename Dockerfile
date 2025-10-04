FROM python:3.13.7
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt
RUN pip install flask
RUN pip install flask-smorest
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]