cd ./work/meaning_procedure/code
( echo "zodiac parity month"; echo "zodiac parity latin"; echo "zodiac gallows month"; echo "zodiac gallows latin"; echo "plant2 x x" ) | xargs -P 3 -L 1 sh -c 'python3 d6c3.py $0 $1 $2 > ../d6c3_$0_$1_$2.out 2>&1'
