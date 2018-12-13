#!/bin/bash

j=StationAdjacent

nohup python -m macgraph.input.build \
	--gqa-paths input_data/raw/multistep/gqa-$j* \
	--name $j &> nohup-build-$j.out&
