import time
import json
import sys
import os
import datetime
from zapv2 import ZAPv2

def main():
    target = None

    # Prendre la cible en argument ou via variable d'environnement
    if len(sys.argv) >= 2:
        target = sys.argv[1]
    else:
        target = os.getenv('TARGET_URL')

    if not target:
        print("Usage : python zapscan.py <url>  ou définir la variable d'environnement TARGET_URL")
        sys.exit(1)

    # Récupérer variables d'environnement pour ZAP API
    zap_api_key = os.getenv('ZAP_API_KEY', '')
    zap_host = os.getenv('ZAP_HOST', 'localhost')
    zap_port = os.getenv('ZAP_PORT', '8080')

    proxies = {
        'http': f'http://{zap_host}:{zap_port}',
        'https': f'http://{zap_host}:{zap_port}'
    }

    zap = ZAPv2(apikey=zap_api_key, proxies=proxies)

    print(f"🔍 Lancement du scan actif sur {target} via ZAP API {zap_host}:{zap_port}...")

    # Accéder à la cible pour initier le crawl
    zap.urlopen(target)
    time.sleep(2)  # Pause pour que ZAP charge la page

    # Lancer le scan actif
    scan_id = zap.ascan.scan(target)

    while int(zap.ascan.status(scan_id)) < 100:
        print(f"Progression du scan actif : {zap.ascan.status(scan_id)}%")
        time.sleep(5)

    print("✅ Scan actif terminé.")

    # Récupérer les alertes
    alerts = zap.core.alerts(baseurl=target)

    # Sauvegarder les résultats dans ./results
    os.makedirs("./results", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_target = target.replace("://", "_").replace("/", "_")
    output_file = f"./results/zap-result-{safe_target}-{timestamp}.json"

    with open(output_file, "w") as f:
        json.dump(alerts, f, indent=2)

    print(f"💾 Résultats sauvegardés dans : {output_file}")

if __name__ == "__main__":
    main()
