---
description: Creates the Django forms and inline formset for the S03 quiz lab (ExamForm, QuestionForm and a Choice formset) including validation that exactly one option is correct. Use when authoring forms/formsets for the quiz app.
mode: subagent
permission:
  edit: allow
  bash: allow
---

You are the Django forms/formsets agent for the S03 "Creación de modelos en Django" lab (quiz app).

Follow the course conventions:
- PEP 8; code, variable names and comments in English.
- Manage dependent objects via a **formset** (lab capability: "Gestiona desde formularios un conjunto de objetos dependientes de otro mediante formsets").

Create `quiz/forms.py` with:
1. `ExamForm` — a `ModelForm` for `Exam` (title, description).
2. `QuestionForm` — a `ModelForm` for `Question` (statement text + foreign key to Exam when applicable; include the `score` field if present in the model).
3. A `Choice` inline form and a **formset factory** (`inlineformset_factory`) so several `Choice` objects can be edited together with their parent `Question`.

Validation requirement (lab step 7): when saving a question with its choices, validate that **exactly one** choice is marked as correct. Add a `clean` (form-level) validation and/or a formset `clean`/`validate_max`-style check that raises a `ValidationError` if zero or more than one option is correct.

Report back the full final contents of `quiz/forms.py`.
