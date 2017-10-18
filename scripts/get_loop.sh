#!/bin/bash
#url=http://hello-world-demo.collectalot.org/
url=http://hello-world-demo.52.138.137.196.nip.io/
for i in {1..100000}
do
   echo -ne $i
   echo -ne ' '
   curl $url
   echo ''
   sleep 2
done

