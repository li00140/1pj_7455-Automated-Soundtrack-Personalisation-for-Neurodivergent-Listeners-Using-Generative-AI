#!/bin/bash

echo "Generating waveform comparison..."
python3 waveform.py \
    --baseline outputs/Bowie_Test/baseline/Bowie_Test_baseline_accessible_mix.wav \
    --dsp outputs/Bowie_Test/dsp_only/Bowie_Test_dsp_only_accessible_mix.wav \
    --generative outputs/Bowie_Test/generative/Bowie_Test_generative_accessible_mix.wav \
    --combined outputs/Bowie_Test/combined/Bowie_Test_combined_accessible_mix.wav \
    --output evaluation_results/Bowie_Test/waveforms.png

echo "Generating spectrogram comparison..."
python3 spectrograms.py \
    --baseline outputs/Bowie_Test/baseline/Bowie_Test_baseline_accessible_mix.wav \
    --dsp outputs/Bowie_Test/dsp_only/Bowie_Test_dsp_only_accessible_mix.wav \
    --generative outputs/Bowie_Test/generative/Bowie_Test_generative_accessible_mix.wav \
    --combined outputs/Bowie_Test/combined/Bowie_Test_combined_accessible_mix.wav \
    --output evaluation_results/Bowie_Test/spectrograms.png

echo "Generating metrics bar chart..."
python3 metrics_barplot.py \
    --input evaluation_results/Bowie_Test/evaluation_results.json \
    --output evaluation_results/Bowie_Test/metrics_barplot.png

echo "Generating radar chart..."
python3 radar_chart.py \
    --input evaluation_results/Bowie_Test/evaluation_results.json \
    --output evaluation_results/Bowie_Test/radar_chart.png

echo "Generating difference heatmap..."
python3 difference_heatmap.py \
    --input evaluation_results/Bowie_Test/evaluation_results.json \
    --output evaluation_results/Bowie_Test/difference_heatmap.png

echo ""
echo "=========================="
echo " All figures generated!"
echo "=========================="