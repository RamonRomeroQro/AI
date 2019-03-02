#!/bin/bash
rm -fr ./out
mkdir ./out
python3 program.py < ./testFiles/1.txt > ./out/out1.txt
python3 program.py < ./testFiles/2.txt > ./out/out2.txt
python3 program.py < ./testFiles/3.txt > ./out/out3.txt
python3 program.py < ./testFiles/4.txt > ./out/out4.txt
python3 program.py < ./testFiles/5.txt > ./out/out5.txt

