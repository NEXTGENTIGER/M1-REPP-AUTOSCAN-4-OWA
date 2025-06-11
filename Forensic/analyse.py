import subprocess
import json
import os
import sys
import hashlib
from datetime import datetime

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

def compute_hashes(file_path):
    hashes = {"md5": "", "sha1": "", "sha256": ""}
    with open(file_path, "rb") as f:
        data = f.read()
        hashes["md5"] = hashlib.md5(data).hexdigest()
        hashes["sha1"] = hashlib.sha1(data).hexdigest()
        hashes["sha256"] = hashlib.sha256(data).hexdigest()
    return hashes

def analyse(file_path):
    results = {
        "file": file_path,
        "timestamp": datetime.utcnow().isoformat(),
        "filetype": run_cmd(f"file {file_path}"),
        "hashes": compute_hashes(file_path),
        "ssdeep": run_cmd(f"ssdeep {file_path}"),
        "clamav": run_cmd(f"clamdscan --fdpass --no-summary {file_path}"),
        "strings": run_cmd(f"strings -n 6 {file_path} | head -n 50"),
        "exiftool": json.loads(run_cmd(f"exiftool -j {file_path}")["stdout"] or "[]"),
        "upx": run_cmd(f"upx -t {file_path}"),  # test si binaire packé
        "binwalk": run_cmd(f"binwalk {file_path}"),
        "foremost": run_cmd(f"foremost -i {file_path} -o /tmp/foremost_out && ls /tmp/foremost_out"),
        "yara": {},
        "peframe": {},
        "volatility": {}
    }

    # Analyse YARA
    if os.path.exists("/rules"):
        for rule_file in os.listdir("/rules"):
            if rule_file.endswith((".yar", ".yara")):
                full_path = os.path.join("/rules", rule_file)
                results["yara"][rule_file] = run_cmd(f"yara {full_path} {file_path}")

    # PEFRAME si .exe ou .dll
    if file_path.lower().endswith((".exe", ".dll")):
        results["peframe"] = run_cmd(f"peframe {file_path}")

    # Volatility si mémoire dump
    if file_path.lower().endswith((".raw", ".mem", ".vmem")):
        results["volatility"] = run_cmd(f"vol.py -f {file_path} windows.info.Info")

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyse.py /data/fichier.ext")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(json.dumps({"error": "Fichier introuvable"}, indent=2))
        sys.exit(1)

    report = analyse(file_path)
    
    # Sauvegarde automatique
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"/data/report_{ts}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))
    print(f"\n✅ Rapport JSON sauvegardé dans : {filename}")
