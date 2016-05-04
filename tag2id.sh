tail -n +2 vec_all.txt | sort -k1 -n > ./Data/tagtest2.txt
#grep "^u" tagtest2.txt | nl| awk '{$1="u"$1; print}' > ./Data/ulist.txt
#grep "^b" tagtest2.txt | nl| awk '{$1="b"$1; print}' > ./Data/blist.txt
#grep "^s" tagtest2.txt | nl| awk '{$1="s"$1; print}' > ./Data/slist.txt
#grep "^v" tagtest2.txt | nl| awk '{$1="v"$1; print}' > ./Data/vlist.txt

grep "^u" ./Data/tagtest2.txt > ./Data/ulist.txt
grep "^b" ./Data/tagtest2.txt > ./Data/blist.txt
grep "^s" ./Data/tagtest2.txt > ./Data/slist.txt
grep "^v" ./Data/tagtest2.txt > ./Data/vlist.txt
