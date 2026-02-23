<div align="center">

# KABAN
![boar-running](https://github.com/user-attachments/assets/a2afef81-9ec7-447a-a747-f0916518a28b)

KABANchik

**A small Kanban/IT-project management database + Python init/tests (SQLite).**

</div>

---

## Quest Log
You found an *IT Projects Kanban* database with:
- `developers`, `projects`, `tasks` tables
- views for quick analytics (`view_task_details`, `view_project_stats`, `view_developer_stats`)
- triggers that protect from duplicates (upsert-like behavior)
- seed data for instant queries

If you’re a recruiter: this repo is mostly about **SQL schema design** + **Python automation/tests**.

---

## Tech Stack
- **Python**: simple DB init + smoke tests
- **SQLite**: single-file database
- **SQL**: schema, indexes, views, triggers, seed data

---

## Map
- `database/kaban.sql` — schema + views + triggers + demo data
- `database/init_db.py` — creates/initializes the SQLite DB from SQL script
- `database/kabanmanagement_it-projects.sqlite` — generated DB (example)
- `docs/BD_diagram.png` — ER diagram
- `src/tests/db.py` — unittest suite that validates tables/views/triggers

---

## Quickstart
### 1) Create DB from SQL
```bash
python database/init_db.py
```
What it does:
- reads `database/kaban.sql`
- creates `database/kabanmanagement_it-projects.sqlite`
- prints tables + row counts

### 2) Run tests
```bash
python -m unittest src.tests.db
```
Tests include:
- tables/views exist
- seed data present
- foreign keys are consistent
- triggers prevent duplicates and update existing rows

---

## Database Diagram
Open: `docs/BD_diagram.png`

---

## Example Queries
A few “quick loot” queries you can try (after initialization):

```sql
-- Tasks with project + developer details
SELECT * FROM view_task_details LIMIT 10;

-- Project progress and costs
SELECT * FROM view_project_stats ORDER BY completion_percentage DESC;

-- Developer workload and earnings
SELECT * FROM view_developer_stats ORDER BY total_earnings DESC;
```

---

## Notes
- The `src/main/**` package structure is prepared for a future app layer (controllers/services/views), but the core of the project is the **DB layer**.
- If you want to open the DB visually, any SQLite client works (DB Browser for SQLite / DBeaver).

---

<div align="center">

good luck ;)

</div>
