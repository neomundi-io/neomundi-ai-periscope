# NeoMundi AI Periscope

**Version: v0.1.0 — Experimental**

[🇫🇷 Version française](#-version-française) · [🇬🇧 English version](#-english-version)

---

# 🇫🇷 Version française

## NeoMundi AI Periscope v0.1.0

### Lancez votre propre campagne de mesure IA et repartez avec un snapshot partageable

**AI Periscope** est un launcher expérimental minimal permettant de lancer vos propres campagnes de prompts vers le modèle IA de votre choix en passant par la couche de mesure **NeoMundi ControlTower**.

Vous choisissez librement :

- votre provider IA ;
- votre modèle ;
- votre propre fichier de prompts ;
- le nombre de répétitions par prompt ;
- vos paramètres de génération.

AI Periscope exécute ensuite votre campagne via NeoMundi ControlTower.

À la fin de la campagne, le dispositif peut produire un **Campaign Snapshot HTML et PDF** présentant de manière simple les principaux éléments de l’expérience et les signaux de mesure disponibles.

Le snapshot peut être **co-brandé** avec :

- l’identité NeoMundi ;
- le nom de votre organisation ;
- votre logo, de manière optionnelle.

Le parcours est volontairement simple :

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
Snapshot HTML + PDF
```

> **Vous définissez l’expérience.  
> AI Periscope fournit le chemin vers la mesure.**

---

## Ce que vous obtenez

Une campagne AI Periscope peut produire un dossier de résultats contenant notamment :

```text
results/
└── campaign_...
    ├── campaign_results.json
    ├── campaign_results.csv
    ├── AI_PERISCOPE_SNAPSHOT.html
    └── AI_PERISCOPE_SNAPSHOT.pdf
```

Le fichier HTML constitue une sortie légère, lisible et réutilisable.

Le PDF constitue un artefact partageable de la campagne.

Le snapshot peut inclure notamment :

- le provider ;
- le modèle ;
- le fichier de prompts utilisé ;
- le nombre total d’observations ;
- les principaux signaux de mesure disponibles ;
- la couverture ;
- les erreurs éventuelles ;
- les informations d’exécution ;
- les limites d’interprétation ;
- le logo NeoMundi ;
- votre nom d’organisation ;
- votre logo, de manière optionnelle.

> **Signal mesuré, pas verdict.**

Le snapshot résume une campagne observée. Il ne constitue ni un verdict factuel, ni une certification de sécurité, ni une conclusion réglementaire.

---

## À quoi sert AI Periscope ?

AI Periscope permet par exemple de tester :

- des questions juridiques ;
- des questions réglementaires ;
- des prompts métier ;
- des scénarios de conformité ;
- des questions scientifiques ;
- des questions internes à une organisation ;
- un benchmark existant ;
- un dataset expérimental ;
- la répétabilité des réponses ;
- la variabilité comportementale d’un modèle ;
- plusieurs campagnes successives sur un même ensemble de prompts.

Vous pouvez envoyer chaque prompt une seule fois ou le répéter autant de fois que vous le souhaitez.

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

Avant de télécharger AI Periscope, vous aurez besoin de :

1. un compte NeoMundi ControlTower ;
2. une clé API NeoMundi ;
3. une clé API du provider IA que vous souhaitez utiliser ;
4. Python installé sur votre ordinateur.

Les deux clés API ont des fonctions différentes.

### Clé NeoMundi

Elle permet à AI Periscope de communiquer avec NeoMundi ControlTower.

### Clé provider

Elle permet d’appeler le modèle que vous avez choisi chez votre provider.

Par exemple :

```text
Clé NeoMundi
+
Clé OpenAI
```

ou :

```text
Clé NeoMundi
+
Clé Anthropic
```

ou :

```text
Clé NeoMundi
+
Clé Mistral
```

---

# 2. Créer votre compte NeoMundi

Ouvrez :

https://controltower.neomundi.io/welcome

Créez votre compte en suivant les indications affichées.

Une fois votre inscription effectuée, votre compte peut nécessiter une validation avant que votre accès soit pleinement actif.

Attendez cette validation avant de lancer votre première campagne.

---

# 3. Récupérer votre clé API NeoMundi

Une fois votre compte activé :

1. connectez-vous à ControlTower ;
2. accédez à votre environnement ;
3. récupérez votre clé API NeoMundi ;
4. conservez-la dans un endroit privé.

Vous utiliserez cette clé plus tard dans AI Periscope.

### Important

Ne publiez jamais votre clé API NeoMundi.

Ne la mettez jamais :

- sur un dépôt GitHub public ;
- dans une capture d’écran ;
- dans un message public ;
- dans un document partagé ;
- dans un ticket support public.

---

# 4. Vérifier vos requêtes disponibles

AI Periscope consomme des requêtes NeoMundi lorsqu’une campagne est exécutée.

Pour commencer, vous pouvez utiliser les requêtes offertes avec votre accès NeoMundi lorsque celles-ci sont disponibles, notamment les **100 requêtes de démarrage**, ou charger votre compte si vous souhaitez lancer une campagne plus importante.

AI Periscope v0.1.0 utilise le parcours de mesure **Tier 1** prévu pour ce launcher expérimental.

Avant de lancer une campagne, vérifiez toujours le nombre total de requêtes que vous allez utiliser.

Exemple :

```text
20 prompts
×
5 répétitions
=
100 requêtes
```

---

# 5. Obtenir une clé API chez votre provider

AI Periscope ne remplace pas votre compte chez le provider IA.

Vous devez disposer de votre propre clé API provider.

AI Periscope v0.1.0 prévoit actuellement les providers suivants :

```text
openai
anthropic
mistral
deepseek
perplexity
cohere
xai
qwen
together
moonshot
```

Vous ne devez renseigner que la clé correspondant au provider que vous souhaitez utiliser.

---

# 6. Télécharger AI Periscope depuis GitHub

Ouvrez :

https://github.com/neomundi-io/neomundi-ai-periscope

Vous arrivez sur la page principale du dépôt.

Si vous n’êtes pas développeur, la méthode la plus simple consiste à télécharger un fichier ZIP.

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
2. trouvez le fichier `neomundi-ai-periscope-main.zip` ;
3. faites un clic droit dessus ;
4. choisissez **Extraire tout** ;
5. choisissez l’emplacement souhaité ;
6. cliquez sur **Extraire**.

Vous obtenez maintenant un dossier normal.

Par exemple :

```text
Documents
└── neomundi-ai-periscope-main
```

C’est votre copie locale de AI Periscope.

Les modifications que vous réalisez dans ce dossier ne modifient pas le dépôt GitHub original.

---

# 8. Vérifier les fichiers

Ouvrez le dossier :

```text
neomundi-ai-periscope-main
```

Vous devez notamment trouver :

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

Le dossier `assets/` contient notamment le logo NeoMundi utilisé pour les snapshots.

---

# 9. Ajouter votre clé NeoMundi

Ouvrez le fichier :

```text
RUN_PERISCOPE.ps1
```

Vous pouvez l’ouvrir avec :

- Bloc-notes ;
- Notepad++ ;
- Visual Studio Code ;
- un autre éditeur de texte.

Repérez :

```powershell
$NEOMUNDI_API_KEY = ""
```

Placez votre clé NeoMundi entre les guillemets.

Exemple fictif :

```powershell
$NEOMUNDI_API_KEY = "votre-cle-neomundi"
```

Ne partagez jamais votre vraie clé.

---

# 10. Ajouter votre clé provider

Dans le même fichier `RUN_PERISCOPE.ps1`, vous trouverez :

```powershell
$OPENAI_API_KEY    = ""
$ANTHROPIC_API_KEY = ""
$MISTRAL_API_KEY   = ""
$DEEPSEEK_API_KEY  = ""
$PPLX_API_KEY      = ""
$COHERE_API_KEY    = ""
$XAI_API_KEY       = ""
$QWEN_API_KEY      = ""
$TOGETHER_API_KEY  = ""
$MOONSHOT_API_KEY  = ""
```

Remplissez **uniquement la clé du provider que vous voulez utiliser**.

Exemple avec OpenAI :

```powershell
$OPENAI_API_KEY = "votre-cle-openai"
```

Exemple avec Mistral :

```powershell
$MISTRAL_API_KEY = "votre-cle-mistral"
```

Laissez les autres champs vides.

Enregistrez ensuite le fichier.

---

# 11. Configurer votre campagne

Ouvrez :

```text
config.yaml
```

La configuration de départ est :

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

# 12. Choisir votre provider

Exemple OpenAI :

```yaml
provider: openai
```

Exemple Anthropic :

```yaml
provider: anthropic
```

Exemple Mistral :

```yaml
provider: mistral
```

Le provider indiqué dans `config.yaml` doit correspondre à la clé provider renseignée dans `RUN_PERISCOPE.ps1`.

---

# 13. Choisir votre modèle

Indiquez ensuite le nom exact du modèle que vous souhaitez utiliser.

Exemple :

```yaml
provider: openai
model: VOTRE_MODELE
```

Le modèle n’est pas imposé par AI Periscope.

Choisissez un modèle accessible avec votre propre compte provider.

Le nom exact du modèle dépend :

- du provider ;
- de votre compte ;
- des modèles actuellement disponibles ;
- de vos droits d’accès.

---

# 14. Préparer votre propre fichier de prompts

AI Periscope n’impose aucun dataset.

Vous pouvez créer le fichier texte de votre choix.

Par exemple :

```text
questions_rgpd.txt
questions_ai_act.txt
legal_test.txt
my_experiment.txt
```

Vous pouvez utiliser le nom que vous voulez.

---

# 15. Écrire vos prompts

Dans votre fichier texte, séparez chaque prompt avec :

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

AI Periscope ne définit pas la taille de votre dataset.

---

# 16. Placer votre fichier de prompts

Le dossier `input/` est prévu pour faciliter l’organisation de vos fichiers.

Par exemple :

```text
input/questions_rgpd.txt
```

Vous pouvez toutefois utiliser un autre emplacement si vous le souhaitez.

---

# 17. Indiquer le fichier à utiliser

Dans `config.yaml`, renseignez :

```yaml
prompt_file: input/questions_rgpd.txt
```

AI Periscope utilisera ce fichier.

Si votre fichier s’appelle `my_experiment.txt`, vous pouvez écrire :

```yaml
prompt_file: input/my_experiment.txt
```

---

# 18. Choisir le nombre de répétitions

Le paramètre :

```yaml
runs_per_prompt:
```

détermine combien de fois chaque prompt sera envoyé au modèle.

Exemple :

```yaml
runs_per_prompt: 1
```

Chaque prompt sera envoyé une fois.

Avec :

```yaml
runs_per_prompt: 10
```

chaque prompt sera envoyé dix fois.

Avec :

```yaml
runs_per_prompt: 100
```

chaque prompt sera envoyé cent fois.

### Exemple

Si votre fichier contient :

```text
5 prompts
```

et que vous utilisez :

```yaml
runs_per_prompt: 10
```

AI Periscope exécutera :

```text
5 × 10 = 50 requêtes
```

---

# 19. Temperature — optionnel

Vous pouvez définir une température si votre modèle accepte ce paramètre.

Exemple :

```yaml
temperature: 0.2
```

Si vous ne souhaitez pas imposer de température :

```yaml
temperature:
```

Laissez simplement le champ vide.

---

# 20. Max tokens — optionnel

Vous pouvez définir une limite si vous le souhaitez.

Exemple :

```yaml
max_tokens: 2000
```

Si vous souhaitez laisser le comportement par défaut de ControlTower et du provider :

```yaml
max_tokens:
```

Laissez simplement le champ vide.

---

# 21. Exemple de configuration complète

```yaml
provider: openai
model: VOTRE_MODELE

prompt_file: input/questions_rgpd.txt
runs_per_prompt: 10

temperature:
max_tokens:
```

Cette configuration signifie :

```text
Provider        → OpenAI
Modèle          → modèle choisi par l'utilisateur
Dataset         → questions_rgpd.txt
Répétitions     → 10 par prompt
Temperature     → non imposée
Max tokens      → non imposé
```

---

# 22. Ajouter le logo de votre organisation — optionnel

Le snapshot utilise le logo NeoMundi situé dans :

```text
assets/LOGO_NeoMundi_Controltower.png
```

Vous pouvez également ajouter votre propre logo dans :

```text
assets/organization_logo.png
```

Le logo utilisateur est facultatif.

Lorsqu’il est fourni, le snapshot peut présenter :

```text
[Votre organisation] + [NeoMundi]
```

L’identité de votre organisation présente la campagne.

L’identité NeoMundi indique la couche de mesure utilisée.

---

# 23. Vérifier Python

AI Periscope nécessite Python.

Ouvrez PowerShell et tapez :

```powershell
python --version
```

Si Python est correctement installé, vous devez obtenir quelque chose ressemblant à :

```text
Python 3.x.x
```

Si Windows indique que Python n’est pas installé, installez Python avant de continuer.

---

# 24. Ouvrir PowerShell dans le dossier AI Periscope

Vous devez lancer PowerShell depuis le dossier contenant :

```text
RUN_PERISCOPE.ps1
```

Par exemple :

```text
C:\Users\VotreNom\Documents\neomundi-ai-periscope-main
```

---

# 25. Lancer AI Periscope

Dans PowerShell, tapez :

```powershell
.\RUN_PERISCOPE.ps1
```

puis appuyez sur **Entrée**.

---

# 26. Ce que vérifie le launcher

AI Periscope vérifie notamment :

- que `config.yaml` existe ;
- que `periscope.py` existe ;
- que `requirements.txt` existe ;
- que Python est disponible ;
- que votre clé NeoMundi est renseignée ;
- que votre provider est renseigné ;
- que la clé correspondant au provider sélectionné est renseignée.

Le launcher sélectionne automatiquement la bonne clé provider en fonction de :

```yaml
provider:
```

---

# 27. Vérifier votre campagne

Lors du lancement, AI Periscope affiche notamment :

```text
Provider
Model
Prompt file
Prompts
Runs per prompt
Total requests
```

Vérifiez particulièrement :

```text
Total requests
```

Exemple :

```text
Prompts         : 20
Runs per prompt : 50
Total requests  : 1000
```

Cela signifie que la campagne effectuera 1 000 requêtes.

---

# 28. Ce que fait AI Periscope

Le parcours est le suivant :

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
Couche de mesure NeoMundi
        ↓
Résultats de campagne
```

AI Periscope permet donc de conserver :

```text
votre provider
+
votre modèle
+
votre dataset
+
vos paramètres
```

tout en ajoutant le chemin vers la mesure NeoMundi.

---

# 29. Générer le snapshot HTML et PDF

Le fichier :

```text
snapshot.py
```

est destiné à transformer les résultats d’une campagne en snapshot partageable.

Le principe est :

```text
Résultats de campagne
        ↓
snapshot.py
        ↓
HTML
        ↓
PDF
```

Le HTML est la sortie source du snapshot.

Le PDF est généré à partir de cette représentation lorsque le moteur PDF nécessaire est disponible.

Le snapshot peut intégrer :

- le logo NeoMundi ;
- le nom de votre organisation ;
- votre logo ;
- le provider ;
- le modèle ;
- le nombre d’observations ;
- les signaux disponibles ;
- les informations de couverture ;
- les limites d’interprétation.

### Exemple de commande

Lorsque vous disposez d’un fichier de résultats compatible :

```powershell
python snapshot.py `
  --input "results/campaign_results.json" `
  --config "config.yaml" `
  --neomundi-logo "assets/LOGO_NeoMundi_Controltower.png" `
  --organization-name "Votre organisation" `
  --organization-logo "assets/organization_logo.png"
```

Le logo d’organisation est optionnel.

---

# 30. Sorties du snapshot

Le générateur peut produire :

```text
AI_PERISCOPE_SNAPSHOT.html
AI_PERISCOPE_SNAPSHOT.pdf
```

Si la génération PDF n’est pas disponible sur votre environnement, le HTML reste généré et utilisable.

---

# 31. Frontière d’interprétation

AI Periscope et son snapshot exposent des signaux de mesure.

Ils ne déterminent pas automatiquement :

- la vérité absolue d’une réponse ;
- la sécurité générale d’un modèle ;
- la conformité juridique complète ;
- la pertinence métier finale ;
- la décision organisationnelle.

Une observation peut nécessiter une analyse complémentaire, une revue humaine ou une couche externe spécialisée.

> **Signal mesuré, pas verdict.**

---

# 32. Liberté expérimentale

AI Periscope ne vous impose pas :

- un benchmark ;
- un dataset ;
- un provider ;
- un modèle ;
- un domaine ;
- un nombre de prompts ;
- un nombre de répétitions ;
- un protocole expérimental.

Vous construisez votre propre campagne.

AI Periscope fournit le launcher et le chemin vers la mesure.

---

# 33. Sécurité

## Ne publiez jamais vos clés API

Votre copie locale de :

```text
RUN_PERISCOPE.ps1
```

peut contenir vos vraies clés API.

Cette copie devient donc **privée**.

Ne republiez jamais ce fichier sur GitHub avec vos clés à l’intérieur.

Avant de partager un launcher ou un dossier, vérifiez toujours que les champs sont redevenus vides :

```powershell
$NEOMUNDI_API_KEY = ""

$OPENAI_API_KEY    = ""
$ANTHROPIC_API_KEY = ""
$MISTRAL_API_KEY   = ""
```

Ne partagez jamais vos clés :

- dans un email ;
- dans une capture d’écran ;
- dans un chat ;
- dans un ticket public ;
- dans un dépôt GitHub ;
- dans un document public.

---

# 34. Structure de AI Periscope

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

Il sélectionne le provider, récupère localement les clés renseignées par l’utilisateur et démarre AI Periscope.

### `periscope.py`

Moteur minimal de la campagne.

Il lit la configuration, charge les prompts et transmet les requêtes à NeoMundi ControlTower.

### `snapshot.py`

Générateur léger de snapshot HTML/PDF.

### `config.yaml`

Configuration libre de la campagne.

### `assets/`

Contient les éléments visuels utilisés par le snapshot.

### `input/`

Emplacement recommandé pour les datasets et fichiers de prompts.

### `results/`

Emplacement destiné aux résultats et aux snapshots générés.

---

# 35. Vous ne savez pas télécharger ou lancer le repo ?

Copiez le prompt ci-dessous dans votre assistant IA préféré.

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
- vérifier que Python est installé ;
- ouvrir RUN_PERISCOPE.ps1 ;
- renseigner localement ma clé NeoMundi ;
- renseigner localement la clé de mon provider ;
- configurer config.yaml ;
- choisir mon provider ;
- choisir mon modèle ;
- utiliser mon propre fichier texte de prompts ;
- choisir le nombre de répétitions par prompt ;
- lancer RUN_PERISCOPE.ps1 ;
- récupérer les résultats ;
- ajouter éventuellement le logo de mon organisation ;
- générer le snapshot HTML et PDF ;
- comprendre et corriger les éventuels messages d'erreur.

Commence uniquement par la première étape et attends ma réponse.
```

---

# Version

**NeoMundi AI Periscope v0.1.0**

**Status: Experimental launcher**

Cette première version vise volontairement un objectif simple :

> permettre à un utilisateur de lancer sa propre campagne de prompts à travers la couche de mesure NeoMundi avec un minimum d’intégration, puis de transformer les observations en un artefact léger et partageable.

---

# NeoMundi

**NeoMundi Research**

Real-time measurement of AI behavior at runtime.

---

# 🇬🇧 English version

## NeoMundi AI Periscope v0.1.0

### Run your own AI measurement campaign and leave with a shareable snapshot

**AI Periscope** is a minimal experimental launcher designed to run your own prompt campaigns against the AI model of your choice through the **NeoMundi ControlTower** measurement layer.

You freely choose:

- your AI provider;
- your model;
- your own prompt file;
- the number of repetitions per prompt;
- your generation parameters.

AI Periscope then runs the campaign through NeoMundi ControlTower.

At the end of the campaign, the workflow can produce an **HTML and PDF Campaign Snapshot** presenting the experiment and selected available measurement signals in a simple format.

The snapshot can be **co-branded** with:

- NeoMundi branding;
- your organization name;
- your optional logo.

The flow is deliberately simple:

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

An AI Periscope campaign can produce a results folder containing:

```text
results/
└── campaign_...
    ├── campaign_results.json
    ├── campaign_results.csv
    ├── AI_PERISCOPE_SNAPSHOT.html
    └── AI_PERISCOPE_SNAPSHOT.pdf
```

The HTML file is a lightweight, readable and reusable output.

The PDF is a shareable campaign artifact.

The snapshot may include:

- provider;
- model;
- prompt file;
- total observations;
- selected available measurement signals;
- coverage;
- execution errors;
- execution information;
- interpretation boundaries;
- NeoMundi branding;
- your organization name;
- your optional logo.

> **Measured signal, not a verdict.**

The snapshot summarizes an observed campaign. It is not a factual verdict, a safety certification, or a regulatory conclusion.

---

## What can AI Periscope be used for?

AI Periscope can be used to test:

- legal questions;
- regulatory questions;
- business prompts;
- compliance scenarios;
- scientific questions;
- organization-specific questions;
- existing benchmarks;
- experimental datasets;
- response repeatability;
- behavioral variability;
- successive campaigns on the same prompt set.

You may send each prompt once or repeat it as many times as needed.

Example:

```text
10 prompts × 10 repetitions = 100 requests
```

Another example:

```text
50 prompts × 20 repetitions = 1,000 requests
```

You define the campaign.

---

# 1. What you need

Before downloading AI Periscope, you need:

1. a NeoMundi ControlTower account;
2. a NeoMundi API key;
3. an API key from the AI provider you want to use;
4. Python installed on your computer.

The two API keys have different purposes.

### NeoMundi key

This allows AI Periscope to communicate with NeoMundi ControlTower.

### Provider key

This allows the selected provider to execute the model you choose.

---

# 2. Create your NeoMundi account

Open:

https://controltower.neomundi.io/welcome

Create your account and follow the instructions displayed on screen.

Your account may require validation before access becomes fully active.

Wait for validation before running your first campaign.

---

# 3. Retrieve your NeoMundi API key

Once your account is active:

1. log in to ControlTower;
2. access your environment;
3. retrieve your NeoMundi API key;
4. keep it private.

Never publish your API key.

---

# 4. Check your available requests

AI Periscope consumes NeoMundi requests when a campaign is executed.

You can begin with the requests made available with your NeoMundi access, including the **100 introductory requests** when available, or fund your account for larger campaigns.

AI Periscope v0.1.0 uses the **Tier 1** measurement path intended for this experimental launcher.

Always calculate your campaign size before running it.

---

# 5. Get a provider API key

AI Periscope does not replace your provider account.

You need your own provider API key.

AI Periscope v0.1.0 currently provides launcher fields for:

```text
openai
anthropic
mistral
deepseek
perplexity
cohere
xai
qwen
together
moonshot
```

Only fill in the key for the provider you intend to use.

---

# 6. Download AI Periscope from GitHub

Open:

https://github.com/neomundi-io/neomundi-ai-periscope

For non-developers, the simplest method is to download the repository as a ZIP file.

1. click the green **Code** button;
2. open the menu;
3. click **Download ZIP**;
4. wait for the download to finish.

---

# 7. Extract the ZIP

On Windows:

1. open your Downloads folder;
2. locate the ZIP file;
3. right-click it;
4. choose **Extract All**;
5. select a destination;
6. click **Extract**.

You now have your own local copy of AI Periscope.

---

# 8. Check the files

Inside the folder you should find:

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

# 9. Add your NeoMundi key

Open:

```text
RUN_PERISCOPE.ps1
```

Find:

```powershell
$NEOMUNDI_API_KEY = ""
```

Place your NeoMundi key between the quotation marks.

Never share your real key.

---

# 10. Add your provider key

The launcher contains:

```powershell
$OPENAI_API_KEY    = ""
$ANTHROPIC_API_KEY = ""
$MISTRAL_API_KEY   = ""
$DEEPSEEK_API_KEY  = ""
$PPLX_API_KEY      = ""
$COHERE_API_KEY    = ""
$XAI_API_KEY       = ""
$QWEN_API_KEY      = ""
$TOGETHER_API_KEY  = ""
$MOONSHOT_API_KEY  = ""
```

Fill in only the provider key you intend to use.

Leave all other provider fields empty.

Save the file.

---

# 11. Configure your experiment

Open:

```text
config.yaml
```

The configuration structure is:

```yaml
provider:
model:

prompt_file:
runs_per_prompt:

temperature:
max_tokens:
```

You define the experiment here.

---

# 12. Select your provider

Example:

```yaml
provider: openai
```

The selected provider must match the provider key entered in `RUN_PERISCOPE.ps1`.

---

# 13. Select your model

Enter the exact model identifier available through your provider account.

Example:

```yaml
provider: openai
model: YOUR_MODEL
```

AI Periscope does not impose a model.

---

# 14. Prepare your prompt file

You may use any text file you want.

Separate prompts using:

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

# 15. Select your prompt file

If your file is:

```text
input/my_experiment.txt
```

set:

```yaml
prompt_file: input/my_experiment.txt
```

---

# 16. Choose repetitions

Set:

```yaml
runs_per_prompt:
```

Example:

```yaml
runs_per_prompt: 10
```

With 5 prompts:

```text
5 × 10 = 50 requests
```

---

# 17. Optional parameters

Temperature:

```yaml
temperature: 0.2
```

or leave empty:

```yaml
temperature:
```

Maximum tokens:

```yaml
max_tokens: 2000
```

or leave empty:

```yaml
max_tokens:
```

Leaving them empty means AI Periscope does not impose those parameters.

---

# 18. Add your organization logo — optional

The NeoMundi snapshot logo is located at:

```text
assets/LOGO_NeoMundi_Controltower.png
```

You may also add your own logo at:

```text
assets/organization_logo.png
```

Your organization logo is optional.

---

# 19. Check Python

Open PowerShell and run:

```powershell
python --version
```

You should see something similar to:

```text
Python 3.x.x
```

---

# 20. Run AI Periscope

Open PowerShell in the AI Periscope folder.

Run:

```powershell
.\RUN_PERISCOPE.ps1
```

AI Periscope will check the configuration and start the campaign.

---

# 21. Check campaign size

AI Periscope displays:

```text
Provider
Model
Prompt file
Prompts
Runs per prompt
Total requests
```

Always check the total number of requests before running a large campaign.

---

# 22. How it works

```text
Your prompt file
       ↓
AI Periscope
       ↓
NeoMundi ControlTower
       ↓
Selected provider
       ↓
Selected model
       ↓
AI response
       ↓
NeoMundi measurement layer
       ↓
Campaign results
```

---

# 23. Generate the HTML and PDF snapshot

The file:

```text
snapshot.py
```

is designed to transform campaign results into a shareable snapshot.

The flow is:

```text
Campaign results
       ↓
snapshot.py
       ↓
HTML
       ↓
PDF
```

Example command:

```powershell
python snapshot.py `
  --input "results/campaign_results.json" `
  --config "config.yaml" `
  --neomundi-logo "assets/LOGO_NeoMundi_Controltower.png" `
  --organization-name "Your organization" `
  --organization-logo "assets/organization_logo.png"
```

The organization logo is optional.

---

# 24. Snapshot outputs

The generator can produce:

```text
AI_PERISCOPE_SNAPSHOT.html
AI_PERISCOPE_SNAPSHOT.pdf
```

If PDF generation is not available in your environment, the HTML output remains available.

---

# 25. Interpretation boundary

AI Periscope exposes measurement signals.

It does not automatically determine:

- absolute factual truth;
- general model safety;
- full legal compliance;
- final business relevance;
- organizational decisions.

Additional analysis, human review or specialized external validation may be required.

> **Measured signal, not a verdict.**

---

# 26. Security

Never publish a modified `RUN_PERISCOPE.ps1` containing real keys.

Before sharing the launcher, restore all key fields to empty values.

Never share API keys in:

- screenshots;
- emails;
- public repositories;
- public tickets;
- chats;
- public documents.

---

# 27. Repository structure

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

# 28. Need help installing it?

Copy the prompt below into your preferred AI assistant:

```text
I want to install and use NeoMundi AI Periscope v0.1.0 on my computer.

GitHub repository:

https://github.com/neomundi-io/neomundi-ai-periscope

I am not a developer.

Guide me ONE STEP AT A TIME.

Never give me several steps at once.

At each step:

1. explain in one sentence what we are going to do;
2. tell me exactly where to click or what command to copy;
3. wait until I confirm completion before continuing;
4. if I send you a screenshot, inspect it before moving on;
5. never ask me to paste my real API keys into the chat;
6. warn me clearly before any action that could publish an API key.

I need to:

- download AI Periscope from GitHub;
- extract the ZIP;
- check that Python is installed;
- open RUN_PERISCOPE.ps1;
- add my NeoMundi key locally;
- add my provider API key locally;
- configure config.yaml;
- choose my provider;
- choose my model;
- select my own prompt text file;
- choose repetitions per prompt;
- run RUN_PERISCOPE.ps1;
- retrieve the results;
- optionally add my organization logo;
- generate the HTML and PDF snapshot;
- understand and fix errors if they occur.

Start only with the first step and wait for my reply.
```

---

# Version

**NeoMundi AI Periscope v0.1.0**

**Status: Experimental launcher**

The purpose of this first version is deliberately simple:

> allow a user to run their own prompt campaign through the NeoMundi measurement layer with minimal integration and transform the resulting observations into a lightweight shareable artifact.

---

# NeoMundi

**NeoMundi Research**

Real-time measurement of AI behavior at runtime.
