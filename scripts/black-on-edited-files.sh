#!/bin/bash
if [[ -z ${GITHUB_TOKEN} ]]
then
    echo "must define the environment variable GITHUB_TOKEN, try: 'GITHUB_TOKEN : \$\{\{ secrets.GITHUB_TOKEN \}\}' in your workflow's main.yml"
    exit 1
fi

github_pr_url=$(jq '.pull_request.url' "${GITHUB_EVENT_PATH}")
github_pr_url=$(sed -e 's/^"//' -e 's/"$//' <<<"$github_pr_url")
echo "looking for changes at ${github_pr_url}"
curl --request GET --url "${github_pr_url}" --header "authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github.v3.diff" > github_diff.txt
git_diff_length=$(wc -l github_diff.txt)
echo "size of changes: ${git_diff_length}"
python_files=$(cat github_diff.txt | grep -E -- "\+\+\+ |\-\-\- " | awk '{print $2}' | grep -Po -- "(?<=[ab]/).+\.py$")
echo "Files changed = ${python_files}"

black --check "${python_files}"