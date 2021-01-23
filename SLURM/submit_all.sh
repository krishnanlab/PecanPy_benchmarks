#!/bin/bash
cd $(dirname $(realpath $0))

for i in $(cat ../data/implementation_list.txt); do
    echo Submitting test job for $i...

    sid=$(sbatch test_$i\.sb)
    sid_list+=(${sid##* })

    sid=$(sbatch test_$i\_single.sb)
    sid_list+=(${sid##* })
done

j=0
for sid in ${sid_list[@]}; do
    if (( $j == 1 )); then
        sid_str+=,
    else
        j=1
    fi
    sid_str+=$sid
done

echo sbatch IDs: $sid_str

sbatch --dependency=afterany:$sid_str aggregate.sb
