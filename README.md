<div align="center">

# MsunPV Integration

![Home Assistant](https://img.shields.io/badge/home%20assistant-%2341BDF5.svg?style=for-the-badge&logo=home-assistant&logoColor=white)
[![Hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)]

[![GitHub release](https://img.shields.io/github/release/pvergezac/msunpvintegration.svg)](https://GitHub.com/pvergezac/msunpvintegration/releases/)
![GitHub Release Date](https://img.shields.io/github/release-date/pvergezac/MSunPVIntegration)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/pvergezac/MSunPVIntegration/total)

[![GitHub license](https://badgen.net/github/license/pvergezac/msunpvintegration)](https://github.com/pvergezac/msunpvintegration/blob/master/LICENSE)
[![GitHub forks](https://badgen.net/github/forks/pvergezac/msunpvintegration/)](https://GitHub.com/pvergezac/msunpvintegration/network/)
[![GitHub stars](https://badgen.net/github/stars/pvergezac/msunpvintegration)](https://GitHub.com/pvergezac/msunpvintegration/stargazers/)

- [[Documentation]](https://github.com/pvergezac/MSunPVIntegration/blob/main/DOCUMENTATION/Documentation.md)
- [[Issues]](https://github.com/pvergezac/MSunPVIntegration/issues)
- [**MSunPV Integration** on Home Assistant Community](https://community.home-assistant.io/t/msunpv-solar-router-integration/862047)
- [**MSunPV Integration**  sur le Forum Ard-Tek](https://ard-tek.com/index.php/forum/bienvenue/2747-home-assistant-integration-msunpv-hacs)


</div>

## 📋 Description

**MsunPV Integration** est une intégration personnalisée pour **Home Assistant** qui permet le suivi des mesures du routeur solaire **MSunPV** de [**Ard-Tek**](https://ard-tek.com).

L'intégration permet de suivre des mesures :
- Production instantanée des panneaux solaire
- Consommation ou injection instantanée sur le réseau électrique
- Taux de routage vers le ballon d'eau chaude
- Température du ballon (si sonde installée)
- Production Solaire journalière et cumulée
- Consommation réseau journalière
- Injection réseau journalière
- Valeurs complémentaires calculés (Consommation totale, production consommée, etc.)
- Infos routeur (modèle, version, config, etc.)
- Installation et mises à jour via HACS, et l'interface graphique de HA

Le choix à été fait de transformer les valeurs du MSunPV en valeur positives (sauf puissance réseau, négative en cas d'injection).
Il semble plus logique de voir une courbe montante quand le production PV augmente. C'est également plus simple d'alimenter le Dashboard Energie de Home Assistant avec ces valeurs. (On pourra si nécessaire, doubler certaines entités pour avoir aussi les valeur en négatif comme sur le routeur).

Les développements et tests ont été réalisés sur un routeur MSunPV MS_PV2_2d, V5.0.1, Fw Wifi 104b, Fw Routeur 104b, en configuration d'origine.

### Fonctionnalités à venir (TODO List)

- État et pilotage des commandes Manu/Auto (ballon & radiateur)
- État et pilotage des commandes TestRouteur (Inject, Zéro, Moyen, Fort)
- État et pilotage des consignes de température (ballon & radiateur)
- Automatisations

L'idée est de pouvoir agir sur le routage depuis HA, pour par exemple intégrer les prévisions de production du lendemain, ou prioriser la production d'eau chade par rapport à la filtration d'un piscine, ou encore tenir compte de la couleur du jour de TEMPO.

## Le routeur solaire MSunPV

Le routeur solaire **MSunPV** de [**Ard-Tek**](https://ard-tek.com) permet d'utiliser l’excédant de production d'energie de panneaux solaires, pour par exemple recharger un ballon d'eau chaude ou alimenter un radiateur, au lieu de l'injecter gratuitement ou a faible prix sur le réseau EDF.

Tous les détails sur le routeur **MSunPV** sont sur le site de [Ard-Tek](https://ard-tek.com).

## 📦 Installation via HACS (recommandé)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=pvergezac&repository=MSunPVIntegration=integration)

### Prérequis

- Home Assistant version 2025.2.4 ou supérieure
- [HACS installé](https://hacs.xyz/docs/setup/download) sur votre instance Home Assistant

### Étape 1 — Ajouter le dépôt personnalisé dans HACS

> HACS ne référence pas encore ce dépôt par défaut. Ajoutez-le manuellement.

1. Dans Home Assistant, ouvrez **HACS** dans la barre latérale
2. Cliquez sur les **⋮** (trois points) en haut à droite
3. Sélectionnez **Dépôts personnalisés**
4. Dans le champ **Dépôt**, saisissez l'URL du dépôt GitHub :
   ```
   https://github.com/pvergezac/MSunPVIntegration
   ```
5. Dans **Catégorie**, sélectionnez **Intégration**
6. Cliquez sur **Ajouter**

### Étape 2 — Installer l'intégration

1. Toujours dans HACS, allez dans **Intégrations**
2. Cliquez sur **+ Explorer et télécharger des dépôts**
3. Recherchez **MSunPV Intégration**
4. Cliquez sur le résultat puis sur **Télécharger**
5. Confirmez en cliquant sur **Télécharger** dans la fenêtre de confirmation

### Étape 3 — Redémarrer Home Assistant

Après l'installation, un redémarrage est nécessaire :

**Paramètres → Système → Redémarrer → Redémarrer Home Assistant**

Attendez que Home Assistant soit complètement redémarré avant de continuer.


---

## ⚙️ Configuration

### Étape 1 — Ajouter l'intégration

**Paramètres → Appareils et services → Ajouter une intégration → MSunPV Intégration**

Saisissez :

- l'adresse locale de votre routeur.
  - Ex : ```http://192.168.xxx.xxx``` (**http** uniquement)
- le nom désignant le routeur dans votre installation
- l'activation ou non des sondes complémentaires 8 à 15

***
***

## Notice for Developpement

HAVE FUN! 😎

### What?

This repository contains multiple files, here is a overview:

| File | Purpose | Documentation |
| ---- | ------- | ------------- |
| `.devcontainer.json` | Used for development/testing with Visual Studio Code. | [Documentation](https://code.visualstudio.com/docs/remote/containers) |
| `.github/ISSUE_TEMPLATE/*.yml` | Templates for the issue tracker | [Documentation](https://help.github.com/en/github/building-a-strong-community/configuring-issue-templates-for-your-repository) |
| `custom_components/msunpv/*` | Integration files, this is where everything happens. | [Documentation](https://developers.home-assistant.io/docs/creating_component_index) |
| `CONTRIBUTING.md` | Guidelines on how to contribute. | [Documentation](https://help.github.com/en/github/building-a-strong-community/setting-guidelines-for-repository-contributors) |
| `LICENSE` | The license file for the project. | [Documentation](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/licensing-a-repository) |
| `README.md` | The file you are reading now, should contain info about the integration, installation and configuration instructions. | [Documentation](https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax) |
| `requirements.txt` | Python packages used for development/lint/testing this integration. | [Documentation](https://pip.pypa.io/en/stable/user_guide/#requirements-files) |

### How?

1. Open this repository in **Visual Studio Code** devcontainer (Preferably with the "`Dev Containers: Clone Repository in Named Container Volume...`" option).
1. Run the `scripts/develop` to start HA and test out this integration.

# 🤝 Contribution

Les contributions sont les bienvenues ! Pour signaler un bug ou proposer une amélioration, ouvrez une [issue](https://github.com/pvergezac/SmartPoolFiltraMSunPVIntegrationtionManager/issues) sur GitHub.

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">
Fait avec ❤️ pour la communauté Home Assistant francophone

Si vous aimez ce projet, ajouter une ⭐ étoile sur [Github](https://github.com/pvergezac/![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/pvergezac/MSunPVIntegration/total)
)
</div>
