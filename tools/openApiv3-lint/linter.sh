#!/bin/sh


## while getops 'sf:' p
## do
##   case $p in
##     s) failonerror=true ;;
##     f) file=$OPTARG ;;
##   esac
## done

statusCode=0

if [ $# -gt 0 ]
then
  file="$1"
fi

if [ -n "$file" ]
then
  speccy lint "$file"
  statusCode=$?
else
  cat /dev/stdin > content
  speccy lint content
  statusCode=$?
  if [ $statusCode -eq 0 ] || [ $failonerror ]
  then
    cat content
  fi
  rm content
fi

exit $statusCode
