import { supabaseServer } from "@/lib/supabase/server";
import CheckClient from "./CheckClient";

export const revalidate = 300; // catalogue data changes rarely

export default async function CheckPage() {
  const sb = await supabaseServer();
  const [inst, progs, courses, eqs] = await Promise.all([
    sb.from("institutions").select("id, name, short_code, credit_system").order("name"),
    sb.from("programs").select("code, name, area").order("name"),
    sb.from("courses").select("id, institution_id, code, title, program_area, requirement_type, credits").order("code"),
    sb.from("equivalencies").select("source_course_id, outcome, bu_course_id, bu_label, units, requirement_satisfied, condition, decision_id").eq("active", true),
  ]);
  const err = inst.error || progs.error || courses.error || eqs.error;
  if (err) return <div className="card text-red-700">Could not load catalogue data: {err.message}</div>;
  if (!courses.data?.length) return <div className="card">No catalogue data yet. Run <code>supabase/seed.sql</code> in the Supabase SQL Editor.</div>;
  return <CheckClient institutions={inst.data!} programs={progs.data!} courses={courses.data!} equivalencies={eqs.data!} />;
}
