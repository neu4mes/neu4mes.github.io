# Nuovo paper sul sito

## Cosa fai tu

1. Crea una cartella in `publications/data/new-paper/`, ad esempio:
   ```
   publications/data/new-paper/2026-my-topic/
   ```

2. Metti dentro **solo** questi file:

   | File | Obbligatorio | Note |
   |------|--------------|------|
   | `paper.pdf` | sì | PDF dell’articolo |
   | `figure1.png`, `figure2.png`, … | sì* | Nomi come nel paper (Fig. 1 → `figure1.png`; sottopannelli → `figure1-a.png`, `figure1-b.png`) |
   | `links.yaml` | no | Link YouTube, codice GitHub, DOI (se già li conosci) |

   Esempio `links.yaml`:
   ```yaml
   youtube: "https://www.youtube.com/watch?v=XXXXXXXX"
   code: "https://github.com/tonegas/nnodely-applications/tree/main/..."
   doi: "10.1109/OJITS.XXXXXXXX"
   type: journal   # oppure conference
   ```

3. Apri Cursor (o altro assistente), incolla il **prompt per AI** qui sotto e indica la cartella che hai creato (es. `2026-my-topic`).

4. Controlla in preview: `/publications/` e `/publications/papers/.../`.

Fatto. Non serve creare a mano `index.qmd` né spostare file in `publications/papers/`: lo fa l’AI seguendo il prompt.

---

## Prompt per AI (copia tutto da qui)

