#!/bin/bash
for i in {1..100000}
do
   echo -ne $i
   echo -ne ' '
   curl http://hello-world-demo.collectalot.org/
   echo ''
   sleep 1
done

