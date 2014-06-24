#!/bin/bash
#sed -i -e 's/qid WChoice NumMachine NumForEach k LevelRs Pivots RepeatTime MatCost NaiveCost Cost QCost/qid WChoice NumMachine NumForEach k LevelRs Pivots RepeatTime MatCost NaiveCost Cost QCost EstResSite/g' run01.py
NumSpace=21
#DIRS=./Exp0618*
DIRS=./tttt
zz="'EstResSite'"
space="\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ "
msg1=$space"if time % 100 == 0:'"
msg2=$space"\ \ \ \ record['$zz'] = '_'.join(map(lambda x:str(round(x,4)),level_rs_est))'"
msg3=$space"else:'"
msg4=$space"\ \ \ \ record['$zz'] = '-1';'"
cmd="sed -i -e '157i"
dcmd="sed -i -e '157d"
for d in $DIRS
do
    for f in $d/*.py
    #for (( i=1; i<=$NumSpace; i=i+1 ))
    do
        echo $f
        sed -i -e 's/qid WChoice NumMachine NumForEach k LevelRs Pivots RepeatTime MatCost NaiveCost Cost QCost/qid WChoice NumMachine NumForEach k LevelRs Pivots RepeatTime MatCost NaiveCost Cost QCost EstResSite/g' $f
#        awk '/level_rs_est = update_pivot/{print NR}' $f
#        echo $line
#        echo NR
#        awk '/level_rs_est = update_pivot/{eval $cmd$1i$msg4 $f}' $f
#        awk '/level_rs_est = update_pivot/{print NR;line=NR;echo $line;eval $cmd$linei$msg4 $f}' $f

        eval $dcmd $f
        eval $dcmd $f
        eval $dcmd $f
        eval $dcmd $f
        eval $cmd$msg4 $f
        eval $cmd$msg3 $f
        eval $cmd$msg2 $f
        eval $cmd$msg1 $f
    done
done
#sed -i -e '155i\ ' run01.py
#sed '154i                    haha' run01.py
