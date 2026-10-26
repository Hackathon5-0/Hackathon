-- =====================================================================
-- Change: students email their transcripts to the college (BU's Gmail inbox).
-- Admins no longer send transcript requests, so that feature is removed.
-- Safe to run whether or not migrations 1-2 and the seed have already run.
-- =====================================================================

drop table if exists transcript_requests;
drop type  if exists request_status;

-- Who sent the email: the student, a college registrar, or unknown
alter table inbound_emails
  add column if not exists sender_type        text not null default 'unknown'
    check (sender_type in ('student', 'college_registrar', 'unknown')),
  add column if not exists matched_student_id uuid references students(id),
  add column if not exists matched_institution_id uuid references institutions(id);

-- Official vs unofficial copy: a PDF the student forwards is treated as unofficial
alter table transcripts
  add column if not exists is_official        boolean not null default false,
  add column if not exists verification_note  text;

-- Used to recognise registrar emails (e.g. registrar@hcc.example.edu -> official)
alter table institutions
  add column if not exists email_domain text;
update institutions set email_domain = lower(short_code) || '.example.edu' where email_domain is null;

-- Seeded transcripts were "uploaded by admin" from the registrar copy -> official
update transcripts set is_official = true where source = 'admin_upload' and notes = 'Synthetic seed transcript';

-- New rule: unofficial transcripts can be evaluated as a preview, but not posted
insert into transfer_rules (id, name, parameter, applies_to, action, source) values
 ('R12', 'Official transcript required to post',
  '{"official_sources": ["college_registrar", "admin_upload_verified"], "unofficial_action": "preview_only"}',
  'All transcripts', 'Evaluate as preview; block final posting until an official copy is received',
  'Problem statement step 2 (official final transcripts)')
on conflict (id) do nothing;

-- Review queue now shows whether the transcript is official
drop view if exists review_queue;
create view review_queue with (security_invoker = true) as
select ei.id as item_id, t.id as transcript_id, s.external_id, s.full_name as student_name,
       i.name as institution, t.source, t.is_official, tc.course_code, tc.course_title, tc.credits, tc.grade,
       ei.path, ei.recommended_label, ei.units_recommended, ei.flags, ei.status, e.run_at
from evaluation_items ei
join evaluations e         on e.id = ei.evaluation_id
join transcript_courses tc on tc.id = ei.transcript_course_id
join transcripts t         on t.id = tc.transcript_id
join students s            on s.id = t.student_id
left join institutions i   on i.id = t.institution_id;
