"""Generate supabase/seed.sql from the synthetic data pack (deterministic UUIDs)."""
import sys, uuid, json, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "synth"))
import build as B

NS = uuid.UUID("6f1c2a52-5d1e-4c1a-9a51-0b7e3c1f0a11")
U = lambda *k: str(uuid.uuid5(NS, "|".join(map(str, k))))
def q(v):
    if v is None: return "null"
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, (int, float)): return repr(v)
    if isinstance(v, list): return "array[" + ",".join(q(x) for x in v) + "]::text[]" if v else "'{}'::text[]"
    return "'" + str(v).replace("'", "''") + "'"
def ins(table, cols, rows):
    out = [f"insert into {table} ({', '.join(cols)}) values"]
    out.append(",\n".join("  (" + ", ".join(q(x) for x in r) + ")" for r in rows) + ";\n")
    return "\n".join(out)

INST = [(B.BUN, "BU", "receiving_university", "semester", False), (B.NUN, "NU", "peer_university", "semester", False),
        (B.NYUN, "NYU", "peer_university", "semester", False), (B.HCC_NAME, "HCC", "community_college", "semester", True),
        (B.PCU_NAME, "PCU", "university", "quarter", True)]
SC = {n: s for n, s, *_ in INST}
sql = ["-- Seed data generated from the SYNTHETIC data pack (FDE AI Hackathon 5.0). Not official BU data.",
       "begin;"]
sql.append(ins("institutions", ["id", "name", "short_code", "type", "credit_system", "is_fictional", "registrar_email"],
    [(U("inst", s), n, s, t, c, f, f"registrar@{s.lower()}.example.edu") for n, s, t, c, f in INST]))

progs = B.rows("Programs")
PCODE = {"Computer Science": "CS-BA", "Economics": "EC-BA", "Psychology": "PS-BA", "Biology": "BI-BA", "Mathematics": "MA-BA"}
sql.append(ins("programs", ["id", "code", "name", "area", "school", "key_rules", "source_url"],
    [(U("prog", PCODE[p["Program area"]]), PCODE[p["Program area"]], p["BU program"], p["Program area"], p["BU school"], p["BU key rules"], p["BU source"]) for p in progs]))

bu_meta = {r["Course code"]: r for r in B.rows("BU Courses")}
ver = {}
for sh, inst in [("BU Courses", B.BUN), ("Northeastern Courses", B.NUN), ("NYU Courses", B.NYUN)]:
    for r in B.rows(sh): ver[(inst, r["Course code"])] = r["Verified"]
CID = lambda inst, code: U("course", SC[inst], code)
sql.append(ins("courses", ["id", "institution_id", "code", "title", "program_area", "requirement_type", "credits", "description", "learning_outcomes", "verified", "data_origin"],
    [(CID(c["inst"], c["code"]), U("inst", SC[c["inst"]]), c["code"], c["title"], c["program"],
      bu_meta[c["code"]]["Requirement type"] if c["inst"] == B.BUN else None, c["credits"], c["desc"], c["outcomes"].split("; "),
      ver.get((c["inst"], c["code"])), c["src"]) for c in B.cat]))

RULES = [
 ("R1", "Minimum grade", {"min_grade": "C", "passing": ["A", "A-", "B+", "B", "B-", "C+", "C"]}, "All courses", "Set units to 0 and explain", "Problem statement"),
 ("R2", "Quarter conversion", {"factor": "2/3", "rounding": "truncate", "decimals": 2}, "Quarter-system schools", "Convert units before posting", "Problem statement; truncation = assumption A1"),
 ("R3", "No Hub units", {"hub_units": 0}, "All transfer courses", "Never award Hub units", "Problem statement"),
 ("R4", "Deadline", {"days_from_start": 365}, "All transcripts", "Flag; posting needs an exception", "Problem statement; assumption A6"),
 ("R5", "Grade posted as T", {"posted_grade": "T"}, "All courses", "Post grade T; external grades excluded from GPA", "Problem statement"),
 ("R6", "CS Group C BU-only", {"program": "CS-BA", "courses": ["CAS CS 320", "CAS CS 332", "CAS CS 350"]}, "BA Computer Science", "Elective credit only", "Supplied workbook; assumption A3"),
 ("R7", "Economics 200+ cap", {"program": "EC-BA", "max_courses": 4, "bu_courses": ["CAS EC 201", "CAS EC 202", "CAS EC 203", "CAS EC 204"], "after_matriculation": True}, "BA Economics", "Hold 5th and later", "Supplied workbook"),
 ("R8", "Biology residency", {"program": "BI-BA", "min_bi_at_bu_beyond_107_108": 5}, "BA Biology", "Warn when exceeded", "Supplied workbook"),
 ("R9", "Pass/Fail", {"grades": ["P"]}, "All courses", "Hold for evaluator", "Assumption A4"),
 ("R10", "Developmental courses", {"courses": ["HCC:MAT 090"]}, "Pre-college courses", "No credit", "Assumption A5"),
 ("R11", "Final decision", {"auto_post_new_matches": False}, "All new matches", "Recommend only", "Problem statement ground rule")]
sql.append(ins("transfer_rules", ["id", "name", "parameter", "applies_to", "action", "source"],
    [(i, n, json.dumps(p), a, ac, s) for i, n, p, a, ac, s in RULES]).replace("'::text", "'::text"))

