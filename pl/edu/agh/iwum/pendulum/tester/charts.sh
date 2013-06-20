#!/bin/bash

function plot_results {
    files_to_plot=""
    for result in *; do
        files_to_plot="'$result' with linespoints, $files_to_plot"
    done
    files_to_plot=`echo ${files_to_plot%?}`
    files_to_plot=`echo ${files_to_plot%?}`
    echo $files_to_plot
    gnuplot -e "$plot_settings; set title '$1'; set ylabel '$3'; set output '../../../charts/$1_$2.png'; plot $files_to_plot"
}

mkdir ../charts
plot_settings="set terminal png size 1360,700; set xlabel 'Learning steps'"
for controller in *; do
    echo $controller
    if [ -d "${controller}" ]; then
        cd $controller
        cd steps
        plot_results $controller steps "Survived steps"
        cd ..
        cd angles
        plot_results $controller angles "Average angle"
        cd ../..
    fi
done
