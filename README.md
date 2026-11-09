# Wikipedia Scraper

A personal, one-time data-preparation project for the AquaFlora aquarium app.
Python scripts converted saved Wikipedia species lists into JSON catalogs, added
model-generated descriptions and care fields, and assigned suggested popularity
scores. The saved inputs, intermediate exports and model responses preserve how
that catalog was assembled.

**Status:** historical project, kept for reference. Scraping work stopped in
March 2025 with remaining corrections left to manual review. There is no supported
end-to-end rebuild or documented, verified final export. Generated care information
must not be treated as verified husbandry guidance.

## Workflow

1. **Fish discovery:** [`Main1.py`](Main1.py) parses the saved fish list in
   [`wikipage.html`](wikipage.html) into `fish_data_links.json`, extracting names,
   image URLs, source links and available table fields. Groups follow a hardcoded
   table order. [`Main.py`](Main.py) is an earlier alternative that writes the same
   output with different field names; the two scripts are not sequential stages.
2. **Fish descriptions:** [`Enrich.py`](Enrich.py) fetches linked species pages and
   sends paragraph text to [`GPTSummarize.py`](GPTSummarize.py), then writes
   `fish_data_descriptions2.json`. This stage uses Wikipedia and OpenAI over the
   network. The summarizer's client initialization is currently commented out,
   so it cannot run successfully as checked in.
3. **Invertebrates:** [`invert/Main.py`](invert/Main.py) parses
   [`invert/Inverts.html`](invert/Inverts.html) into `invert/inverts_data.json`.
   Saved enrichment requests are in `invert/inverts_requests.jsonl`;
   [`invert/RunBatch.py`](invert/RunBatch.py) uploads them to OpenAI and submits a
   batch, and [`invert/CheckBatch.py`](invert/CheckBatch.py) downloads the replies.
   The current [`invert/GPTGenerate.py`](invert/GPTGenerate.py) **merges saved
   responses** by `invert-<id>` into `invert/inverts_data_complete.json`. The
   request generator that fetched species pages exists in
   [commit 8c139ed](https://github.com/Shup04/Wikipedia-Scraper/blob/8c139ed/invert/GPTGenerate.py).
   `invert/InjectGPTResponse.py` is an incomplete alternative that does not save a
   merged catalog.
4. **Popularity:** [`rankPopularity.py`](rankPopularity.py) creates
   `invert_requests.jsonl` from the root `inverts_data_complete.json`.
   [`rankPopularity2.py`](rankPopularity2.py) submits those requests;
   [`checkBatchStatus.py`](checkBatchStatus.py) downloads `batch_output.jsonl`;
   [`injectRanking.py`](injectRanking.py) writes `updated_invert_data.json`.
   These scripts currently process invertebrates even where prompts, variable
   names or log messages still say "fish". Scores are model estimates on a 1–25
   scale, not measured popularity.

The root and `invert/` catalogs are separate copies; no script synchronizes them.
Current parsers, ranking-request creation and response merging operate on local
files. Batch submission and retrieval contact OpenAI; submissions can incur charges.

## Saved data

These are intermediate artifacts, not interchangeable final releases. Counts below
describe the committed files, not their factual accuracy.

| Files | Contents and caveats |
| --- | --- |
| [`fish_data_links.json`](fish_data_links.json) | 639 fish records with unique IDs and source links. |
| `fish_data_descriptions2.json`, `fish_data.json` | 639 positions each, including 41 `null` entries; image-field names differ. |
| [`invert/inverts_data.json`](invert/inverts_data.json) | 128 initial invertebrate records with mostly empty enrichment fields. |
| `invert/inverts_data_complete.json`, `inverts_data_complete.json` | 128 records each, including 26 with parsing errors; image-field names differ. |
| `updated_invert_data.json`, `updated_fish_data.json` | Both contain 128 invertebrate records with popularity fields and the same 26 parsing-error records, despite the latter filename. |
| Root and `invert/` `*.jsonl` files | Saved model requests and responses for enrichment or ranking. |

## Setup and inspection

Reading the saved HTML, JSON and source files requires no API key. To explore or
adapt the scripts, use Python 3 and a fresh virtual environment; the committed
`myprojectenv/` is a historical environment, not a portable installation. From the
repository root, a POSIX shell setup is:

```sh
python3 -m venv ../wikipedia-scraper-env
. ../wikipedia-scraper-env/bin/activate
python -m pip install requests beautifulsoup4 openai
```

Dependencies are unpinned and there is no project dependency manifest. This setup
does not reproduce the original environment; compatibility with current SDKs and
the historical model names has not been validated.

For a read-only inspection using only Python's standard library:

```sh
python3 - <<'PY'
import json
from pathlib import Path

for path in sorted([*Path('.').glob('*.json'), *Path('invert').glob('*.json')]):
    rows = json.loads(path.read_text(encoding='utf-8'))
    nulls = sum(row is None for row in rows)
    print(f'{path}: {len(rows)} entries, {nulls} nulls')
PY
```

Before rerunning any stage, work on copies of its inputs and outputs. Most scripts
execute work on import and overwrite fixed filenames; there is no shared CLI or
dry-run mode. Root scripts expect the repository root as their working directory,
and `invert/` scripts expect that directory. OpenAI stages require
`OPENAI_API_KEY` in the environment; keep credentials out of the repository. Batch
retrieval scripts contain historical job/file IDs that must be replaced for a new
run, and fish enrichment needs its client initialization repaired first.

## Provenance and limits

- **Extracted fields:** names, links and available table values can be traced to
  the saved Wikipedia lists; they are source-derived, not independently checked.
  A record's `link` does not establish support for every subsequently added field.
- **Generated fields:** summaries, missing care values and suggested image URLs
  may include unsupported claims. Some saved invertebrate requests explicitly
  instruct the model to "invent plausible details" when no reliable source
  exists. The exports do not consistently label which individual values were
  extracted or generated. Check claims against reliable species-specific sources
  before reuse; keep unsupported values unknown. Valid JSON does not verify care
  requirements, species identity or image accuracy.
- **Known code issues:** `Main1.py` can reuse ID 426 after its hardcoded
  platy/swordtail insertion, although the committed fish-link export has unique
  IDs. `injectRanking.py` assigns scores by response position instead of
  `custom_id`, so missing or reordered replies can attach scores to the wrong
  species. These are regeneration risks, not proof that saved scores are wrong.
- **Incomplete exports:** null entries, retained parsing errors, differing schemas
  and undocumented manual corrections remain. There is no project test suite or
  validated reconstruction sequence.
- **Attribution and reuse:** the saved Wikipedia pages retain source and license
  notices, but the JSON exports do not provide a complete attribution trail for
  text and images. Image URLs alone do not document authorship or reuse terms.
  Check the original article and image-file notices before redistribution. No
  project-level license is included; bundled dependencies have their own notices.
