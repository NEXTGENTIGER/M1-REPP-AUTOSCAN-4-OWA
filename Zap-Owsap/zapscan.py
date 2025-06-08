import os
import sys
import time
from zapv2 import ZAPv2
import datetime
import json

def main():
    # Récupération de la cible depuis la variable d'environnement
    target = os.getenv("TARGET_URL")
    if not target:
        print("❌ Veuillez définir TARGET_URL en variable d'environnement.")
        sys.exit(1)

    # Configuration ZAP
    zap_api_key = os.getenv("ZAP_API_KEY", "")
    zap_host = os.getenv("ZAP_HOST", "host.docker.internal")
    zap_port = os.getenv("ZAP_PORT", "8080")

    # Création de l'objet ZAPv2 avec proxy sur le daemon ZAP
    zap = ZAPv2(apikey=zap_api_key,
                proxies={"http": f"http://{zap_host}:{zap_port}",
                         "https": f"http://{zap_host}:{zap_port}"})

    print(f"▶️ Début du scan OWASP ZAP sur la cible : {target}")

    # Ouvrir la cible dans ZAP (préparer la session)
    zap.urlopen(target)

    # Pause pour que le site soit bien accessible avant scan
    print("⏳ Attente que la cible soit accessible...")
    time.sleep(5)

    # Lancer le scan actif
    print("🚀 Lancement du scan actif...")
    scan_id = zap.ascan.scan(target)

    # Suivre la progression du scan actif
    while int(zap.ascan.status(scan_id)) < 100:
        progress = zap.ascan.status(scan_id)
        print(f"🔄 Progression du scan : {progress}%")
        time.sleep(5)

    print("✅ Scan actif terminé. Récupération des résultats...")

    # Récupérer les alertes détectées
    alerts = zap.core.alerts(baseurl=target)

    # Préparer nom de fichier horodaté
    safe_target = target.replace("https://", "").replace("http://", "").replace("/", "_")
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"/app/results/zap-result-{safe_target}-{timestamp}.json"

    # Sauvegarder le rapport JSON
    with open(filename, "w") as f:
        json.dump(alerts, f, indent=2)

    print(f"💾 Rapport sauvegardé dans : {filename}")

if __name__ == "__main__":
    main()
