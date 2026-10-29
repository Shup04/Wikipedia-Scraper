# Wikipedia Scraper

A collection of Python scripts that assembled aquarium species information and image URLs for the AquaFlora app. The project turns Wikipedia's human-readable fish tables and invertebrate lists into JSON records, adds short descriptions and other fields through OpenAI, and prepares popularity scores for the catalog.

This repository is the working history of that data-preparation effort. It contains saved pages, intermediate catalogs, model requests and responses, and scripts adapted as the work moved from fish to invertebrates. It is not a single repeatable command that rebuilds a verified final dataset.

## The idea behind the project

An aquarium app needs browseable species records: common and scientific names, pictures, groups, descriptions, and care-related fields. Wikipedia already provides much of that information, but in tables, lists and prose rather than the app's desired record structure. The first part of this project converts those pages into a catalog without entering every species by hand.

The code then addresses two different gaps:

- **A species list is not a useful short description.** The fish enrichment path follows each species link, extracts paragraphs and asks for a concise summary intended for a mobile app. [`GPTSummarize.py`](GPTSummarize.py) makes that purpose explicit and caps the response at 100 tokens.
- **The source does not fill every desired field.** The later invertebrate workflow prepares batch requests to supplement sparse records with descriptions, image URLs and care details. A separate batch asks for a 1–25 popularity score based on aquarium use and store availability.

The resulting design separates discovery, enrichment and merging into files that can be inspected between stages. Saved inputs and responses preserve the work already paid for or collected. The history also shows a deliberate stopping point: once automated collection was good enough, remaining corrections were to be made by hand.

## How the data moves

### Fish: tables, groups and short descriptions

[`Main1.py`](Main1.py) reads the saved [`wikipage.html`](wikipage.html), finds Wikipedia tables and assigns each table to a hardcoded group/subgroup sequence. It extracts names, image URLs, size, remarks, tank size, temperature, pH and species-page links. IDs provide a handle for later processing. The platies/swordtail special case shows the parser being adapted to specific awkward source rows, rather than attempting to infer an arbitrary table schema.

The image fields contain URLs; this path does not download a local image library. Group assignment depends on the saved table order. It is not automatic taxonomic classification.

[`Enrich.py`](Enrich.py) reads `fish_data_links.json`, fetches linked species pages and passes their paragraph text to the summarizer. It uses five worker threads, with a delay in each enrichment task, and writes `fish_data_descriptions2.json`. A failed or unavailable description can leave a `null` entry because that task returns no record. The current summarizer's client initialization is commented out, so this enrichment path requires attention before it can make calls successfully.

[`Main.py`](Main.py) is an earlier table parser that writes the same `fish_data_links.json` filename. It and `Main1.py` are alternatives, not successive steps. Their field names differ; neither should be run over preserved exports without first choosing the intended schema.

### Invertebrates: sparse lists and batch enrichment

[`invert/Main.py`](invert/Main.py) reads [`invert/Inverts.html`](invert/Inverts.html). It looks for list items containing an italicized linked name, splits the text into scientific/common names, and creates records with the remaining catalog fields initially empty.

