# SET BASE IMAGE OS
FROM python:3.9-alpine

# UPDATE AND INSTALL GIT
RUN apk update && apk add --no-cache git

# CLONE REPOSITORY DARI GITHUB BARU
RUN git clone \
    https://github.com/temankuya/subia \
    /home/subia && chmod -R 777 /home/subia

# SET WORKDIR
WORKDIR /home/subia

# SET GIT CONFIG (opsional, bisa dihapus kalau nggak perlu)
RUN git config --global user.name "subia"
RUN git config --global user.email "subia@e.mail"

# IGNORE PIP WARNING 
ENV PIP_ROOT_USER_ACTION=ignore

# UPDATE PIP
RUN pip install -U pip

# INSTALL REQUIREMENTS
RUN pip install -U --no-cache-dir -r requirements.txt

# COMMAND TO RUN
CMD ["python", "main.py"]
