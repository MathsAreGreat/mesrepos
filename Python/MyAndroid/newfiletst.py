from tqdm import tqdm
pbar = tqdm(total=100, unit="B", unit_scale=True)

for _ in range(10):
    pbar.update(10)  # Update progress
    pbar.set_postfix({"Speed": "500KiB/s", "ETA": "2m30s"})  # Dynamic info
    time.sleep(1)  # Simulating download delay

pbar.close()