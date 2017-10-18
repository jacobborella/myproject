#!/bin/bash
url=http://hello-world-demo.collectalot.org/
#url=http://hello-world-ansibledemo.40.113.10.216.nip.io/
for i in {1..100000}
do
   echo -ne $i
   echo -ne ' '
   curl $url
   echo ''
   sleep 2
done

