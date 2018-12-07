#!/bin/bash

python -m macgraph.train \
	--dataset StationShortestCount \
	--max-decode-iterations 3 \
	--train-max-steps 50 \
	--tag no_read \
	--tag small \
	--tag upto_3 \
	--tag iter_3 \
	--filter-output-class 0 \
	--filter-output-class 1 \
	--filter-output-class 2 \
	--filter-output-class 3 \
	--disable-read-cell \
	--control-heads 2 \
	--memory-width 8 \
	--eval-every 180 \

# python -m macgraph.train \
# 	--dataset StationShortestCount \
# 	--max-decode-iterations 3 \
# 	--train-max-steps 50 \
# 	--tag no_read_node \
# 	--tag no_mp \
# 	--tag upto_3 \
# 	--tag iter_3 \
# 	--filter-output-class 0 \
# 	--filter-output-class 1 \
# 	--filter-output-class 2 \
# 	--filter-output-class 3 \
# 	--disable-kb-node \
# 	--disable-message-passing \
# 	--learning-rate 1.96e-3 \


# python -m macgraph.train \
# 	--dataset StationShortestCount \
# 	--max-decode-iterations 3 \
# 	--train-max-steps 50 \
# 	--tag lr_finder \
# 	--tag no_read_node \
# 	--tag no_mp \
# 	--tag upto_3 \
# 	--tag iter_3 \
# 	--filter-output-class 0 \
# 	--filter-output-class 1 \
# 	--filter-output-class 2 \
# 	--filter-output-class 3 \
# 	--disable-kb-node \
# 	--disable-message-passing \
# 	--enable-lr-finder 


# python -m macgraph.train \
# 	--dataset StationShortestCount \
# 	--max-decode-iterations 3 \
# 	--train-max-steps 50 \
# 	--tag no_read \
# 	--tag no_mp \
# 	--tag upto_3 \
# 	--tag iter_3 \
# 	--filter-output-class 0 \
# 	--filter-output-class 1 \
# 	--filter-output-class 2 \
# 	--filter-output-class 3 \
# 	--disable-read-cell \
# 	--disable-message-passing \
# 	