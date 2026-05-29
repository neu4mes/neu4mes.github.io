# Nuova presentazione sul sito

## Cosa fai tu

1. Crea una cartella in `publications/data/new-presentation/`, ad esempio:
   ```
   publications/data/new-presentation/2026-my-seminar/
   ```

2. Metti dentro questi file:

   | File | Obbligatorio | Note |
   |------|--------------|------|
   | `presentation.pdf` | sì | PDF delle slide (o rinomina il tuo PDF in `presentation.pdf`) |
   | `slide.png` | no | Anteprima listing; generabile con `scripts/pdf_first_page_preview.py` da `presentation.pdf` |
   | `links.yaml` | no | Venue, titolo/evento, YouTube, anno (vedi esempio sotto) |

   Esempio `links.yaml`:
   ```yaml
   venue: "Workshop-COSENO, University of Trento, Italy"
   publication: "University of Trento, Italy (2026)"
   journ: "University of Trento, Italy"
   year: 2026
   youtube: "https://www.youtube.com/watch?v=XXXXXXXX"
   ```

3. Incolla il **prompt per AI** qui sotto e indica la cartella (es. `2026-my-seminar`).

4. Controlla in preview: `/publications/` (sezione Presentations) e `/publications/presentations/.../`.

Non creare a mano `index.qmd` né la cartella in `publications/presentations/`: lo fa l’AI.

---

## Prompt per AI (copia tutto da qui)

```
Sei un agente che aggiorna il sito Quarto neu4mes.github.io aggiungendo una presentazione (talk / seminar / invited lecture) alla sezione Publications → Presentations.

## Input dell’utente

Tutte le cartelle all'interno di `publications/data/new-presentation/` sono cartelle sorgente :
  publications/data/new-presentation/<NOME_CARTELLA>/ (relativa alla root del repo)

File attesi:
  - presentation.pdf  — PDF delle slide (obbligatorio)
  - slide.png         — anteprima prima slide (opzionale; se assente, vedi script sotto)
  - links.yaml        — opzionale: venue, publication, journ, year, youtube, doi, code

Per ogni cartella esegui le seguenti operazioni
Poi elimina la cartella source publications/data/new-presentation/<NOME_CARTELLA>/

## Obiettivo

Creare publications/presentations/<YYYY-slug>/ con index.qmd e tutti gli asset copiati. L’utente verifica solo il preview.

## Riferimenti (leggi prima)

Studia struttura e tono di queste pagine già online:

  - publications/presentations/2025-09-nnodely-ekumen/index.qmd   (con video YouTube)
  - publications/presentations/2025-10-framework-trento/index.qmd
  - publications/presentations/2025-08-framework-design-trento/index.qmd
  - publications/presentations/2025-06-framework-upaep/index.qmd
  - publications/presentations/2024-11-framework-dii/index.qmd

Configurazione sito (non modificare senza motivo):

  - publications/_metadata.yml → title-metadata.html (autori; link PDF in testata)
  - _quarto.yml resources: publications/**/presentation.pdf
  - Listing: publications/index.qmd, presentations/**/index.qmd, sort pub_number desc
  - Sidebar Publications: ordine prev/next con campo order: -{pub_number}
  - Anteprima: blocco ::: {.presentation-preview} con slide.png
  - CSS: .presentation-preview in styles.css (già presente)

## Anteprima prima slide (unico script automatico supportato)

Se manca `slide.png` e c’è `presentation.pdf`, genera solo la thumbnail così:

```bash
.venv/bin/python scripts/pdf_first_page_preview.py \\
  publications/data/new-presentation/<NOME_CARTELLA>/presentation.pdf \\
  -o publications/presentations/<YYYY-slug>/slide.png
