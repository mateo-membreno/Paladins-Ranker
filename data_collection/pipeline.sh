#!/bin/bash

set -Eeuo pipefail

# Optional input directory argument
PIPELINE_INPUT=urls.txt

# Print commands
set -x

rm -rf output

madoop \
  -input ${PIPELINE_INPUT} \
  -output output \
  -mapper ./map.py \
  -reducer ./reduce.py


