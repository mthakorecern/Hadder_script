# Hadding ROOT files in batches

This code has several modifications. However, at the root level, it has the same logic and commands that were written by Ganesh Parida.


## Usage 

```
python3 modified_hadder.py \
    --basePath /hdfs/store/user/mithakor/2024_skimmed/WtoENu_4Jets_TuneCP5_13p6TeV_madgraphMLM_v2-v2_29Jul25_1803_000 \
    --savePath /hdfs/store/user/mithakor/2024_skimmed_hadded \
    --outputName WtoENu_4Jets_TuneCP5_13p6TeV_madgraphMLM_pythia8.root \
    --temp /nfs_scratch/mithakor/temp \
    --batchSize 100  \
    &> log_WtoENu_4Jets_TuneCP5_13p6TeV_madgraphMLM_pythia8.txt &
```