```

Non usare script di estrazione figure singole dal PDF (non affidabili).

## REGOLA CRITICA sui campi YAML

- Usa sempre pdf: presentation.pdf (NON paper.pdf, NON presentation.pdf con altro nome nel YAML).
- Usa image: slide.png per la thumbnail del listing.
- type: presentation
- categories: ["Presentations", "Model-Structured Neural Networks"]
- NON usare poster_pdf:, article_pdf:, né blocco poster-preview.

Video YouTube (opzionale):
  - In YAML: video: ID11caratteri   (solo ID, es. mz70WepnwMM) oppure URL completo se già usato così nel repo
  - Nel corpo, dopo Summary:
    ## Video {#video}
    {{< video https://www.youtube.com/watch?v=ID >}}

## Procedura

### 1. Analizza publications/data/new-presentation/<NOME_CARTELLA>/

- Elenca i file presenti.
- Leggi links.yaml se c’è.
- Da presentation.pdf (pymupdf/fitz in .venv se disponibile) estrai dalla prima slide e/o note:
  titolo talk, autori (ordine slide), evento, istituzione/venue, anno.
- Integra con links.yaml (links.yaml ha priorità su venue/journ/year se forniti dall’utente).

### 2. Slug e pub_number

- Slug: YYYY-slug-corto-inglese (es. 2026-icra-msnn-tutorial).
- Anno: da links.yaml, prima slide o nome cartella.
- pub_number: max tra publications/presentations/**/index.qmd + 1 (numero più alto = più in alto in elenco).
- order: -{pub_number}  (sidebar Quarto: avanti/indietro tra presentazioni).

### 3. Crea publications/presentations/<YYYY-slug>/

Copia dalla cartella new-presentation:
  - presentation.pdf → publications/presentations/<YYYY-slug>/presentation.pdf
  - slide.png → se presente; altrimenti esegui scripts/pdf_first_page_preview.py su presentation.pdf

Archivio opzionale: copia presentation.pdf in publications/data/presentation/ con nome descrittivo (anno + titolo corto), come per gli altri talk già archiviati.

### 4. Scrivi index.qmd

YAML (campi minimi, allineati ai riferimenti):

  - title: dal PDF / links.yaml
  - author: lista "Nome Cognome" (profili People se membri del gruppo)
  - publication: riga breve per listing, con anno — es. "University of Trento, Italy (2026)" o da links.yaml
  - type: presentation
  - categories: ["Presentations", "Model-Structured Neural Networks"]
  - journ: nome evento / serie / dipartimento (può coincidere con publication o essere più formale)
  - venue: luogo fisico o host (azienda, università, città) — da links.yaml o PDF
  - year, doi, code (se in links.yaml)
  - url_source:, url_preprint: (vuoti se non applicabile)
  - pdf: presentation.pdf
  - image: slide.png
  - pub_number: (calcolato)
  - order: -{pub_number}
  - video: (solo se youtube in links.yaml)

Corpo:

  ## Summary

  Un paragrafo in inglese che usa SOLO metadati verificati (title, author, venue, journ, publication, year):
  - Apri con "Presentation by **Autori** at **venue** (year)"
  - Cita il titolo del talk in corsivo una volta
  - 2–3 frasi sul contenuto (MSNN, nnodely, Neu4mes, applicazioni) senza inventare date (mese/giorno) non presenti nel YAML
  - NON confondere venue con città diverse da quelle in journ/venue/publication

  ## Video {#video}
  (solo se youtube in links.yaml)

  ::: {.presentation-preview}
  ![](slide.png){fig-alt="First slide: <titolo breve>" width=95%}
  :::

Nessun abstract lungo né sezioni MSNN con figure (quelle sono per i paper).

### 5. Vincoli

- NON eseguire scripts/build_publications.py.
- NON rinominare presentation.pdf in paper.pdf nella cartella pubblicata.
- NON aggiungere filtri Lua o HTML custom.
- La cartella new-presentation può restare come archivio upload.

### 6. Verifica

  quarto render publications/presentations/<YYYY-slug>/index.qmd

Controlla in _site/publications/presentations/<YYYY-slug>/:
  - link Download PDF → presentation.pdf
  - slide.png in listing e blocco presentation-preview
  - Summary coerente con venue/journ/year in testata
  - video embed se applicabile
  - prev/next in fondo pagina (sidebar Presentations)

### 7. Report (italiano)

  - percorso creato, pub_number, order
  - file copiati
  - URL: /publications/presentations/<YYYY-slug>/
  - eventuali dati mancanti da completare in links.yaml
```

---

## Esempio cartella pronta per l’AI

```
publications/data/new-presentation/2026-esempio-seminar/
├── presentation.pdf
├── slide.png          # opzionale
└── links.yaml
```

Dopo il prompt, il sito avrà ad esempio `publications/presentations/2026-esempio-seminar/` con `index.qmd`, `presentation.pdf` e `slide.png`.

---

Per i **paper** vedi [../new-paper/README.md](../new-paper/README.md).  
Per i **poster** vedi [../new-poster/README.md](../new-poster/README.md).  
Per i **related works** vedi [../new-related/README.md](../new-related/README.md).
