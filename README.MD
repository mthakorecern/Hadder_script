# Hadding ROOT files in batches

## Usage 

```
python3 haddFiles_batchFiles.py \
    --basePath <path-of-directory-containing-root-files-to-be-merged> \
    --savePath <Destination-directory> \
    --outputName <output-name>.root \
    --temp /nfs_scratch/$USER/temp \
    --batchSize 10  \ # Hadding is done in batches
    &> log.txt &
```