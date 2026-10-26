import { getStaff } from "@/lib/supabase/server";

export default async function AdminHome() {
  const { sb } = await getStaff();
  const count = async (table: string, filter?: (q: any) => any) => {
    let q = sb.from(table).select("*", { count: "exact", head: true });
    if (filter) q = filter(q);
    const { count } = await q; return count ?? 0;
  };
  const [received, review, done, students, eqs] = await Promise.all([
    count("transcripts", (q) => q.in("status", ["received", "parsed"])),
    count("evaluation_items", (q) => q.eq("status", "pending_review")),
    count("transcripts", (q) => q.eq("status", "completed")),
    count("students"),
    count("equivalencies", (q) => q.eq("active", true)),
  ]);
  const { data: recent } = await sb.from("transcripts")
    .select("id, received_date, status, source, is_official, students(external_id, full_name), institutions(short_code)")
    .order("received_date", { ascending: false }).limit(8);

  const tiles = [["Transcripts waiting", received], ["Courses to review", review], ["Completed", done], ["Students", students], ["Equivalencies", eqs]];
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
        {tiles.map(([l, v]) => (
          <div key={l as string} className="card p-4"><div className="text-xs text-slate-500">{l}</div><div className="text-2xl font-bold">{v}</div></div>
        ))}
      </div>
      <div className="card p-0">
        <div className="border-b px-5 py-3 font-semibold">Recent transcripts</div>
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
            <tr><th className="px-5 py-2">Student</th><th>From</th><th>Received</th><th>Source</th><th>Copy</th><th>Status</th></tr>
          </thead>
          <tbody>
            {(recent ?? []).map((t: any) => (
              <tr key={t.id} className="border-t">
                <td className="px-5 py-2">{t.students?.full_name} <span className="text-slate-400">{t.students?.external_id}</span></td>
                <td>{t.institutions?.short_code}</td><td>{t.received_date}</td><td>{t.source.replace("_", " ")}</td>
                <td>{t.is_official ? <span className="chip bg-green-100 text-green-800">official</span> : <span className="chip bg-amber-100 text-amber-800">unofficial</span>}</td>
                <td>{t.status.replace("_", " ")}</td>
              </tr>
            ))}
            {!recent?.length && <tr><td colSpan={6} className="px-5 py-6 text-center text-slate-500">No transcripts yet. Run seed.sql to load the synthetic data.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
