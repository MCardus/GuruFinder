FROM python:3.6-stretch

# Installing external dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Installing internal dependencies
COPY . ./gurufinder
RUN pip install gurufinder/