```
Sei un agente che aggiorna il sito Quarto neu4mes.github.io aggiungendo un paper journal o conference.

## Input dell’utente

Cartella sorgente (relativa alla root del repo):
  publications/data/new-paper/<NOME_CARTELLA>/

L’utente ha indicato: <NOME_CARTELLA>   ← sostituisci con il nome reale prima di inviare

Contenuto atteso nella cartella:
  - paper.pdf
  - figure*.png (e eventuali figure1-a.png, figure1-b.png, …) con nomi allineati alle figure del PDF
  - links.yaml (opzionale): youtube, code, doi, type (journal|conference)

## Obiettivo

Produrre una pagina paper completa sul sito e spostare/copiare tutti gli asset nei percorsi definitivi. L’utente non deve fare altro dopo il tuo lavoro, salvo verificare il preview.

## Riferimenti obbligatori (leggi prima di scrivere)

Studia lo stile e la struttura di queste pagine già online (non copiarle alla cieca, adattale al nuovo paper):

  - publications/papers/2025-road-friction-aware-abs/index.qmd
  - publications/papers/2026-vehicle-dynamics-msnn/index.qmd
  - publications/papers/2025-itsc-steering-dynamics-a2rl/index.qmd  (conference + video)

Configurazione già attiva (non modificare senza motivo):

  - publications/papers/_metadata.yml  → partial title-metadata (DOI + github code in testata)
  - format/html margin-header globale in _quarto.yml (logo neu4mes)
  - Math: markdown+tex_math_single_backslash, mathjax
  - Listing: publications/index.qmd legge papers/**/index.qmd, sort pub_number desc

## Procedura (esegui in ordine)

### 1. Analizza la cartella sorgente

- Elenca tutti i file in publications/data/new-paper/<NOME_CARTELLA>/.
- Leggi links.yaml se presente.
- Estrai dal PDF paper.pdf (usa pymupdf/fitz se disponibile nel progetto .venv, altrimenti altro metodo):
  titolo, autori (ordine del paper), abstract completo, journal o venue, anno, DOI (se non già in links.yaml),
  didascalie di FIGURE/Fig. per mappare ogni file immagine al numero di figura nel testo.

### 2. Definisci slug e pub_number

- Slug cartella destinazione: YYYY-slug-inglese-corto (minuscolo, trattini, max ~50 caratteri).
  Esempio: 2026-vehicle-dynamics-msnn
- Anno: dal PDF o dal nome cartella utente.
- pub_number: leggi tutti i pub_number in publications/papers/**/index.qmd e usa max + 1
  (ordinamento listing: numero più alto = più in alto).
- order: -{pub_number} (stesso numero con segno meno: serve alla sidebar Quarto per avanti/indietro tra paper).

### 3. Crea la cartella pubblicata

Percorso finale:
  publications/papers/<YYYY-slug>/

Copia (non lasciare solo in new-paper):
  - paper.pdf  → publications/papers/<YYYY-slug>/paper.pdf
  - ogni figure*.png → stessa cartella, stessi nomi
  - main.png: se non fornito dall’utente, copia la figura più rappresentativa (di solito figure1.png o la figura overview) come main.png per la thumbnail del listing

Archivio (opzionale ma consigliato):
  - copia anche paper.pdf in publications/data/paper/ con nome descrittivo (anno + titolo corto)

### 4. Scrivi index.qmd

File: publications/papers/<YYYY-slug>/index.qmd

YAML (campi minimi):
  - title, author (lista "Nome Cognome" come nei paper esistenti, allineata ai profili People se possibile)
  - publication (riga breve per listing, con anno)
  - type: journal o conference (da links.yaml o PDF)
  - categories: ["Journal Articles"|"Conference Papers", "Model-Structured Neural Networks"]
  - journ, year, doi, code (da links.yaml o PDF)
  - image: main.png
  - pdf: paper.pdf
  - pub_number: (calcolato)
  - order: -{pub_number}
  - venue: solo se conference
  - video: solo se conference/video; ID YouTube o URL (da links.yaml)

Corpo:
  ## Abstract
  (testo completo dal PDF, inglese)

  ## Video {#video}
  (solo se youtube in links.yaml o metadati)
  {{< video https://www.youtube.com/watch?v=ID >}}

  ## Model-structured neural network for … {toc-text="abbreviazione corta TOC"}
  - 1–2 paragrafi introduttivi sul MS-NN / contributo (chiaro, non solo bullet)
  - Per OGNI immagine presente nella cartella (escluso main.png se è duplicato di una figura già descritta):
      ### Titolo descrittivo (Figure N)
      Paragrafo che spiega la figura come nel paper (riferimento a Fig./FIGURE del PDF).
      ::: {.paper-network-figures}
      ![](nome-file.png){fig-alt="descrizione accessibilità" width=95%}
      :::
  - Ultima frase: implementazione con framework **nnodely** (come negli altri paper).

Regole di stile:
  - Simboli in LaTeX inline: $v_x$, $\delta$, $\hat{a}_x$, ecc.
  - Non referenziare file immagine inesistenti nella cartella.
  - Non usare network.png o nomi generici se l’utente ha fornito figure1.png, ecc.
  - Non aggiungere filtri Lua né include HTML custom per DOI/code (già gestiti da title-metadata.html).

### 5. Pulizia e vincoli

- NON eseguire scripts/build_publications.py (cancella papers/ e sovrascrive il lavoro manuale).
- NON modificare publications/papers/_metadata.yml, title-metadata.html, _quarto.yml salvo bug evidente.
- La cartella publications/data/new-paper/<NOME_CARTELLA>/ può restare come archivio upload; non è servita al render del sito.

### 6. Verifica

Esegui:
  quarto render publications/papers/<YYYY-slug>/index.qmd

Controlla nell’HTML generato (_site/...):
  - presenza immagini, abstract, sezione MSNN
  - link DOI e github code in testata se presenti in YAML
  - video embed se applicabile

### 7. Report all’utente

Riassumi in italiano:
  - slug e percorso creato
  - pub_number assegnato
  - elenco file copiati
  - URL locale preview: /publications/papers/<YYYY-slug>/
  - eventuali campi mancanti (DOI, code, figure non mappate) da completare a mano in links.yaml
```

---

## Esempio cartella pronta per l’AI

```
publications/data/new-paper/2026-esempio/
├── paper.pdf
├── figure1.png
├── figure2.png
└── links.yaml
```

Dopo il prompt, il sito avrà ad esempio `publications/papers/2026-esempio/` con `index.qmd`, `paper.pdf`, `main.png` e le figure.

Per i **poster** vedi [../new-poster/README.md](../new-poster/README.md).  
Per le **presentazioni** vedi [../new-presentation/README.md](../new-presentation/README.md).  
Per i **related works** vedi [../new-related/README.md](../new-related/README.md).
