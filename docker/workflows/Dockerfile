FROM python:3-slim

RUN apt update && apt -y upgrade
RUN apt install -y curl jq build-essential

RUN pip install black

COPY scripts/run_black_on_git_diff_adds.sh /scripts/run_black_on_git_diff_adds.sh

ENTRYPOINT ["scripts/run_black_on_git_diff_adds.sh"]