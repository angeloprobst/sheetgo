#!/bin/bash
. /etc/profile

CURL=$(which curl)
XDG_OPEN=$(which xdg-open)
IMAGE_PATH=$1
OUTPUT_FORMAT=$2
OUTPUT_FILE=$3

[ -z "${CURL}" ] && \
    echo "curl not found" && \
    exit 1

[ -z "${DROPBOX_ACCESS_TOKEN}" ] && \
    echo "DROPBOX_ACCESS_TOKEN env var is empty or wasn't set" && \
    exit 1

usage() {
    echo
    echo "  Usage:"
    echo
    echo "    ${0}  <image_path_on_dropbox>  <output_format>  <output_file_path>"
    echo
    echo "    Example:"
    echo "    export DROPBOX_ACCESS_TOKEN=2a406f5556f2bdeb9caf93b67522c1a3  # this is not a valid token"
    echo "    ${0}  /Photos/bali.png  jpeg  /tmp/bali.jpg"
    echo
    echo "    DROPBOX_ACCESS_TOKEN env var must be set previously."
    echo
}

[ -z "${IMAGE_PATH}" -o -z "${OUTPUT_FORMAT}" -o -z "${OUTPUT_FILE}" ] && usage && exit 1

$CURL -v -s -XPOST "http://127.0.0.1:5000/image/convert/fromdropbox?image_path=${IMAGE_PATH}&format=${OUTPUT_FORMAT}" \
    -H "Authorization: $(python generate_jwt.py)" \
    --output ${OUTPUT_FILE}

[ -n "${XDG_OPEN}" -a -e "${OUTPUT_FILE}" ] && ${XDG_OPEN} ${OUTPUT_FILE}

exit 0
