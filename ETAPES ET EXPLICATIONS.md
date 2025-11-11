## Étapes du projet couvertes par le script Python

Avec le script **Python (`fsr_gui_arduino.py`)** et le code **Arduino actuel**, les étapes suivantes du projet sont complétées :

### ✅ Step 6 – Accumulation / affichage / enregistrement
- Lancement automatique d’un essai de **10 secondes**.  
- Lecture continue des **données série** envoyées par l’Arduino.  
- **Affichage en temps réel** des trames reçues dans la zone de log.  
- **Enregistrement** automatique dans un fichier `.csv`.

### ✅ Step 7 – Plusieurs essais
- **Préfixe configurable** (ex. `Sujet01_FSR`).  
- **Numéro d’essai** géré automatiquement (`T01`, `T02`, `T03`, …).  
- **Création d’un fichier par essai** avec incrémentation automatique.

### ✅ Step 8 – Interface Homme-Machine (IHM)
- Interface graphique réalisée avec **Tkinter** :  
  - Sélection du **dossier de sortie**.  
  - Configuration du **préfixe** et du **numéro d’essai**.  
  - **Bouton Start (10s)** : démarre un essai chronométré.  
  - **Bouton Stop** : arrêt manuel possible avant la fin.  
  - **Affichage de l’état courant** (attente, en cours, terminé).  
  - **Zone de log** affichant les trames série reçues.

### 🔄 Protocole exploité
- **Commandes Arduino :**
  - `'r'` → calibration + démarrage du streaming (Step 1–2)
  - `'s'` → arrêt du streaming (Step 1–2)
- **Format des données :**
  - `time_ms,value` (Step 3–4–5)

---

**Bilan :**  
→ Le script Python complète les **Steps 6 à 8**, tout en exploitant les **Steps 1 à 5** réalisés sur Arduino.  
Tu disposes ainsi d’une chaîne complète de mesure et d’enregistrement automatisée entre le capteur FSR et le PC.
