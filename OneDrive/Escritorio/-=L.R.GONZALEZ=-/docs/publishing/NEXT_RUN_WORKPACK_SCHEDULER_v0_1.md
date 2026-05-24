# Next Technical Run - Workpack Scheduler v0.1

Goal: add a local-only scheduler for approved Workpacks.

Required posture:

- no cloud;
- no NVIDIA;
- no DeepSeek;
- no publication;
- no push/deploy from scheduler;
- max concurrency local = 1 by default;
- scheduler cannot execute unless Workpack Bridge and Local Execute gates pass.

Queue states:

- `DRAFT`
- `READY`
- `APPROVED`
- `SCHEDULED`
- `RUNNING`
- `EXECUTED`
- `FAILED`
- `ROLLED_BACK`
- `BLOCKED`

Integration targets:

- Agent Chat;
- Local Hub;
- Workpack Bridge;
- WitnessLog;
- Wabi UI.
