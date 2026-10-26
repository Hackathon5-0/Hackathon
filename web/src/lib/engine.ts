/**
 * Transfer credit rules engine (deterministic, no AI).
 * Shared by the public Transfer Check screen and the admin evaluation pipeline.
 * Rule IDs match the `transfer_rules` table (R1–R12).
 */

export type CreditSystem = "semester" | "quarter";
export type Outcome = "bu_equivalent" | "combined_equivalent" | "elective_credit" | "no_credit";
export type Path = "existing_equivalency" | "maybe_syllabus_review" | "maybe_request_syllabus" | "blocked_by_rule";
export type LineStatus = "secure" | "pending" | "hold" | "blocked";

export interface Institution { id: string; name: string; short_code: string; credit_system: CreditSystem }
export interface Course {
  id: string; institution_id: string; code: string; title: string; program_area: string | null;
  requirement_type: string | null; credits: number; description?: string | null; learning_outcomes?: string[] | null;
}
export interface Equivalency {
  source_course_id: string; outcome: Outcome; bu_course_id: string | null; bu_label: string;
  units: number; requirement_satisfied: string | null; condition: string | null; decision_id: string | null;
}

export interface LineInput {
  ref: string;                      // any stable id (transcript_course id or UI row id)
  institution_id: string;
  course_id: string | null;         // matched catalogue course, null if unknown
  code: string; title?: string; credits: number; grade: string;
  taken_after_matriculation?: boolean;
}

export interface EvalContext {
  institutions: Map<string, Institution>;
  courses: Map<string, Course>;                 // all courses by id (incl. BU)
  equivalencyBySource: Map<string, Equivalency>; // active equivalency by source course id
  programCode?: string | null;                  // CS-BA, EC-BA, ...
  buStartDate?: string | null;                  // ISO date
  receivedDate?: string | null;                 // ISO date the transcript arrived
  isOfficial?: boolean | null;                  // R12; null/undefined = not applicable (public check)
  priorEcon200AfterMatric?: number;
}

export interface LineResult {
  ref: string; code: string;
  path: Path; status: LineStatus;
  buCourseId: string | null; buLabel: string | null;
  unitsConverted: number;      // after quarter conversion (R2)
  unitsSecure: number;         // counted now
  unitsPending: number;        // may be added after review
  ruleIds: string[]; flags: string[];
  rationale: string;
  decisionId: string | null;
}

export const PASSING_GRADES = ["A", "A-", "B+", "B", "B-", "C+", "C"];
export const DEVELOPMENTAL = new Set(["HCC:MAT 090"]);
export const ECON_CAP = { program: "EC-BA", max: 4, courses: new Set(["CAS EC 201", "CAS EC 202", "CAS EC 203", "CAS EC 204"]) };
export const GROUP_C = ["CAS CS 320", "CAS CS 332", "CAS CS 350"];
export const ENGINE_VERSION = "rules-1.0";

/** R2: quarter credits × 2/3, truncated to 2 decimals (BU example: 4 → 2.66). */
export function toBuUnits(credits: number, system: CreditSystem): number {
  if (system !== "quarter") return credits;
  return Math.floor(Math.round(credits * 2 / 3 * 1e6) / 1e4) / 100;
}

const daysBetween = (a: string, b: string) => (Date.parse(b) - Date.parse(a)) / 86_400_000;