The historical version of `invert/GPTGenerate.py` at [commit `8c139ed`](https://github.com/Shup04/Wikipedia-Scraper/blob/8c139ed/invert/GPTGenerate.py) fetched valid species pages, built prompts from the available text, and generated full-information requests for missing pages. Its saved output is [`invert/inverts_requests.jsonl`](invert/inverts_requests.jsonl). That generator was subsequently replaced: **the current file with the same name is a response merger.** Recovering the original request-building stage therefore requires consulting history, not just executing the current files in name order.

[`invert/RunBatch.py`](invert/RunBatch.py) uploads the JSONL requests and submits an OpenAI batch. [`invert/CheckBatch.py`](invert/CheckBatch.py) retrieves a configured batch and saves `inverts_responses.jsonl`. The current [`invert/GPTGenerate.py`](invert/GPTGenerate.py) extracts JSON from the replies, attempts limited formatting repairs, joins replies to records using `invert-<id>`, and writes `inverts_data_complete.json`. Unresolved parsing problems can be retained as `error` and `raw_response` fields for manual inspection. `invert/InjectGPTResponse.py` stops after building a response dictionary; despite its name, it does not save a merged catalog.

**Generated enrichment is not verified care information.** Some saved requests explicitly say, “If no reliable source exists, invent plausible details.” Other historical prompts ask for plausible missing values. Those instructions explain how empty fields were filled; they do not establish that the results are true. Unknown or unsupported animal-care claims need review before the data is treated as a reference.

### Popularity scores

[`rankPopularity.py`](rankPopularity.py) creates ranking requests, [`rankPopularity2.py`](rankPopularity2.py) submits them, `checkBatchStatus.py` downloads replies, and [`injectRanking.py`](injectRanking.py) adds `popularity_score` to records.

These scripts were reused for invertebrates. At the current revision they use root-level `inverts_data_complete.json`, `invert_requests.jsonl`, `batch_output.jsonl` and `updated_invert_data.json`, even where variable names, prompts or console messages still say “fish.” The score is a model's suggested ordering, not a measured count of purchases, ownership or searches.

## Files to preserve before resuming

The checked-in artifacts are not interchangeable versions of one proven final export:

| Artifact | What the current file contains |
| --- | --- |
| `fish_data_links.json` | 639 fish records with unique IDs and source links. |
| `fish_data_descriptions2.json` and `fish_data.json` | 639 array positions each, including 41 `null` entries; their image-field names differ. |
| `invert/inverts_data.json` | 128 initial invertebrate records. |
| `invert/inverts_data_complete.json` and root `inverts_data_complete.json` | Separate 128-record enriched exports with different image-field names; each still contains 26 records marked with parsing errors. |
| `updated_invert_data.json` and `updated_fish_data.json` | Both currently contain 128 invertebrate records with popularity fields, despite the second filename. |
| `*.jsonl` and `invert/*.jsonl` | Saved model requests and replies for enrichment or ranking. |

These counts describe the committed snapshot, not an assertion that every row is complete or accurate. There is no documented authoritative final export or complete record of manual corrections. Choosing which data to keep comes before rerunning a producer that may overwrite it.

## Running or reconstructing a stage

Use a separate working copy of the saved data. Python 3 and the imported packages `requests`, `beautifulsoup4` and `openai` are needed across the scripts. There is no dependency manifest outside the committed historical `myprojectenv/`; that environment is not a verified portable installation. A new environment can be prepared with:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests beautifulsoup4 openai
```

This installs unpinned dependencies, so it does not recreate the original environment exactly. The scripts and saved requests contain historical model names; current API/model compatibility has not been established. OpenAI calls require `OPENAI_API_KEY` in the environment. The fish summarizer additionally needs its commented client initialization restored before use.

There is no common CLI or dry-run mode. Most scripts execute their work when imported, so inspect them as text rather than importing them to discover their behavior.

| Working directory | Command/stage | Effect |
| --- | --- | --- |
| Repository root | `python Main1.py` | Parses saved HTML and replaces `fish_data_links.json`; see the ID issue below before reuse. |
| Repository root | `python Enrich.py` | Fetches species pages, makes model calls and replaces `fish_data_descriptions2.json`. |
| `invert/` | `python Main.py` | Parses saved HTML and replaces `inverts_data.json`. |
| `invert/` | `python RunBatch.py` | Uploads `inverts_requests.jsonl` and starts a paid batch. |
| `invert/` | `python CheckBatch.py` | Polls its configured historical batch ID and replaces `inverts_responses.jsonl`; select the intended job first. |
| `invert/` | `python GPTGenerate.py` | Locally merges saved responses and replaces `inverts_data_complete.json`. |
| Repository root | `python rankPopularity.py` | Replaces `invert_requests.jsonl`; generating this file makes no API call. |
| Repository root | `python rankPopularity2.py` | Uploads that request file and starts a paid batch. |
| Repository root | `python checkBatchStatus.py` | Uses configured batch/file IDs and replaces `batch_output.jsonl`; select the intended job/output first. |
| Repository root | `python injectRanking.py` | Locally merges scores and replaces `updated_invert_data.json`. |

The root and `invert/` directories are separate working contexts. There is no automatic step that synchronizes their similarly named catalogs. The table describes existing side effects, not a validated end-to-end runbook.

## Known correctness limits

- **Fish ID generation has a conditional collision.** `Main1.py` inserts IDs 424, 425 and 426, then can assign 426 to the following ordinary row. An isolated reproduction of the actual functions demonstrated the duplicate. The committed `fish_data_links.json` has unique IDs; this does not mean that export is already corrupted.
- **Popularity merging assumes reply order.** `injectRanking.py` consumes responses by position rather than matching `custom_id`. Missing or reordered replies can assign a score to another species. The inspected committed replies were ordered; incorrect current assignments were not demonstrated.
- **Schema and factual cleanup remain manual.** The differing field names, null entries, retained parsing errors and generated care claims must be resolved for whichever export is selected. JSON parsing success alone does not establish a usable or accurate catalog.

## Where development stopped

The February–April 2024 work developed fish grouping, links, descriptions and parallel enrichment. March 2025 added popularity scoring and the invertebrate batch workflow. Commit `799a1da` explicitly stopped scraping for the time being and left the remaining work to manual repair; the final commit applied invertebrate rankings.

That history supports a finite finish: preserve a usable AquaFlora catalog and explain how it was assembled. A crawler service, scheduler or generalized ingestion framework is unnecessary to close this project.

## Definition of done

- [ ] Select and preserve one authoritative fish export and one invertebrate export. Record their schemas, source artifacts and manual corrections so similarly named intermediate files cannot be mistaken for final data.
- [ ] Resolve null entries, parsing-error records and unsupported care claims in those exports. Retain traceable source information; leave unknown facts unknown rather than silently presenting generated guesses as verified values.
- [ ] Make supported regeneration paths preserve unique IDs and merge replies by identifiers. Check duplicate-ID, missing-response and reordered-response examples before replacing any final data.
- [ ] Record a working environment and exact input → script → output sequence for the stages worth keeping, including the historical request generator if regeneration is needed. Demonstrate the local transformations on copies of saved inputs without another paid batch.
- [ ] Check that the chosen exports satisfy AquaFlora's intended record format and review representative records and images. Preserve the resulting exports and a short account of the remaining limits; further scraping can then be considered optional.
