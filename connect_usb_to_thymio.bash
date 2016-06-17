#!/bin/bash
killall asebamedulla >& /dev/null
rm -f /tmp/aseba.log ; touch /tmp/aseba.log
asebamedulla ser:name=Thymio-II &> /tmp/aseba.log &
tail -f /tmp/aseba.log