OUT = {"BU equivalent": "bu_equivalent", "Combined equivalent": "combined_equivalent", "Elective credit": "elective_credit", "No credit": "no_credit"}
BUC = lambda lbl: CID(B.BUN, lbl) if lbl in B.BUT else None
sql.append(ins("past_decisions", ["id", "decision_date", "source_course_id", "outcome", "bu_course_id", "bu_label", "units_awarded", "requirement_satisfied",
    "syllabus_reviewed", "department", "evaluator_code", "status", "reusable", "rationale"],
    [(d["id"], d["date"].isoformat(), CID(d["inst"], d["code"]), OUT[d["outcome"]], BUC(d["bu"]), d["bu"], d["units"], d["req"], d["syl"] == "Yes",
      d["dept"], d["evaluator"], d["status"].lower(), d["reusable"] == "Yes", d["rationale"]) for d in B.decisions]))

act = [d for d in B.decisions if d["status"] == "Active" and d["reusable"] == "Yes"]
sql.append(ins("equivalencies", ["id", "source_course_id", "outcome", "bu_course_id", "bu_label", "units", "requirement_satisfied", "condition", "effective_date", "review_by", "decision_id"],
    [(U("eq", d["id"]), CID(d["inst"], d["code"]), OUT[d["outcome"]], BUC(d["bu"]), d["bu"], d["units"], d["req"],
      ("Group C: BU-only requirement, elective credit only" if "Group C" in d["rationale"] else (d["req"] if d["req"].startswith("Only") else None)), d["date"].isoformat(), (d["date"].replace(day=1).replace(year=d["date"].year + 5)).isoformat(), d["id"]) for d in act]))

PMAP = {"BA in Computer Science": "CS-BA", "BA in Psychology": "PS-BA", "BA in Biology": "BI-BA", "BA in Economics": "EC-BA"}
sql.append(ins("students", ["id", "external_id", "full_name", "email", "intended_program_id", "bu_start_date", "prior_econ_200_after_matric", "notes"],
    [(U("stu", s["sid"]), s["sid"], s["name"], f"{s['sid'].lower()}@student.example.edu", U("prog", PMAP[s["program"]]), s["start"].isoformat(), s["prior200"], s["note"]) for s in B.students]))

tr, tc = [], []
for s in B.students:
    for inst in dict.fromkeys(l["inst"] for l in B.lines if l["sid"] == s["sid"]):
        ls = [l for l in B.lines if l["sid"] == s["sid"] and l["inst"] == inst]; sc = SC[inst]
        tid = U("tr", s["sid"], sc)
        tr.append((tid, U("stu", s["sid"]), U("inst", sc), "admin_upload", f"{s['sid']}_{sc}_transcript.pdf", ls[0]["rec"].isoformat(), "received", "Synthetic seed transcript"))
        for l in ls:
            known = (inst, l["code"]) in B.CAT
            tc.append((U("tc", l["lid"]), tid, l["lid"], l["term"], l["code"], l["title"], l["credits"], l["grade"], l["am"] == "Yes", CID(inst, l["code"]) if known else None))
sql.append(ins("transcripts", ["id", "student_id", "institution_id", "source", "file_path", "received_date", "status", "notes"], tr))
sql.append(ins("transcript_courses", ["id", "transcript_id", "line_ref", "term", "course_code", "course_title", "credits", "grade", "taken_after_matriculation", "course_id"], tc))
sql.append("commit;")
p = "/home/claude/transfer-credit-app/supabase/seed.sql"
open(p, "w").write("\n".join(sql))
# ---- JSON fixture for the TypeScript engine tests ----
fx = dict(
  institutions=[dict(id=U("inst", s_), name=n, short_code=s_, credit_system=c) for n, s_, t, c, f in INST],
  courses=[dict(id=CID(c["inst"], c["code"]), institution_id=U("inst", SC[c["inst"]]), code=c["code"], title=c["title"], program_area=c["program"],
                requirement_type=(bu_meta[c["code"]]["Requirement type"] if c["inst"] == B.BUN else None), credits=c["credits"]) for c in B.cat],
  equivalencies=[dict(source_course_id=CID(d["inst"], d["code"]), outcome=OUT[d["outcome"]], bu_course_id=BUC(d["bu"]), bu_label=d["bu"], units=d["units"],
                requirement_satisfied=d["req"], condition=("Group C: BU-only requirement, elective credit only" if "Group C" in d["rationale"] else (d["req"] if d["req"].startswith("Only") else None)),
                decision_id=d["id"]) for d in act],
  students=[dict(external_id=s_["sid"], program=PMAP[s_["program"]], bu_start_date=s_["start"].isoformat(), prior_econ=s_["prior200"]) for s_ in B.students],
  lines=[dict(line_ref=l["lid"], sid=l["sid"], institution_id=U("inst", SC[l["inst"]]), course_id=(CID(l["inst"], l["code"]) if (l["inst"], l["code"]) in B.CAT else None),
              code=l["code"], title=l["title"], credits=l["credits"], grade=l["grade"], after_matric=l["am"] == "Yes", received=l["rec"].isoformat()) for l in B.lines],
  answer_key=B.key)
os.makedirs("/home/claude/transfer-credit-app/web/scripts", exist_ok=True)
json.dump(fx, open("/home/claude/transfer-credit-app/web/scripts/fixture.json", "w"), indent=1, default=str)
print("wrote", p, len(B.cat), "courses", len(B.decisions), "decisions", len(act), "equivalencies", len(tr), "transcripts", len(tc), "lines")
