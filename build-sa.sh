#!/bin/bash

j=StationAdjacent

nohup python -m macgraph.input.build \
	--gqa-paths input_data/raw/bulk/gqa-$j* \
	--name $j &> nohup-build-$j.out&
