FROM python:3.8
        EXPOSE 8501
        WORKDIR /01_query_model.py
        COPY requirements.txt ./requirements.txt
        RUN pip3 install -r requirements.txt
        COPY . .
        CMD streamlit run 01_query_model.py
        