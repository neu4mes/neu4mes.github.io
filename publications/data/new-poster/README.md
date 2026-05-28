# Nuovo poster sul sito

## Cosa fai tu

1. Crea una cartella in `publications/data/new-poster/`, ad esempio:
   ```
   publications/data/new-poster/2026-icra-my-workshop/
   ```

2. Metti dentro i file del poster:

   | File | Quando serve | Note |
   |------|----------------|------|
   | `poster.pdf` | poster da mostrare in pagina | PDF del poster (formato verticale/orizzontale) |
   | `paper.pdf` | opzionale | Articolo / extended abstract associato |
   | `poster.png` | opzionale | Anteprima listing; generabile con `scripts/pdf_first_page_preview.py` da `poster.pdf` |
   | `links.yaml` | opzionale | Venue, DOI, link codice |

   **Casi tipici**

   - Solo poster → `poster.pdf` (e opz. `poster.png`)
   - Solo paper (nessun file poster) → `paper.pdf`
   - Poster + paper → `poster.pdf` + `paper.pdf`

   Esempio `links.yaml`:
   ```yaml
   venue: "ICRA 2026 — Late breaking results"
   doi: ""
   code: "https://github.com/tonegas/nnodely-applications/tree/main/..."
   ```

3. Incolla il **prompt per AI** qui sotto e indica la cartella (es. `2026-icra-my-workshop`).

4. Controlla in preview: `/publications/` (sezione Posters) e `/publications/posters/.../`.

Non creare a mano `index.qmd` né la cartella in `publications/posters/`: lo fa l’AI.

---

## Prompt per AI (copia tutto da qui)

```
Sei un agente che aggiorna il sito Quarto neu4mes.github.io aggiungendo un poster alla sezione Publications → Posters.

## Input dell’utente

Tutte le cartelle all'interno di `publications/data/new-poster/` sono cartelle sorgente :
  publications/data/new-poster/<NOME_CARTELLA>/ (relativa alla root del repo)

File attesi (almeno uno tra poster.pdf e paper.pdf):
  - poster.pdf  — PDF del poster
  - paper.pdf   — PDF dell’articolo (opzionale)
  - poster.png  — anteprima (opzionale; se assente e c’è poster.pdf, vedi script sotto)
  - links.yaml  — opzionale: venue, doi, code

Per ogni cartella esegui le seguenti operazioni

## Obiettivo

Creare publications/posters/<YYYY-slug>/ con index.qmd e tutti gli asset copiati. L’utente verifica solo il preview.

## Riferimenti (leggi prima)

  - publications/posters/2025-icra-lbr-nnodely/index.qmd       (solo poster)
  - publications/posters/2026-icra-lbr-msnn-overview/index.qmd (poster + paper)
  - publications/posters/2026-icra-ad-workshop/index.qmd      (solo paper.pdf)

Configurazione sito (non modificare senza motivo):

  - publications/_metadata.yml → title-metadata.html (autori a sinistra; link a destra)
  - Testata poster: poster_pdf → “Download PDF”; article_pdf → “Download paper”; pdf → solo se c’è solo paper.pdf
  - _quarto.yml resources: publications/**/paper.pdf, publications/**/poster.pdf
  - Listing: publications/index.qmd, posters/**/index.qmd, sort pub_number desc
  - Anteprima sotto autori: blocco ::: {.poster-preview} con poster.png (solo se esiste poster.pdf)

## Anteprima prima pagina (unico script automatico supportato)

Se manca `poster.png` e c’è `poster.pdf`, genera solo la thumbnail così:

```bash
.venv/bin/python scripts/pdf_first_page_preview.py \\
  publications/data/new-poster/<NOME_CARTELLA>/poster.pdf \\
  -o publications/posters/<YYYY-slug>/poster.png
