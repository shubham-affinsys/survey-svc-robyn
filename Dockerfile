# FROM python:3.11-bookworm
# RUN apt-get update && apt-get install -y supervisor
# WORKDIR /workspace
# COPY . .
# RUN pip install -r requirements.txt
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# EXPOSE 8080
# CMD ["/usr/bin/supervisord"]


FROM python:3.11-bookworm
RUN apt-get update && apt-get install -y supervisor
WORKDIR /workspace    
ENV PYTHONPATH="${PYTHONPATH}:/workspace/src"    
COPY . .    
RUN pip install -r requirements.txt    
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf    
EXPOSE 8080    

ENV PROCESSES=1
ENV WORKERS=1
ENV FAST_MODE="false"
    # ENTRYPOINT ["python3", "-m", "svc"]
CMD ["python3", "-m", "src", "--log-level=INFO"]    