export function evaluateLines(lines: LineInput[], ctx: EvalContext): LineResult[] {
  let econCount = ctx.priorEcon200AfterMatric ?? 0;
  const codesByInstitution = new Map<string, Set<string>>();
  for (const l of lines) {
    if (!codesByInstitution.has(l.institution_id)) codesByInstitution.set(l.institution_id, new Set());
    codesByInstitution.get(l.institution_id)!.add(l.code.trim().toUpperCase());
  }

  return lines.map((l) => {
    const inst = ctx.institutions.get(l.institution_id);
    const system: CreditSystem = inst?.credit_system ?? "semester";
    const units = toBuUnits(Number(l.credits), system);
    const flags: string[] = [];
    const ruleIds: string[] = [];
    const grade = (l.grade || "").trim().toUpperCase();
    const r: LineResult = {
      ref: l.ref, code: l.code, path: "maybe_syllabus_review", status: "pending",
      buCourseId: null, buLabel: null, unitsConverted: units, unitsSecure: 0, unitsPending: 0,
      ruleIds, flags, rationale: "", decisionId: null,
    };

    if (system === "quarter") { ruleIds.push("R2"); flags.push(`Quarter conversion: ${l.credits} × 2/3 = ${units} BU units`); }

    // --- Lookup (process steps 3–5) ---
    const eq = l.course_id ? ctx.equivalencyBySource.get(l.course_id) : undefined;
    if (!l.course_id) {
      r.path = "maybe_request_syllabus";
      r.rationale = "Course not found in catalogue data. Request the syllabus for department review.";
    } else if (!eq) {
      r.path = "maybe_syllabus_review";
      r.rationale = "No existing equivalency. Listed as 'maybe': department evaluator reviews the syllabus.";
    } else {
      r.path = "existing_equivalency";
      r.decisionId = eq.decision_id;
      r.buCourseId = eq.bu_course_id;
      r.buLabel = eq.bu_label;
      r.rationale = `Existing equivalency${eq.decision_id ? ` (${eq.decision_id})` : ""}.`;
      if (eq.outcome === "no_credit") {
        r.path = "blocked_by_rule"; r.status = "blocked"; r.buLabel = "No credit";
        r.rationale = `Existing decision${eq.decision_id ? ` ${eq.decision_id}` : ""}: no credit.`;
      }
      if (eq.condition?.startsWith("Only with")) {
        const partner = eq.condition.replace("Only with", "").trim().toUpperCase();
        if (!codesByInstitution.get(l.institution_id)?.has(partner)) {
          r.buCourseId = null; r.buLabel = "Elective credit (partner course missing)";
          flags.push(`Combined equivalency: counts as ${eq.bu_label} only together with ${partner}`);
        } else flags.push(`Combined with ${partner} = ${eq.bu_label}`);
      }
      if (eq.condition?.startsWith("Group C")) {
        ruleIds.push("R6"); flags.push("CS Group C requirement must be taken at BU: elective credit only");
      }
    }

    // --- Rules that change units ---
    const devKey = `${inst?.short_code}:${l.code}`;
    if (DEVELOPMENTAL.has(devKey)) {
      ruleIds.push("R10"); flags.push("Developmental (pre-college) course: no credit");
      r.path = "blocked_by_rule"; r.status = "blocked";
    }
    if (grade === "P") {
      ruleIds.push("R9"); flags.push("Pass/Fail grade: cannot confirm C or higher, so the evaluator decides");
      if (r.status !== "blocked") r.status = "hold";
    } else if (grade && !PASSING_GRADES.includes(grade)) {
      ruleIds.push("R1"); flags.push(`Grade ${grade} is below C: no credit`);
      r.path = "blocked_by_rule"; r.status = "blocked";
    }
    if (ctx.buStartDate && ctx.receivedDate && daysBetween(ctx.buStartDate, ctx.receivedDate) > 365) {
      ruleIds.push("R4"); flags.push("Transcript received more than 1 year after BU start: deadline exceeded, exception needed");
      r.status = "blocked";
    }
    if (ctx.programCode === ECON_CAP.program && l.taken_after_matriculation && r.buCourseId) {
      const buCode = ctx.courses.get(r.buCourseId)?.code;
      if (buCode && ECON_CAP.courses.has(buCode)) {
        econCount += 1;
        if (econCount > ECON_CAP.max) {
          ruleIds.push("R7");
          flags.push(`Economics cap: 200+ level transfer #${econCount} after matriculation (max ${ECON_CAP.max}); the evaluator chooses which count`);
          if (r.status !== "blocked") r.status = "hold";
        }
      }
    }

    // --- Units ---
    if (r.status === "blocked") { r.unitsSecure = 0; r.unitsPending = 0; }
    else if (r.status === "hold") { r.unitsPending = units; }
    else if (r.path === "existing_equivalency") { r.status = "secure"; r.unitsSecure = units; }
    else { r.status = "pending"; r.unitsPending = units; }
    if (ctx.isOfficial === false) {
      ruleIds.push("R12"); flags.push("Unofficial copy: preview only, posting needs an official transcript");
    }
    return r;
  });
}

export interface ProgramCoverage {
  courseId: string; code: string; title: string; requirementType: string | null;
  state: "satisfied" | "pending" | "bu_only" | "open"; byRef?: string;
}

/** Which BU programme courses the transfer lines would satisfy. */
export function programCoverage(programArea: string, results: LineResult[], ctx: EvalContext, buInstitutionId: string): ProgramCoverage[] {
  const bu = [...ctx.courses.values()].filter((c) => c.institution_id === buInstitutionId && c.program_area === programArea);
  return bu.map((c) => {
    const sat = results.find((r) => r.buCourseId === c.id && r.status === "secure");
    const pend = results.find((r) => r.buCourseId === c.id && (r.status === "hold" || r.status === "pending"));
    const state: ProgramCoverage["state"] = GROUP_C.includes(c.code) ? "bu_only" : sat ? "satisfied" : pend ? "pending" : "open";
    return { courseId: c.id, code: c.code, title: c.title, requirementType: c.requirement_type, state, byRef: (sat ?? pend)?.ref };
  });
}

export function summarize(results: LineResult[]) {
  const sum = (f: (r: LineResult) => number) => Math.round(results.reduce((a, r) => a + f(r), 0) * 100) / 100;
  return {
    courses: results.length,
    secure: results.filter((r) => r.status === "secure").length,
    pending: results.filter((r) => r.status === "pending").length,
    hold: results.filter((r) => r.status === "hold").length,
    blocked: results.filter((r) => r.status === "blocked").length,
    unitsSecure: sum((r) => r.unitsSecure),
    unitsPending: sum((r) => r.unitsPending),
  };
}
