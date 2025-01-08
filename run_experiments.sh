#!/bin/bash

source vars.sh

# Looping over different number of nodes (with one key)
# SIZES=(3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 24 26 28 30)
SIZES=(3 4 5)

# SECURITY=shamir
SECURITY=malicious-shamir

mkdir -p $OUTPUT_DIR/$SECURITY

setting='local'
for size in ${SIZES[@]}; do

    FILENAME=$setting'_mean_est_comp_nodes'.txt

    # echo required to parse logs
    echo num_servers=$size >>$OUTPUT_DIR/$SECURITY/$FILENAME
    IP_FILE_PREFIX=$setting'_'$size
    ./2-send_and_compile.sh mean_est_0
    ./3-run_protocol.sh mean_est_0 $IP_FILE_PREFIX $SECURITY >>$OUTPUT_DIR/$SECURITY/$FILENAME 2>&1

done

# SIZES=(3 6 10 20)
SIZES=(3)
for setting in 'ew' 'eu'; do
    for size in ${SIZES[@]}; do

        FILENAME=$setting'_mean_est_comp_nodes'.txt

        # echo required to parse logs
        echo num_servers=$size >>$OUTPUT_DIR/$SECURITY/$FILENAME
        IP_FILE_PREFIX=$setting'_'$size
        ./2-send_and_compile.sh mean_est_0
        ./3-run_protocol.sh mean_est_0 $IP_FILE_PREFIX $SECURITY >>$OUTPUT_DIR/$SECURITY/$FILENAME 2>&1

    done
done
