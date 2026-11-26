cd ./work/meaning_procedure/code
for cfg in "onset start" "ending start" "parity start" "gallows start" "cell end" "onset end" "ending end" "parity end" "gallows end"; do echo $cfg; done | xargs -P 4 -L 1 sh -c 'python3 d6c2.py $0 $1 > ../d6c2_$0_$1.out 2>&1'
