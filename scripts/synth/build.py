import random, datetime as dt, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import openpyxl
from catalog import T, BU, NU, NYU, HCC, PCU, HCC_NAME, PCU_NAME

SRC = "/root/.claude/uploads/da0e2569-97a7-5d6f-86f0-02a18cddff01/597cb9e4-BU_Transfer_Program_Course_Match.xlsx"
random.seed(42)
wb = openpyxl.load_workbook(SRC, data_only=True)

def rows(ws):
    r = list(wb[ws].iter_rows(values_only=True)); h = r[0]
    return [dict(zip(h, x)) for x in r[1:] if x[0]]

NUN, NYUN, BUN = "Northeastern University", "New York University", "Boston University"
cat = []  # catalog rows
def add_cat(inst, system, c, title, prog, cr, topic, src):
    d, o = T[topic]
    cat.append(dict(inst=inst, system=system, code=c, title=title, program=prog, credits=cr, desc=d, outcomes=o, src=src, topic=topic))
for sheet, inst, tmap in [("BU Courses", BUN, BU), ("Northeastern Courses", NUN, NU), ("NYU Courses", NYUN, NYU)]:
    for r in rows(sheet):
        add_cat(inst, "Semester", r["Course code"], r["Course title"], r["Program"], r["Credits"], tmap[r["Course code"]],
                "Code/title/credits from supplied workbook; description & outcomes synthetic")
for c, ti, p, cr, tp in HCC: add_cat(HCC_NAME, "Semester", c, ti, p, cr, tp, "Fully synthetic")
for c, ti, p, cr, tp in PCU: add_cat(PCU_NAME, "Quarter", c, ti, p, cr, tp, "Fully synthetic")
CAT = {(x["inst"], x["code"]): x for x in cat}
BUT = {x["code"]: x["title"] for x in cat if x["inst"] == BUN}

def sem(cr, system):  # BU rule: quarter credits x 2/3, truncated to 2 dp (4 -> 2.66)
    return math.floor(cr * 2 / 3 * 100) / 100 if system == "Quarter" else cr

DEPT = {"Computer Science": "CAS Computer Science", "Economics": "CAS Economics", "Psychology": "CAS Psychological & Brain Sciences",
        "Biology": "CAS Biology", "Chemistry": "CAS Chemistry", "Mathematics": "CAS Mathematics & Statistics",
        "English": "CAS Writing Program", "History": "CAS History", "Communication": "COM", "Hospitality": "Credit Evaluation Dept"}
ELEC = {"Computer Science": "CAS CS elective", "Economics": "CAS EC elective", "Psychology": "CAS PS elective", "Biology": "CAS BI elective",
        "Chemistry": "CAS CH elective", "Mathematics": "CAS MA elective", "English": "CAS general elective", "History": "CAS HI elective",
        "Communication": "COM general elective", "Hospitality": "—"}
def dept_of(prog, code=""):
    if code.startswith(("CHEM", "CHM")): return "Chemistry"
    return prog

# ---------------- Past decisions ----------------
decisions = []
def rand_date(a=2021, b=2026):
    s = dt.date(a, 1, 15); e = dt.date(b, 8, 31)
    return s + dt.timedelta(days=random.randint(0, (e - s).days))
def dec(inst, code, outcome, bu, req, rationale, syl, status="Active", reusable="Yes", date=None):
    c = CAT[(inst, code)]; d = dept_of(c["program"], code)
    decisions.append(dict(inst=inst, code=code, title=c["title"], credits=c["credits"], system=c["system"], outcome=outcome, bu=bu,
        bu_title=BUT.get(bu, "—"), units=0 if outcome == "No credit" else sem(c["credits"], c["system"]), req=req,
        syl=syl, dept=DEPT[d], evaluator=f"EVAL-{d[:3].upper()}-{random.randint(1,3):02d}", rationale=rationale,
        status=status, reusable=reusable, date=date or rand_date()))

