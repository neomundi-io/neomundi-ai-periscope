# NeoMundi AI Periscope Layer

[🇬🇧 English version](./README.md)

**Sondez, benchmarkez, établissez une baseline et évaluez des systèmes IA à travers modèles, providers et datasets.**

Exécutez des campagnes d'évaluation IA reproductibles à partir des mesures runtime NeoMundi, puis transformez ces observations en datasets comparables, analyses et rapports décisionnels.

**Un moteur de campagne · Plusieurs providers · Mesures reproductibles · Résultats comparables · Preuves prêtes pour la décision**

```text
NeoMundi Runtime Measurement Layer
        |
        v
NeoMundi AI Periscope Layer
        |
        v
Campagne / Benchmark / Baseline / Évaluation
        |
        v
Datasets canoniques  ->  Analyse  ->  Bibliothèque de rapports
```

AI Periscope consomme les mesures NeoMundi — il ne les redéfinit pas. Voir
[`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md).

---

## Benchmarker un nouveau modèle IA dès sa sortie

Rejouez le même corpus contre un modèle nouvellement publié et votre baseline actuelle.

AI Periscope capture les mesures runtime NeoMundi, construit un dataset de campagne comparable et produit un rapport de benchmark reproductible.

```bash
periscope run ma_campagne.yaml
periscope report id_campagne --type model-release-benchmark --lang fr
```

Cas d'usage :

- évaluation de sortie de modèle
- comparaison de providers
- évaluation de migration
- changement de version de modèle
- baseline pré-production
- comparaison post-upgrade

Ce n'est **pas un classement universel**. Le rapport présente des deltas
mesurés sous un corpus, un protocole et une version de mesure documentés —
jamais « Le modèle X est le meilleur modèle ». Voir
[`docs/BENCHMARK.md`](./docs/BENCHMARK.md).

---

## Deux rapports ouverts, disponibles dès aujourd'hui

| Rapport | Répond à | Commande |
|---|---|---|
| **Snapshot exécutif** | Ce qui a été testé, ce qui a changé, ce qui mérite attention | `periscope report <id> --type snapshot` |
| **Benchmark de sortie de modèle** | Comment un nouveau modèle se compare sur ce corpus | `periscope report <id> --type model-release-benchmark` |

Les deux : HTML + PDF, FR + EN, construits à partir d'un dataset canonique
pour que les résultats soient reproductibles par un tiers. Voir
[`docs/REPORTING.md`](./docs/REPORTING.md).

### Reporting avancé — sur demande

Métrologie complète · Gouvernance / Revue · FinOps · Longitudinal · Preuve
de conformité · Rapport sur mesure.

Les fonctions d'analyse sous-jacentes sont déjà publiques dans
[`periscope/analysis/`](./periscope/analysis/) — seul le rendu packagé de
ces rapports n'est pas livré dans cette version. Voir
[`docs/REPORT_LIBRARY.md`](./docs/REPORT_LIBRARY.md) pour le détail de
chacun.

**Contactez NeoMundi via [neomundi.io](https://neomundi.io).**

---

## Démarrage rapide

```bash
python -m pip install -e .

# Sans clé API :
periscope run examples/campaigns/sample_campaign.yaml --simulate
periscope report sample_release_check --type snapshot --lang both
```

Parcours complet, y compris l'exécution contre les API NeoMundi et
providers réelles : [`QUICKSTART.md`](./QUICKSTART.md).

## Ce qui a été testé doit rester reproductible

Chaque campagne produit :

- un **dataset canonique** (`campaign_results.json` / `.csv`) — une ligne
  par observation, avec les champs de mesure NeoMundi (`nm_*`) et les
  champs opérationnels de campagne (`op_*`) strictement séparés de toute
  analyse dérivée Periscope ;
- un **manifeste de campagne** (`campaign_manifest.json`) — hash du
  dataset, arms, répétitions, versions de schéma/moteur de mesure
  observées, nombre d'erreurs, et hashes des fichiers de sortie.

Rien n'est masqué : les erreurs d'exécution sont comptées et traçables,
jamais silencieusement écartées. Voir
[`docs/CAMPAIGN_MODEL.md`](./docs/CAMPAIGN_MODEL.md).

## Providers

Seuls les providers documentés par NeoMundi sont supportés — rien de
hardcodé au-delà de cette liste (`periscope/providers/registry.py`) :

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

## Plan de la documentation

| Document | Objet |
|---|---|
| [`QUICKSTART.md`](./QUICKSTART.md) | Une première campagne et un premier rapport en quelques minutes |
| [`docs/PRODUCT_ARCHITECTURE.md`](./docs/PRODUCT_ARCHITECTURE.md) | Comment le moteur, la bibliothèque d'analyse et la bibliothèque de rapports s'articulent |
| [`docs/CAMPAIGN_MODEL.md`](./docs/CAMPAIGN_MODEL.md) | Le schéma `campaign.yaml`, le plan d'exécution, les providers |
| [`docs/BENCHMARK.md`](./docs/BENCHMARK.md) · [`BASELINE.md`](./docs/BASELINE.md) · [`AUDIT.md`](./docs/AUDIT.md) · [`EVALUATION.md`](./docs/EVALUATION.md) | La bibliothèque d'analyse |
| [`docs/REPORTING.md`](./docs/REPORTING.md) | Les deux rapports ouverts |
| [`docs/REPORT_LIBRARY.md`](./docs/REPORT_LIBRARY.md) | Catalogue complet des rapports, ouverts et sur demande |
| [`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md) | Mesure NeoMundi vs. analyse Periscope — la règle que tout le reste suit |
| [`VERSIONING.md`](./VERSIONING.md) | Version du package vs. versions de mesure NeoMundi |
| [`reference/NOTES.md`](./reference/NOTES.md) | Pointeurs vers les sources normatives NeoMundi avec lesquelles ce produit s'aligne |

## Ce que ce produit ne prétend pas faire

AI Periscope ne certifie pas, ne déclare pas un système sûr ou dangereux,
conforme ou non conforme, et ne produit pas de classement universel des
modèles. Il mesure, via NeoMundi, et transforme ces mesures en preuves
comparables et reproductibles — l'interprétation, la politique et la
décision restent celles de l'organisation consommatrice. Voir
[`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md).

## Référence méthodologique privée

La bibliothèque d'analyse et les rapports ouverts ont été généralisés à
partir du générateur de reporting privé Euria/Fatima de NeoMundi, utilisé
ici uniquement comme référence méthodologique. Ce générateur, sa logique de
reporting spécifique client, et tout dataset identifiant un client ne font
**pas** partie de ce dépôt.

## Licence

[MIT](./LICENSE) — Copyright (c) 2026 NeoMundi.io
