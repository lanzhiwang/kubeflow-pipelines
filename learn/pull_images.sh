#!/usr/bin/env bash

# nohup pull_images.sh > pull_images.log 2>&1 &
# docker images --format "{{.Repository}}:{{.Tag}}"

echo ${BASH_SOURCE[0]}
DIR=$(dirname "${BASH_SOURCE[0]}")

while read -r line; do
    if [[ "$line" != "#"* ]]; then
        printf '%s\n' "$line"
        printf 'docker pull m.daocloud.io/%s\n' "$line"
        docker pull m.daocloud.io/${line}
        printf 'docker tag m.daocloud.io/%s %s\n' "$line" "$line"
        docker tag m.daocloud.io/${line} ${line}
        docker rmi m.daocloud.io/${line}
        printf '%s\n' "----------------------------------------"
    fi
done < "${DIR}/images.txt"
