start=1
end=30
for i in $(seq $start $end); do
    cp example/ex$(printf %02d $i)/ex$(printf %02d $i).hif example/ex$(printf %02d $i)/ex$(printf %02d $i).hif.bak
    cp example/ex$(printf %02d $i)/ex$(printf %02d $i).hsf example/ex$(printf %02d $i)/ex$(printf %02d $i).hsf.bak
done