# Peer universities, derived from the supplied Course Match sheet
cm = rows("Course Match")
SKIP = {(NUN, "CS 2100"), (NYUN, "PSYCH-UA 25")}  # left without decisions -> 'maybe' cases
OVR = {  # (inst, code): (outcome, bu, req, rationale, syllabus)
 (NUN, "MATH 2331"): ("BU equivalent", "CAS MA 242", "Yes", "Full linear-algebra content. Per BU CS BA rules MA 242 may also substitute for CS 132.", "No"),
 (NUN, "MATH 3081"): ("Elective credit", "CAS MA elective", "No", "Combines probability and statistics; probability depth below MA 581 and CS 237. Elective credit only.", "Yes"),
 (NUN, "ECON 2560"): ("Elective credit", "CAS EC elective", "No", "Applied regression only; instrumental variables and panel methods not covered at EC 204 depth. Elective (200-level) credit.", "Yes"),
 (NUN, "PSYC 2320"): ("Elective credit", "CAS PS elective", "No", "Statistics only; BU PS 211 requires experimental design and lab reports. Elective credit.", "Yes"),
 (NUN, "BIOL 2301"): ("BU equivalent", "CAS BI 206", "Yes", "Syllabus review: genetics content (inheritance, mapping, regulation) meets BI 206; molecular content is additional.", "Yes"),
 (NUN, "CHEM 1161"): ("BU equivalent", "CAS CH 101", "Yes", "Accelerated one-semester course. Meets CH 101; does NOT satisfy CH 102 (electrochemistry/thermodynamics depth insufficient). Extra credit is elective.", "Yes"),
 (NUN, "MATH 2341"): ("Elective credit", "CAS MA elective", "No", "Half-depth ODE coverage combined with linear algebra; does not meet MA 226.", "Yes"),
 (NUN, "MATH 1365"): ("Elective credit", "CAS MA elective", "No", "Proof-writing course without combinatorics or graph theory; does not meet MA 293.", "Yes"),
 (NUN, "CS 2700"): ("Elective credit", "CAS CS elective", "No", "Data-structures content matches part of CS 112 but assumes CS 2100 design content. If student also completed CS 2100, refer to evaluator for combined CS 112 review.", "Yes"),
 (NYUN, "PSYCH-UA 10"): ("Elective credit", "CAS PS elective", "No", "Statistics only; does not cover experimental design required for PS 211.", "Yes"),
 (NYUN, "BIOL-UA 21"): ("BU equivalent", "CAS BI 203", "Yes", "Syllabus review: cellular content meets BI 203.", "Yes"),
 (NYUN, "ECON-UA 266"): ("BU equivalent", "CAS EC 204", "Yes", "Syllabus review: covers multiple regression, IV and panel data with an empirical project. Meets EC 204.", "Yes"),
 (NYUN, "MATH-UA 140"): ("BU equivalent", "CAS MA 242", "Yes", "Full linear-algebra content. MA 242 may substitute for CS 132.", "No"),
 (NYUN, "MATH-UA 233"): ("BU equivalent", "CAS MA 581", "Yes", "Calculus-based probability. MA 581 may substitute for CS 237.", "No"),
 (NYUN, "MATH-UA 120"): ("BU equivalent", "CAS CS 131", "Yes", "Covers logic, proofs, counting, recurrences, graphs and discrete probability. Also accepted for MA 293.", "No"),
}
for inst, col_code, col_lvl, tmap in [(NUN, "Northeastern course", "NU match level", NU), (NYUN, "NYU course", "NYU match level", NYU)]:
    for code in tmap:
        if (inst, code) in SKIP: continue
        if (inst, code) in OVR:
            o, b, rq, ra, sy = OVR[(inst, code)]; dec(inst, code, o, b, rq, ra, sy); continue
        m = [r for r in cm if r[col_code] == code]
        c = CAT[(inst, code)]; prog = dept_of(c["program"], code)
        if m:
            r = m[0]; lvl = r[col_lvl]
            if lvl == "Likely equivalent":
                dec(inst, code, "BU equivalent", r["BU course"], "Yes", f"Content and level align with {r['BU course']} ({r['BU title']}).", random.choice(["No", "No", "Yes"]))
            elif lvl == "Must be taken at BU":
                dec(inst, code, "Elective credit", ELEC[prog], "No", f"Comparable to {r['BU course']}, but CS Group C courses must be taken at BU. Elective credit only.", "No")
            else:
                dec(inst, code, "Elective credit", ELEC[prog], "No", f"Partial overlap with {r['BU course']}; evaluator judged content insufficient for equivalency.", "Yes")
        else:
            dec(inst, code, "Elective credit", ELEC[prog], "No", "No matching BU core course; academic content earns departmental elective credit.", random.choice(["No", "Yes"]))

