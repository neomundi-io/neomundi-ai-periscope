# NeoMundi AI Periscope — Quick Start

**Version v0.1.0 — Experimental**

[🇫🇷 Français](#-français) · [🇬🇧 English](#-english)

---

# 🇫🇷 Français

## Démarrage rapide

### 1. Créez votre compte NeoMundi

Ouvrez :

https://controltower.neomundi.io/welcome

Créez votre compte, attendez sa validation puis récupérez votre clé API NeoMundi.

Vous pouvez commencer avec les requêtes disponibles sur votre compte ou charger votre compte pour une campagne plus importante.

---

### 2. Téléchargez AI Periscope

Ouvrez :

https://github.com/neomundi-io/neomundi-ai-periscope

Cliquez sur :

**Code → Download ZIP**

Puis décompressez le dossier sur votre ordinateur.

---

### 3. Ajoutez vos clés

Ouvrez :

```text
RUN_PERISCOPE.ps1
```

Renseignez :

```powershell
$NEOMUNDI_API_KEY = ""
```

Puis renseignez **uniquement la clé du provider que vous utilisez**.

Exemple :

```powershell
$OPENAI_API_KEY = ""
```

Ne partagez jamais vos vraies clés API.

---

### 4. Configurez votre campagne

Ouvrez :

```text
config.yaml
```

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

`temperature` et `max_tokens` sont optionnels.

---

### 5. Ajoutez vos prompts

Créez ou utilisez le fichier `.txt` de votre choix.

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

Indiquez ensuite son chemin dans `config.yaml`.

---

### 6. Lancez AI Periscope

Ouvrez PowerShell dans le dossier AI Periscope.

Lancez :

```powershell
.\RUN_PERISCOPE.ps1
```

AI Periscope lit votre dataset, utilise votre provider et votre modèle, puis exécute votre campagne via NeoMundi ControlTower.

---

### Taille de la campagne

```text
Nombre de prompts × runs_per_prompt = nombre total de requêtes
```

Exemple :

```text
10 prompts × 10 répétitions = 100 requêtes
```

Vérifiez toujours le nombre total de requêtes avant une campagne importante.

---

### Besoin de plus de détails ?

Consultez le [README complet](./README.md).

---

# 🇬🇧 English

## Quick Start

### 1. Create your NeoMundi account

Open:

https://controltower.neomundi.io/welcome

Create your account, wait for validation, then retrieve your NeoMundi API key.

You can start with the requests available on your account or fund your account for a larger campaign.

---

### 2. Download AI Periscope

Open:

https://github.com/neomundi-io/neomundi-ai-periscope

Click:

**Code → Download ZIP**

Then extract the folder on your computer.

---

### 3. Add your API keys

Open:

```text
RUN_PERISCOPE.ps1
```

Enter your NeoMundi key:

```powershell
$NEOMUNDI_API_KEY = ""
```

Then enter **only the API key for the provider you want to use**.

Example:

```powershell
$OPENAI_API_KEY = ""
```

Never share your real API keys.

---

### 4. Configure your campaign

Open:

```text
config.yaml
```

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

`temperature` and `max_tokens` are optional.

---

### 5. Add your prompts

Create or use any `.txt` file.

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

Then enter the file path in `config.yaml`.

---

### 6. Run AI Periscope

Open PowerShell in the AI Periscope folder.

Run:

```powershell
.\RUN_PERISCOPE.ps1
```

AI Periscope reads your dataset, uses your provider and model, and runs the campaign through NeoMundi ControlTower.

---

### Campaign size

```text
Number of prompts × runs_per_prompt = total requests
```

Example:

```text
10 prompts × 10 repetitions = 100 requests
```

Always check the total number of requests before running a large campaign.

---

### Need more detail?

See the [full README](./README.md).

---

**NeoMundi AI Periscope v0.1.0**  
**Experimental launcher**
