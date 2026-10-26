-- =====================================================================
-- Transfer Credit Evaluation: core schema
-- Step 1 of the build. Run in the Supabase SQL Editor (or `supabase db push`).
-- =====================================================================

create extension if not exists "pgcrypto";

-- ---------- Enums ----------
create type credit_system      as enum ('semester', 'quarter');
create type institution_type   as enum ('receiving_university', 'peer_university', 'community_college', 'university');
create type outcome_type       as enum ('bu_equivalent', 'combined_equivalent', 'elective_credit', 'no_credit');
create type decision_status    as enum ('active', 'superseded');
create type transcript_source  as enum ('gmail', 'admin_upload', 'manual_entry', 'web_form');
create type transcript_status  as enum ('received', 'parsed', 'evaluating', 'pending_review', 'completed', 'rejected', 'error');
create type evaluation_path    as enum ('existing_equivalency', 'maybe_syllabus_review', 'maybe_request_syllabus', 'blocked_by_rule');
create type item_status        as enum ('pending_review', 'approved', 'edited', 'rejected', 'awaiting_syllabus');
create type review_action      as enum ('approve', 'edit', 'reject', 'request_syllabus', 'comment');
create type staff_role         as enum ('admin', 'evaluator');
create type request_status     as enum ('draft', 'sent', 'received', 'cancelled');

-- ---------- Staff (only evaluators/admins log in) ----------
create table staff_profiles (
  user_id     uuid primary key references auth.users(id) on delete cascade,
  full_name   text not null,
  role        staff_role not null default 'evaluator',
  department  text,
  active      boolean not null default true,
  created_at  timestamptz not null default now()
);

-- ---------- Reference data ----------
create table institutions (
  id             uuid primary key default gen_random_uuid(),
  name           text not null unique,
  short_code     text not null unique,
  type           institution_type not null,
  credit_system  credit_system not null default 'semester',
  is_fictional   boolean not null default false,
  registrar_email text,                       -- used by "Request transcript"
  created_at     timestamptz not null default now()
);

create table programs (
  id          uuid primary key default gen_random_uuid(),
  code        text not null unique,           -- e.g. CS-BA
  name        text not null,                  -- BA in Computer Science
  area        text not null,                  -- Computer Science (matches courses.program_area)
  school      text not null,
  key_rules   text,
  source_url  text
);

create table courses (
  id                 uuid primary key default gen_random_uuid(),
  institution_id     uuid not null references institutions(id) on delete cascade,
  code               text not null,
  title              text not null,
  program_area       text,
  requirement_type   text,                    -- BU only: Core (Group A), Group C (BU only) ...
  credits            numeric(4,2) not null,
  description        text,
  learning_outcomes  text[],
  verified           text,                    -- Yes / Check (from supplied workbook)
  data_origin        text,
  unique (institution_id, code)
);
create index on courses (institution_id);

create table transfer_rules (
  id          text primary key,               -- R1..R11
  name        text not null,
  parameter   jsonb not null default '{}'::jsonb,
  applies_to  text,
  action      text,
  source      text,
  active      boolean not null default true
);

create table past_decisions (
  id                    text primary key,     -- D-001
  decision_date         date not null,
  source_course_id      uuid not null references courses(id),
  outcome               outcome_type not null,
  bu_course_id          uuid references courses(id),
  bu_label              text not null,        -- BU code or 'CAS CS elective' / '—'
  units_awarded         numeric(5,2) not null,
  requirement_satisfied text,
  syllabus_reviewed     boolean not null default false,
  department            text,
  evaluator_code        text,
  status                decision_status not null default 'active',
  reusable              boolean not null default true,
  rationale             text
);

-- Equivalency DB: the lookup table checked first
create table equivalencies (
  id                    uuid primary key default gen_random_uuid(),
  source_course_id      uuid not null references courses(id) on delete cascade,
  outcome               outcome_type not null,
  bu_course_id          uuid references courses(id),
  bu_label              text not null,
  units                 numeric(5,2) not null,  -- already converted to BU semester units
  requirement_satisfied text,
  condition             text,                   -- e.g. 'Only with CSE 143'
  effective_date        date not null default current_date,
  review_by             date,
  decision_id           text references past_decisions(id),
  active                boolean not null default true,
  created_by            uuid references auth.users(id),
  created_at            timestamptz not null default now()
);
create unique index equivalencies_one_active on equivalencies (source_course_id) where active;

-- ---------- Students & transcripts (students do not log in) ----------
create table students (
  id                          uuid primary key default gen_random_uuid(),
  external_id                 text unique,      -- SYN-1001
  full_name                   text not null,
  email                       text,
  intended_program_id         uuid references programs(id),
  bu_start_date               date,
  prior_econ_200_after_matric int not null default 0,
  notes                       text,
  created_at                  timestamptz not null default now()
);

create table inbound_emails (
  id            uuid primary key default gen_random_uuid(),
  provider      text not null default 'gmail',
  message_id    text not null unique,           -- prevents double-processing
  from_address  text,
  subject       text,
  received_at   timestamptz,
  body_text     text,
  attachment_paths text[],
  status        text not null default 'received', -- received / processed / ignored / error
  error         text,
  created_at    timestamptz not null default now()
);