H, P = HCC_NAME, PCU_NAME
for code, o, b, rq, ra, sy in [
 ("CSC 110", "BU equivalent", "CAS CS 111", "Yes", "Syllabus confirms Python, recursion, dictionaries and intro to classes. Meets CS 111.", "Yes"),
 ("CSC 120", "No credit", "—", "No", "Software-applications course with no programming; not comparable to BU coursework.", "No"),
 ("MAT 090", "No credit", "—", "No", "Developmental (pre-college) course; carries no degree credit at the sending institution.", "No"),
 ("MAT 140", "Elective credit", "CAS MA elective", "No", "Precalculus; below MA 123. Elective credit.", "No"),
 ("MAT 151", "BU equivalent", "CAS MA 123", "Yes", "Limits, derivatives, applications and intro to integration. Meets MA 123.", "No"),
 ("MAT 152", "BU equivalent", "CAS MA 124", "Yes", "Integration techniques and series. Meets MA 124.", "No"),
 ("MAT 220", "BU equivalent", "CAS MA 242", "Yes", "Full linear-algebra content in a 3-credit course; requirement satisfied, 3 units awarded.", "Yes"),
 ("STA 150", "Elective credit", "CAS MA elective", "No", "Non-calculus statistics; elective credit.", "No"),
 ("ENG 101", "Elective credit", "CAS general elective", "No", "Composition course. General elective credit; transfer courses do not earn BU Hub units.", "No"),
 ("ENG 102", "Elective credit", "CAS general elective", "No", "Research writing. General elective credit; no Hub units.", "No"),
 ("ECO 201", "BU equivalent", "CAS EC 102", "Yes", "Principles of macroeconomics. Meets EC 102.", "No"),
 ("ECO 202", "BU equivalent", "CAS EC 101", "Yes", "Principles of microeconomics. Meets EC 101.", "No"),
 ("PSY 101", "BU equivalent", "CAS PS 101", "Yes", "Introductory psychology survey. Meets PS 101.", "No"),
 ("PSY 210", "Elective credit", "CAS PS elective", "No", "Lifespan survey; child/adolescent development is about one third of the course, below PS 241 depth.", "Yes"),
 ("BIO 121", "BU equivalent", "CAS BI 107", "Yes", "Intro biology I with lab. Meets BI 107.", "No"),
 ("BIO 122", "BU equivalent", "CAS BI 108", "Yes", "Intro biology II with lab. Meets BI 108.", "No"),
 ("CHM 121", "BU equivalent", "CAS CH 101", "Yes", "General chemistry I with lab. Meets CH 101.", "No"),
 ("CHM 122", "BU equivalent", "CAS CH 102", "Yes", "General chemistry II with lab. Meets CH 102.", "No"),
 ("HIS 111", "Elective credit", "CAS HI elective", "No", "U.S. history survey; elective credit.", "No"),
 ("HSP 101", "No credit", "—", "No", "Career-technical course; not comparable to BU academic coursework.", "No"),
 ("COM 105", "Elective credit", "COM general elective", "No", "Public speaking; general elective credit.", "No")]:
    dec(H, code, o, b, rq, ra, sy)
for code, o, b, rq, ra, sy in [
 ("CSE 142", "Combined equivalent", "CAS CS 111", "Only with CSE 143", "Two-quarter sequence. CSE 142 + CSE 143 together = CS 111. CSE 142 alone = CS elective.", "Yes"),
 ("CSE 143", "Combined equivalent", "CAS CS 111", "Only with CSE 142", "Second half of the two-quarter sequence; see CSE 142.", "Yes"),
 ("CSE 373", "Elective credit", "CAS CS elective", "No", "One-quarter data structures & algorithms; overlaps CS 112 and CS 330 but meets neither fully.", "Yes"),
 ("MATH 124", "BU equivalent", "CAS MA 123", "Yes", "Quarter calculus I. Accepted for MA 123; 3.33 units after quarter conversion.", "No"),
 ("MATH 125", "BU equivalent", "CAS MA 124", "Yes", "Quarter calculus II (integration). Accepted for MA 124.", "Yes"),
 ("MATH 126", "Elective credit", "CAS MA elective", "No", "Series plus an introduction to vectors; does not meet MA 225.", "Yes"),
 ("MATH 208", "Elective credit", "CAS MA elective", "No", "Matrix algebra without vector spaces; does not meet MA 242.", "Yes"),
 ("STAT 311", "Elective credit", "CAS MA elective", "No", "Non-calculus statistics; elective credit.", "No"),
 ("ECON 200", "BU equivalent", "CAS EC 101", "Yes", "Principles of microeconomics. Meets EC 101; units reduced by quarter conversion.", "No"),
 ("ECON 201", "BU equivalent", "CAS EC 102", "Yes", "Principles of macroeconomics. Meets EC 102; units reduced by quarter conversion.", "No"),
 ("PSYCH 101", "BU equivalent", "CAS PS 101", "Yes", "Intro psychology. Meets PS 101.", "No"),
 ("BIOL 180", "BU equivalent", "CAS BI 107", "Yes", "Intro biology I. Meets BI 107.", "No"),
 ("CHEM 142", "BU equivalent", "CAS CH 101", "Yes", "General chemistry I. Meets CH 101.", "No")]:
    dec(P, code, o, b, rq, ra, sy)
