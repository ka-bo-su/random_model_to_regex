#for文を実行
start=19
end=30
for i in $(seq $start $end); do
    #iをゼロ埋めしてechoを使って出力
    mkdir example/ex$(printf %02d $i)
    cp example/ex01/*hif* example/ex$(printf %02d $i)/
    cp example/ex01/*hsf* example/ex$(printf %02d $i)/
    rename "s/ex01/ex$(printf %02d $i)/;" example/ex$(printf %02d $i)/*
done
