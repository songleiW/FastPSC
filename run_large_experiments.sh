#!/bin/bash

source vars.sh

# SECURITY=shamir
SECURITY=malicious-shamir

mkdir -p $OUTPUT_DIR_LARGE/$SECURITY

# Five computation nodes and different number of keys (10, 100, 1000, 10000)
size=5
for setting in 'local' 'ew' 'eu'; do
    IP_FILE_PREFIX=large_$setting'_'$size
    for keys in 1 2 3 4; do
        ./2-send_and_compile.sh mean_est_$keys
        ./3-run_protocol.sh mean_est_$keys $IP_FILE_PREFIX $SECURITY >$OUTPUT_DIR_LARGE/$SECURITY/$setting'_mean_est_keys_'$keys.txt  2>&1
    done
done


# Validation Experiments
mkdir -p $OUTPUT_DIR_INPUT_VALIDATION/$SECURITY

for setting in 'local' 'ew' 'eu'; do
    for keys in 1 2 3 4; do
        for size in 3 4 5; do
            FILENAME=$setting'_input_validation_'$keys'.txt'
            echo num_servers=$size >>$OUTPUT_DIR_INPUT_VALIDATION/$SECURITY/$FILENAME
            IP_FILE_PREFIX=large_$setting'_'$size
            ./2-send_and_compile.sh input_validation_$keys
            ./3-run_protocol.sh input_validation_$keys $IP_FILE_PREFIX $SECURITY >>$OUTPUT_DIR_INPUT_VALIDATION/$SECURITY/$FILENAME  2>&1
        done
    done
done