```

(dopo aver creato la cartella destinazione, oppure in `new-poster/` prima della copia). Non usare altri script di estrazione figure dal PDF.

## REGOLA CRITICA sui campi YAML (due voci, non tre)

NON usare mai insieme pdf + poster_pdf + article_pdf.

1) Solo poster.pdf nella cartella:
   poster_pdf: poster.pdf
   image: poster.png
   (+ blocco poster-preview nel corpo)
   NON mettere pdf: né article_pdf:

2) Solo paper.pdf nella cartella:
   pdf: paper.pdf
   NON mettere poster_pdf:, article_pdf:, image:, né blocco poster-preview

3) poster.pdf E paper.pdf:
   poster_pdf: poster.pdf
   article_pdf: paper.pdf
   image: poster.png
   (+ blocco poster-preview)
   NON mettere pdf:   ← obbligatorio: pdf: poster.pdf fa sovrascrivere paper.pdf nel sito con il poster

## Procedura

### 1. Analizza publications/data/new-poster/<NOME_CARTELLA>/

- Elenca i file presenti.
- Leggi links.yaml se c’è.
- Da poster.pdf o paper.pdf (pymupdf/fitz in .venv se disponibile) estrai: titolo, autori, venue/evento, anno.

### 2. Slug e pub_number

- Slug: YYYY-slug-corto-inglese (es. 2026-icra-lbr-nnodely).
- pub_number: max tra publications/posters/**/index.qmd + 1 (numero più alto = più in alto in elenco).

### 3. Crea publications/posters/<YYYY-slug>/

Copia dalla cartella new-poster:
  - poster.pdf → se presente
  - paper.pdf  → se presente
  - poster.png → se presente; altrimenti esegui scripts/pdf_first_page_preview.py su poster.pdf

Archivio opzionale: copia i PDF in publications/data/poster/<sottocartella descrittiva>/ se esiste una struttura coerente col resto del repo.

### 4. Scrivi index.qmd

type: poster
categories: ["Posters", "Model-Structured Neural Networks"]
author: lista "Nome Cognome" come negli altri poster
publication e journ/venue: es. "ICRA 2026 — Workshop name (2026)" (da PDF o links.yaml)
year, doi, pub_number

Campi file (vedi REGOLA CRITICA sopra).

Corpo (solo se poster_pdf + poster.png):
```markdown
::: {.poster-preview}
![](poster.png){fig-alt="Poster: <titolo>" width=95%}
:::
```

Nessun abstract né sezione MSNN per i poster.

### 5. Vincoli

- NON eseguire scripts/build_publications.py.
- NON usare il campo YAML paper: (riservato da Quarto).
- NON aggiungere pdf: poster.pdf quando esiste anche paper.pdf.
- La cartella new-poster può restare come archivio upload.

### 6. Verifica

  quarto render publications/posters/<YYYY-slug>/index.qmd

Controlla in _site/publications/posters/<YYYY-slug>/:
  - poster.pdf e paper.pdf distinti (MD5 diversi se entrambi presenti)
  - link Download PDF → poster.pdf; Download paper → paper.pdf (solo se article_pdf)
  - anteprima poster.png visibile solo con poster

### 7. Report (italiano)

  - percorso creato, pub_number, file copiati
  - URL: /publications/posters/<YYYY-slug>/
  - eventuali dati mancanti in links.yaml
```

---

## Esempi cartella

**Solo poster**
```
publications/data/new-poster/2025-icra-esempio/
├── poster.pdf
└── links.yaml
```

**Poster + articolo**
```
publications/data/new-poster/2026-icra-esempio/
├── poster.pdf
├── paper.pdf
└── links.yaml
```

**Solo paper (workshop senza immagine poster)**
```
publications/data/new-poster/2026-workshop-esempio/
├── paper.pdf
└── links.yaml
```

---

Per i **paper** journal/conference vedi [../new-paper/README.md](../new-paper/README.md).  
Per le **presentazioni** vedi [../new-presentation/README.md](../new-presentation/README.md).  
Per i **related works** vedi [../new-related/README.md](../new-related/README.md).
