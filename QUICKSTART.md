# NeoMundi AI Periscope — Quick Start

**Version v0.1.0 — Experimental**

[🇫🇷 Français](#-français) · [🇬🇧 English](#-english)

---

# 🇫🇷 Français

## Ce qui va se passer

Avec AI Periscope, vous allez :

1. créer ou utiliser votre compte NeoMundi ControlTower ;
2. utiliser votre propre provider IA et votre propre modèle ;
3. charger votre propre fichier de prompts ;
4. choisir vos paramètres expérimentaux ;
5. lancer votre campagne ;
6. faire passer les requêtes par la couche de mesure NeoMundi ;
7. obtenir à la fin un **snapshot de campagne HTML et PDF**, partageable et éventuellement co-brandé avec votre organisation.

Le principe est simple :

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
Snapshot HTML + PDF
```

Le snapshot peut inclure notamment :

- le provider ;
- le modèle ;
- le nombre de prompts ;
- le nombre total d’observations ;
- les principaux signaux de mesure disponibles ;
- la couverture et les erreurs éventuelles ;
- les limites d’interprétation ;
- le logo NeoMundi ;
- votre nom d’organisation et votre logo, de manière optionnelle.

> **Votre expérience. Votre identité. La mesure NeoMundi.**

---

## Démarrage rapide

### 1. Créez votre compte NeoMundi

Ouvrez :

https://controltower.neomundi.io/welcome

Créez votre compte.

Attendez sa validation si nécessaire.

Une fois votre accès actif, récupérez votre clé API NeoMundi.

Vous pouvez utiliser les requêtes disponibles sur votre compte pour démarrer ou charger votre compte si vous souhaitez lancer une campagne plus importante.

---

### 2. Téléchargez AI Periscope

Ouvrez :

https://github.com/neomundi-io/neomundi-ai-periscope

Cliquez sur :

**Code → Download ZIP**

Téléchargez le fichier ZIP puis décompressez-le sur votre ordinateur.

---

### 3. Ajoutez vos clés API

Ouvrez :

`RUN_PERISCOPE.ps1`

Renseignez votre clé NeoMundi :

```powershell
$NEOMUNDI_API_KEY = ""
```

Puis renseignez **uniquement la clé du provider que vous souhaitez utiliser**.

Exemple avec OpenAI :

```powershell
$OPENAI_API_KEY = ""
```

Laissez les autres clés provider vides.

Ne partagez jamais vos vraies clés API.

---

### 4. Configurez votre campagne

Ouvrez :

`config.yaml`

Renseignez :

```yaml
provider:
model:

prompt_file:
runs_per_prompt:

temperature:
max_tokens:
```

Exemple :

```yaml
provider: openai
model: VOTRE_MODELE

prompt_file: input/mes_questions.txt
runs_per_prompt: 10

temperature:
max_tokens:
```

Vous choisissez librement :

- le provider ;
- le modèle ;
- le fichier de prompts ;
- le nombre de répétitions.

`temperature` et `max_tokens` sont optionnels.

Si vous ne souhaitez pas les imposer, laissez-les vides.

---

### 5. Ajoutez vos prompts

Créez ou utilisez le fichier `.txt` de votre choix.

Exemple :

`input/mes_questions.txt`

Séparez chaque prompt avec :

```text
---
```

Exemple :

```text
Premier prompt.

---

Deuxième prompt.

---

Troisième prompt.
```

Vous pouvez utiliser autant de prompts que nécessaire.

Indiquez simplement le chemin du fichier dans `config.yaml`.

---

### 6. Vérifiez la taille de votre campagne

Le nombre total de requêtes est :

```text
Nombre de prompts × runs_per_prompt
```

Exemple :

```text
10 prompts × 10 répétitions = 100 requêtes
```

Autre exemple :

```text
50 prompts × 20 répétitions = 1 000 requêtes
```

Vérifiez toujours le volume total avant une campagne importante.

---

### 7. Lancez AI Periscope

Ouvrez PowerShell dans le dossier AI Periscope.

Lancez :

```powershell
.\RUN_PERISCOPE.ps1
```

AI Periscope lit votre configuration, utilise votre provider et votre modèle, charge votre fichier de prompts et exécute la campagne via NeoMundi ControlTower.

---

### 8. Récupérez vos résultats

À la fin de la campagne, AI Periscope peut générer un dossier de résultats contenant notamment :

```text
results/
└── campaign_...
    ├── campaign_results.json
    ├── campaign_results.csv
    ├── AI_PERISCOPE_SNAPSHOT.html
    └── AI_PERISCOPE_SNAPSHOT.pdf
```

Le HTML constitue une sortie légère et réutilisable.

Le PDF constitue un artefact partageable de la campagne.

---

### 9. Ajouter votre logo — optionnel

Le logo NeoMundi utilisé par le snapshot se trouve dans :

`assets/LOGO_NeoMundi_Controltower.png`

Vous pouvez également ajouter le logo de votre organisation dans :

`assets/organization_logo.png`

Le snapshot peut alors être généré avec les deux identités.

Votre logo est facultatif.

---

### Besoin de plus de détails ?

Consultez le [README complet](./README.md).

---

# 🇬🇧 English

## What will happen

With AI Periscope, you will:

1. create or use your NeoMundi ControlTower account;
2. use your own AI provider and model;
3. load your own prompt file;
4. choose your experimental parameters;
5. run your campaign;
6. route the requests through the NeoMundi measurement layer;
7. receive a shareable **HTML and PDF Campaign Snapshot**, optionally co-branded with your organization.

The flow is simple:

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
HTML + PDF Snapshot
```

The snapshot may include:

- provider;
- model;
- number of prompts;
- total observations;
- selected available measurement signals;
- coverage and execution errors;
- interpretation boundaries;
- NeoMundi branding;
- your organization name and optional logo.

> **Your experiment. Your identity. NeoMundi measurement.**

---

## Quick Start

### 1. Create your NeoMundi account

Open:

https://controltower.neomundi.io/welcome

Create your account.

Wait for validation if required.

Once your access is active, retrieve your NeoMundi API key.

You can use the requests available on your account to get started or fund your account for a larger campaign.

---

### 2. Download AI Periscope

Open:

https://github.com/neomundi-io/neomundi-ai-periscope

Click:

**Code → Download ZIP**

Download the ZIP file and extract it on your computer.

---

### 3. Add your API keys

Open:

`RUN_PERISCOPE.ps1`

Enter your NeoMundi API key:

```powershell
$NEOMUNDI_API_KEY = ""
```

Then enter **only the API key for the provider you want to use**.

Example with OpenAI:

```powershell
$OPENAI_API_KEY = ""
```

Leave all other provider keys empty.

Never share your real API keys.

---

### 4. Configure your campaign

Open:

`config.yaml`

Set:

```yaml
provider:
model:

prompt_file:
runs_per_prompt:

temperature:
max_tokens:
```

Example:

```yaml
provider: openai
model: YOUR_MODEL

prompt_file: input/my_questions.txt
runs_per_prompt: 10

temperature:
max_tokens:
```

You freely choose:

- provider;
- model;
- prompt file;
- repetitions per prompt.

`temperature` and `max_tokens` are optional.

Leave them empty if you do not want AI Periscope to impose them.

---

### 5. Add your prompts

Create or use any `.txt` file.

Example:

`input/my_questions.txt`

Separate each prompt with:

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

You may use as many prompts as needed.

Simply set the file path in `config.yaml`.

---

### 6. Check your campaign size

The total number of requests is:

```text
Number of prompts × runs_per_prompt
```

Example:

```text
10 prompts × 10 repetitions = 100 requests
```

Another example:

```text
50 prompts × 20 repetitions = 1,000 requests
```

Always check the total volume before running a large campaign.

---

### 7. Run AI Periscope

Open PowerShell in the AI Periscope folder.

Run:

```powershell
.\RUN_PERISCOPE.ps1
```

AI Periscope reads your configuration, uses your provider and model, loads your prompt file and runs the campaign through NeoMundi ControlTower.

---

### 8. Retrieve your results

At the end of the campaign, AI Periscope can generate a results folder containing:

```text
results/
└── campaign_...
    ├── campaign_results.json
    ├── campaign_results.csv
    ├── AI_PERISCOPE_SNAPSHOT.html
    └── AI_PERISCOPE_SNAPSHOT.pdf
```

The HTML is a lightweight reusable output.

The PDF is a shareable campaign artifact.

---

### 9. Add your logo — optional

The NeoMundi logo used by the snapshot is located at:

`assets/LOGO_NeoMundi_Controltower.png`

You may also add your organization logo at:

`assets/organization_logo.png`

The snapshot can then be generated with both identities.

Your organization logo is optional.

---

### Need more detail?

See the [full README](./README.md).

---

**NeoMundi AI Periscope v0.1.0**  
**Experimental launcher**
