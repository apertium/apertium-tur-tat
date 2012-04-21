#!/bin/bash

if [ -z $TMPDIR ]; then
	TMPDIR="/tmp"
fi

if [[ $1 = "tr-tt" ]]; then

hfst-fst2strings ../.deps/tr.LR-debug.hfst | sort -u |  sed 's/:/%/g' | cut -f1 -d'%' |  sed 's/^/^/g' | sed 's/$/$ ^.<sent>$/g' | tee $TMPDIR/tmp_testvoc1.txt |
        apertium-pretransfer|
        lt-proc -b ../tr-tt.autobil.bin |
        apertium-transfer -b ../apertium-tr-tt.tr-tt.t1x  ../tr-tt.t1x.bin  |
        apertium-interchunk ../apertium-tr-tt.tr-tt.t2x  ../tr-tt.t2x.bin  |
        apertium-postchunk ../apertium-tr-tt.tr-tt.t3x  ../tr-tt.t3x.bin  | tee $TMPDIR/tmp_testvoc2.txt |
        hfst-proc -d ../tr-tt.autogen.hfst > $TMPDIR/tmp_testvoc3.txt
paste -d _ $TMPDIR/tmp_testvoc1.txt $TMPDIR/tmp_testvoc2.txt $TMPDIR/tmp_testvoc3.txt | sed 's/\^.<sent>\$//g' | sed 's/_/   --------->  /g'

elif [[ $1 = "tt-tr" ]]; then

hfst-fst2strings ../.deps/tt.LR-debug.hfst | sort -u | sed 's/:/%/g' | cut -f1 -d'%' |  sed 's/^/^/g' | sed 's/$/$ ^.<sent>$/g' | tee $TMPDIR/tmp_testvoc1.txt |
        apertium-pretransfer|
        lt-proc -b ../tt-tr.autobil.bin | 
        apertium-transfer -b ../apertium-tr-tt.tt-tr.t1x  ../tt-tr.t1x.bin |
        apertium-interchunk ../apertium-tr-tt.tt-tr.t2x  ../tt-tr.t2x.bin |
        apertium-postchunk ../apertium-tr-tt.tt-tr.t3x  ../tt-tr.t3x.bin | tee $TMPDIR/tmp_testvoc2.txt |
        hfst-proc -d ../tt-tr.autogen.hfst > $TMPDIR/tmp_testvoc3.txt
paste -d _ $TMPDIR/tmp_testvoc1.txt $TMPDIR/tmp_testvoc2.txt $TMPDIR/tmp_testvoc3.txt | sed 's/\^.<sent>\$//g' | sed 's/_/   --------->  /g'


else
	echo "sh inconsistency.sh <direction>";
fi
