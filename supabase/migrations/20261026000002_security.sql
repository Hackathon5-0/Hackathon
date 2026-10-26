-- =====================================================================
-- Row Level Security + Storage
--   * anon (public site):  read-only catalogue data for the Transfer Check screen.
--                          No direct writes. The public "Submit transcript" form
--                          goes through an Edge Function (service role), not anon.
--   * staff (logged-in evaluators/admins): full access to operational data.
--   * admin only:          manage staff, rules and the equivalency DB directly.
-- =====================================================================

create or replace function is_staff() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from staff_profiles where user_id = auth.uid() and active)
$$;

create or replace function is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from staff_profiles where user_id = auth.uid() and active and role = 'admin')
$$;

-- Enable RLS on every table
do $$ declare t text; begin
  foreach t in array array['staff_profiles','institutions','programs','courses','transfer_rules','past_decisions',
    'equivalencies','students','inbound_emails','transcripts','transcript_courses','syllabi','evaluations',
    'evaluation_items','reviews','transcript_requests','audit_log']
  loop execute format('alter table %I enable row level security', t); end loop;
end $$;

-- ---------- Public read (Transfer Check screen) ----------
create policy "public read institutions" on institutions   for select to anon, authenticated using (true);
create policy "public read programs"     on programs       for select to anon, authenticated using (true);
create policy "public read courses"      on courses        for select to anon, authenticated using (true);
create policy "public read rules"        on transfer_rules for select to anon, authenticated using (active);
create policy "public read equivalencies" on equivalencies for select to anon, authenticated using (active);

-- ---------- Reference data writes: admin only ----------
create policy "admin write institutions" on institutions   for all to authenticated using (is_admin()) with check (is_admin());
create policy "admin write programs"     on programs       for all to authenticated using (is_admin()) with check (is_admin());
create policy "admin write courses"      on courses        for all to authenticated using (is_admin()) with check (is_admin());
create policy "admin write rules"        on transfer_rules for all to authenticated using (is_admin()) with check (is_admin());
-- evaluators may add equivalencies (via "add to equivalency DB" on approve)
create policy "staff write equivalencies" on equivalencies for all to authenticated using (is_staff()) with check (is_staff());
-- staff also need to see inactive equivalencies
create policy "staff read all equivalencies" on equivalencies for select to authenticated using (is_staff());

-- ---------- Staff profiles ----------
create policy "staff read staff"   on staff_profiles for select to authenticated using (is_staff());
create policy "admin manage staff" on staff_profiles for all    to authenticated using (is_admin()) with check (is_admin());

-- ---------- Operational data: staff only ----------
do $$ declare t text; begin
  foreach t in array array['past_decisions','students','inbound_emails','transcripts','transcript_courses',
    'syllabi','evaluations','evaluation_items','transcript_requests']
  loop
    execute format('create policy "staff all %1$s" on %1$I for all to authenticated using (is_staff()) with check (is_staff())', t);
  end loop;
end $$;

-- Reviews: staff read all; can only insert as themselves; no edits/deletes (keeps history honest)
create policy "staff read reviews"   on reviews for select to authenticated using (is_staff());
create policy "staff insert reviews" on reviews for insert to authenticated with check (is_staff() and reviewer_id = auth.uid());

-- Audit log: staff read, insert as themselves; never update/delete
create policy "staff read audit"   on audit_log for select to authenticated using (is_staff());
create policy "staff insert audit" on audit_log for insert to authenticated with check (is_staff() and actor_id = auth.uid());

-- ---------- Storage buckets (private) ----------
insert into storage.buckets (id, name, public) values ('transcripts', 'transcripts', false) on conflict (id) do nothing;
insert into storage.buckets (id, name, public) values ('syllabi', 'syllabi', false)         on conflict (id) do nothing;

create policy "staff read files"   on storage.objects for select to authenticated using (bucket_id in ('transcripts','syllabi') and is_staff());
create policy "staff upload files" on storage.objects for insert to authenticated with check (bucket_id in ('transcripts','syllabi') and is_staff());
create policy "staff update files" on storage.objects for update to authenticated using (bucket_id in ('transcripts','syllabi') and is_staff());
