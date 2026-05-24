# Formal to PSI Intake - 2026-05-08

## Estado

CERTEZA:
- Source root: `C:\Users\L-Tyr\OneDrive\Escritorio\Formal`.
- Curador preflight decision: `NEEDS_FICHA_BEFORE_USE`.
- Files observed in the latest recheck: `50`.
- Exact SHA256 matches against `-=PSI=-`, `MEDIOEVO_OBSERVACIONISMO_MASTER` and `runtime/cerebro_master_index`: `0`.
- No files were moved, deleted, renamed, imported into canon or executed by this pass.

INFERENCIA:
- `Formal` is a new or materially different source lane, not a pure mirror of the current PSI/master canon.
- The folder contains a mixed corpus: formal theory, protocol prompts, code prototypes, experiment evidence, visual evidence and unsafe execution snippets.

INCOGNITA:
- PDF/PNG/ZIP contents need page/visual/quarantined extraction before any cleanup or claim closure.
- Several text files appear to be iterative session outputs; semantic equivalence to current canon is not proven by hash.

ACCION:
- Treat `Formal` as `INBOX / RAW_SOURCE`.
- Use `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-` as formal PSI authority.
- Use `MEDIOEVO_OBSERVACIONISMO_MASTER` as the human consolidated entry.
- Use `runtime/cerebro_master_index` as agent evidence, not as a new canon.

## Evidence

Commands run:

- `python tools\release\pending_review.py --write --quiet` -> `active_dedup=31`, `claudio_open=0`, generated `docs/pending/PENDING_REVIEW_2026-05-08.md`.
- `python tools\release\curador_preflight.py --path C:\Users\L-Tyr\OneDrive\Escritorio\Formal --json` -> `NEEDS_FICHA_BEFORE_USE`.
- `python -m wabi_sabi.cli.main --workspace ... --json cerebro-audit` -> `file_count_total=652`, `total_lines=294203`, `variant_group_count=119`, source mutations not requested.
- `python -m wabi_sabi.cli.main --workspace ... --json variant-compare` -> `variant_group_count=118`, no merge performed.
- `python -m wabi_sabi.cli.main --workspace ... --json duplicate-migration-plan` -> `dry_run_only=true`, `source_mutations=0`.
- `python -m wabi_sabi.cli.main --workspace ... --json cerebro-merge-review` -> `auto_merge_actions=0`, `source_mutations=0`.

## Classification Summary

| Classification | Count | Meaning |
|---|---:|---|
| `CANON_CANDIDATE` | 7 | May contain canon delta, but must pass claim and duplicate review first. |
| `RAW_SOURCE` | 20 | Keep as source material; extract only deltas with provenance. |
| `CODE_INSIGHT` | 8 | Extract contracts/patterns, not raw code import. |
| `EXPERIMENT_EVIDENCE` | 8 | Evidence or data lane; requires method notes before claim use. |
| `BLOCKED_EXECUTION` | 4 | Do not execute; extract only safe concepts if useful. |
| `PRIVATE_SECRET_CONFIG` | 1 | Secret/config evidence only; never copy raw content into canon, logs or public docs. |

## File Manifest

