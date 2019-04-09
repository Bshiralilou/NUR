#!/bin/bash

echo "Run handin excercises"

echo "Creating the plotting directory if it does not exist"
if [ ! -d "Plots" ]; then
  mkdir plots
fi

echo "Run problem one.a ..."
python3 one_a.py

echo "Run problem one.b ..."
python3 one_b.py > seedvalue.txt

echo "Run problem two.a ..."
python3 two_a.py > poisson_rands.txt

echo "Run problem two.b ..."
python3 two_b.py

echo "Run problem two.c ..."
python3 two_c.py

echo "Run problem two.d ..."
python3 two_d.py

echo "Run problem two.e ..."
python3 two_e.py

echo "Run problem two.f ..."
python3 two_f.py

echo "Run problem two.g ..."
python3 two_g.py

echo "Run problem two.h ..."
python3 two_h.py

echo "Run problem three.a ..."
python3 three_a.py

echo "Generating the pdf"

pdflatex solution.tex
bibtex solution.aux
pdflatex solution.tex
pdflatex solution.tex
