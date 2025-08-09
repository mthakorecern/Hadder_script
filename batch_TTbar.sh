  
########################################### BKG ####################################

# python3 modified_hadder.py \
#     --basePath /hdfs/store/user/mithakor/2024_skimmed/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2_02Aug25_1235_001 \
#     --savePath /hdfs/store/user/mithakor/2024_skimmed_hadded \
#     --outputName TTto4Q_TuneCP5_13p6TeV_powheg-pythia8.root \
#     --temp /nfs_scratch/mithakor/temp \
#     --batchSize 20  \
#     &> log_TTto4Q_TuneCP5_13p6TeV_powheg-pythia8.txt &

python3 modified_hadder.py \
    --basePath /hdfs/store/user/mithakor/2024_skimmed/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8_RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v3_02Aug25_1215_000 \
    --savePath /hdfs/store/user/mithakor/2024_skimmed_hadded \
    --outputName TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8.root \
    --temp /nfs_scratch/mithakor/temp \
    --batchSize 50  \
    &> log_TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8.txt &

python3 modified_hadder.py \
    --basePath /hdfs/store/user/mithakor/2024_skimmed/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2_02Aug25_1252_002 \
    --savePath /hdfs/store/user/mithakor/2024_skimmed_hadded \
    --outputName TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8.root \
    --temp /nfs_scratch/mithakor/temp \
    --batchSize 50  \
    &> log_TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8.txt &

