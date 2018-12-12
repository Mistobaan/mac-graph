#!/bin/bash

python -m macgraph.train \
	--dataset StationShortestCount \
	--max-decode-iterations 1 \
	--train-max-steps 8 \
	--tag upto_1 \
	--tag iter_1 \
	--tag mp_vanilla \
	--filter-output-class 1 \
	--filter-output-class 0 \
	--control-heads 2 \
	--disable-memory-cell \
	--disable-read-cell \
	--eval-every 60 \

