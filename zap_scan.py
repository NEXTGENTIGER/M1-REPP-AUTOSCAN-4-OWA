import requests
import time
import sys

ZAP_API_URL = "http://zap:8080"  # zap service hostname + port dans docker-compose

def start_scan(target_url):
    print(f"Lancement du scan ZAP sur {target_url}...")

    # Démarrer un scan actif
    scan_response = requests.get(f"{ZAP_API_URL}/JSON/ascan/action/scan/", params={"url": target_url, "recurse": True})
    scan_id = scan_response.json().get("scan")

    if not scan_id:
        print("Erreur: impossible de démarrer le scan")
        sys.exit(1)

    print(f"Scan démarré avec scanId={scan_id}")

    # Poller le statut du scan
    while True:
        status_response = requests.get(f"{ZAP_API_URL}/JSON/ascan/view/status/", params={"scanId": scan_id})
        status = int(status_response.json().get("status", 0))
        print(f"Progression du scan : {status}%")
        if status >= 100:
            break
        time.sleep(5)

    print("Scan terminé!")

def get_report():
    print("Récupération du rapport JSON...")
    report_response = requests.get(f"{ZAP_API_URL}/JSON/core/view/alerts/")
    alerts = report_response.json().get("alerts", [])
    report_file = "/app/results/zap_report.json"
    with open(report_file, "w") as f:
        import json
        json.dump(alerts, f, indent=2)
    print(f"Rapport sauvegardé dans {report_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python zap_scan.py <url_target>")
        sys.exit(1)

    target = sys.argv[1]
    start_scan(target)
    get_report()
