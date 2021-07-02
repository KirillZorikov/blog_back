FROM python:3.8.5-slim as builder

ENV WORKDIR=/usr/src/blog_django

WORKDIR ${WORKDIR}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir ${WORKDIR}/wheels -r requirements.txt

FROM python:3.8.5-slim

ENV USER blog
ENV GROUP developer
ENV HOME=/home/blog
ENV PROJECTPATH=/home/blog/blog_django
ENV BUILDERWORKDIR=/usr/src/blog_django

RUN useradd -m -d /home/${USER} ${USER}

RUN groupadd ${GROUP} \
    && usermod -aG ${GROUP} ${USER}

RUN mkdir ${PROJECTPATH}
RUN mkdir ${PROJECTPATH}/media/
RUN mkdir ${PROJECTPATH}/media/posts/

WORKDIR ${PROJECTPATH}

RUN apt-get -yqq update && apt-get install -yqq --no-install-recommends \
    libpq-dev postgresql \
    && apt-get purge -yqq --auto-remove \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder ${BUILDERWORKDIR}/wheels /wheels
COPY --from=builder ${BUILDERWORKDIR}/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . ${PROJECTPATH}

RUN chgrp developer -R ${PROJECTPATH} \
    && chmod -R 775 ${PROJECTPATH}

USER ${USER}