create table transcripts (
  id               uuid primary key default gen_random_uuid(),
  student_id       uuid not null references students(id) on delete cascade,
  institution_id   uuid references institutions(id),
  source           transcript_source not null,
  inbound_email_id uuid references inbound_emails(id),
  file_path        text,                        -- storage: transcripts/<id>.pdf
  received_date    date not null default current_date,
  status           transcript_status not null default 'received',
  submitted_by     uuid references auth.users(id),
  notes            text,
  created_at       timestamptz not null default now()
);
create index on transcripts (status);

create table transcript_courses (
  id                        uuid primary key default gen_random_uuid(),
  transcript_id             uuid not null references transcripts(id) on delete cascade,
  line_ref                  text,               -- TL-001 (synthetic data)
  term                      text,
  course_code               text not null,
  course_title              text,
  credits                   numeric(4,2) not null,
  grade                     text,
  taken_after_matriculation boolean not null default false,
  course_id                 uuid references courses(id)  -- matched catalogue course, if any
);
create index on transcript_courses (transcript_id);

create table syllabi (
  id           uuid primary key default gen_random_uuid(),
  course_id    uuid references courses(id),
  transcript_course_id uuid references transcript_courses(id),
  file_path    text not null,
  uploaded_by  uuid references auth.users(id),
  uploaded_at  timestamptz not null default now()
);

-- ---------- Evaluation (written by the rules engine / agent) ----------
create table evaluations (
  id             uuid primary key default gen_random_uuid(),
  transcript_id  uuid not null references transcripts(id) on delete cascade,
  engine_version text not null,
  run_at         timestamptz not null default now(),
  summary        jsonb                          -- secure / pending units etc.
);

create table evaluation_items (
  id                       uuid primary key default gen_random_uuid(),
  evaluation_id            uuid not null references evaluations(id) on delete cascade,
  transcript_course_id     uuid not null references transcript_courses(id) on delete cascade,
  path                     evaluation_path not null,
  equivalency_id           uuid references equivalencies(id),
  recommended_bu_course_id uuid references courses(id),
  recommended_label        text,
  units_converted          numeric(5,2),        -- after quarter conversion
  units_recommended        numeric(5,2),        -- 0 if a rule blocks
  rule_ids                 text[] not null default '{}',
  flags                    text[] not null default '{}',
  confidence               numeric(3,2),        -- filled by AI matcher later
  rationale                text,
  status                   item_status not null default 'pending_review',
  final_bu_course_id       uuid references courses(id),
  final_label              text,
  final_units              numeric(5,2),
  decided_by               uuid references auth.users(id),
  decided_at               timestamptz
);
create index on evaluation_items (evaluation_id);
create index on evaluation_items (status);

create table reviews (
  id                   uuid primary key default gen_random_uuid(),
  evaluation_item_id   uuid not null references evaluation_items(id) on delete cascade,
  reviewer_id          uuid not null references auth.users(id),
  action               review_action not null,
  final_bu_course_id   uuid references courses(id),
  final_label          text,
  final_units          numeric(5,2),
  feedback             text,
  add_to_equivalency_db boolean not null default false,
  created_at           timestamptz not null default now()
);

-- ---------- Transcript requests (admin asks a college to send one) ----------
create table transcript_requests (
  id              uuid primary key default gen_random_uuid(),
  student_id      uuid references students(id),
  student_name    text not null,
  student_email   text,
  institution_id  uuid references institutions(id),
  sent_to_email   text,
  message         text,
  status          request_status not null default 'draft',
  requested_by    uuid references auth.users(id),
  sent_at         timestamptz,
  created_at      timestamptz not null default now()
);

-- ---------- Audit log ----------
create table audit_log (
  id          bigint generated always as identity primary key,
  actor_id    uuid,
  action      text not null,
  entity      text not null,
  entity_id   text,
  details     jsonb,
  at          timestamptz not null default now()
);

-- ---------- Helpers ----------
-- BU rule R2: quarter credits x 2/3, truncated to 2 dp (4 -> 2.66)
create or replace function to_bu_units(credits numeric, sys credit_system)
returns numeric language sql immutable as $$
  select case when sys = 'quarter' then trunc(credits * 2 / 3, 2) else credits end
$$;

-- Reviewer queue view
create or replace view review_queue with (security_invoker = true) as
select ei.id as item_id, t.id as transcript_id, s.external_id, s.full_name as student_name,
       i.name as institution, tc.course_code, tc.course_title, tc.credits, tc.grade,
       ei.path, ei.recommended_label, ei.units_recommended, ei.flags, ei.status, e.run_at
from evaluation_items ei
join evaluations e        on e.id = ei.evaluation_id
join transcript_courses tc on tc.id = ei.transcript_course_id
join transcripts t        on t.id = tc.transcript_id
join students s           on s.id = t.student_id
left join institutions i  on i.id = t.institution_id;
