FROM docker.io/usercont/frambo

ENV NAME=zdravomil \
    RELEASE=1 \
    ARCH=x86_64 \
    SUMMARY="Dockerfile linter" \
    DESCRIPTION="Dockerfiles verifier, which uses colin (https://github.com/user-cont/colin)" \
    HOME=/home/zdravomil

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$SUMMARY" \
      io.k8s.display-name="$NAME" \
      name="$FGC/$NAME" \
      release="$RELEASE.$DISTTAG" \
      architecture="$ARCH" \
      usage="docker run -e REPO_URL=<url> $FGC/$NAME" \
      maintainer="Userspace Containerization <user-cont@redhat.com>"

COPY requirements.sh /requirements.sh

RUN cd /etc/yum.repos.d/ && \
    bash /requirements.sh && \
    dnf clean all && \
    mkdir -p ${HOME} && \
    chown root ${HOME} && \
    chgrp root ${HOME} && \
    chmod g+rwx ${HOME}

WORKDIR ${HOME}

COPY ./files/bin /bin

COPY ./ /tmp/zdravomil/
RUN cd /tmp/zdravomil/ && \
    pip3 install -r requirements.txt && \
    pip3 install .

# Random UID to make sure container doesn't run as root
USER 9513578

CMD ["run.sh"]
