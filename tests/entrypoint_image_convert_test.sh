#!/bin/bash
. /etc/profile

CURL=$(which curl)
XDG_OPEN=$(which xdg-open)
INPUT_FILE=$1
OUTPUT_FORMAT=$2
OUTPUT_FILE=$3

[ -z "${CURL}" ] && \
    echo "curl not found" && \
    exit 1

usage() {
    echo
    echo "  Usage:"
    echo
    echo "    ${0}  <input_file_path>  <output_format>  <output_file_path>"
    echo
    echo "    Example:"
    echo "    ${0}  tests/street-lights.jpg  png  /tmp/street-lights.png"
    echo
}

[ -z "${INPUT_FILE}" -o -z "${OUTPUT_FORMAT}" -o -z "${OUTPUT_FILE}" ] && usage && exit 1

$CURL -v -s -XPOST "http://127.0.0.1:5000/image/convert?format=${OUTPUT_FORMAT}" \
    -H "Authorization: $(python generate_jwt.py)" \
    -F file=@${INPUT_FILE} \
    --output ${OUTPUT_FILE}

[ -n "${XDG_OPEN}" -a -e "${OUTPUT_FILE}" ] && ${XDG_OPEN} ${OUTPUT_FILE}

exit 0
