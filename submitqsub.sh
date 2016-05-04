for c in uu ub us uv bu bb bs bv su sb ss sv vu vb vs vv; do
    a=${c:0:1}
    b=${c:1:2}
    count=0
    for iname in ${a}lista*; do
       for jname in ${b}lista*; do
           i=${iname:6:7}
           j=${jname:6:7}
           qsub ./pbs/pbs.script.${a}${b}${count}_${i}${j}
           count=$((count+1))
       done
    done
done
