#!/bin/bash
# Deletes the n oldest files in the directory this script is run.
# Set it to run via cron every n minutes, like:
# */15 * * * * cd /usr/src/app/cache/test && /usr/src/app/cron/expire_cache.sh
# Make sure to run the cron daemon too!
set -eo pipefail

# Get % of used disk space
THRESHOLD_PCT=95 #%. Above this % of used diskspace, cache is expired
USED_PCT=$(df | grep /usr/src/app | awk '{print $5}' | sed 's/%$//')
if (( $USED_PCT < $THRESHOLD_PCT )); then
  echo 'No need to prune. Exiting...'
  exit #no need to prune
fi

# From: http://unix.stackexchange.com/a/29205
DELETE_LIMIT=2000 # number of oldest files deleted
echo 'Pruning older cached files...'
while IFS= read -r -d $'\0' line ; do
  file="${line#* }"
  
  echo "Deleting $file..."
  rm $file
  
  let DELETE_LIMIT-=1
  [[ $DELETE_LIMIT -le 0 ]] && break
done < <(find . -type f -maxdepth 1 -printf '%T@ %p\0' \
         2>/dev/null | sort -z -n)
