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
  oval validate "$file"
  statusCode=$?
else
  cat /dev/stdin > content
  oval validate content
  statusCode=$?
  if [ $statusCode -eq 0 ] || [ $failonerror ]
  then
    cat content
  fi
  rm content
fi

exit $statusCode
