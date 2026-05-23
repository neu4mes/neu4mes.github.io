# Nuovo related work sul sito

## Cosa fai tu

1. Crea una cartella in `publications/data/new-related/`, ad esempio:
   ```
   publications/data/new-related/2024-author-topic/
   ```

2. Metti dentro:

   | File | Obbligatorio | Note |
   |------|--------------|------|
   | `paper.pdf` | sì | PDF dell’articolo / related work |
   | `figure1.png`, `figure2.png`, … | no | Se mancano, l’AI le estrae dal PDF (figure di architettura / overview) |
   | `main.png` | no | Copertina listing; se manca, copia di `figure1.png` |
   | `links.yaml` | no | DOI, autori aggiuntivi, venue |

   Esempio `links.yaml`:
   ```yaml
   doi: "10.1109/XXXXXXXX"
   venue: "Journal name"
   authors:
     - "Nome Cognome"
   ```

3. Incolla il **prompt per AI** qui sotto e indica la cartella.

4. Controlla in preview: `/publications/` (Related works) e `/publications/related/.../`.

---

## Prompt per AI (copia tutto da qui)

```
Sei un agente che aggiorna il sito Quarto neu4mes.github.io aggiungendo un related work.

## Input

Cartella: publications/data/new-related/<NOME_CARTELLA>/
L’utente ha indicato: <NOME_CARTELLA>

File: paper.pdf (+ opz. figure*.png, main.png, links.yaml)

## Obiettivo

Creare publications/related/<YYYY-slug>/ con pagina completa come i paper del gruppo (abstract + sezione descrittiva + figure in .paper-network-figures).

## Riferimenti

  - publications/related/2021-gastone-pietro-rosati-papini-a-reinforcement-learning-a/index.qmd
  - publications/related/2019-mauro-da-lio-modelling-longitudinal-vehicle-dynamics-wi/index.qmd
  - publications/related/2021-luca-antonucci-efficient-prediction-of-human-motion-for/index.qmd
  - publications/papers/2025-road-friction-aware-abs/index.qmd  (stile MSNN / figure)

## Procedura

1. Analizza paper.pdf (pymupdf o lettura diretta): titolo, autori, abstract, DOI, figure con architettura di rete.
2. Slug YYYY-slug-corto; pub_number = max(related/**/pub_number)+1; order: -{pub_number}.
3. Copia in publications/related/<slug>/: `paper.pdf` e le figure esportate **manualmente** dal PDF (es. `figure1.png`, `figure2.png`, …). `main.png` = copertina listing (di solito la figura overview, es. `figure1.png`). Non usare estrazione automatica da pagina intera: qualità insufficiente.
4. Scrivi index.qmd:
   - YAML come related esistenti: type: related, categories: ["Related works", "Model-Structured Neural Networks"], image: main.png, pdf: paper.pdf, doi se noto
   - ## Abstract (testo completo dal PDF)
   - ## Sezione tematica {toc-text="..."} con 1–2 paragrafi
   - Per ogni figure: ### … (Figure N), testo, blocco ::: {.paper-network-figures}
5. NON eseguire scripts/build_publications.py.
6. quarto render publications/related/<slug>/index.qmd e verifica immagini + DOI in testata.

Report in italiano: percorso, pub_number, URL preview, campi mancanti.
```

---

Per **paper**, **poster** e **presentazioni** vedi rispettivamente [../new-paper/README.md](../new-paper/README.md), [../new-poster/README.md](../new-poster/README.md), [../new-presentation/README.md](../new-presentation/README.md).
