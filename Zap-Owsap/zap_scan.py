from zapv2 import ZAPv2
import time
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 zap_scan.py <url_cible>")
        sys.exit(1)

    target = sys.argv[1]

    zap = ZAPv2(apikey='changeme', proxies={'http': 'http://zap:8080', 'https': 'http://zap:8080'})

    print(f"Lancement du scan actif sur {target} ...")
    scan_id = zap.ascan.scan(target)

    while int(zap.ascan.status(scan_id)) < 100:
        print(f"Progression du scan actif : {zap.ascan.status(scan_id)}%")
        time.sleep(5)

    print("Scan actif terminé.")

    alerts = zap.core.alerts(baseurl=target)
    print(f"Nombre d'alertes : {len(alerts)}")
    for alert in alerts:
        print(f"- {alert['alert']} (Risque: {alert['risk']})")

if __name__ == "__main__":
    main()
