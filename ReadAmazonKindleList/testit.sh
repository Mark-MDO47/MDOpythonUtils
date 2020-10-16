echo " (1) example without approximate author match (default)" > tmp.txt
echo " " >> tmp.txt
python ReadAmazonKindleList.py exampleKindleList.txt example_KindleBooks_Favorites.xlsx >> tmp.txt
echo " " >> tmp.txt
echo " " >> tmp.txt
echo " " >> tmp.txt
echo " " >> tmp.txt
echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" >> tmp.txt
echo " " >> tmp.txt
echo " " >> tmp.txt
echo " (2) example with approximate author match, preserving OLD author (-o or --oldapproxmatch)" >> tmp.txt
echo " " >> tmp.txt
python ReadAmazonKindleList.py -o exampleKindleList.txt example_KindleBooks_Favorites.xlsx >> tmp.txt
echo " " >> tmp.txt
echo " " >> tmp.txt
echo " " >> tmp.txt
echo " " >> tmp.txt
echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" >> tmp.txt
echo " " >> tmp.txt
echo " " >> tmp.txt
echo " (3) example with approximate author match, preserving NEW author (-n or --newapproxmatch)" >> tmp.txt
echo " " >> tmp.txt
python ReadAmazonKindleList.py -n exampleKindleList.txt example_KindleBooks_Favorites.xlsx >> tmp.txt
diff tmp.txt exampleReadAmazonKindleListOutput.txt
