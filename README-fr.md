# Integration VEEAM avec Visual TOM
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.md)&nbsp;
[![fr](https://img.shields.io/badge/lang-en-red.svg)](README.md)  
Ce projet permet l’intégration de Veeam Backup avec l’ordonnanceur Visual TOM.

Deux solutions sont proposées ici :

  * Solution 1 : Une intégration Windows uniquement qui repose sur les commandes PowerShell
  * Solution 2 : Une intégration générique Windows/Linux pour exécuter des jobs sur des agents Veeam

Deux scripts Python à utiliser avec les queues associées : 

  * Intégration Windows : veeam_wnt.py et submit_queue_veeam_wnt.bat
  * Intégration Windows/Linux : veeam.py avec submit_queue_veeam.bat (Win) ou tom_submit.veeam (Linux)

Actions supportées :

Solution 1 : Veeam Backup
Le script appelle les commandes Veeam PowerShell à travers Python en utilisant subprocess. Il gère les éléments suivants :
Lancer un job (incrémental ou full)
Arrêter un job
Activer / désactiver un job
Consulter le statut d’un job

Solution 2 (multiplateforme) : Veeam Agent + Veeam Config Tool (veeamconfig)
Veeam Agent (Windows ou Linux) permet de faire des sauvegardes locales, vers des partages réseau ou des répositories Veeam.
veeamconfig (Linux)
Veeam.Agent.Configurator.exe (Windows)

Fonctionnement général
Le script appelle les commandes Veeam à travers Python en utilisant subprocess. Il gère les éléments suivants :
- Lancement d’un job pour une sauvegarde.
- Consultation du status des jobs.
- Consultation de la liste des jobs.

# Disclaimer
Aucun support ni garanties ne seront fournis par Absyss SAS pour ce projet et fichiers associés. L'utilisation est à vos propres risques.
Absyss SAS ne peut être tenu responsable des dommages causés par l'utilisation d'un des fichiers mis à disposition dans ce dépôt Github.
Il est possible de faire appel à des jours de consulting pour l'implémentation.

# Prérequis

  * Visual TOM 7.1.2 or supérieur
  * Windows avec PowerShell installé
  * Python version supérieure à 3.x
  * Module Veeam.Backup.PowerShell installé et accessible

# Consignes

Le modèle applicatif est à importer en fonction de la solution (1/2) choisie et le traitement VTOM est à exécuter soit à partir du serveur Veeam (solution 1) soit à partir d'un agent Veeam (solution 2).

Le script Python veeam_wnt.py est défini avec des variables génériques et le script veeam.py nécessite de renseigner le chemin d'installation des commandes Veeam pour la partie Windows : Veeam.Agent.Configurator.exe

Tests avec la solution 1: 
  ```Appel direct (Python seul)
python veeam_wnt.py "NomDuJob" --start
python veeam_wnt.py "NomDuJob" --status
python veeam_wnt.py --list
  ```
  ```Execution avec la queue batch Windows
queue_veeam_wnt.bat NomDuJob START FULL
queue_veeam_wnt.bat NomDuJob START INCR
queue_veeam_wnt.bat NomDuJob STOP
queue_veeam_wnt.bat NomDuJob ENABLE
queue_veeam_wnt.bat NomDuJob DISABLE
queue_veeam_wnt.bat NomDuJob STATUS
  ```

# Actions disponibles

## Pour Windows seulement (queue_veeam_wnt.bat)


<img width="694" height="283" alt="image" src="https://github.com/user-attachments/assets/5b4916e1-e995-4e23-9264-db65e3d8ae32" />


| Action           | Description                  |
| ---------------- | ---------------------------- |
| `--list`         | Lister tous les jobs         |
| `--start --full` | Lancer un backup full        |
| `--start --incr` | Lancer un backup incremental |
| `--stop`         | Arrêter un job               |
| `--disable`      | Désactiver un job            |
| `--enable`       | Réactiver un job             |
| `--status`       | Statut du dernier run        |

### Lister tous les jobs
- Backup Job Name : vide
- Action : list
- Backup type : vide

### Lancer un job de backup
- Backup Job Name : nom du job
- Action : start
- Backup type : FULL ou INCR (sauvegarde totale ou incrémentale)

### Arrêter un job de backup
- Backup Job Name : nom du job
- Action : stop
- Backup type : vide

### Désactiver un job
- Backup Job Name : nom du job
- Action : disable
- Backup type : vide

### Réactiver un job
- Backup Job Name : nom du job
- Action : enable
- Backup type : vide

### Statut du dernier job
- Backup Job Name : vide
- Action : status
- Backup type : vide

## Pour Windows ou Linux (submit_queue_veeam.bat ou tom_submit.veeam)


<img width="692" height="236" alt="image" src="https://github.com/user-attachments/assets/33d9a31e-3ab5-4937-998c-d321dd2e998b" />

### Lister tous les jobs
- Action : list
- Backup Job Name : vide

### Démarrer un job
- Action : start
- Backup Job Name : nom du job

### Statut d'un job
- Action : status
- Backup Job Name : nom du job
  
# Licence
Ce projet est sous licence Apache 2.0. Voir le fichier [LICENCE](license) pour plus de détails.


# Code de conduite
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](code-of-conduct.md)  
Absyss SAS a adopté le [Contributor Covenant](CODE_OF_CONDUCT.md) en tant que Code de Conduite et s'attend à ce que les participants au projet y adhère également. Merci de lire [document complet](CODE_OF_CONDUCT.md) pour comprendre les actions qui seront ou ne seront pas tolérées.
