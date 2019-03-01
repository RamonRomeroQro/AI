#!/bin/bash
rm -fr ./out
mkdir ./out
python3 graph.py < ./testFiles/1.txt > ./out/out1.txt
python3 graph.py < ./testFiles/2.txt > ./out/out2.txt
python3 graph.py < ./testFiles/3.txt > ./out/out3.txt
python3 graph.py < ./testFiles/4.txt > ./out/out4.txt

