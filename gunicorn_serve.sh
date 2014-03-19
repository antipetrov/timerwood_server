#!/bin/bash

PROJECTDIR=$(dirname $(readlink -f "$0"))
CONFFILE="$PROJECTDIR/config/gunicorn_serve.conf"

# Default config values

LOGDIR=$(readlink -f "$PROJECTDIR/../logs")
LOGFILE="$LOGDIR/gunicorn.log"
LOGLEVEL=debug

NUM_WORKERS=2
IP=127.0.0.1
PORT=8055
EXTRA_OPTIONS=

# Override defaults with values from config if it exists

[ -r "$CONFFILE" ] && source "$CONFFILE"


if [ ! -d "$LOGDIR" ] ; then
    mkdir -p "$LOGDIR"
fi

source "$PROJECTDIR/env/bin/activate"
export PYTHONPATH=$PYTHONPATH:"$PROJECTDIR"
cd "$PROJECTDIR/twoodapp"
exec "$PROJECTDIR/env/bin/gunicorn" -b $IP:$PORT -w $NUM_WORKERS \
    --log-level=$LOGLEVEL --log-file=$LOGFILE $EXTRA_OPTIONS 2>>$LOGFILE twoodapp:app
