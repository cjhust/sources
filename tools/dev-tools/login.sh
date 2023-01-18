HOSTLIST='/tmp/host.txt'
NUM=$1


cat > $HOSTLIST << EOF
dev                             direct   1.1.1.1              22      chenjie
sh-k8s-master-01                jump     root@2.2.2.2         22      root
qd-hd-22(testenv)               dev      root@3.3.3.3         22      chenjie
EOF


LINECOUNT=`wc -l $HOSTLIST | awk '{print $1}'`
[ $# -ne 0  ] || { echo 'Choose the host number:'; awk '{ printf "%-2s  %-30s %-20s %-20s %-10s %-10s\n", NR, $1, $2, $3, $4, $5 }' $HOSTLIST; read NUM;  }
[ $NUM -le $LINECOUNT  ] || { echo "Your input number is invalid!"; exit;  }


mode=`awk -v num=$NUM 'NR== num {print $2}' $HOSTLIST`
host=`awk -v num=$NUM 'NR== num {print $3}' $HOSTLIST`
port=`awk -v num=$NUM 'NR== num {print $4}' $HOSTLIST`
user=`awk -v num=$NUM 'NR== num {print $5}' $HOSTLIST`
rm -rf $HOSTLIST


if [[ $mode == "direct" ]]
then
    cmd="$user@$host -p $port"
elif [[ $mode == "jump" ]]
then
    cmd="-J $user@10.10.10.10 $host"
else
    cmd="-J $user@20.20.20.20 $host"
fi

echo $cmd
ssh $cmd