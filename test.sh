#!/bin/bash

while [ 1 ];
do
    X=`socat - UNIX-CONNECT:/tmp/bmp280_socket`
    T=`echo $X | cut -d';' -f 1`
    P=`echo $X | cut -d';' -f 2`
    echo "{\"0\": \"T: $T C\", \"1\": \"P: $P hPa\"}" | socat - UNIX-CONNECT:/tmp/lcd_socket
    sleep 1
done
