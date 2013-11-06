#!/bin/bash

# Assuming that you have the whole apertium tree in your source dir and you are in tur-tat directory.

# You have to compile apertium-tur and apertium-tat first.

cp ../../incubator/apertium-tur/tur.automorf.att.gz apertium-tur-tat.tur-tat.LR.att.gz
cp ../../incubator/apertium-tur/tur.autogen.att.gz apertium-tur-tat.tat-tur.RL.att.gz
cp ../../languages/apertium-tat/tat.automorf.att.gz apertium-tur-tat.tat-tur.LR.att.gz
cp ../../languages/apertium-tat/tat.autogen.att.gz apertium-tur-tat.tur-tat.RL.att.gz

DIFF=$(diff ../../languages/apertium-tur/apertium-tur.tur.rlx apertium-tur-tat.tur-tat.rlx)
if [ "$DIFF" != "" ]; then
        cp ../../incubator/apertium-tur/apertium-tur.tur.rlx apertium-tur-tat.tur-tat.rlx
fi;

DIFF=$(diff ../../languages/apertium-tat/apertium-tat.tat.rlx apertium-tur-tat.tat-tur.rlx)
if [ "$DIFF" != "" ]; then
        cp ../../languages/apertium-tat/apertium-tat.tat.rlx apertium-tur-tat.tat-tur.rlx
fi;

exit 0


