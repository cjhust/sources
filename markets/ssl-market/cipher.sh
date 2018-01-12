#!/bin/bash


SERVER=www.alipay.com:443
ciphers=$(openssl ciphers 'ALL:eNULL' | sed -e 's/:/ /g')


echo "Version: " $(openssl version)
echo "Server : " $SERVER
echo "Command:  echo -n | openssl s_client -connect ${SERVER} -cipher xxx"


for cipher in ${ciphers[@]}
do
result=$(echo -n | openssl s_client -connect $SERVER -cipher "$cipher" 2>&1)
if [[ "$result" =~ "Cipher is ${cipher}" || "$result" =~ "Cipher    :" ]] ; then  
    echo -e "\033[32m [YES]: \033[0m" $cipher
fi
done

