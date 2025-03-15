# Routeur solaire MSunPV
Le **MSunPV** est un routeur solaire permettant d'utiliser l’excédant de production solaire des panneaux pour par exemple recharger un ballon d'eau chaude ou alimenter un radiateur, au lieu de l'injecter sur le réseau.

Tous les détails sur le **MSunPV** sont sur le site de [Ard-Tek](https://ard-tek.com).


# L'intégration MSunPV

Cette intégration permet le suivi des mesures du routeur **MSunPV**.
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


![Home Assistant](https://img.shields.io/badge/home%20assistant-%2341BDF5.svg?style=for-the-badge&logo=home-assistant&logoColor=white) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![hacs][hacsbadge]][hacs]

## A propos
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![GitHub release](https://img.shields.io/github/release/pvergezac/msunpvintegration.svg)](https://GitHub.com/pvergezac/msunpvintegration/releases/) [![GitHub tag](https://img.shields.io/github/tag/pvergezac/msunpvintegration.svg)](https://GitHub.com/pvergezac/msunpvintegration/tags/) [![GitHub license](https://badgen.net/github/license/pvergezac/msunpvintegration)](https://github.com/pvergezac/msunpvintegration/blob/master/LICENSE) [![GitHub forks](https://badgen.net/github/forks/pvergezac/msunpvintegration/)](https://GitHub.com/pvergezac/msunpvintegration/network/) [![GitHub stars](https://badgen.net/github/stars/pvergezac/msunpvintegration)](https://GitHub.com/pvergezac/msunpvintegration/stargazers/)

- [[Documentation]](github.com/pvergezac/MSunPVIntegration/blob/main/DOCUMENTATION/Documentation.md)
- [[Issues]](https://github.com/pvergezac/MSunPVIntegration/issues)
- [[MSunPV Integration]  on Home Assistant Community](https://community.home-assistant.io/t/msunpv-solar-router-integration/862047)
- [[MSunPV Integration]  sur le Forum Ard-Tek](https://ard-tek.com/index.php/forum/bienvenue/2747-home-assistant-integration-msunpv-hacs)

## A venir (TODO)
- État et pilotage des commandes Manu/Auto (ballon & radiateur)
- État et pilotage des commandes TestRouteur (Inject, Zéro, Moyen, Fort)
- État et pilotage des consignes de température (ballon & radiateur)
- Automatisations

L'idée est de pouvoir agir sur le routage depuis HA, pour par exemple intégrer les prévisions de production du lendemain, ou prioriser par rapport à la filtration d'un piscine, ou encore tenir compte de la couleur du jour de TEMPO.


## Installation
Cette intégration nécessite HACS.

- Dans HACS, à l'aide du menu (trois points en haut à droite), ajouter un **Dépôt personnalisé** de type **Intégration** :
    - dépôt : https://github.com/pvergezac/MSunPVIntegration
- Dans HACS, Rechercher l'intégration **MSunPV Intégration**.
- Télécharger l'intégration
- Relancer Home Assistant
- Dans : Paramètres / Appareils et services / Intégration
    - Ajouter une intégration
    - rechercher **MSunPV Intégration**

<p>Ou utilisez le bouton ci-dessous :<br>

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=pvergezac&repository=https%3A%2F%2Fgithub.com%2Fpvergezac%2Fmsunpvintegration&category=Integration)<br>


## Configuration
Saisissez l'adresse locale de votre routeur.
- Ex : http://192.168.xxx.xxx

<p><br>

***
***

# Notice for Developpement

HAVE FUN! 😎

## What?

This repository contains multiple files, here is a overview:

File | Purpose | Documentation
-- | -- | --
`.devcontainer.json` | Used for development/testing with Visual Studio Code. | [Documentation](https://code.visualstudio.com/docs/remote/containers)
`.github/ISSUE_TEMPLATE/*.yml` | Templates for the issue tracker | [Documentation](https://help.github.com/en/github/building-a-strong-community/configuring-issue-templates-for-your-repository)
`custom_components/msunpv/*` | Integration files, this is where everything happens. | [Documentation](https://developers.home-assistant.io/docs/creating_component_index)
`CONTRIBUTING.md` | Guidelines on how to contribute. | [Documentation](https://help.github.com/en/github/building-a-strong-community/setting-guidelines-for-repository-contributors)
`LICENSE` | The license file for the project. | [Documentation](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/licensing-a-repository)
`README.md` | The file you are reading now, should contain info about the integration, installation and configuration instructions. | [Documentation](https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax)
`requirements.txt` | Python packages used for development/lint/testing this integration. | [Documentation](https://pip.pypa.io/en/stable/user_guide/#requirements-files)

## How?

1. Open this repository in Visual Studio Code devcontainer (Preferably with the "`Dev Containers: Clone Repository in Named Container Volume...`" option).
1. Run the `scripts/develop` to start HA and test out this integration.
