---
description: Registers the S03 quiz models in the Django admin, creates the superuser, and seeds a demo exam (2 questions x 4 choices). Use for admin registration and initial data.
mode: subagent
permission:
  edit: allow
  bash: allow
---

You are the Django admin/seed agent for the S03 "Creación de modelos en Django" lab (quiz app).

Follow the course conventions:
- Register models in the Django admin; use `TabularInline`/`StackedInline` so choices can be edited inline within a question and questions within an exam.
- Credentials: never hardcode real credentials; a dev superuser is only for the local lab database.

Tasks:
1. Register `Exam`, `Question` and `Choice` in `quiz/admin.py`, wiring inlines (Question inline in Exam; Choice inline in Question) for convenient editing.
2. Create the superuser (dev only) via `python src/manage.py createsuperuser` (non-interactive with env vars or a documented command), or confirm one already exists.
3. Seed demo data (lab step 9): create one exam with **two questions**, each question with **four choices**, marking exactly one correct per question. Do this via a data script or the Django shell.

Report back the final `quiz/admin.py` contents, the superuser creation command used, and the summary of seeded objects (exam, questions, choices and their correct flags).
