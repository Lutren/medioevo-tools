# Action Gate Register

| Action | Gate | Rule |
|---|---|---|
| CEREBRO_LINE_AUDIT | APPROVE | read-only source scan plus runtime artifacts |
| WRITE_MASTER_INDEX | APPROVE | writes only under runtime/cerebro_master_index |
| MERGE_VARIANTS | REVIEW | different hashes are not merged automatically |
| MOVE_SOURCE_TREE | REVIEW | physical reorganization requires migration log and backup |
| BROWSER_LOCAL_OR_READONLY | APPROVE_LOGGED | no login, no form submit, no publication |
| BROWSER_AUTH_PUBLISH_OR_PAYMENT | REVIEW_OR_BLOCK | requires explicit target-specific gate |
| AGENT_WRITE_CODE | APPROVE_WITH_SAFE_EXECUTOR | patch plan, rollback, py_compile/tests, witness |
| PUBLIC_STRONG_PHYSICS_CLAIM | BLOCK_UNTIL_NUMERIC | needs formalism and falsifier |
