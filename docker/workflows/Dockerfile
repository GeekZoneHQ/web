FROM python:3-slim

RUN apt update && apt -y upgrade
RUN apt install -y curl jq build-essential

RUN pip install black

COPY scripts/black-on-edited-files.sh /scripts/black-on-edited-files.sh

ENTRYPOINT ["scripts/black-on-edited-files.sh"]