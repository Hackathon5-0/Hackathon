"use client";
import { useMemo, useState } from "react";
import {
  evaluateLines, programCoverage, summarize,
  type Course, type Equivalency, type Institution, type LineInput, type LineResult,
} from "@/lib/engine";

type Program = { code: string; name: string; area: string };
type Row = { id: string; institutionId: string; courseId: string | "other" | ""; code: string; title: string; credits: string; grade: string };

const GRADES = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "P"];
const uid = () => Math.random().toString(36).slice(2, 9);

const STATUS: Record<LineResult["status"], { label: string; cls: string }> = {
  secure:  { label: "Likely transfers", cls: "bg-green-100 text-green-800" },
  pending: { label: "Needs department review", cls: "bg-amber-100 text-amber-800" },
  hold:    { label: "Evaluator decides", cls: "bg-blue-100 text-blue-800" },
  blocked: { label: "Will not transfer", cls: "bg-red-100 text-red-800" },
};
const NEXT_STEP: Record<string, string> = {
  maybe_syllabus_review: "Keep the course syllabus: the department will compare it with BU courses.",
  maybe_request_syllabus: "This course isn't in our data yet. You'll need to send its syllabus.",
};

export default function CheckClient(props: { institutions: Institution[]; programs: Program[]; courses: Course[]; equivalencies: Equivalency[] }) {
  const bu = props.institutions.find((i) => i.short_code === "BU")!;
  const sources = props.institutions.filter((i) => i.id !== bu.id);
  const [program, setProgram] = useState(props.programs[0]?.code ?? "");
  const [rows, setRows] = useState<Row[]>([{ id: uid(), institutionId: sources[0]?.id ?? "", courseId: "", code: "", title: "", credits: "", grade: "A" }]);

  const ctx = useMemo(() => ({
    institutions: new Map(props.institutions.map((i) => [i.id, i])),
    courses: new Map(props.courses.map((c) => [c.id, c])),
    equivalencyBySource: new Map(props.equivalencies.map((e) => [e.source_course_id, e])),
  }), [props]);
  const coursesByInst = useMemo(() => {
    const m = new Map<string, Course[]>();
    props.courses.forEach((c) => m.set(c.institution_id, [...(m.get(c.institution_id) ?? []), c]));
    return m;
  }, [props.courses]);

  const prog = props.programs.find((p) => p.code === program);
  const lines: LineInput[] = rows
    .filter((r) => r.courseId && (r.courseId !== "other" || (r.code && Number(r.credits) > 0)))
    .map((r) => {
      const c = r.courseId !== "other" ? ctx.courses.get(r.courseId) : undefined;
      return { ref: r.id, institution_id: r.institutionId, course_id: c?.id ?? null, code: c?.code ?? r.code.trim(),
               title: c?.title ?? r.title, credits: c ? Number(c.credits) : Number(r.credits), grade: r.grade };
    });
  const results = useMemo(() => evaluateLines(lines, { ...ctx, programCode: program }), [JSON.stringify(lines), program, ctx]);
  const byRef = new Map(results.map((r) => [r.ref, r]));
  const sum = summarize(results);
  const coverage = prog ? programCoverage(prog.area, results, ctx, bu.id) : [];
  const covered = coverage.filter((c) => c.state === "satisfied").length;

  const update = (id: string, patch: Partial<Row>) => setRows((rs) => rs.map((r) => (r.id === id ? { ...r, ...patch } : r)));
  const addRow = () => setRows((rs) => [...rs, { id: uid(), institutionId: rs.at(-1)?.institutionId ?? sources[0].id, courseId: "", code: "", title: "", credits: "", grade: "A" }]);
  const loadDemo = () => {
    const find = (sc: string, code: string) => {
      const inst = sources.find((s) => s.short_code === sc)!; const c = coursesByInst.get(inst.id)?.find((x) => x.code === code);
      return { id: uid(), institutionId: inst.id, courseId: c?.id ?? "", code: "", title: "", credits: "", grade: "A" } as Row;
    };
    setProgram("CS-BA");
    setRows([
      { ...find("HCC", "CSC 110"), grade: "A" }, { ...find("HCC", "MAT 151"), grade: "B+" }, { ...find("HCC", "ENG 101"), grade: "A-" },
      { ...find("HCC", "CSC 215"), grade: "B" }, { ...find("HCC", "MAT 210"), grade: "B" }, { ...find("PCU", "ECON 200"), grade: "B+" },
    ]);
  };
  const label = (id: string | null) => (id ? ctx.courses.get(id) : undefined);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">Transfer Check</h1>
          <p className="text-sm text-slate-600">An instant, unofficial estimate. Nothing you enter is submitted or saved.</p>
        </div>
        <button className="btn-ghost" onClick={loadDemo}>Load example student</button>
      </div>

      <div className="card space-y-4">
        <div className="max-w-sm">
          <label className="label" htmlFor="prog">BU programme you want to join</label>
          <select id="prog" className="input" value={program} onChange={(e) => setProgram(e.target.value)}>
            {props.programs.map((p) => <option key={p.code} value={p.code}>{p.name}</option>)}
          </select>
        </div>

        <div>
          <div className="label">Courses you've completed</div>
          <div className="space-y-2">
            {rows.map((r) => {
              const list = coursesByInst.get(r.institutionId) ?? [];
              const res = byRef.get(r.id);
              return (
                <div key={r.id} className="grid gap-2 rounded-lg border border-slate-200 p-2 md:grid-cols-[1.3fr_2fr_90px_auto]">
                  <select aria-label="College" className="input" value={r.institutionId}
                    onChange={(e) => update(r.id, { institutionId: e.target.value, courseId: "" })}>
                    {sources.map((s) => <option key={s.id} value={s.id}>{s.name}{s.credit_system === "quarter" ? " (quarter)" : ""}</option>)}
                  </select>
                  <div className="space-y-2">
                    <select aria-label="Course" className="input" value={r.courseId} onChange={(e) => update(r.id, { courseId: e.target.value })}>
                      <option value="">Select a course…</option>
                      {list.map((c) => <option key={c.id} value={c.id}>{c.code}: {c.title} ({Number(c.credits)} cr)</option>)}
                      <option value="other">My course isn't listed…</option>
                    </select>
                    {r.courseId === "other" && (
                      <div className="grid grid-cols-[1fr_2fr_80px] gap-2">
                        <input className="input" placeholder="Code" value={r.code} onChange={(e) => update(r.id, { code: e.target.value })} />
                        <input className="input" placeholder="Title" value={r.title} onChange={(e) => update(r.id, { title: e.target.value })} />
                        <input className="input" placeholder="Credits" inputMode="decimal" value={r.credits} onChange={(e) => update(r.id, { credits: e.target.value })} />
                      </div>
                    )}
                  </div>
                  <select aria-label="Grade" className="input" value={r.grade} onChange={(e) => update(r.id, { grade: e.target.value })}>
                    {GRADES.map((g) => <option key={g}>{g}</option>)}
                  </select>
                  <div className="flex items-center gap-2">
                    {res && <span className={`chip ${STATUS[res.status].cls}`}>{STATUS[res.status].label}</span>}
                    <button aria-label="Remove course" className="btn-ghost px-2" onClick={() => setRows((rs) => rs.filter((x) => x.id !== r.id))}>✕</button>
                  </div>
                </div>
              );
            })}
          </div>
          <button className="btn-ghost mt-2" onClick={addRow}>+ Add course</button>
        </div>
      </div>

      {results.length > 0 && (
        <>
          <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
            <Tile label="Units likely to transfer" value={sum.unitsSecure} tone="text-green-700" />
            <Tile label="Units pending review" value={sum.unitsPending} tone="text-amber-700" />
            <Tile label="Courses not transferring" value={sum.blocked} tone="text-red-700" />
            <Tile label={`${prog?.name ?? "Programme"} courses covered`} value={`${covered}/${coverage.length}`} />
          </div>

          <div className="grid gap-6 lg:grid-cols-[1.6fr_1fr]">
            <div className="card p-0">
              <div className="border-b px-5 py-3 font-semibold">Course by course</div>
              <ul className="divide-y">
                {results.map((r) => {
                  const row = rows.find((x) => x.id === r.ref)!; const inst = ctx.institutions.get(row.institutionId);
                  const buc = label(r.buCourseId);
                  return (
                    <li key={r.ref} className="space-y-1 px-5 py-3">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div className="font-medium">{r.code} <span className="text-sm font-normal text-slate-500">· {inst?.short_code}</span></div>
                        <span className={`chip ${STATUS[r.status].cls}`}>{STATUS[r.status].label}</span>
                      </div>
                      <div className="text-sm">
                        {r.path === "existing_equivalency" && r.status !== "blocked" ? (
                          <>→ <b>{r.buLabel}</b>{buc && <span className="text-slate-500">: {buc.title}</span>} · {r.unitsConverted} units</>
                        ) : r.status === "blocked" ? <>→ 0 units</> : <>→ Possible {r.unitsConverted} units after review</>}
                      </div>
                      {NEXT_STEP[r.path] && <div className="text-sm text-slate-600">{NEXT_STEP[r.path]}</div>}
                      {r.flags.length > 0 && <ul className="list-disc pl-5 text-xs text-slate-600">{r.flags.map((f) => <li key={f}>{f}</li>)}</ul>}
                    </li>
                  );
                })}
              </ul>
            </div>

            <div className="card p-0">
              <div className="border-b px-5 py-3 font-semibold">{prog?.name}: programme courses</div>
              <ul className="divide-y text-sm">
                {coverage.map((c) => (
                  <li key={c.courseId} className="flex items-start justify-between gap-2 px-5 py-2">
                    <div><div className="font-medium">{c.code}</div><div className="text-xs text-slate-500">{c.title} · {c.requirementType}</div></div>
                    <CoverageChip state={c.state} />
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <p className="text-xs text-slate-500">
            Transfer courses never earn BU Hub units. Grades below C don't transfer, and outside grades don't count toward your BU GPA.
            Quarter credits convert at 2/3. This is an estimate: the Credit Evaluation office and academic departments make the final decision.
          </p>
        </>
      )}
    </div>
  );
}

function Tile({ label, value, tone = "" }: { label: string; value: number | string; tone?: string }) {
  return <div className="card p-4"><div className="text-xs text-slate-500">{label}</div><div className={`text-2xl font-bold ${tone}`}>{value}</div></div>;
}
function CoverageChip({ state }: { state: "satisfied" | "pending" | "bu_only" | "open" }) {
  const m = { satisfied: ["Covered", "bg-green-100 text-green-800"], pending: ["Pending", "bg-amber-100 text-amber-800"],
              bu_only: ["Must take at BU", "bg-slate-200 text-slate-700"], open: ["Still to take", "bg-slate-100 text-slate-500"] }[state];
  return <span className={`chip whitespace-nowrap ${m[1]}`}>{m[0]}</span>;
}
