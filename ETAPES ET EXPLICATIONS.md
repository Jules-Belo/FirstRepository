# 1️⃣ Étapes du projet couvertes par ce code Arduino

### Avec ce code :
	•	**Step 1** – Synchronisation 1
	  •	Vitesse série : Serial.begin(1000000); ✅
	  •	Démarrage de l’acquisition uniquement après réception de 'r' ✅
	•	**Step 2** – Synchronisation 2
	  •	Commande 's' pour arrêter le streaming proprement (started = false, LED ON, message) ✅
	•	**Step 3** – Comptage temporel
	  •	Utilisation de millis() et mémorisation d’un t0 au moment du 'r'. ✅
	•	**Step 4** – Transmission du temps
	  •	Chaque ligne envoyée est au format : time_ms,value (ex : 37,12) ✅
	•	**Step 5** – Transmission du signal FSR
	  •	Lecture du capteur sur A0, baseline par calibration, valeur corrigée envoyée en continu ✅

⸻
————

# 2️⃣ Explication rapide du fonctionnement

  • **Au démarrage** :
  	•	LED intégrée allumée → Arduino en attente.
  	•	Message d’info sur la liaison série.
  •	**Quand le PC envoie 'r'** :
  	•	*Calibration* : moyenne de plusieurs lectures sans pression.
  	•	*Stockage* de cette baseline.
  	•	t0 = millis() → temps zéro de l’essai.
  	•	started = true, LED éteinte.
  •	**Ensuite, la boucle envoie en continu** :
  	•	le temps écoulé (ms depuis t0),
  	•	la valeur FSR corrigée (raw - baseline, forcée ≥ 0),
  	•	au format time_ms,value.
  •	**Quand le PC envoie 's'** :
  	•	started = false, arrêt immédiat de l’envoi.
  	•	LED rallumée.
  	•	Message "Streaming stopped.".
