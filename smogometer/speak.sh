#!/bin/bash

while [ 1 ];
do
    X=`socat - UNIX-CONNECT:/tmp/bmp280_socket`
    T1=`echo $X | cut -d';' -f 1`
    P=`echo $X | cut -d';' -f 2`
    X=`socat - UNIX-CONNECT:/tmp/dust_socket`
    T2=`echo $X | cut -d';' -f 1`
    H=`echo $X | cut -d';' -f 2`
    D=`echo $X | cut -d';' -f 3`
    curl --data "api_key=1T58VEP890JRNZGG&field1=$T1&field2=$P&field3=$T2&field4=$H&field5=$D" https://api.thingspeak.com/update.json
    sleep 60
done
