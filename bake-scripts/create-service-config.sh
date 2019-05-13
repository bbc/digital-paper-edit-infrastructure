#! /bin/bash

set -e

COMPONENT=`cat $1 | python -c 'import sys, json; print json.load(sys.stdin)["name"]'`
ENV=`cat $1 | python -c 'import sys, json; print json.load(sys.stdin)["environment"]'`
RELEASE=`cat $1 | python -c 'import sys, json; print json.load(sys.stdin)["release"]'`
CONFIGURATION=`cat $1 | python -c 'import sys, json; print json.dumps(json.dumps(json.load(sys.stdin)["configuration"]))[1:-1]'`

mkdir -p /etc/systemd/system/$COMPONENT.service.d

cat << EOF > /etc/systemd/system/$COMPONENT.service.d/environment.conf
[Service]
Environment=NODE_ENV=$ENV
Environment="NODE_CONFIG={\"version\": \"$RELEASE\", \"cosmos\": $CONFIGURATION}"
EOF