| File | Ext | Bytes | Lines | SHA256 | Classification | Gate / target |
|---|---:|---:|---:|---|---|---|
| `# PROTOCOLO OPERATIVO MEDIOEVO v3.1.txt` | `.txt` | 25879 | 609 | `1A97821F37D49178F236DBDD22B109DD74589FE049A81C77978F32C2A717078A` | `CANON_CANDIDATE` | compare to operational protocol / skill lane |
| `## ESTADO R0.01.txt` | `.txt` | 139123 | 3291 | `3B64D79A3BB68BC14545A191C8468367C38346C94D6DBFC0F43930CA6725ADF7` | `RAW_SOURCE` | split by claim/protocol/code blocks before use |
| `Auto.txt` | `.txt` | 37928 | 838 | `ABAC8265B8045A30DC16F91EE40BF105BE579AE024F00BF471F2896DB49A6EAD` | `CANON_CANDIDATE` | compare to master 00-22; no wholesale import |
| `banananana.txt` | `.txt` | 365 | 19 | `2FA50B657189AE22D371CFECADC25857770914235CCD3DC2233DFA6EF311D5B2` | `PRIVATE_SECRET_CONFIG` | NVIDIA/NGC provider credential/config evidence; redact always; no canon import |
| `BIBLIA_MEDIOEVO_Canon_Unificado.pdf` | `.pdf` | 183817 | 0 | `4E652E9E816C8A0E5313B4EEFDCDDDDF444DFCF1EDD7FB990A9E6C4A0D35BFF3` | `CANON_CANDIDATE` | `REVIEW_EXTRACTION_REQUIRED` |
| `Completar01.txt` | `.txt` | 30269 | 406 | `74D7BF4E4808B6350A2D039D70BEEF90140203B1BE8C92B9F37BB1C06890286F` | `EXPERIMENT_EVIDENCE` | preserve as experiment/protocol evidence |
| `Completar02.txt` | `.txt` | 35388 | 1188 | `0E763C96DDCE3F54561530AF683640D01835A81C0282723CEC90254520FE728D` | `CANON_CANDIDATE` | EML-heavy delta review |
| `Completar03.txt` | `.txt` | 27491 | 419 | `06F25829294069AB37C1C357E2A07F08FB5FE90FF4E9BFDA3982BD58EA6D0261` | `RAW_SOURCE` | extract only deltas |
| `Completar04.txt` | `.txt` | 71025 | 1658 | `83E1470C4622AA408C3C3758AC7F73619405DC02BB56C91F86CB310B1B639528` | `CODE_INSIGHT` | inspect defs/classes before contract reuse |
| `Completar05.txt` | `.txt` | 32614 | 800 | `61B1581CD733B3C3E09AA00CB2BB3A968E7DCA2ECD0598DD74FCCBB316382DD1` | `CODE_INSIGHT` | inspect as mixed code/protocol source |
| `Completar06.txt` | `.txt` | 17430 | 430 | `6839E29AFBB3FFCA752E5B32DB92D83C4DBD72E95735543CB299011A9A3B73BA` | `CODE_INSIGHT` | inspect as mixed code/protocol source |
| `Completar07.txt` | `.txt` | 75608 | 1579 | `E848898E404CCD6F77A007E6A918F4CB9A5D54CC501E51CD698DB5EFD18D49AA` | `CODE_INSIGHT` | inspect defs/classes before reuse |
| `eml_renormalizacion.png` | `.png` | 371546 | 0 | `B49CDEFB573D55C31A38F669DAAE119B9BD6550D10311371B51BEFDCDC8E4EF5` | `EXPERIMENT_EVIDENCE` | visual QA required |
| `Es la primera vez que no me pregunt.txt` | `.txt` | 86181 | 1461 | `B85E99D56D628D9786DAA1FCA0FD5B3721887F5AEC46C8D833BE01444799F5D0` | `RAW_SOURCE` | split session/code/claim sections |
| `experimento_medioevo2_datos.json` | `.json` | 19217 | 1006 | `84824EF8561585B294E08E84B2B0C36F447A6A502DC6A2A6D23AF9FF6F4EFFE1` | `EXPERIMENT_EVIDENCE` | keep as dataset evidence |
| `experimento_medioevo2_resultados.png` | `.png` | 238140 | 0 | `F13793638124C6334FC9727F9388B61C68528B8317D2201CDFBC13FC5BC98A6E` | `EXPERIMENT_EVIDENCE` | visual QA required |
| `fig1_eml_landscape.png` | `.png` | 231761 | 0 | `45CB1B9E9C54871F23D0AF51BF00E94519478D3DF28B793B0750A088449AE584` | `EXPERIMENT_EVIDENCE` | visual QA required |
| `fig2_isomorphism_map.png` | `.png` | 272390 | 0 | `F805795239EB401FE97D7931C4CE7D46BB7D344786F6FEA361615BD7B781774C` | `EXPERIMENT_EVIDENCE` | visual QA required |
| `image (1).png` | `.png` | 89013 | 0 | `3C9100CC5E9C4EFBA1B3E0DD8D23DD998BE57E8C334CF4A390BBA58D8D7BFCA0` | `RAW_SOURCE` | visual review before claims |
| `image (2).png` | `.png` | 174825 | 0 | `0ACA5FBC563E0CC4650A225AEB4867AE98E461D6E47DC1FDFC167E38AB731132` | `RAW_SOURCE` | visual review before claims |
| `image (3).png` | `.png` | 327326 | 0 | `43AC6013465A5CA312A9EB7A5890401849D2040014A300A884B4A3EFAA94EFBE` | `RAW_SOURCE` | visual review before claims |
| `image.png` | `.png` | 167067 | 0 | `C1CBAA0A4BE7E2492FDA24A5F4B6301748228114C63DDC53778CEF6CE993FEDB` | `RAW_SOURCE` | visual review before claims |
| `medioevo_agent_core.py` | `.py` | 20299 | 548 | `F646B34113FB7CA39AE918D22D8FF4E268364E863D9906ED4C8A9EA0CAC7FCBF` | `CODE_INSIGHT` | compare to Wabi/Sabi contracts |
| `medioevo_core_v01.py` | `.py` | 20936 | 564 | `FD8941B2B009604C1A8AFBF1ADCF27752ED947543787C6B73A53D1CB17877690` | `CODE_INSIGHT` | compare to Wabi/Sabi contracts |
| `medioevo_info_chemistry_v0_2.zip` | `.zip` | 10795 | 0 | `2ABF02A879318E35AA88246F81FDD5AC1A954912252613839964AD6BC461FE54` | `CODE_INSIGHT` | quarantined archive intake required |
| `medioevo_prompt_compression_experiment_bundle.zip` | `.zip` | 31117 | 0 | `E2BC987C24F7D46706481033EDA3C5981241854EF2675CFEAD3770890817727C` | `EXPERIMENT_EVIDENCE` | quarantined archive intake required |
| `nucleo.txt` | `.txt` | 5809 | 110 | `C0AB7837967BAAA3C208BD36C7742DDEA05A2AB97BD4EE45B18DA846B79A526E` | `BLOCKED_EXECUTION` | do not execute host/process actions |
| `OI_P6R_paper_v0_1.md` | `.md` | 22170 | 549 | `E391DC46087216DBF6193209AEC9315DBE1F7712F4D3F52A9FBCAEA169A106C5` | `CANON_CANDIDATE` | compare to OI canon and claims |
| `P1R.txt` | `.txt` | 116981 | 2050 | `BB87FEA7F87DC7E9D64B27930668C989860A65F0C3A1EF136AA96132965938D9` | `RAW_SOURCE` | iterative research source |
| `P2R.txt` | `.txt` | 63013 | 1389 | `0D5B494F93A2E5B84462C558FC6324EBD9DFCC4C9802428A944B042E5C01804D` | `RAW_SOURCE` | iterative research source |
| `P3R.txt` | `.txt` | 63763 | 1368 | `C70BB0CD9CAFD237D181D88468FA353C1B84251F665E2047920BAFF835694B69` | `RAW_SOURCE` | iterative research source |
| `P4R.txt` | `.txt` | 74098 | 2329 | `E5172FF2C9A501A00F74D4BEC2A06C39901578D7BDF30C1508B674EE0CFD6B91` | `RAW_SOURCE` | iterative research source |
| `P5R.txt` | `.txt` | 67496 | 1562 | `808FA52A94E534975B7633AE5FE95C099B92000162BB29F73CA9DDF991218A28` | `RAW_SOURCE` | iterative research source |
| `P6R.txt` | `.txt` | 51742 | 1130 | `F470019EE6FF3B4A80E6C1D16ECEE14803B96963900CF53EE893DDA5DEE2B319` | `RAW_SOURCE` | compare to OI paper before cleanup |
| `P7R.txt` | `.txt` | 56957 | 1345 | `F36E6F26F62279F65B7EBC265CB45B9953435DAED5BC485D532D311B6FD0B664` | `RAW_SOURCE` | iterative research source |
| `P8R.txt` | `.txt` | 72764 | 932 | `018354D5515966CC240C643C991F2315BA934175819378BD1B5F8080E920F659` | `RAW_SOURCE` | iterative research source |
| `paper_observacionismo_inverso.md` | `.md` | 11509 | 212 | `D48B2F619947A88D82A35DFB17CFDCF29CBA7E82503A3993CFC3DAE9315F06F0` | `CANON_CANDIDATE` | compare to OI canon and claims |
| `Para materializar este Pipeline Dir.txt` | `.txt` | 13107 | 270 | `41823504BB655EE2E478B98FE89F6658E2FA9996CEC69009E035B6247401993E` | `BLOCKED_EXECUTION` | raw shell/API execution pattern blocked |
| `PR10.txt` | `.txt` | 36319 | 1065 | `C87938547EB7BE153EB00F88CA08205F1284C344CC92F025020A6ED4D3E4528D` | `RAW_SOURCE` | iterative research source |
| `PR11.txt` | `.txt` | 21497 | 508 | `F31664D1AF3C51AA984778AE5C9C14A9040A1B5AFA206BC197652BA090FE82DF` | `CODE_INSIGHT` | inspect as agent/runtime source |
| `PR12.txt` | `.txt` | 13492 | 252 | `5CB4138A98A7726BAA34AF05672C26B82F103E508C823C4BBF1FD66F0A7F8698` | `RAW_SOURCE` | iterative research source |
| `PR9.txt` | `.txt` | 32228 | 595 | `968CE5A64B2A33533F0015DF5C42E9E6F0D103F0077AA74CEE61C163E93B642A` | `RAW_SOURCE` | iterative research source |
| `report.md` | `.md` | 66283 | 385 | `66A78CFE98D6565365BDC5587075036467F40A695BFFB4FA1E7F4903E6B02A4C` | `CANON_CANDIDATE` | formal math/claims delta review |
| `results_full.csv` | `.csv` | 8394 | 61 | `B369124582176956E033C14BE7D60CE9CD5FA1E3C7D5949671460EA13325346C` | `EXPERIMENT_EVIDENCE` | keep with compression experiment evidence |
| `The Solution deploy_overlord.shThis.txt` | `.txt` | 7780 | 148 | `B2241A5C87A8DD767D5E4948A54597C73C8D44EA4AB94EBB276E06E2B61A6058` | `BLOCKED_EXECUTION` | raw deploy/API/shell execution blocked |
| `uno.py` | `.py` | 3226 | 72 | `DDCDE60CE0B837675EDFFACFE0EFAF6DA31B0190953C7C266976C09D290C6EF6` | `BLOCKED_EXECUTION` | process priority/kill/cache actions blocked |
| `Untitled.txt` | `.txt` | 5041 | 75 | `A7A444EDE762900577E5D7B0FB7EF2C5AAF1C63B641CB2B372A5C8A7D1CE89EA` | `RAW_SOURCE` | security/legal/commercial prompt review |
| `Untitledqq.txt` | `.txt` | 26141 | 787 | `3C4F5A40D55D816B2CDFCE0A3DC3CD4052035AC583617F5C53F60C3951596E26` | `RAW_SOURCE` | mixed protocol/claim/code review |

