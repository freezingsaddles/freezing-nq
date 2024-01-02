# BUILD
# =====

FROM ubuntu:22.04 as buildstep
LABEL maintainer="Richard Bullington-McGuire <richard@obscure.org>"

RUN apt-get update

RUN apt-get install -y software-properties-common
RUN apt-get update

RUN apt-get install -y python3 python3-dev python3-pip curl build-essential git

RUN mkdir -p /build/wheels

RUN pip3 install --upgrade pip setuptools wheel

ADD requirements.txt /tmp/requirements.txt
RUN pip3 wheel -r /tmp/requirements.txt --wheel-dir=/build/wheels

ADD . /app
WORKDIR /app

RUN python3 setup.py bdist_wheel -d /build/wheels


# DEPLOY
# =====

FROM ubuntu:22.04 as deploystep
LABEL maintainer="Richard Bullington-McGuire <richard@obscure.org>"

RUN apt-get update \
  && apt-get install -y software-properties-common curl \
  && apt-get update \
  && apt-get install -y python3 python3-pip vim-tiny --no-install-recommends \
  && apt-get clean \
  && pip3 install --upgrade pip setuptools wheel \
  && rm -rf /var/lib/apt/lists/*

COPY --from=buildstep /build/wheels /tmp/wheels

RUN pip3 install /tmp/wheels/*

EXPOSE 8000

ENTRYPOINT gunicorn --bind 0.0.0.0:8000 'freezing.nq.app:make_app()'
