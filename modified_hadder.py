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

print(f"[INFO] Found {n_files} ROOT files to merge.")
print(f"[INFO] Temporary output will be: {temp_path}/{output_file}")
print(f"[INFO] Final output will be: {save_path}/{output_file}")

start = time.time()

if args.data:
    if n_files > batch_size:
        print(f"[INFO] Data detected with > {batch_size} files. Using haddnano.py in batches.")
        tmp_outputs = []
        num_batches = (n_files - 1) // batch_size + 1

        with tqdm(total=num_batches, desc="Merging batches", unit="batch") as pbar:
            for i in range(num_batches):
                batch_files = root_files[i * batch_size: (i + 1) * batch_size]
                tmp_file = temp_path / f"tmp_{i}_{output_file}"
                cmd = f'PhysicsTools/NanoAODTools/scripts/haddnano.py {tmp_file} {" ".join(str(f) for f in batch_files)}'
                tqdm.write(f"[DEBUG] Batch {i+1}/{num_batches}")
                subprocess.check_call(cmd, shell=True)
                tmp_outputs.append(str(tmp_file))
                pbar.update(1)

        final_cmd = f'PhysicsTools/NanoAODTools/scripts/haddnano.py {temp_path}/{output_file} {" ".join(tmp_outputs)}'
        total_size_bytes = sum(Path(f).stat().st_size for f in tmp_outputs)
        total_size_gb = total_size_bytes / (1024**3)

        if total_size_gb > 3:
            tqdm.write(f"[WARNING] Total size of temporary files is {total_size_gb:.2f} GB (>3 GB). Skipping final merge.")
            
            for i, f in enumerate(tmp_outputs):
                out_path = save_path / f"{Path(f).name}"
                mv_cmd = f'mv {f} {out_path}'
                tqdm.write(f"[DEBUG] Moving tmp file {f} to {out_path}")
                subprocess.check_call(mv_cmd, shell=True)
            
            tqdm.write(f"[INFO] All batch outputs moved individually. Skipping final merged output.")
            exit(0)
        tqdm.write(f"[DEBUG] Final merge")
        subprocess.check_call(final_cmd, shell=True)

        cleanup_cmd = f'rm {" ".join(tmp_outputs)}'
        tqdm.write(f"[DEBUG] Cleaning up temp files")
        subprocess.check_call(cleanup_cmd, shell=True)

    else:
        cmd = f'PhysicsTools/NanoAODTools/scripts/haddnano.py {temp_path}/{output_file} {" ".join(str(f) for f in root_files)}'
        print(f"[DEBUG] Single-step haddnano")
        subprocess.check_call(cmd, shell=True)

else:
    # MC case
    if n_files > batch_size:
        print(f"[INFO] MC detected with > {batch_size} files. Using hadd in batches.")
        tmp_outputs = []
        num_batches = (n_files - 1) // batch_size + 1

        with tqdm(total=num_batches, desc="Merging batches", unit="batch") as pbar:
            for i in range(num_batches):
                batch_files = root_files[i * batch_size: (i + 1) * batch_size]
                tmp_file = temp_path / f"{output_file}_{i}"
                cmd = f'hadd {tmp_file} {" ".join(str(f) for f in batch_files)}'
                tqdm.write(f"[DEBUG] Batch {i+1}/{num_batches}")
                subprocess.check_call(cmd, shell=True)
                tmp_outputs.append(str(tmp_file))
                pbar.update(1)

        final_cmd = f'hadd {temp_path}/{output_file} {" ".join(tmp_outputs)}'
        total_size_bytes = sum(Path(f).stat().st_size for f in tmp_outputs)
        total_size_gb = total_size_bytes / (1024**2)

        if total_size_gb > 3:
            tqdm.write(f"[WARNING] Total size of temporary files is {total_size_gb:.2f} GB (>3 GB). Skipping final merge.")
            
            for i, f in enumerate(tmp_outputs):
                out_path = save_path / f"{Path(f).name}"
                mv_cmd = f'mv {f} {out_path}'
                tqdm.write(f"[DEBUG] Moving tmp file {f} to {out_path}")
                subprocess.check_call(mv_cmd, shell=True)
            
            tqdm.write(f"[INFO] All batch outputs moved individually. Skipping final merged output.")
            for f in tmp_outputs:
                try:
                    Path(f).unlink()
                except Exception as e:
                    tqdm.write(f"[WARNING] Could not delete {f}: {e}")
            exit(0)
        tqdm.write(f"[DEBUG] Final merge")
        subprocess.check_call(final_cmd, shell=True)

        cleanup_cmd = f'rm {" ".join(tmp_outputs)}'
        tqdm.write(f"[DEBUG] Cleaning up temp files")
        subprocess.check_call(cleanup_cmd, shell=True)

    else:
        cmd = f'hadd {temp_path}/{output_file} {" ".join(str(f) for f in root_files)}'
        print(f"[DEBUG] Single-step hadd")
        subprocess.check_call(cmd, shell=True)

# Move final output
mv_cmd = f'mv {temp_path}/{output_file} {save_path}'
tqdm.write(f"[DEBUG] Moving to final location")
subprocess.check_call(mv_cmd, shell=True)

elapsed = time.time() - start
print(f"\n All done in {elapsed:.2f} seconds.")
