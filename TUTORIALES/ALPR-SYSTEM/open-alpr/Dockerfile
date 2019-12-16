FROM ubuntu:16.04
RUN apt-get update && apt-get install -y \
      openalpr \
      openalpr-daemon \
      python-openalpr && \
      touch /usr/share/openalpr/is_docker

# Adjust beanstalkd to also allow remote connections
# RUN sed -i 's/BEANSTALKD_LISTEN_ADDR\s*=\s*127.0.0.1/BEANSTALKD_LISTEN_ADDR=0.0.0.0/' /etc/default/beanstalkd

# Expose the beanstalkd port and the web service
EXPOSE 11300 8355

# Allow the plate images to be persisted on the host
VOLUME /var/lib/openalpr/
VOLUME /etc/openalpr/

WORKDIR ~/

# Override script for "service" to allow alprlink to restart service
COPY daemon/service-override /bin/systemctl

# Startup script for OpenALPR services
COPY daemon/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# send over the license key and the alprd configuration
#COPY license.conf /etc/openalpr/license.conf
COPY daemon/alprd.conf /etc/openalpr/alprd.conf

# CMD ["/usr/bin/supervisord"]


# PYTHON CODE WEB SERVICE

RUN apt-get update && apt-get install -y python-pip python-openalpr

COPY webservice/src/requirements.txt /opt/openalprapi/

RUN pip install -r /opt/openalprapi/requirements.txt

# send over the license key 
#COPY license.conf /etc/openalpr/license.conf

COPY  webservice/src/webservice.py /opt/openalprapi/

EXPOSE 8080

CMD ["python", "/opt/openalprapi/webservice.py", "-p", "8080"]