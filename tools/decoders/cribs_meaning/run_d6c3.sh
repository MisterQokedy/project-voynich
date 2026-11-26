cd ./work/meaning_procedure/code
( for ch in cell onset ending parity gallows; do for cs in month latin; do echo "zodiac $ch $cs"; done; done; echo "plant2 x x" ) | xargs -P 4 -L 1 sh -c 'python3 d6c3.py $0 $1 $2 > ../d6c3_$0_$1_$2.out 2>&1'
