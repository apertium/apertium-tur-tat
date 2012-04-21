if [ -z $TMPDIR ]; then
	TMPDIR="/tmp"
fi
bash inconsistency.sh tr-tt > $TMPDIR/testvoc.tr-tt; bash inconsistency-summary.sh $TMPDIR/testvoc.tr-tt tr-tt
bash inconsistency.sh tt-tr > $TMPDIR/testvoc.tt-tr; bash inconsistency-summary.sh $TMPDIR/testvoc.tt-tr tt-tr
