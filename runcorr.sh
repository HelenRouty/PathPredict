for i in ulist.txt blist.txt slist.txt vlist.txt; do  
     for j in ulist.txt blist.txt slist.txt vlist.txt; do  
          ./pearson $i $j 
     done
done