# superseded history (shows decisions change over time)
dec(H, "CSC 110", "Elective credit", "CAS CS elective", "No", "2021 syllabus taught spreadsheet macros, not general programming. Superseded after course redesign.", "Yes", "Superseded", "No", dt.date(2021, 6, 3))
dec(NYUN, "PSYCH-UA 51", "Elective credit", "CAS PS elective", "No", "Earlier review before BU PS 371 was renamed. Superseded.", "No", "Superseded", "No", dt.date(2021, 9, 20))
dec(NUN, "CHEM 1161", "Combined equivalent", "CAS CH 101", "Yes", "Earlier decision awarded CH 101 + CH 102. Reversed after department review in 2024.", "Yes", "Superseded", "No", dt.date(2022, 2, 11))
decisions.sort(key=lambda d: d["date"])
for i, d in enumerate(decisions, 1): d["id"] = f"D-{i:03d}"
# superseded decisions must predate the active one
ACTIVE = {(d["inst"], d["code"]): d for d in decisions if d["status"] == "Active"}

# ---------------- Students & transcripts ----------------
students = [
 dict(sid="SYN-1001", name="Jordan Alvarez", program="BA in Computer Science", start=dt.date(2026, 9, 2), prior200=0,
      note="Demo scenario: 6 courses (3 existing equivalencies, 2 'maybe', 1 quarter-system)."),
 dict(sid="SYN-1002", name="Priya Raman", program="BA in Computer Science", start=dt.date(2026, 9, 2), prior200=0,
      note="Northeastern transfer: Group C rule, grade below C, 5-credit lab courses, course with no catalogue data."),
 dict(sid="SYN-1003", name="Daniel Kim", program="BA in Psychology", start=dt.date(2026, 9, 2), prior200=0,
      note="NYU transfer: partial matches, a Pass/Fail grade, a 'maybe' with no decision, and an unlisted course."),
 dict(sid="SYN-1004", name="Aisha Thompson", program="BA in Biology", start=dt.date(2026, 1, 20), prior200=0,
      note="Community college + quarter school: developmental course, quarter conversion, and a transcript received after the one-year deadline."),
 dict(sid="SYN-1005", name="Marcus Lee", program="BA in Economics", start=dt.date(2025, 9, 2), prior200=2,
      note="Current BU student taking summer courses after matriculation: tests the 4-course cap on 200+ level Economics transfers."),
]
# sid, inst, term, code, grade, after_matric, received
TL = [
 ("SYN-1001", H, "Fall 2024", "CSC 110", "A", "No", dt.date(2026, 6, 20)),
 ("SYN-1001", H, "Fall 2024", "MAT 151", "B+", "No", dt.date(2026, 6, 20)),
 ("SYN-1001", H, "Fall 2024", "ENG 101", "A-", "No", dt.date(2026, 6, 20)),
 ("SYN-1001", H, "Spring 2025", "CSC 215", "B", "No", dt.date(2026, 6, 20)),
 ("SYN-1001", H, "Spring 2025", "MAT 210", "B", "No", dt.date(2026, 6, 20)),
 ("SYN-1001", P, "Summer 2025", "ECON 200", "B+", "No", dt.date(2026, 7, 8)),
 ("SYN-1002", NUN, "Fall 2024", "CS 2000", "A", "No", dt.date(2026, 6, 30)),
 ("SYN-1002", NUN, "Fall 2024", "CS 1800", "A-", "No", dt.date(2026, 6, 30)),
 ("SYN-1002", NUN, "Fall 2024", "MATH 1341", "B", "No", dt.date(2026, 6, 30)),
 ("SYN-1002", NUN, "Fall 2024", "ENGW 1111", "A", "No", dt.date(2026, 6, 30)),
 ("SYN-1002", NUN, "Spring 2025", "CS 2100", "B+", "No", dt.date(2026, 6, 30)),
 ("SYN-1002", NUN, "Spring 2025", "MATH 1342", "C-", "No", dt.date(2026, 6, 30)),
 ("SYN-1002", NUN, "Spring 2025", "MATH 2331", "B+", "No", dt.date(2026, 6, 30)),
 ("SYN-1002", NUN, "Fall 2025", "CS 2700", "B", "No", dt.date(2026, 6, 30)),
 ("SYN-1002", NUN, "Fall 2025", "CS 3000", "B", "No", dt.date(2026, 6, 30)),
 ("SYN-1002", NUN, "Spring 2026", "CS 3800", "A-", "No", dt.date(2026, 6, 30)),
 ("SYN-1003", NYUN, "Fall 2024", "PSYCH-UA 1", "A", "No", dt.date(2026, 7, 15)),
 ("SYN-1003", NYUN, "Fall 2024", "MATH-UA 121", "C", "No", dt.date(2026, 7, 15)),
 ("SYN-1003", NYUN, "Fall 2024", "EXPOS-UA 1", "B+", "No", dt.date(2026, 7, 15)),
 ("SYN-1003", NYUN, "Spring 2025", "PSYCH-UA 10", "B+", "No", dt.date(2026, 7, 15)),
 ("SYN-1003", NYUN, "Spring 2025", "BIOL-UA 11", "B-", "No", dt.date(2026, 7, 15)),
 ("SYN-1003", NYUN, "Fall 2025", "PSYCH-UA 25", "A-", "No", dt.date(2026, 7, 15)),
 ("SYN-1003", NYUN, "Fall 2025", "PSYCH-UA 32", "B", "No", dt.date(2026, 7, 15)),
 ("SYN-1003", NYUN, "Spring 2026", "PSYCH-UA 34", "P", "No", dt.date(2026, 7, 15)),
 ("SYN-1004", H, "Fall 2023", "MAT 090", "P", "No", dt.date(2025, 12, 1)),
 ("SYN-1004", H, "Fall 2023", "BIO 121", "A", "No", dt.date(2025, 12, 1)),
 ("SYN-1004", H, "Fall 2023", "CHM 121", "B", "No", dt.date(2025, 12, 1)),
 ("SYN-1004", H, "Spring 2024", "BIO 122", "B+", "No", dt.date(2025, 12, 1)),
 ("SYN-1004", H, "Spring 2024", "CHM 122", "B-", "No", dt.date(2025, 12, 1)),
 ("SYN-1004", H, "Spring 2024", "STA 150", "A", "No", dt.date(2025, 12, 1)),
 ("SYN-1004", P, "Fall 2024", "MATH 124", "B+", "No", dt.date(2027, 3, 15)),
 ("SYN-1004", P, "Fall 2024", "CHEM 237", "B", "No", dt.date(2027, 3, 15)),
 ("SYN-1005", NYUN, "Summer 2026", "ECON-UA 12", "B", "Yes", dt.date(2026, 8, 25)),
 ("SYN-1005", NYUN, "Summer 2026", "ECON-UA 18", "A", "Yes", dt.date(2026, 8, 25)),
 ("SYN-1005", NYUN, "Summer 2026", "ECON-UA 266", "B+", "Yes", dt.date(2026, 8, 25)),
]
UNLISTED = {"ENGW 1111": ("First-Year Writing", 4), "EXPOS-UA 1": ("Writing as Exploration", 4)}
lines = []
for i, (sid, inst, term, code, g, am, rec) in enumerate(TL, 1):
    c = CAT.get((inst, code))
    title, cr = (c["title"], c["credits"]) if c else UNLISTED[code]
    system = "Quarter" if inst == P else "Semester"
    lines.append(dict(lid=f"TL-{i:03d}", sid=sid, inst=inst, system=system, term=term, code=code, title=title, credits=cr, grade=g, am=am, rec=rec))

