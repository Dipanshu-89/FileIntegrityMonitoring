import os, hashlib, json, time
Watch_dir = './monitor_folder'
Baseline_file = 'baseline.json'
Alerts_file = 'alerts.json'
sleep_interval = 10  
def hash_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
def scan_directory(directory):
    return {f: hash_file(os.path.join(directory, f)) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))}
def load_json(path):
    if os.path.exists(path):
        with open(path,'r') as f: return json.load(f)
    return {}
def save_json(path, data):
    with open(path,'w') as f: json.dump(data, f, indent=2)
def compare_hashes(old, new):
    alerts = []
    for f in new:
        if f not in old:
            alerts.append(f"New file added: {f}")
        elif old[f] != new[f]:
            alerts.append(f"File modified: {f}")
    for f in old:
        if f not in new:
            alerts.append(f"File deleted: {f}")
    return alerts
def main():
    baseline = load_json(Baseline_file)
    while True:
        current = scan_directory(Watch_dir)
        alerts = compare_hashes(baseline, current)
        if alerts:
            for a in alerts: print("[ALERT]", a)
            save_json(Alerts_file, alerts)
        baseline = current
        save_json(Baseline_file, baseline)
        time.sleep(sleep_interval)
if __name__ == "__main__":
    main()

