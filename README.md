# NeoMundi AI Periscope

**Version: v0.1.0 — Experimental**

[🇫🇷 Version française](#-version-française) · [🇬🇧 English version](#-english-version)

---

# 🇫🇷 Version française

## NeoMundi AI Periscope v0.1.0

### Lancez votre propre campagne de mesure IA et repartez avec un snapshot partageable

**AI Periscope** est un launcher expérimental léger permettant de lancer vos propres campagnes de prompts vers le modèle IA de votre choix en passant par la couche de mesure **NeoMundi ControlTower**.

Vous choisissez librement :

- votre provider IA ;
- votre modèle ;
- votre propre fichier de prompts ;
- le nombre de répétitions par prompt ;
- vos paramètres de génération.

AI Periscope utilise ensuite NeoMundi ControlTower pour exécuter et mesurer la campagne.

À la fin, le workflow est conçu pour produire :

- les résultats de campagne en formats exploitables ;
- un **Campaign Snapshot HTML** ;
- un **Campaign Snapshot PDF** ;
- un snapshot éventuellement **co-brandé** avec votre organisation.

Le principe :

```text
Votre dataset
      ↓
Votre provider + votre modèle
      ↓
AI Periscope
      ↓
NeoMundi ControlTower
      ↓
Mesure runtime
      ↓
Résultats de campagne
      ↓
HTML + PDF Snapshot
```

> **Vous définissez l’expérience.  
> AI Periscope fournit le chemin vers la mesure.**

---

## Ce que vous obtenez

Une campagne AI Periscope est destinée à produire un dossier de résultats de ce type :

```text
results/
└── campaign_...
    ├── campaign_results.json
    ├── campaign_results.csv
    ├── AI_PERISCOPE_SNAPSHOT.html
    └── AI_PERISCOPE_SNAPSHOT.pdf
```

### JSON / CSV

Ces fichiers permettent de conserver et réutiliser les observations de campagne.

Ils peuvent notamment servir pour :

- une analyse complémentaire ;
- un benchmark ;
- un reporting externe ;
- un traitement Python ;
- une comparaison entre campagnes ;
- une intégration dans un autre système.

### HTML

Le HTML constitue une représentation légère et réutilisable du snapshot.

### PDF

Le PDF constitue un artefact partageable et figé de la campagne.

Le snapshot peut inclure :

- votre organisation ;
- votre logo, de manière optionnelle ;
- l’identité NeoMundi ;
- le provider ;
- le modèle ;
- le fichier de prompts ;
- le nombre d’observations ;
- les principaux signaux disponibles ;
- la couverture ;
- les erreurs éventuelles ;
- les limites d’interprétation.

> **Signal mesuré, pas verdict.**

Le snapshot résume les observations réalisées pendant la campagne.

Il ne constitue ni un verdict factuel, ni une certification de sécurité, ni une conclusion réglementaire.

---

## À quoi sert AI Periscope ?

AI Periscope peut par exemple être utilisé pour tester :

- des questions juridiques ;
- des questions réglementaires ;
- des prompts métier ;
- des scénarios de conformité ;
- des questions scientifiques ;
- des cas d’usage internes ;
- un benchmark ;
- un dataset expérimental ;
- la répétabilité des réponses ;
- la variabilité comportementale ;
- plusieurs campagnes successives sur un même corpus.

Vous pouvez envoyer chaque prompt une seule fois ou le répéter autant de fois que nécessaire.

Exemple :

```text
10 prompts × 10 répétitions = 100 requêtes
```

Autre exemple :

```text
50 prompts × 20 répétitions = 1 000 requêtes
```

C’est vous qui définissez la campagne.

---

# 1. Ce dont vous avez besoin

Avant de commencer, vous aurez besoin de :

1. un compte NeoMundi ControlTower ;
2. une clé API NeoMundi ;
3. une clé API valide chez le provider IA de votre choix ;
4. Python installé sur votre ordinateur.

Deux clés sont utilisées.

### Clé NeoMundi

Elle permet à AI Periscope de communiquer avec NeoMundi ControlTower.

### Clé provider

Elle permet à ControlTower d’appeler le modèle que vous avez choisi auprès de votre provider.

Exemple :

```text
Clé NeoMundi
+
Clé de votre provider
```

Ces deux clés sont différentes.

---

# 2. Créer votre compte NeoMundi

Ouvrez :

https://controltower.neomundi.io/welcome

Créez votre compte en suivant les indications affichées.

Votre compte peut nécessiter une validation avant que votre accès soit complètement actif.

Attendez cette validation avant de lancer votre première campagne.

---

# 3. Récupérer votre clé API NeoMundi

Une fois votre compte activé :

1. connectez-vous à ControlTower ;
2. accédez à votre environnement ;
3. récupérez votre clé API NeoMundi ;
4. conservez-la dans un endroit privé.

Cette clé sera utilisée localement par AI Periscope.

### Important

Ne publiez jamais votre clé API.

Ne la placez jamais :

- dans un dépôt GitHub public ;
- dans une capture d’écran ;
- dans un message public ;
- dans un document partagé ;
- dans un ticket support public.

---

# 4. Vérifier vos requêtes disponibles

AI Periscope utilise des requêtes NeoMundi lorsque la campagne est exécutée.

Vous pouvez commencer avec les requêtes disponibles sur votre compte, notamment les requêtes de démarrage lorsqu’elles sont proposées avec votre accès, ou charger votre compte pour une campagne plus importante.

AI Periscope v0.1.0 est conçu autour du parcours de mesure **Tier 1**.

Avant de lancer une campagne, calculez toujours son volume.

Exemple :

```text
20 prompts
×
5 répétitions
=
100 requêtes
```

---

# 5. Obtenir votre clé provider

AI Periscope ne remplace pas votre compte chez votre provider IA.

Vous devez disposer :

- de votre propre compte provider ;
- d’une clé API valide ;
- des droits nécessaires pour appeler le modèle choisi.

La liste des providers actuellement pris en charge par NeoMundi ControlTower est maintenue dans la documentation officielle :

[**Voir les providers actuellement pris en charge →**](https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md#5-providers-actuellement-pris-en-charge)

Cette documentation est la source de référence pour :

- les providers supportés ;
- les valeurs exactes à utiliser dans `provider:` ;
- les exemples de modèles ;
- les éventuelles particularités d’intégration.

AI Periscope n’a donc pas besoin de dupliquer cette liste.

---

# 6. Télécharger AI Periscope depuis GitHub

Ouvrez :

https://github.com/neomundi-io/neomundi-ai-periscope

Si vous n’êtes pas développeur, la méthode la plus simple consiste à télécharger le dépôt sous forme de ZIP.

### Étape par étape

1. cliquez sur le bouton vert **Code** ;
2. un menu s’ouvre ;
3. cliquez sur **Download ZIP** ;
4. attendez la fin du téléchargement.

Vous obtenez un fichier ressemblant à :

```text
neomundi-ai-periscope-main.zip
```

---

# 7. Décompresser AI Periscope

Sur Windows :

1. ouvrez votre dossier **Téléchargements** ;
2. trouvez `neomundi-ai-periscope-main.zip` ;
3. faites un clic droit ;
4. choisissez **Extraire tout** ;
5. choisissez l’emplacement souhaité ;
6. cliquez sur **Extraire**.

Vous obtenez votre copie locale de AI Periscope.

Par exemple :

```text
Documents
└── neomundi-ai-periscope-main
```

Les modifications réalisées dans cette copie ne modifient pas le dépôt GitHub original.

---

# 8. Vérifier les fichiers

Dans le dossier AI Periscope, vous devez notamment trouver :

```text
RUN_PERISCOPE.ps1
periscope.py
snapshot.py
config.yaml
requirements.txt
README.md
QUICKSTART.md
assets/
input/
```

---

# 9. Ajouter vos deux clés

Ouvrez :

```text
RUN_PERISCOPE.ps1
```

Le launcher doit contenir deux champs utilisateur :

```powershell
$NEOMUNDI_API_KEY = ""
$PROVIDER_API_KEY = ""
```

### Ajouter votre clé NeoMundi

Exemple fictif :

```powershell
$NEOMUNDI_API_KEY = "votre-cle-neomundi"
```

### Ajouter votre clé provider

Exemple fictif :

```powershell
$PROVIDER_API_KEY = "votre-cle-provider"
```

La clé utilisée ici doit appartenir au provider déclaré dans `config.yaml`.

Ne partagez jamais vos vraies clés.

---

# 10. Configurer votre campagne

Ouvrez :

```text
config.yaml
```

La structure est :

```yaml
provider:
model:

prompt_file:
runs_per_prompt:

temperature:
max_tokens:
```

C’est ici que vous définissez votre expérience.

---

# 11. Choisir votre provider

Dans :

```yaml
provider:
```

indiquez la valeur exacte du provider.

Exemple :

```yaml
provider: openai
```

ou :

```yaml
provider: anthropic
```

ou :

```yaml
provider: mistral
```

La liste officielle et à jour se trouve ici :

[**Providers NeoMundi ControlTower →**](https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md#5-providers-actuellement-pris-en-charge)

Utilisez exactement la valeur documentée.

---

# 12. Choisir votre modèle

Dans :

```yaml
model:
```

indiquez l’identifiant exact du modèle que vous souhaitez appeler.

Exemple :

```yaml
provider: openai
model: VOTRE_MODELE
```

Le modèle n’est pas imposé par AI Periscope.

Il dépend :

- de votre provider ;
- de votre compte ;
- de vos droits ;
- des modèles disponibles au moment de votre campagne.

Pour les informations à jour, consultez :

[**Guide providers ControlTower →**](https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md)

---

# 13. Préparer votre fichier de prompts

AI Periscope n’impose aucun dataset.

Vous pouvez créer le fichier texte de votre choix.

Exemples :

```text
questions_rgpd.txt
questions_ai_act.txt
legal_test.txt
benchmark.txt
my_experiment.txt
```

Vous pouvez utiliser le nom que vous voulez.

---

# 14. Écrire vos prompts

Chaque prompt doit être séparé du suivant par :

```text
---
```

Exemple :

```text
Quels sont les principaux risques juridiques liés à l'utilisation d'un assistant IA dans les ressources humaines ?

---

Quelles obligations de transparence peuvent s'appliquer à un système d'IA ?

---

Dans quelles conditions des données personnelles peuvent-elles être utilisées pour entraîner un modèle ?
```

Vous pouvez utiliser :

- 1 prompt ;
- 10 prompts ;
- 100 prompts ;
- plusieurs centaines de prompts.

AI Periscope ne fixe pas la taille du dataset.

---

# 15. Placer votre fichier de prompts

Le dossier recommandé est :

```text
input/
```

Par exemple :

```text
input/questions_rgpd.txt
```

Vous pouvez toutefois utiliser un autre fichier ou emplacement.

---

# 16. Indiquer le fichier dans `config.yaml`

Exemple :

```yaml
prompt_file: input/questions_rgpd.txt
```

Si votre fichier s’appelle :

```text
my_experiment.txt
```

utilisez :

```yaml
prompt_file: input/my_experiment.txt
```

---

# 17. Choisir le nombre de répétitions

Le paramètre :

```yaml
runs_per_prompt:
```

détermine combien de fois chaque prompt sera envoyé au modèle.

Exemple :

```yaml
runs_per_prompt: 1
```

Une exécution par prompt.

Avec :

```yaml
runs_per_prompt: 10
```

chaque prompt est exécuté dix fois.

Avec :

```yaml
runs_per_prompt: 100
```

chaque prompt est exécuté cent fois.

### Exemple

```text
5 prompts × 10 répétitions = 50 requêtes
```

---

# 18. Temperature — optionnel

Vous pouvez définir `temperature` si votre provider et votre modèle acceptent ce paramètre.

Exemple :

```yaml
temperature: 0.2
```

Si vous ne souhaitez pas imposer ce paramètre :

```yaml
temperature:
```

Laissez le champ vide.

---

# 19. Max tokens — optionnel

Vous pouvez définir une limite de génération si nécessaire.

Exemple :

```yaml
max_tokens: 2000
```

Si vous ne souhaitez pas imposer cette limite depuis AI Periscope :

```yaml
max_tokens:
```

Laissez le champ vide.

ControlTower et le provider appliqueront alors leur comportement prévu.

---

# 20. Exemple de configuration complète

```yaml
provider: openai
model: VOTRE_MODELE

prompt_file: input/questions_rgpd.txt
runs_per_prompt: 10

temperature:
max_tokens:
```

Cela signifie :

```text
Provider        → OpenAI
Modèle          → modèle choisi
Dataset         → questions_rgpd.txt
Répétitions     → 10 par prompt
Temperature     → non imposée
Max tokens      → non imposé
```

---

# 21. Ajouter votre logo — optionnel

Le logo NeoMundi utilisé pour le snapshot se trouve dans :

```text
assets/LOGO_NeoMundi_Controltower.png
```

Vous pouvez également ajouter le logo de votre organisation dans :

```text
assets/organization_logo.png
```

Le logo utilisateur est facultatif.

Lorsqu’il est fourni, le snapshot peut afficher :

```text
[Votre organisation] + [NeoMundi]
```

L’identité de votre organisation présente la campagne.

L’identité NeoMundi identifie la couche de mesure utilisée.

---

# 22. Vérifier Python

AI Periscope nécessite Python.

Ouvrez PowerShell et tapez :

```powershell
python --version
```

Si Python est disponible, vous devez obtenir quelque chose ressemblant à :

```text
Python 3.x.x
```

Si Python n’est pas installé, installez-le avant de continuer.

---

# 23. Ouvrir PowerShell dans le dossier AI Periscope

Vous devez ouvrir PowerShell dans le dossier contenant :

```text
RUN_PERISCOPE.ps1
```

Exemple :

```text
C:\Users\VotreNom\Documents\neomundi-ai-periscope-main
```

---

# 24. Lancer AI Periscope

Dans PowerShell :

```powershell
.\RUN_PERISCOPE.ps1
```

Puis appuyez sur **Entrée**.

---

# 25. Vérifications réalisées avant la campagne

AI Periscope vérifie notamment :

- que `config.yaml` existe ;
- que `periscope.py` existe ;
- que Python est disponible ;
- que la clé NeoMundi est renseignée ;
- que la clé provider est renseignée ;
- que le provider est renseigné ;
- que le modèle est renseigné ;
- que le fichier de prompts existe.

---

# 26. Vérifier la taille de la campagne

Avant les appels, AI Periscope doit afficher notamment :

```text
Provider
Model
Prompt file
Prompts
Runs per prompt
Total requests
```

Exemple :

```text
Prompts         : 20
Runs per prompt : 50
Total requests  : 1000
```

Cela signifie que la campagne prévoit 1 000 requêtes.

Vérifiez toujours ce chiffre avant une campagne importante.

---

# 27. Ce que fait AI Periscope

Le parcours est :

```text
Votre fichier de prompts
        ↓
AI Periscope
        ↓
NeoMundi ControlTower
        ↓
Provider choisi
        ↓
Modèle choisi
        ↓
Réponse IA
        ↓
Mesure runtime NeoMundi
        ↓
Résultats
```

Vous conservez :

```text
votre provider
+
votre modèle
+
votre dataset
+
vos paramètres
```

AI Periscope ajoute le chemin vers la mesure NeoMundi.

---

# 28. Résultats de campagne

AI Periscope est conçu pour conserver les observations dans un dossier dédié.

Structure cible :

```text
results/
└── campaign_YYYYMMDD_HHMMSS/
    ├── campaign_results.json
    └── campaign_results.csv
```

### JSON

Utile pour :

- les intégrations ;
- les traitements programmatiques ;
- l’archivage structuré ;
- les benchmarkeurs ;
- les systèmes externes.

### CSV

Utile pour :

- Excel ;
- les analyses tabulaires ;
- Python / pandas ;
- les analyses statistiques ;
- les comparaisons de campagne.

---

# 29. Générer le snapshot

Le fichier :

```text
snapshot.py
```

transforme les résultats d’une campagne en snapshot.

Le parcours est :

```text
campaign_results
        ↓
snapshot.py
        ↓
AI_PERISCOPE_SNAPSHOT.html
        ↓
AI_PERISCOPE_SNAPSHOT.pdf
```

Le HTML constitue la représentation source du snapshot.

Le PDF est généré à partir de cette représentation lorsque le moteur PDF est disponible.

---

# 30. Exemple de génération du snapshot

Exemple :

```powershell
python snapshot.py `
  --input "results/campaign_YYYYMMDD_HHMMSS/campaign_results.json" `
  --config "config.yaml" `
  --neomundi-logo "assets/LOGO_NeoMundi_Controltower.png" `
  --organization-name "Votre organisation" `
  --organization-logo "assets/organization_logo.png"
```

Si vous ne souhaitez pas utiliser de logo organisationnel, vous pouvez omettre :

```text
--organization-logo
```

---

# 31. Contenu du snapshot

Le snapshot peut notamment présenter :

```text
Organisation
Provider
Model
Prompt file
Date
Nombre d'observations

Stabilité moyenne
ΔG moyen
Taux FLAG
Latence moyenne
Tokens moyens
Couverture
Erreurs éventuelles
Prompt le plus variable
```

Seules les métriques réellement disponibles dans les résultats doivent être présentées.

---

# 32. HTML et PDF

Le générateur peut produire :

```text
AI_PERISCOPE_SNAPSHOT.html
AI_PERISCOPE_SNAPSHOT.pdf
```

Le HTML reste utilisable même si la génération PDF n’est pas disponible dans l’environnement local.

Pour le PDF, `snapshot.py` peut utiliser :

1. Playwright / Chromium ;
2. WeasyPrint.

---

# 33. Frontière d’interprétation

AI Periscope expose des **signaux de mesure runtime**.

Ces signaux ne déterminent pas automatiquement :

- la vérité absolue ;
- la sécurité générale d’un modèle ;
- la conformité réglementaire ;
- la décision métier ;
- la causalité d’un changement.

Une revue humaine, un oracle externe ou une autre couche spécialisée peut être nécessaire selon le cas d’usage.

> **Signal mesuré, pas verdict.**

---

# 34. Liberté expérimentale

AI Periscope ne vous impose pas :

- un benchmark ;
- un dataset ;
- un provider ;
- un modèle ;
- un domaine ;
- un nombre de prompts ;
- un nombre de répétitions ;
- un protocole expérimental particulier.

Vous construisez votre campagne.

AI Periscope fournit le chemin vers la mesure.

---

# 35. Sécurité

Votre copie locale de :

```text
RUN_PERISCOPE.ps1
```

peut contenir vos vraies clés API.

Cette copie devient donc privée.

Ne republiez jamais le fichier avec des clés réelles.

Avant de partager le launcher, remettez :

```powershell
$NEOMUNDI_API_KEY = ""
$PROVIDER_API_KEY = ""
```

Ne partagez jamais vos clés :

- dans un email ;
- dans une capture d’écran ;
- dans un chat ;
- dans un ticket public ;
- dans un dépôt GitHub ;
- dans un document public.

---

# 36. Structure du repo

```text
neomundi-ai-periscope/
│
├── RUN_PERISCOPE.ps1
├── periscope.py
├── snapshot.py
├── config.yaml
├── requirements.txt
├── README.md
├── QUICKSTART.md
│
├── assets/
│   ├── README.md
│   ├── LOGO_NeoMundi_Controltower.png
│   └── organization_logo.png
│
├── input/
│   └── prompts.txt
│
└── results/
    └── campaign_...
```

### `RUN_PERISCOPE.ps1`

Launcher principal.

Il récupère localement les deux clés et démarre AI Periscope.

### `periscope.py`

Moteur de campagne.

Il lit la configuration, charge les prompts et transmet les requêtes à NeoMundi ControlTower.

### `snapshot.py`

Générateur léger de snapshot HTML/PDF.

### `config.yaml`

Configuration de la campagne.

### `assets/`

Contient les éléments visuels.

### `input/`

Contient les fichiers de prompts.

### `results/`

Contient les résultats de campagne et les snapshots.

---

# 37. Besoin d’un guide très court ?

Consultez :

[**QUICKSTART.md →**](./QUICKSTART.md)

---

# 38. Besoin d’aide pour l’installation ?

Copiez le prompt suivant dans votre assistant IA préféré :

```text
Je souhaite installer et utiliser NeoMundi AI Periscope v0.1.0 sur mon ordinateur.

Voici le dépôt GitHub :

https://github.com/neomundi-io/neomundi-ai-periscope

Je ne suis pas développeur.

Guide-moi UNE SEULE ÉTAPE À LA FOIS.

Ne me donne jamais plusieurs étapes simultanément.

À chaque étape :

1. explique-moi en une phrase ce que nous allons faire ;
2. indique-moi exactement où cliquer ou quelle commande copier ;
3. attends que je te confirme que l'étape est terminée avant de continuer ;
4. si je t'envoie une capture d'écran, vérifie-la avant de poursuivre ;
5. ne me demande jamais de partager mes vraies clés API dans le chat ;
6. signale-moi clairement toute action susceptible de publier une clé API.

Je dois pouvoir :

- télécharger AI Periscope depuis GitHub ;
- décompresser le ZIP ;
- vérifier Python ;
- renseigner localement ma clé NeoMundi ;
- renseigner localement la clé de mon provider ;
- consulter la liste officielle des providers pris en charge ;
- configurer config.yaml ;
- choisir mon provider ;
- choisir mon modèle ;
- utiliser mon propre fichier de prompts ;
- choisir le nombre de répétitions ;
- lancer RUN_PERISCOPE.ps1 ;
- récupérer les résultats JSON et CSV ;
- ajouter éventuellement le logo de mon organisation ;
- générer le snapshot HTML et PDF ;
- comprendre et corriger les éventuels messages d'erreur.

Commence uniquement par la première étape et attends ma réponse.
```

---

# Version

**NeoMundi AI Periscope v0.1.0**

**Status: Experimental launcher**

Cette première version poursuit volontairement un objectif simple :

> permettre à un utilisateur de lancer sa propre campagne à travers la couche de mesure NeoMundi avec un minimum d’intégration, puis de transformer les observations produites en artefacts légers, réutilisables et partageables.

---

# NeoMundi

**NeoMundi Research**

Real-time measurement of AI behavior at runtime.

---

# 🇬🇧 English version

## NeoMundi AI Periscope v0.1.0

### Run your own AI measurement campaign and leave with a shareable snapshot

**AI Periscope** is a lightweight experimental launcher for running your own prompt campaigns against the AI model of your choice through the **NeoMundi ControlTower** measurement layer.

You freely choose:

- your AI provider;
- your model;
- your own prompt file;
- repetitions per prompt;
- your generation parameters.

AI Periscope then uses NeoMundi ControlTower to execute and measure the campaign.

The workflow is designed to produce:

- reusable campaign results;
- an **HTML Campaign Snapshot**;
- a **PDF Campaign Snapshot**;
- optional co-branding with your organization.

The flow is intentionally simple:

```text
Your dataset
      ↓
Your provider + your model
      ↓
AI Periscope
      ↓
NeoMundi ControlTower
      ↓
Runtime measurement
      ↓
Campaign results
      ↓
HTML + PDF Snapshot
```

> **You define the experiment.  
> AI Periscope provides the path to measurement.**

---

## What you get

A campaign is designed to produce a results folder such as:

```text
results/
└── campaign_...
    ├── campaign_results.json
    ├── campaign_results.csv
    ├── AI_PERISCOPE_SNAPSHOT.html
    └── AI_PERISCOPE_SNAPSHOT.pdf
```

### JSON / CSV

These files allow observations to be retained and reused for:

- additional analysis;
- benchmarks;
- external reporting;
- Python processing;
- campaign comparison;
- integration with other systems.

### HTML

The HTML file is the lightweight reusable representation of the snapshot.

### PDF

The PDF is the fixed, shareable campaign artifact.

The snapshot may include:

- your organization;
- your optional logo;
- NeoMundi branding;
- provider;
- model;
- prompt file;
- number of observations;
- available measurement signals;
- coverage;
- execution errors;
- interpretation boundaries.

> **Measured signal, not a verdict.**

The snapshot summarizes observations made during the campaign.

It is not a factual verdict, a safety certification, or a regulatory conclusion.

---

# 1. What you need

You need:

1. a NeoMundi ControlTower account;
2. a NeoMundi API key;
3. a valid API key from your AI provider;
4. Python installed on your computer.

Two separate API keys are used:

```text
NeoMundi key
+
Provider key
```

---

# 2. Create your NeoMundi account

Open:

https://controltower.neomundi.io/welcome

Create your account and follow the instructions.

Your account may require validation before access becomes fully active.

---

# 3. Retrieve your NeoMundi API key

Once your account is active:

1. log in to ControlTower;
2. access your environment;
3. retrieve your NeoMundi API key;
4. keep it private.

Never publish this key.

---

# 4. Check your available requests

AI Periscope uses NeoMundi requests during a campaign.

You may begin with the requests available on your account, including introductory requests when provided with your access, or fund your account for larger campaigns.

AI Periscope v0.1.0 is designed around the **Tier 1** measurement path.

Always calculate campaign size before running it.

---

# 5. Get your provider API key

AI Periscope does not replace your provider account.

You need:

- your own provider account;
- a valid API key;
- permission to access the model you want to use.

The current list of providers supported by NeoMundi ControlTower is maintained in the official documentation:

[**See currently supported providers →**](https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md#5-providers-actuellement-pris-en-charge)

This documentation is the canonical source for supported provider values and integration details.

---

# 6. Download AI Periscope

Open:

https://github.com/neomundi-io/neomundi-ai-periscope

For non-developers:

1. click **Code**;
2. click **Download ZIP**;
3. download the file;
4. extract it on your computer.

---

# 7. Check the files

You should find:

```text
RUN_PERISCOPE.ps1
periscope.py
snapshot.py
config.yaml
requirements.txt
README.md
QUICKSTART.md
assets/
input/
```

---

# 8. Add your two API keys

Open:

```text
RUN_PERISCOPE.ps1
```

Fill in:

```powershell
$NEOMUNDI_API_KEY = ""
$PROVIDER_API_KEY = ""
```

The provider key must correspond to the provider selected in `config.yaml`.

Never share your real keys.

---

# 9. Configure your campaign

Open:

```text
config.yaml
```

Use:

```yaml
provider:
model:

prompt_file:
runs_per_prompt:

temperature:
max_tokens:
```

---

# 10. Select your provider

Example:

```yaml
provider: openai
```

Use the exact provider value documented here:

[**NeoMundi ControlTower providers →**](https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md#5-providers-actuellement-pris-en-charge)

---

# 11. Select your model

Example:

```yaml
provider: openai
model: YOUR_MODEL
```

AI Periscope does not impose a model.

Use a model available through your own provider account.

---

# 12. Prepare your prompt file

You may use any text file.

Separate prompts with:

```text
---
```

Example:

```text
First prompt.

---

Second prompt.

---

Third prompt.
```

---

# 13. Select the prompt file

Example:

```yaml
prompt_file: input/my_experiment.txt
```

---

# 14. Choose repetitions

Example:

```yaml
runs_per_prompt: 10
```

If your file contains 5 prompts:

```text
5 × 10 = 50 requests
```

---

# 15. Optional parameters

Temperature:

```yaml
temperature: 0.2
```

or:

```yaml
temperature:
```

Maximum tokens:

```yaml
max_tokens: 2000
```

or:

```yaml
max_tokens:
```

Leave them empty if you do not want AI Periscope to impose them.

---

# 16. Add your organization logo — optional

NeoMundi logo:

```text
assets/LOGO_NeoMundi_Controltower.png
```

Optional organization logo:

```text
assets/organization_logo.png
```

---

# 17. Check Python

Run:

```powershell
python --version
```

You should see:

```text
Python 3.x.x
```

---

# 18. Run AI Periscope

Open PowerShell in the AI Periscope folder.

Run:

```powershell
.\RUN_PERISCOPE.ps1
```

---

# 19. Check campaign size

Before execution, check:

```text
Provider
Model
Prompt file
Prompts
Runs per prompt
Total requests
```

Always verify `Total requests`.

---

# 20. Campaign results

The target results structure is:

```text
results/
└── campaign_YYYYMMDD_HHMMSS/
    ├── campaign_results.json
    └── campaign_results.csv
```

JSON is useful for programmatic reuse and integrations.

CSV is useful for tabular analysis, spreadsheets, benchmarks and statistics.

---

# 21. Generate the snapshot

Use:

```text
snapshot.py
```

Flow:

```text
Campaign results
       ↓
snapshot.py
       ↓
HTML
       ↓
PDF
```

Example:

```powershell
python snapshot.py `
  --input "results/campaign_YYYYMMDD_HHMMSS/campaign_results.json" `
  --config "config.yaml" `
  --neomundi-logo "assets/LOGO_NeoMundi_Controltower.png" `
  --organization-name "Your organization" `
  --organization-logo "assets/organization_logo.png"
```

The organization logo is optional.

---

# 22. Snapshot outputs

The generator can produce:

```text
AI_PERISCOPE_SNAPSHOT.html
AI_PERISCOPE_SNAPSHOT.pdf
```

HTML remains available even when local PDF generation is unavailable.

---

# 23. Interpretation boundary

AI Periscope exposes runtime measurement signals.

It does not automatically determine:

- absolute factual truth;
- general model safety;
- regulatory compliance;
- final business relevance;
- organizational decisions.

Additional analysis, human review or specialized external validation may be required.

> **Measured signal, not a verdict.**

---

# 24. Security

Never publish `RUN_PERISCOPE.ps1` with real keys.

Before sharing, restore:

```powershell
$NEOMUNDI_API_KEY = ""
$PROVIDER_API_KEY = ""
```

Never share keys in:

- screenshots;
- email;
- public repositories;
- public tickets;
- chats;
- public documents.

---

# 25. Repository structure

```text
neomundi-ai-periscope/
│
├── RUN_PERISCOPE.ps1
├── periscope.py
├── snapshot.py
├── config.yaml
├── requirements.txt
├── README.md
├── QUICKSTART.md
│
├── assets/
│   ├── README.md
│   ├── LOGO_NeoMundi_Controltower.png
│   └── organization_logo.png
│
├── input/
│   └── prompts.txt
│
└── results/
    └── campaign_...
```

---

# 26. Quick guide

See:

[**QUICKSTART.md →**](./QUICKSTART.md)

---

# 27. Need installation help?

Copy this prompt into your preferred AI assistant:

```text
I want to install and use NeoMundi AI Periscope v0.1.0.

Repository:

https://github.com/neomundi-io/neomundi-ai-periscope

I am not a developer.

Guide me ONE STEP AT A TIME.

Do not give me several steps at once.

At each step:

1. explain in one sentence what we are doing;
2. tell me exactly where to click or which command to copy;
3. wait until I confirm completion;
4. inspect any screenshot I send before continuing;
5. never ask me to paste real API keys into the chat;
6. warn me before any action that could publish an API key.

I need to:

- download the repository;
- extract it;
- check Python;
- enter my NeoMundi key locally;
- enter my provider key locally;
- consult the official provider list;
- configure config.yaml;
- select my model;
- select my prompt file;
- choose repetitions;
- run RUN_PERISCOPE.ps1;
- retrieve JSON and CSV results;
- optionally add my organization logo;
- generate the HTML and PDF snapshot;
- understand and fix errors.

Start with only the first step and wait for my reply.
```

---

# Version

**NeoMundi AI Periscope v0.1.0**

**Status: Experimental launcher**

The purpose of this first version is deliberately simple:

> allow a user to run their own prompt campaign through the NeoMundi measurement layer with minimal integration and transform the resulting observations into lightweight, reusable and shareable artifacts.

---

# NeoMundi

**NeoMundi Research**

Real-time measurement of AI behavior at runtime.
