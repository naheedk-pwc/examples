#!/bin/bash

echo "My input is: $my_input_param"

## use of built-in properties to get the current running agent user and password to connect to opereto host and the host URL..

curl -k -u $opereto_user:$opereto_password -X POST -d "{\"key\": \"my_output_param\", \"value\": \"$my_input_param\"}" $opereto_host/processes/$pid/output

prefix="Hello World"

if [[ $my_input_param == $prefix* ]];
then
    exit 0
else
    exit 2
fi
