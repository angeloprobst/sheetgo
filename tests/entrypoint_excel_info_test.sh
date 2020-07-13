#!/bin/bash
. /etc/profile

CURL=$(which curl)
INPUT_FILE=$1

[ -z "${CURL}" ] && \
    echo "curl not found" && \
    exit 1

usage() {
    echo
    echo "  Usage:"
    echo
    echo "    ${0}  <input_file_path>"
    echo
    echo "    Example:"
    echo "    ${0}  sheetgo_tabs_sample.xlsx"
    echo
}

[ -z "${INPUT_FILE}" ] && usage && exit 1

$CURL -s -XPOST "http://127.0.0.1:5000/excel/info" \
    -H "Authorization: Bearer $(python generate_jwt.py)" \
    -F file=@${INPUT_FILE}

exit 0
