for c in uu ub us uv bu bb bs bv su sb ss sv vu vb vs vv; do
    a=${c:0:1}
    b=${c:1:2}
    count=0
    for iname in ${a}lista*; do
       for jname in ${b}lista*; do
           i=${iname:6:7}
           j=${jname:6:7}
          echo "#!/bin/bash
#PBS -l nodes=1:ppn=1,walltime=47:00:00
#PBS -M helen.youshan@gmail.com
./pearson ${iname} ${jname} ./Data/${a}${b}/${a}${b}${count}_${i}${j}.txt" > ./pbs/pbs.script.${a}${b}${count}_${i}${j}
          #echo "pearson ${iname} ${jname} ./Data/${a}${b}/${a}${b}${count}_${i}${j}.txt"
          count=$((count+1))
       done
    done
done
