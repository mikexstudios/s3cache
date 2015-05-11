#!/bin/bash
set -eo pipefail

for i in {1..1000}
do
    RANDOM_MINUTE=$(python -S -c "import random; print '%02i' % random.randrange(0,59)")
    touch -t011119$RANDOM_MINUTE $i
    echo "Creating $i with minute $RANDOM_MINUTE..."
done
