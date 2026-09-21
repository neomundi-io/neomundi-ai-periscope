# NeoMundi AI Periscope

[🇬🇧 English version](./README.md)

## Évaluez les systèmes d’IA avant et après chaque changement — et conservez des preuves reproductibles

AI Periscope exécute des campagnes d’évaluation documentées sur différents
modèles, fournisseurs, prompts et jeux de données à partir des mesures runtime
NeoMundi.

Il transforme les observations obtenues en jeux de données canoniques, analyses
comparables et rapports prêts à éclairer la décision. Ces éléments peuvent
soutenir :

- **l’évaluation de nouveaux modèles et fournisseurs** ;
- **les baselines de préproduction et les comparaisons après mise à niveau** ;
- **les décisions de migration de modèle et de configuration** ;
- **l’audit, la traçabilité et les éléments de preuve de conformité** ;
- **le suivi longitudinal et la comparaison comportementale** ;
- **le FinOps et la revue opérationnelle**.

AI Periscope fournit des éléments de preuve reproductibles. L’organisation
consommatrice conserve l’autorité d’interprétation, de politique et de décision.

**Un moteur de campagne · Plusieurs fournisseurs · Mesures reproductibles · Résultats comparables**

> **Sondez. Comparez. Documentez. Décidez avec le contexte nécessaire.**

### Lancez votre première campagne

1. **Testez AI Periscope localement — aucune clé API requise**

   ```bash
   python -m pip install -e .
   periscope run examples/campaigns/sample_campaign.yaml --simulate
   periscope report sample_release_check --type snapshot --lang both
   ```