# ---------------- Answer key (reference outcome a correct agent should reach) ----------------
GRADE_OK = {"A", "A-", "B+", "B", "B-", "C+", "C"}
key = []
stud = {s["sid"]: s for s in students}
econ_count = {s["sid"]: s["prior200"] for s in students}
MAYBE_EXPECT = {
 ("SYN-1001", "CSC 215"): ("Maybe → syllabus review", "CAS CS 112", "Likely equivalent: syllabus covers linked lists, stacks, queues, BSTs, heaps, hash tables and Big-O in Java."),
 ("SYN-1001", "MAT 210"): ("Maybe → syllabus review", "CAS CS 131 (conditional) or CAS MA 293", "Partial: logic, proofs, induction, counting and graphs covered; recurrences and discrete probability missing; 3 vs 4 credits. Department decides."),
 ("SYN-1002", "CS 2100"): ("Maybe → syllabus review", "CAS CS 112 (with CS 2700)", "Program design without asymptotic analysis. With CS 2700 (also on transcript) the pair likely covers CS 112; flag combined review."),
 ("SYN-1002", "ENGW 1111"): ("Maybe → request syllabus", "CAS general elective (likely)", "Course not in catalogue data; request syllabus. Writing courses typically earn elective credit, no Hub units."),
 ("SYN-1003", "PSYCH-UA 25"): ("Maybe → syllabus review", "CAS PS 231 (uncertain)", "Cognitive neuroscience; limited neurotransmission/hormone coverage vs PS 231. Likely elective unless syllabus shows physiological depth."),
 ("SYN-1003", "EXPOS-UA 1"): ("Maybe → request syllabus", "CAS general elective (likely)", "Course not in catalogue data; request syllabus."),
 ("SYN-1004", "CHEM 237"): ("Maybe → syllabus review", "CAS CH 203 (partial) / CAS CH elective", "One quarter covers only part of Orgo I (no eliminations/alkenes, no lab). Likely elective unless paired with next quarter."),
}
for l in lines:
    s = stud[l["sid"]]; flags = []
    units = sem(l["credits"], l["system"])
    if l["system"] == "Quarter": flags.append(f"Quarter conversion {l['credits']} × 2/3 = {units}")
    if (l["rec"] - s["start"]).days > 365: flags.append("Transcript received > 1 year after BU start: deadline exceeded")
    if l["grade"] == "P": flags.append("Pass/Fail grade: cannot confirm C or higher, needs evaluator decision")
    elif l["grade"] not in GRADE_OK: flags.append("Grade below C: no credit")
    d = ACTIVE.get((l["inst"], l["code"]))
    if (l["sid"], l["code"]) in MAYBE_EXPECT:
        path, bu, why = MAYBE_EXPECT[(l["sid"], l["code"])]; exp_units = f"Pending ({units} if approved)"
    elif d:
        path, bu, why = "Existing equivalency", d["bu"], f"{d['id']}: {d['rationale']}"
        exp_units = 0 if d["outcome"] == "No credit" else units
    secure, pending = (0, units) if path.startswith("Maybe") else (exp_units, 0)
    if l["code"] == "MAT 090": exp_units, secure, pending = 0, 0, 0
    elif any("below C" in f for f in flags): exp_units, secure, pending = 0, 0, 0
    elif any("deadline" in f for f in flags):
        exp_units, secure, pending = "0 (deadline; exception needed)", 0, 0
    elif l["grade"] == "P":
        exp_units, secure, pending = f"Hold ({units} if grade accepted)", 0, units
    if l["am"] == "Yes" and bu in ("CAS EC 201", "CAS EC 202", "CAS EC 203", "CAS EC 204"):
        econ_count[l["sid"]] += 1
        if econ_count[l["sid"]] > 4:
            flags.append(f"Econ cap: this is 200+ level transfer #{econ_count[l['sid']]} after matriculation (max 4); evaluator must choose which count")
            exp_units, secure, pending = f"Hold ({units} if cap allows)", 0, units
    if d and "Group C" in d["rationale"]: flags.append("Group C requirement must be taken at BU: elective credit only")
    flags.append("No BU Hub units (all transfer courses)")
    key.append(dict(lid=l["lid"], sid=l["sid"], code=l["code"], path=path, bu=bu, units=exp_units, secure=secure, pending=pending,
                    flags="; ".join(flags), why=why))

if __name__ == "__main__":
    import collections
    print(len(cat), "catalog rows;", len(decisions), "decisions;", len(ACTIVE), "active;", len(lines), "transcript lines")
    print(collections.Counter(d["outcome"] for d in decisions))
    for k in key: print(k["sid"], k["code"], "|", k["path"], "|", k["bu"], "|", k["units"], "|", k["flags"])