## Decision

- `KEEP_REVIEW`: all files in `Formal`.
- `NO_DELETE`: no item qualifies for third-pass deletion yet.
- `NO_CANON_IMPORT`: no full text import was performed.
- `NO_CODE_IMPORT`: no Python or shell code was copied into runtime.
- `NO_PUBLICATION`: no external action was performed.
- `SECRET_BOUNDARY`: `banananana.txt` is registered as private provider configuration evidence only; its raw content must not be copied, summarized verbatim or placed in canon.

## Update - provider/secret delta

CERTEZA:
- `banananana.txt` was added after the first 47-file pass. A later recheck on
  2026-05-08 observed `50` files in `Formal`.
- Single-file preflight returned `NEEDS_FICHA_BEFORE_USE`; folder preflight now returns `REGISTERED_CONTINUE_WITH_BOUNDARY`.
- Hash evidence: `2FA50B657189AE22D371CFECADC25857770914235CCD3DC2233DFA6EF311D5B2`.

ACCION:
- Treat this file as `PRIVATE_SECRET_CONFIG / BLOCK_PUBLICATION / REDACTED_EVIDENCE_ONLY`.
- Use it only to confirm that provider credential lanes exist and need secret-safe env/vault wiring.
- Do not use it as code, claim, canon source, prompt source or publication material.
