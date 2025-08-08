#!/usr/bin/env python3
from pathlib import Path
import subprocess
import argparse
import time
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Hadd all ROOT files in one directory, optionally in batches.')
parser.add_argument('--basePath', help="Directory containing the ROOT files", required=True)
parser.add_argument('--savePath', help="Directory where to store the final merged file", required=True)
parser.add_argument('--outputName', help="Name of the final output ROOT file", required=True)
parser.add_argument('--temp', help="Temporary location to store intermediate or merged file", required=True)
parser.add_argument('--data', help='Use haddnano.py if it is data', action='store_true')
parser.add_argument('--batchSize', help='Max number of files to hadd in one go (default=1000)', type=int, default=1000)
args = parser.parse_args()

base_path = Path(args.basePath)
save_path = Path(args.savePath)
temp_path = Path(args.temp)
temp_path.mkdir(parents=True, exist_ok=True)
save_path.mkdir(parents=True, exist_ok=True)

output_file = args.outputName
batch_size = args.batchSize

root_files = list(base_path.glob("*.root"))
n_files = len(root_files)

if n_files == 0:
    print(f"[ERROR] No ROOT files found in {base_path}")
    exit(1)

print(f"[INFO] Found {n_files} ROOT files.")
print(f"[INFO] Batch outputs will be named like: {Path(output_file).stem}_<index>{Path(output_file).suffix}")
print(f"[INFO] Temp dir:  {temp_path}")
print(f"[INFO] Save dir:  {save_path}")

start = time.time()

# Compute number of batches (at least 1)
num_batches = (n_files - 1) // batch_size + 1

stem = Path(output_file).stem
suffix = Path(output_file).suffix

with tqdm(total=num_batches, desc="Writing batches", unit="batch") as pbar:
    for i in range(num_batches):
        batch_files = root_files[i * batch_size: (i + 1) * batch_size]
        # Create batch file in temp with desired naming: <name>_<i>.root
        tmp_file = temp_path / f"{stem}_{i}{suffix}"
        out_file = save_path / tmp_file.name  # same filename in save path

        # Build and run the merge command for this batch
        if args.data:
            # haddnano.py (kept as shell=True to match your environment)
            cmd = f'PhysicsTools/NanoAODTools/scripts/haddnano.py "{tmp_file}" ' + " ".join(f'"{f}"' for f in batch_files)
        else:
            # classic hadd
            cmd = f'hadd "{tmp_file}" ' + " ".join(f'"{f}"' for f in batch_files)

        tqdm.write(f"[DEBUG] Batch {i+1}/{num_batches}: creating {tmp_file.name}")
        subprocess.check_call(cmd, shell=True)

        # Immediately move the just-created batch file to save_path
        mv_cmd = f'mv "{tmp_file}" "{out_file}"'
        tqdm.write(f"[DEBUG] Moving {tmp_file.name} -> {out_file}")
        subprocess.check_call(mv_cmd, shell=True)

        pbar.update(1)

elapsed = time.time() - start
print(f"\n[INFO] Wrote {num_batches} batch file(s) to {save_path}. Done in {elapsed:.2f} s.")