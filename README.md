# Routeur solaire MSunPV
Le **MSunPV** est un routeur solaire permettant d'utiliser l'éxèdent de production solaire des panneaux pour par exemple recharger un ballon d'eau chaude ou alimenter un radiateur, au lieu de l'injecter sur le réseau.

Tous les détails sur le **MSunPV** sont sur le site de [Ard-Tek](https://ard-tek.com).


# L'intégration MSunPV

Cette intégration permet le suivi des mesures du routeur **MSunPV**.
- Production instantanée des panneaux solaire
- Consomation ou injection instantanée sur le réseau électrique
- Taux de routage vers le ballon d'eau chaude
- Température du ballon (si sonde installée)
- Production Solaire journalière et cumulée
- Consomation réseau journalière
- Injection réseau journalière
- Infos routeur (modele, version, config, etc.)

## A venir
- Etat des commandes Manu/Auto Ballon et Radiateur
- Etat des commandes TestRouteur (Inject, Zero, Moyen, Fort)
- Consigne Température Ballon
- Automatisation

## Installation
Cette intégration nécessite HACS.

- Dans HACS, à l'aide du menu (trois points en haut à droite), ajouter un **Dépot personalisé** de type **Intégration** :
    - dépot : https://github.com/pvergezac/MSunPVIntegration
- Dans HACS, Rechercher l'intégration **MSunPV Intégration**.
- Télécherger l'intégration
- Relancer Home Assistant
- Dans : Paramètres / Appareils et services / Intégration
    - Ajouter une intégration
    - rechercher **MSunPV Intégration**

<p><br>Ou utilisez le bouton ci-dessous :<br>

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=pvergezac&repository=https%3A%2F%2Fgithub.com%2Fpvergezac%2Fmsunpvintegration&category=Integration)<br>
<br>

## Configuration
Saisicez l'adresse locale de votre routeur.
- Ex : http://192.168.xxx.xxx
<p><br>

***
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
