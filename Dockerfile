FROM centos:7

RUN yum install -y epel-release && \
    yum update -y && \
    yum install -y centos-release-openstack-rocky && \
    yum install -y openstack-dashboard

RUN yum install -y python-pip

COPY . /opt/adjutant-ui
RUN pip install -r /opt/adjutant-ui/requirements.txt && \
    pip install /opt/adjutant-ui/

RUN cp /opt/adjutant-ui/adjutant_ui/enabled/* /usr/share/openstack-dashboard/openstack_dashboard/enabled/

RUN echo "128.31.27.25    devstack" >> /etc/hosts
COPY "etc/local_settings.py" "/etc/openstack-dashboard/local_settings"

EXPOSE 80

ENTRYPOINT ["/usr/sbin/httpd", "-D", "FOREGROUND"]
