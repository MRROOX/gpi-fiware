FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
      openalpr \
      openalpr-daemon \
      openalpr-utils \
      libopenalpr-dev \
      python3-pip \
      python3-openalpr && \
      touch /usr/share/openalpr/is_docker

# # Override script for "service" to allow alprlink to restart service
# COPY webservice/daemon/service-override /bin/systemctl

# # Startup script for OpenALPR services
# COPY webservice/daemon/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# # send over the license key and the alprd configuration

# COPY webservice/daemon/alprd.conf /etc/openalpr/alprd.conf

# PYTHON CODE WEB SERVICE

COPY webservice/requirements.txt /opt/openalprapi/

RUN pip3 install -r /opt/openalprapi/requirements.txt

RUN cp -r /usr/share/openalpr/runtime_data/ocr/tessdata/* /usr/share/openalpr/runtime_data/ocr/

# COPY  webservice/webservice.py /opt/openalprapi/


# EXPOSE 8080

# CMD ["python3", "/opt/openalprapi/webservice.py", "-p", "8080"]