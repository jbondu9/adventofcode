#!/bin/bash

set -e

source env/bin/activate

day_number=$(date +%d)

if [[ $day_number =~ ^0 ]]; then
    day_number=${day_number:1:2}
fi

filename="challenges/day_${day_number}.py"

python $filename

deactivate