2. **Créez votre compte et votre clé API NeoMundi pour les mesures réelles**  
   [Ouvrir la plateforme NeoMundi →](https://controlotower.neomundi.io/welcome)

3. **Configurez une campagne réelle et connectez votre fournisseur**  
   [Suivre le Quickstart complet →](./QUICKSTART.md)

4. **Générez un rapport reproductible**  
   Commencez par un Executive Snapshot ou un Model Release Benchmark.

```text
NeoMundi Runtime Measurement Layer
        |
        v
NeoMundi AI Periscope
        |
        v
Campagne / Benchmark / Baseline / Évaluation
        |
        v
Jeux de données canoniques  ->  Analyse  ->  Bibliothèque de rapports
```

AI Periscope consomme les mesures NeoMundi — il ne les redéfinit pas. Consultez
[`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md).

---

## Évaluez un nouveau modèle d’IA dès sa sortie

Exécutez le même corpus sur un modèle nouvellement publié et sur votre baseline
actuelle.

AI Periscope recueille les mesures runtime NeoMundi, construit un jeu de données
de campagne comparable et produit un rapport de benchmark reproductible.

```bash
periscope run my_campaign.yaml
periscope report my_campaign_id --type model-release-benchmark --lang fr
```

Cas d’usage :

- évaluation d’une nouvelle version de modèle ;
- comparaison de fournisseurs ;
- évaluation d’une migration ;
- changement de version de modèle ;
- baseline de préproduction ;
- comparaison après mise à niveau.

Il ne s’agit **pas d’un classement universel**. Le rapport présente les écarts
mesurés pour un corpus, un protocole et une version de mesure documentés —
jamais « le modèle X est le meilleur modèle ». Consultez
[`docs/BENCHMARK.md`](./docs/BENCHMARK.md).

---

## Deux rapports ouverts, disponibles aujourd’hui

| Rapport | Question traitée | Commande |
|---|---|---|
| **Executive Snapshot** | Qu’est-ce qui a été testé, qu’est-ce qui a changé et quels éléments méritent une attention particulière ? | `periscope report <id> --type snapshot` |
| **Model Release Benchmark** | Comment un modèle nouveau ou différent se compare-t-il sur ce corpus ? | `periscope report <id> --type model-release-benchmark` |

Les deux rapports sont disponibles en HTML + PDF et en français + anglais. Ils
sont construits à partir d’un jeu de données canonique afin qu’un tiers puisse
reproduire les résultats. Consultez
[`docs/REPORTING.md`](./docs/REPORTING.md).

### Rapports avancés — disponibles sur demande

Métrologie complète · Gouvernance / Revue · FinOps · Longitudinal · Éléments de
preuve de conformité · Personnalisé.

Les fonctions d’analyse sous-jacentes sont déjà publiques dans
[`periscope/analysis/`](./periscope/analysis/) — seul le rendu packagé de ces
types de rapports n’est pas distribué dans cette version. Consultez
[`docs/REPORT_LIBRARY.md`](./docs/REPORT_LIBRARY.md) pour connaître le contenu
de chaque rapport.

**Contactez NeoMundi sur [neomundi.io](https://neomundi.io).**

---

## Quickstart

```bash
python -m pip install -e .

# Aucune clé API requise :
periscope run examples/campaigns/sample_campaign.yaml --simulate
periscope report sample_release_check --type snapshot --lang both
```

Parcours complet, incluant une exécution avec les API NeoMundi et fournisseur :
[`QUICKSTART.md`](./QUICKSTART.md).

## Ce qui a été testé doit rester reproductible

Chaque campagne produit :

- un **jeu de données canonique** (`campaign_results.json` / `.csv`) — une ligne
  par observation, avec une séparation stricte entre les champs de mesure
  NeoMundi (`nm_*`), les champs opérationnels de campagne (`op_*`) et toute
  analyse dérivée par Periscope ;
- un **manifeste de campagne** (`campaign_manifest.json`) — empreinte du jeu de
  données, branches expérimentales, répétitions, versions observées du schéma et
  du moteur de mesure, nombre d’erreurs et empreintes des fichiers produits.

Rien n’est masqué : les erreurs d’exécution sont comptabilisées et traçables,
jamais supprimées silencieusement. Consultez
[`docs/CAMPAIGN_MODEL.md`](./docs/CAMPAIGN_MODEL.md).

## Fournisseurs

Seuls les fournisseurs documentés par NeoMundi sont pris en charge — aucun
autre n’est codé en dur au-delà de cette liste
(`periscope/providers/registry.py`) :

```text
openai · anthropic · google (alias gemini) · mistral · cohere · deepseek
xai (alias grok) · perplexity · together · qwen · apertus · euria
```

## CLI

```text
periscope run campaign.yaml [--simulate]
periscope report <campaign_id> --type snapshot [--lang fr|en|both]
periscope report <campaign_id> --type model-release-benchmark [--reference-arm ARM]
```

## Carte de la documentation

| Document | Fonction |
|---|---|
| [`QUICKSTART.md`](./QUICKSTART.md) | Obtenir une première campagne et un premier rapport en quelques minutes |
| [`docs/PRODUCT_ARCHITECTURE.md`](./docs/PRODUCT_ARCHITECTURE.md) | Articulation entre le moteur, la bibliothèque d’analyse et la bibliothèque de rapports |
| [`docs/CAMPAIGN_MODEL.md`](./docs/CAMPAIGN_MODEL.md) | Schéma `campaign.yaml`, plan d’exécution et fournisseurs |
| [`docs/BENCHMARK.md`](./docs/BENCHMARK.md) · [`BASELINE.md`](./docs/BASELINE.md) · [`AUDIT.md`](./docs/AUDIT.md) · [`EVALUATION.md`](./docs/EVALUATION.md) | Bibliothèque d’analyse |
| [`docs/REPORTING.md`](./docs/REPORTING.md) | Les deux rapports ouverts |
| [`docs/REPORT_LIBRARY.md`](./docs/REPORT_LIBRARY.md) | Catalogue complet des rapports, ouverts et sur demande |
| [`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md) | Mesure NeoMundi ou analyse Periscope — la règle qui structure tout le produit |
| [`VERSIONING.md`](./VERSIONING.md) | Version du package ou versions des mesures NeoMundi |
| [`reference/NOTES.md`](./reference/NOTES.md) | Pointeurs vers les sources normatives NeoMundi avec lesquelles le produit est aligné |

## Ce que ce produit ne prétend pas faire

AI Periscope ne certifie pas, ne déclare pas qu’un système est sûr ou dangereux,
conforme ou non conforme, et ne produit pas de classement universel des modèles.
Il mesure par l’intermédiaire de NeoMundi et transforme ces mesures en éléments
de preuve comparables et reproductibles — l’interprétation, la politique et la
décision restent du ressort de l’organisation consommatrice. Consultez
[`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md).

## Référence méthodologique privée

La bibliothèque d’analyse et les rapports ouverts ont été généralisés à partir
du générateur privé de rapports Euria/Fatima de NeoMundi, utilisé ici uniquement
comme référence méthodologique. Ce générateur, sa logique de rapport propre aux
clients et tout jeu de données permettant d’identifier un client ne font
**pas** partie de ce dépôt.

## Licence

[MIT](./LICENSE) — Copyright (c) 2026 NeoMundi.io
