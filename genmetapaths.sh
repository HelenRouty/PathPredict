# meta-paths of lengths <= 5
echo '' > meta-paths.txt
for i1 in u b s v ' '; do 
   for i2 in u b s v ' '; do
       for i3 in u b s v ' '; do
           echo "u $i1 $i2 $i3 b" >> meta-paths.txt
done;done;done

tr -u -d ' ' < meta-paths.txt |sort| uniq > meta-paths1.txt
sed -e "1d" meta-paths1.txt > meta-path.txt
rm meta-paths1.txt
