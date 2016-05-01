# add prefix to each cell in a column. change $1 to the column number. change "u" to prefix
# input_file > output_file
awk '{$1="u"$1; print}' movie2.csv > movie1.csv
