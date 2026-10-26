/** Scores the rules engine against the synthetic Answer Key (35 transcript lines). Run: npm run test:engine */
import fs from "node:fs";
import path from "node:path";
import { evaluateLines, type Course, type Equivalency, type Institution, type LineInput } from "../src/lib/engine";

const fx = JSON.parse(fs.readFileSync(path.join(__dirname, "fixture.json"), "utf8"));
const institutions = new Map<string, Institution>(fx.institutions.map((i: Institution) => [i.id, i]));
const courses = new Map<string, Course>(fx.courses.map((c: Course) => [c.id, c]));
const equivalencyBySource = new Map<string, Equivalency>(fx.equivalencies.map((e: Equivalency) => [e.source_course_id, e]));
const key = new Map<string, any>(fx.answer_key.map((k: any) => [k.lid, k]));

let pass = 0, fail = 0;
for (const s of fx.students) {
  const lines = fx.lines.filter((l: any) => l.sid === s.external_id);
  // evaluate per transcript (institution), as the pipeline does
  const byInst = new Map<string, any[]>();
  lines.forEach((l: any) => byInst.set(l.institution_id, [...(byInst.get(l.institution_id) ?? []), l]));
  let prior = s.prior_econ;
  for (const [, ls] of byInst) {
    const input: LineInput[] = ls.map((l: any) => ({ ref: l.line_ref, institution_id: l.institution_id, course_id: l.course_id, code: l.code,
      credits: l.credits, grade: l.grade, taken_after_matriculation: l.after_matric }));
    const res = evaluateLines(input, { institutions, courses, equivalencyBySource, programCode: s.program, buStartDate: s.bu_start_date,
      receivedDate: ls[0].received, isOfficial: true, priorEcon200AfterMatric: prior });
    for (const r of res) {
      const k = key.get(r.ref);
      const expPath = k.path.startsWith("Maybe") ? (k.path.includes("request") ? "maybe_request_syllabus" : "maybe_syllabus_review") : "existing";
      const gotPath = r.path.startsWith("maybe") ? r.path : "existing";
      const checks: [string, boolean][] = [
        ["path", expPath === gotPath],
        ["bu", expPath !== "existing" || k.bu === r.buLabel || (r.status === "blocked" && (k.bu === "—" || k.units === 0 || String(k.units).startsWith("0")))],
        ["secure", Math.abs(k.secure - r.unitsSecure) < 0.005],
        ["pending", Math.abs(k.pending - r.unitsPending) < 0.005],
        ["quarter flag", k.flags.includes("Quarter conversion") === r.ruleIds.includes("R2")],
        ["grade flag", k.flags.includes("below C") === r.ruleIds.includes("R1")],
        ["P flag", k.flags.includes("Pass/Fail") === r.ruleIds.includes("R9")],
        ["deadline flag", k.flags.includes("deadline") === r.ruleIds.includes("R4")],
        ["econ cap flag", k.flags.includes("Econ cap") === r.ruleIds.includes("R7")],
        ["group C flag", k.flags.includes("Group C") === r.ruleIds.includes("R6")],
      ];
      const bad = checks.filter(([, ok]) => !ok).map(([n]) => n);
      if (bad.length) { fail++; console.log(`FAIL ${r.ref} ${s.external_id} ${r.code}: ${bad.join(", ")}`, { expected: k, got: r }); }
      else pass++;
    }
  }
}
console.log(`\nEngine vs Answer Key: ${pass}/${pass + fail} lines correct`);
process.exit(fail ? 1 : 0);
