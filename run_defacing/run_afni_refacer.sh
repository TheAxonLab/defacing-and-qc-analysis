#!/bin/sh

docker run -u $( id -u ) -it --rm \
        -v /data/datasets/DefacingPilotData:/data:ro \
        -v /data/derivatives/defacing/DefacingPilotData/afni_refacer:/out \
        pennlinc/afni_refacer  \
        -input /data   \
        -mode_all \
        -prefix /out