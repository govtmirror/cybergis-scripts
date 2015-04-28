#!/bin/bash
#This script is a work in development and is not stable.
#This script requires curl and git to be installed
#Run this script using root's login shell under: sudo su -

DATE=$(date)

INIT_CMD=$1

#==================================#

provision_volume(){
  echo "format_volume"
  if [[ $# -ne 3 ]]; then
    echo "Usage: cybergis-script-ec2.sh provision_volume <device> <mount_point>"
  else
    INIT_CMD=$1
    DEVICE=$2
    MOUNT=$3
    #
    sudo mkfs -t ext4 $DEVICE
    CMD1="echo '$DEVICE	$MOUNT	auto	defaults,nobootwait	0	2' >> /etc/fstab"
    sudo bash --login -c "$CMD1"
    sudo mount -a
  fi
}
add_swap(){
  echo "add_swap"
  if [[ $# -ne 3 ]]; then
    echo "Usage: cybergis-script-ec2.sh swap <size> <file>"
  else
    INIT_CMD=$1
    SIZE=$2
    FILE=$3
    #
    fallocate -l $SIZE $FILE
    if (($? = 0)); then
      chmod 600 $FILE
      mkswap $FILE
      swapon $FILE
    else
      echo "facllocate failed"
    fi
  fi
}
delete_swap(){
  echo "delete_swap"
  if [[ $# -ne 2 ]]; then
    echo "Usage: cybergis-script-ec2.sh delete_swap <file>"
  else
    INIT_CMD=$1
    FILE=$2
    #
    swapoff $FILE
    rm $FILE
  fi
}

resize_volume(){
  echo "resize_volume"
  if [[ $# -ne 2 ]]; then
    echo "Usage: cybergis-script-ec2.sh resize <dev>"
  else
    INIT_CMD=$1
    DEVICE=$2
    #
    e2fsck -f $DEVICE
    resize2fs $DEVICE
  fi
}

if [[ "$INIT_CMD" == "provision_volume" ]]; then
        
    if [[ $# -ne 3 ]]; then
        echo "Usage: cybergis-script-ec2.sh $INIT_CMD <device> <mount_point>"
    else
        export -f provision_volume
        bash --login -c "provision_volume $INIT_CMD '${2}' '${3}'"
    fi

elif [[ "$INIT_CMD" == "resize" ]]; then

    if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-ec2.sh $INIT_CMD <device>"
    else
        export -f resize_volume
        bash --login -c "resize_volume $INIT_CMD '${2}'"
    fi

elif [[ "$INIT_CMD" == "swap" ]]; then
    
    if [[ $# -ne 3 ]]; then
        echo "Usage: cybergis-script-ec2.sh $INIT_CMD <size> <file>"
    else
        export -f add_swap
        bash --login -c "add_swap $INIT_CMD '${2}' '${3}'"
    fi
    
elif [[ "$INIT_CMD" == "delete_swap" ]]; then
    
    if [[ $# -ne 2 ]]; then
        echo "Usage: cybergis-script-ec2.sh $INIT_CMD <file>"
    else
        export -f delete_swap
        bash --login -c "delete_swap $INIT_CMD '${2}'"
    fi
    
else
    echo "Usage: cybergis-script-ec2.sh [provision_volume|resize|swap|delete_swap]"
fi
