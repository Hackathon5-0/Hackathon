# Transfer Credit Evaluation: Supabase + Next.js

Hackathon prototype for BU transfer credit evaluation. **All data is synthetic.**

## Build steps
| # | Step | Status |
|---|------|--------|
| 1 | Database schema, security (RLS), storage buckets, seed data | ✅ this package |
| 2 | Next.js app + admin login (email/password) | ✅ `web/` |
| 3 | Public Transfer Check screen (read-only) | ✅ `web/src/app/check` |
| 4 | Admin upload / manual entry + inbox | next |
| 5 | Rules engine + review/approve/feedback screens | |
| 6 | Gmail inbox polling (students email transcripts) + public "Submit transcript" form | |
| 7 | AI matcher for "maybe" courses (Gemini / open source) | later |

## Step 1: set up the database

1. Create a Supabase project.
2. Open **SQL Editor** and run these files **in order**, one at a time:
   1. `supabase/migrations/20261026000001_schema.sql`: tables, enums, the review view and the `to_bu_units()` quarter-conversion function
   2. `supabase/migrations/20261026000002_security.sql`: RLS policies and the private `transcripts` / `syllabi` buckets
   3. `supabase/seed.sql`: synthetic data (154 courses, 111 decisions, 108 equivalencies, 5 students, 7 transcripts, 35 course lines)
   4. `supabase/migrations/20261026000003_student_emails.sql`: students email transcripts in; adds official/unofficial tracking and rule R12; removes admin transcript requests
3. **Turn off public sign-up** (students never log in): Authentication → Sign In / Providers → turn off *Allow new users to sign up*. Keep *Email* provider enabled.
4. **Create your first admin**: Authentication → Users → *Add user* (email + password, auto-confirm). Then in SQL Editor:
   ```sql
   insert into staff_profiles (user_id, full_name, role)
   select id, 'Your Name', 'admin' from auth.users where email = 'you@example.com';
   ```
5. (Optional) Upload the PDFs in `data/transcripts` to the `transcripts` bucket, keeping their file names, and the PDFs in `data/syllabi` to the `syllabi` bucket.
6. Configure the web app with the **Project URL** and either the **anon key** or **publishable key** (Settings → API). **Never use or share the `service_role` key** in the web app.

### Quick checks (SQL Editor)
```sql
select count(*) from courses;           -- 154
select count(*) from equivalencies;     -- 108
select to_bu_units(4, 'quarter');       -- 2.66
```

## Who can see what (RLS)
| Data | Public site (anon) | Evaluator | Admin |
|------|-------------------|-----------|-------|
| Institutions, programmes, courses, rules, active equivalencies | read | read | read/write |
| Students, transcripts, evaluations, past decisions, emails | none | read/write | read/write |
| Reviews, audit log | none | read + insert as self (no edits) | same |
| Staff profiles | none | read | manage |
| Transcript / syllabus files | none | read/upload | read/upload |

The public "Submit transcript" form (step 6) writes through a server function with the service role, never through the anon key.

## Data model (main tables)
`institutions → courses → equivalencies / past_decisions` (reference)
`students → transcripts → transcript_courses` (input; `transcripts.source` = gmail / admin_upload / manual_entry / web_form)
`evaluations → evaluation_items → reviews` (engine output → human decision + feedback)
Supporting: `inbound_emails`, `syllabi`, `staff_profiles`, `audit_log`, `transfer_rules` (R1–R12 as JSON parameters).

## How transcripts arrive
- **Student emails the college** (BU's Gmail inbox) with the transcript PDF attached. The poller saves the email, matches the student by email/ID and marks the copy **unofficial** (`sender_type = student`).
- **College registrar emails it**: a sender on the institution's `email_domain` is marked **official**.
- **Admin upload / manual entry**: the admin sets official or unofficial.
- **Public web form**: treated like a student email (unofficial).

Rule R12: unofficial transcripts are evaluated as a preview, so students and evaluators see likely results early, but final posting waits for an official copy.

## Regenerate seed
`python3 scripts/gen_seed.py` (needs the synthetic generator in `scripts/synth/`).
