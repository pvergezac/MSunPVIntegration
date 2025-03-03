# Routeur solaire MSunPV
Le **MSunPV** est un routeur solaire permettant d'utiliser l'éxèdent de production solaire des panneaux pour par exemple recharger ballon d'eau chaude, ou alimenter un radiateur, au lieu de l'injecter sur le réseau.

Tous les détails sont sur le site d'[Ard-Tek](https://ard-tek.com).


# L'intégration MSunPV

Cette intégration permet le suivi des mesures du routeur **MSunPV**.
- Production instantanée des panneaux solaire
- Consomation ou injection instantanée sur le réseau électrique
- Routage vers le ballon d'eau chaude
- Température du ballon (si sonde installée)
- Production Solaire journalière
- Consomation réseau journalière
- Injection réseau journalière
- Infos routeur (version, config, etc.)

## A venir
- Commande Manu/Auto Bollon et Radiateur
- Commande TestRouteur (Inject, Zero, Moyen, Fort)
- Consigne Température Ballon
- Automatisation

---
---
# Notice for Developpement

The component and platforms in this repository are not meant to be used by a
user, but as a "blueprint" that custom component developers can build
upon, to make more awesome stuff.

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

~~1. Create a new repository in GitHub, using this repository as a template by clicking the "Use this template" button in the GitHub UI.~~
~~1. Open your new repository in Visual Studio Code devcontainer (Preferably with the "`Dev Containers: Clone Repository in Named Container Volume...`" option).~~
~~1. Rename all instances of the `integration_blueprint` to `custom_components/<your_integration_domain>` (e.g. `custom_components/awesome_integration`).~~
~~1. Rename all instances of the `Integration Blueprint` to `<Your Integration Name>` (e.g. `Awesome Integration`).~~
~~1. Run the `scripts/develop` to start HA and test out your new integration.~~

## Next steps

These are some next steps you may want to look into:
- Add tests to your integration, [`pytest-homeassistant-custom-component`](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component) can help you get started.
- Add brand images (logo/icon) to https://github.com/home-assistant/brands.
- Create your first release.
- Share your integration on the [Home Assistant Forum](https://community.home-assistant.io/).
- Submit your integration to [HACS](https://hacs.xyz/docs/publish/start).
