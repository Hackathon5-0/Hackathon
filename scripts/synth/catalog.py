"""Synthetic course content (descriptions + learning outcomes) for the BU transfer hackathon.
All text is written for the hackathon and is NOT copied from any university catalogue."""

T = {}  # topic -> (description, outcomes)
def t(k, d, o): T[k] = (d, o)

# ---------- Computer Science ----------
t("intro_prog", "Introduction to programming and computational problem solving in a high-level language (Python). Covers variables, control flow, functions, recursion, lists and dictionaries, file input/output, an introduction to classes and objects, and testing and debugging practice.",
  "Write, test and debug programs of moderate size; Decompose problems into functions, including recursive solutions; Use lists, dictionaries and simple classes")
t("data_structures", "Second programming course focused on data structures and their analysis, taught in an object-oriented language (Java). Covers linked lists, stacks, queues, trees, binary search trees, heaps, hash tables and an introduction to graphs, with Big-O analysis of each operation.",
  "Implement and use core data structures; Analyse time and space complexity using Big-O notation; Select an appropriate data structure for a given problem")
t("prog_design", "Systematic program design using design recipes, data definitions and test-first development. Emphasises functional decomposition and abstraction; lists and trees are introduced as data, but asymptotic analysis and hash tables are not covered.",
  "Design programs from data definitions; Write tests before code; Use abstraction to remove duplication")
t("prog_design_oo", "Object-oriented program design: classes, interfaces, inheritance, generics, common design patterns and team software projects with unit testing.",
  "Design class hierarchies; Apply common design patterns; Deliver a tested multi-module project")
t("ds_analysis", "Data structures with formal analysis: lists, trees, balanced search trees, heaps, hash tables and graphs, with proofs of running time and an introduction to amortised analysis. Includes a weekly lab.",
  "Implement and analyse data structures; Prove running-time bounds; Choose structures for performance requirements")
t("discrete", "Mathematical foundations of computer science: propositional and predicate logic, proof techniques, induction, sets, functions and relations, counting and combinatorics, recurrence relations, graphs and trees, and an introduction to discrete probability.",
  "Construct direct, contradiction and induction proofs; Solve counting problems and recurrences; Reason about graphs and basic discrete probability")
t("systems", "How programs execute on real machines: data representation, C programming, assembly language, memory hierarchy and caches, linking, processes and an introduction to concurrency.",
  "Write and debug C programs; Explain how high-level code maps to machine instructions; Reason about memory and cache performance")
t("algorithms", "Design and analysis of algorithms: divide and conquer, greedy methods, dynamic programming, graph algorithms (search, shortest paths, minimum spanning trees), network flow and NP-completeness, with proofs of correctness and running time.",
  "Design algorithms using standard paradigms; Prove correctness and running time; Recognise intractable problems")
t("geom_alg", "Linear algebra from a computational perspective: vectors, matrices, linear transformations, eigenvalues and least squares, applied to graphics, data analysis and machine learning, with programming assignments in Python.",
  "Perform core matrix computations; Apply linear algebra to computational problems; Implement linear-algebra algorithms in code")
t("alg_alg", "Algorithms for algebraic structures: modular arithmetic, groups, rings and fields, polynomials, and applications to cryptography and error-correcting codes.",
  "Compute in modular and polynomial arithmetic; Explain algebraic structures used in cryptography; Implement basic cryptographic algorithms")
t("prob_comp", "Probability for computing: sample spaces, conditional probability, random variables, expectation and variance, common distributions, tail bounds and applications to randomised algorithms and simulation.",
  "Compute probabilities and expectations; Apply common distributions and tail bounds; Analyse simple randomised algorithms")
t("prog_lang", "Concepts of programming languages: syntax and semantics, interpreters, scope, type systems, functional programming and language design trade-offs.",
  "Build a small interpreter; Explain type systems and scoping rules; Compare language design choices")
t("theory", "Theory of computation: finite automata, regular languages, context-free grammars, Turing machines, decidability and an introduction to the complexity classes P and NP.",
  "Construct automata and grammars; Prove languages non-regular or undecidable; Explain P versus NP")
t("comp_sys_fund", "Fundamentals of computing systems: performance modelling, queuing, scheduling, concurrency and synchronisation, and operating-system resource management.",
  "Model system performance; Write correct concurrent code; Explain OS resource management")
t("os", "Operating systems: processes and threads, CPU scheduling, synchronisation, memory management and virtual memory, and file systems, with kernel programming projects.",
  "Explain OS abstractions; Implement synchronisation primitives; Build components of a small kernel")
t("logic_comp", "Logic and computation: formal logic, specification and reasoning about programs, and mechanised theorem proving.",
  "Write formal specifications; Prove program properties; Use a theorem prover")
t("ai_math", "Mathematical foundations of artificial intelligence: linear algebra, probability, optimisation and statistics as used in machine learning.",
  "Apply linear algebra and probability to ML problems; Formulate optimisation problems; Interpret statistical models")
# ---------- Economics ----------
t("micro_intro", "Principles of microeconomics: supply and demand, consumer and producer behaviour, market structures, market failure and the role of government.",
  "Use supply and demand to analyse markets; Compare market structures; Evaluate policy responses to market failure")
t("macro_intro", "Principles of macroeconomics: national income accounting, unemployment, inflation, economic growth, money and banking, and fiscal and monetary policy.",
  "Interpret macroeconomic indicators; Explain fiscal and monetary policy; Analyse short-run fluctuations")
t("micro_int", "Intermediate microeconomic theory using calculus: consumer choice, production and cost, general equilibrium, game theory and information economics.",
  "Solve constrained optimisation problems; Analyse strategic interaction; Evaluate welfare outcomes")
t("macro_int", "Intermediate macroeconomic theory: growth models, business cycles, consumption and investment, open-economy macroeconomics and stabilisation policy.",
  "Use formal models of growth and cycles; Analyse policy in open economies; Interpret macroeconomic data")
t("econ_stats", "Probability and statistics for economics: descriptive statistics, probability distributions, sampling, estimation, hypothesis testing and simple linear regression using statistical software.",
  "Summarise economic data; Conduct hypothesis tests; Estimate and interpret simple regressions")
t("econometrics", "Econometrics: multiple regression, inference, specification, heteroskedasticity, instrumental variables, panel data and causal inference, with an independent empirical project.",
  "Estimate and test multiple regression models; Apply IV and panel methods; Complete an empirical research project")
t("econometrics_applied", "Applied regression with economic data: multiple regression, dummy variables and basic diagnostics. Emphasises software use and interpretation; instrumental variables and panel methods are introduced only briefly.",
  "Run and interpret regressions in software; Diagnose common problems; Present empirical results")
# ---------- Psychology ----------
t("intro_psych", "Survey of psychology as a science: research methods, biological bases of behaviour, sensation and perception, learning, memory, development, personality, social behaviour and psychological disorders.",
  "Describe major areas of psychology; Explain basic research methods; Apply psychological concepts to everyday behaviour")
t("exp_design", "Research methods in psychology: experimental design, validity, ethics and the statistics used to analyse experiments (t-tests, ANOVA), with lab reports written in APA style.",
  "Design a controlled experiment; Analyse results with t-tests and ANOVA; Write an APA-style lab report")
t("psych_stats", "Descriptive and inferential statistics for the behavioural sciences: distributions, correlation, t-tests, ANOVA and chi-square. Does not include designing experiments or writing lab reports.",
  "Compute and interpret descriptive statistics; Select and run inferential tests; Interpret statistical output")
t("physio_psych", "Biological bases of behaviour: neurons and neurotransmission, neuroanatomy, hormones, sensory and motor systems, sleep, motivation, emotion and the effects of drugs.",
  "Explain neural communication; Relate brain systems to behaviour; Evaluate biological explanations of behaviour")
t("cog_neuro", "Cognitive neuroscience: the brain basis of perception, attention, memory, language and decision making, using imaging, lesion and electrophysiology evidence. Neurotransmission and hormones receive limited coverage.",
  "Interpret neuroimaging evidence; Relate cognitive functions to brain networks; Critique cognitive-neuroscience studies")
t("perception", "Perception: how sensory systems transform physical energy into experience, with emphasis on vision and hearing, psychophysics and perceptual organisation.",
  "Explain sensory transduction; Apply psychophysical methods; Describe theories of perception")
t("cognition", "Cognitive psychology: attention, memory, categorisation, language, problem solving, reasoning and decision making.",
  "Describe models of memory and attention; Evaluate cognitive experiments; Apply cognitive principles")
t("developmental", "Developmental psychology from infancy through adolescence: physical, cognitive, language, social and emotional development, and research methods for studying children.",
  "Describe developmental milestones; Compare developmental theories; Evaluate developmental research")
t("lifespan", "Human development across the lifespan from conception to late adulthood, with a broad survey of physical, cognitive and social change. Child and adolescent development receive about a third of the course.",
  "Describe change across the lifespan; Compare developmental theories; Apply concepts to life stages")
t("personality", "Theories of personality: psychodynamic, trait, humanistic, social-cognitive and biological approaches, with personality assessment and applications.",
  "Compare personality theories; Evaluate personality assessments; Apply theories to case studies")
t("social", "Social psychology: social cognition, attitudes, persuasion, conformity, group processes, prejudice, aggression and prosocial behaviour.",
  "Explain core social-psychology phenomena; Evaluate classic studies; Apply concepts to real situations")
t("abnormal", "Psychopathology: classification, causes and treatment of psychological disorders, including anxiety, mood, psychotic and personality disorders.",
  "Describe major disorders; Compare causal models; Evaluate treatment approaches")
t("psych_language", "Psychology of language: speech perception, word recognition, sentence processing, language acquisition and the relation of language to thought.",
  "Explain language-processing models; Describe language acquisition; Evaluate psycholinguistic studies")
# ---------- Biology ----------
t("bio1", "First-semester introductory biology with laboratory: chemistry of life, cell structure, metabolism, cell division, Mendelian and molecular genetics.",
  "Explain cell structure and function; Describe metabolism and genetics; Conduct and report basic lab experiments")
t("bio2", "Second-semester introductory biology with laboratory: evolution, biodiversity, organismal physiology and ecology.",
  "Explain evolutionary mechanisms; Compare organism systems; Analyse ecological interactions")
t("cell", "Cell biology: membranes, organelles, protein trafficking, cytoskeleton, cell signalling, cell cycle and cell death.",
  "Explain cellular processes; Interpret experimental cell-biology data; Relate cell function to disease")
t("genetics", "Genetics: Mendelian inheritance, linkage and mapping, chromosomes, gene regulation, mutation, population genetics and genomic methods.",
  "Solve genetics problems; Explain gene regulation; Interpret genomic data")
t("gen_mol", "Genetics and molecular biology combined: inheritance, DNA replication, transcription, translation, gene regulation and recombinant DNA techniques, with a laboratory.",
  "Solve inheritance problems; Explain molecular processes; Perform molecular lab techniques")
t("bio_inquiry", "Inquiry-based course on how biological research is done: hypothesis generation, experimental design, data analysis and scientific writing.",
  "Design a biological experiment; Analyse biological data; Write a scientific report")
t("biochem", "Biochemistry with laboratory: protein structure, enzymes, metabolism and bioenergetics.",
  "Explain protein structure and enzyme kinetics; Describe metabolic pathways; Perform biochemical assays")
t("mol_cell", "Molecular and cell biology: DNA, gene expression, membranes, organelles, signalling and the cell cycle, integrating molecular and cellular levels.",
  "Explain gene expression; Describe cellular processes; Integrate molecular and cellular data")
# ---------- Chemistry ----------
t("genchem1", "General chemistry I with laboratory: atomic structure, periodic trends, bonding, stoichiometry, gases, thermochemistry and solutions.",
  "Solve stoichiometry problems; Explain bonding and periodic trends; Perform quantitative lab work")
t("genchem2", "General chemistry II with laboratory: kinetics, equilibrium, acids and bases, thermodynamics and electrochemistry.",
  "Solve equilibrium and kinetics problems; Explain thermodynamic principles; Perform titrations and analyses")
t("genchem_accel", "Accelerated one-semester general chemistry with laboratory and recitation for students with strong high-school chemistry. Covers the core of a two-semester sequence (structure, bonding, stoichiometry, equilibrium, kinetics, thermodynamics) at a faster pace with less depth in electrochemistry.",
  "Solve general-chemistry problems across the full sequence; Explain equilibrium and thermodynamics; Perform quantitative lab work")
t("orgo1", "Organic chemistry I with laboratory: structure and bonding, stereochemistry, nomenclature, substitution and elimination reactions, alkenes and alkynes.",
  "Draw and name organic structures; Predict reaction mechanisms; Perform organic lab techniques")
t("orgo2", "Organic chemistry II with laboratory: aromatic compounds, carbonyl chemistry, spectroscopy, multistep synthesis and biomolecules.",
  "Predict carbonyl and aromatic reactions; Interpret NMR and IR spectra; Plan multistep syntheses")
# ---------- Mathematics ----------
t("calc1", "Differential calculus: limits, continuity, derivatives and their applications, and an introduction to integration.",
  "Compute limits and derivatives; Apply derivatives to optimisation and related rates; Evaluate basic integrals")
t("calc2", "Integral calculus: techniques of integration, applications of integrals, sequences and series, and power series.",
  "Apply integration techniques; Determine convergence of series; Use power series")
t("calc3", "Multivariable calculus: vectors, partial derivatives, multiple integrals, and vector calculus (Green's, Stokes' and divergence theorems).",
  "Compute partial derivatives and multiple integrals; Apply vector-calculus theorems; Solve multivariable optimisation problems")
t("linalg", "Linear algebra: systems of linear equations, matrices, vector spaces, linear transformations, determinants, eigenvalues and orthogonality.",
  "Solve linear systems; Work with vector spaces and transformations; Compute eigenvalues and eigenvectors")
t("diffeq", "Ordinary differential equations: first-order equations, linear higher-order equations, systems, Laplace transforms and applications.",
  "Solve first- and higher-order ODEs; Use Laplace transforms; Model physical systems with ODEs")
t("diffeq_linalg", "Combined differential equations and linear algebra for engineering: matrix methods, eigenvalues, first-order and linear ODEs and systems. Each topic receives about half the depth of a dedicated course.",
  "Solve linear systems and ODEs; Use eigenvalues to solve systems of ODEs; Apply methods to engineering models")
t("discrete_math", "Discrete mathematics: logic, proof techniques, sets, functions, relations, combinatorics, graph theory and elementary number theory.",
  "Write rigorous proofs; Solve combinatorial problems; Apply graph theory and number theory")
t("math_reasoning", "Introduction to mathematical reasoning and proof: logic, sets, functions, relations and elementary number theory. Combinatorics and graph theory are not covered in depth.",
  "Write clear proofs; Use logic and set notation; Prove basic number-theory results")
t("probability", "Calculus-based probability: axioms, conditional probability, discrete and continuous random variables, joint distributions, expectation, limit theorems.",
  "Compute probabilities with calculus; Work with joint distributions; Apply limit theorems")
t("prob_stats", "Probability and statistics: probability models, random variables, sampling distributions, estimation and hypothesis testing. Probability theory is covered in less depth than a dedicated course.",
  "Compute probabilities; Estimate parameters; Conduct hypothesis tests")
# ---------- Community college / quarter school extras ----------
t("comp_apps", "Computer applications for the workplace: word processing, spreadsheets, presentations and basic database use. No programming.",
  "Produce documents and spreadsheets; Use basic database queries; Prepare presentations")
t("dev_algebra", "Developmental (pre-college) algebra: arithmetic review, linear equations, exponents and polynomials. Does not carry credit toward an associate degree.",
  "Solve linear equations; Manipulate polynomials; Prepare for college algebra")
t("precalc", "Precalculus: functions, polynomial, rational, exponential, logarithmic and trigonometric functions in preparation for calculus.",
  "Analyse functions and graphs; Solve exponential and trig equations; Prepare for calculus")
t("comp1", "English composition I: academic writing, the writing process, argument and the use of sources.",
  "Write organised academic essays; Build evidence-based arguments; Cite sources correctly")
t("comp2", "English composition II: research writing, analysis of texts and a documented research paper.",
  "Conduct library research; Write a documented research paper; Analyse texts critically")
t("elem_stats", "Elementary (non-calculus) statistics: descriptive statistics, probability, normal distribution, confidence intervals and hypothesis tests.",
  "Summarise data; Construct confidence intervals; Perform hypothesis tests")
t("us_hist", "United States history to 1877: colonial era, revolution, early republic, expansion, Civil War and Reconstruction.",
  "Describe major events and themes; Analyse primary sources; Write historical arguments")
t("hospitality", "Introduction to the hospitality industry: hotel, restaurant and tourism operations, customer service and career paths. Career-technical course.",
  "Describe hospitality operations; Apply customer-service principles; Explore industry careers")
t("public_speaking", "Public speaking: speech preparation, organisation, delivery, persuasive speaking and audience analysis.",
  "Prepare and deliver speeches; Use persuasive techniques; Analyse audiences")
t("cc_disc_math", "Discrete mathematics for computer science majors (3 credits): logic, sets, proof techniques including induction, functions and relations, basic counting (permutations and combinations) and an introduction to graphs and trees. Recurrence relations and discrete probability are not covered.",
  "Write proofs, including induction; Solve basic counting problems; Describe graphs and trees")
t("q_prog1", "First quarter of a two-quarter introductory programming sequence (Java): variables, control flow, methods, arrays and simple classes.",
  "Write small programs; Use methods and arrays; Create simple classes")
t("q_prog2", "Second quarter of the introductory programming sequence (Java): recursion, inheritance, interfaces, linked lists, stacks, queues and an introduction to binary trees.",
  "Use recursion and inheritance; Implement linked structures; Write medium-sized programs")
t("q_dsa", "Data structures and algorithms (one quarter): asymptotic analysis, hash tables, balanced trees, heaps, graphs, sorting and basic graph algorithms.",
  "Analyse algorithms with Big-O; Implement hash tables, heaps and graphs; Apply sorting and graph algorithms")
t("q_calc1", "Calculus I (quarter): limits, derivatives and applications of differentiation.",
  "Compute limits and derivatives; Apply derivatives to optimisation")
t("q_calc2", "Calculus II (quarter): the definite integral, techniques of integration and applications.",
  "Evaluate integrals; Apply integration techniques")
t("q_calc3", "Calculus III (quarter): sequences, series, power series and an introduction to vectors and partial derivatives.",
  "Determine convergence of series; Use power series; Compute basic partial derivatives")
t("q_matrix", "Matrix algebra (quarter, 3 credits): systems of linear equations, matrix operations, determinants and an introduction to eigenvalues. Abstract vector spaces are not covered.",
  "Solve linear systems; Perform matrix operations; Compute determinants and eigenvalues")
t("q_orgo1", "Organic chemistry I (quarter): bonding, structure, stereochemistry and an introduction to substitution reactions. Elimination reactions and alkenes are covered in the next quarter. Laboratory is a separate course.",
  "Draw organic structures; Explain stereochemistry; Predict substitution mechanisms")

# ---------- Course -> topic map ----------
BU = {"CAS CS 111":"intro_prog","CAS CS 112":"data_structures","CAS CS 131":"discrete","CAS CS 210":"systems",
 "CAS CS 330":"algorithms","CAS CS 132":"geom_alg","CAS CS 235":"alg_alg","CAS CS 237":"prob_comp","CAS CS 320":"prog_lang",
 "CAS CS 332":"theory","CAS CS 350":"comp_sys_fund","CAS EC 101":"micro_intro","CAS EC 102":"macro_intro","CAS EC 201":"micro_int",
 "CAS EC 202":"macro_int","CAS EC 203":"econ_stats","CAS EC 204":"econometrics","CAS PS 101":"intro_psych","CAS PS 211":"exp_design",
 "CAS PS 231":"physio_psych","CAS PS 222":"perception","CAS PS 336":"cognition","CAS PS 241":"developmental","CAS PS 251":"personality",
 "CAS PS 261":"social","CAS PS 371":"abnormal","CAS BI 107":"bio1","CAS BI 108":"bio2","CAS BI 203":"cell","CAS BI 206":"genetics",
 "CAS CH 101":"genchem1","CAS CH 102":"genchem2","CAS CH 203":"orgo1","CAS CH 204":"orgo2","CAS MA 123":"calc1","CAS MA 124":"calc2",
 "CAS MA 225":"calc3","CAS MA 242":"linalg","CAS MA 226":"diffeq","CAS MA 293":"discrete_math","CAS MA 581":"probability"}
NU = {"CS 2000":"intro_prog","CS 2100":"prog_design","CS 3100":"prog_design_oo","CS 1800":"discrete","CS 2700":"ds_analysis",
 "CS 3000":"algorithms","CS 3650":"systems","CS 3800":"theory","CS 4400":"prog_lang","CS 2800":"logic_comp","DS 3000":"ai_math",
 "ECON 1116":"micro_intro","ECON 1115":"macro_intro","ECON 2316":"micro_int","ECON 2315":"macro_int","ECON 2350":"econ_stats",
 "ECON 2560":"econometrics_applied","PSYC 1101":"intro_psych","PSYC 2320":"psych_stats","PSYC 3458":"physio_psych","PSYC 3402":"social",
 "PSYC 3404":"developmental","PSYC 3464":"psych_language","BIOL 1107":"bio1","BIOL 1113":"bio2","BIOL 2299":"bio_inquiry","BIOL 2301":"gen_mol",
 "BIOL 3611":"biochem","CHEM 1161":"genchem_accel","CHEM 2311":"orgo1","CHEM 2313":"orgo2","MATH 1341":"calc1","MATH 1342":"calc2",
 "MATH 2321":"calc3","MATH 2331":"linalg","MATH 2341":"diffeq_linalg","MATH 1365":"math_reasoning","MATH 3081":"prob_stats"}
NYU = {"CSCI-UA 101":"intro_prog","CSCI-UA 102":"data_structures","CSCI-UA 201":"systems","CSCI-UA 202":"os","CSCI-UA 310":"algorithms",
 "CSCI-UA 453":"theory","MATH-UA 120":"discrete","ECON-UA 2":"micro_intro","ECON-UA 1":"macro_intro","ECON-UA 10":"micro_int",
 "ECON-UA 12":"macro_int","ECON-UA 18":"econ_stats","ECON-UA 266":"econometrics","PSYCH-UA 1":"intro_psych","PSYCH-UA 10":"psych_stats",
 "PSYCH-UA 11":"psych_stats","PSYCH-UA 22":"perception","PSYCH-UA 25":"cog_neuro","PSYCH-UA 29":"cognition","PSYCH-UA 30":"personality",
 "PSYCH-UA 32":"social","PSYCH-UA 34":"developmental","PSYCH-UA 51":"abnormal","BIOL-UA 11":"bio1","BIOL-UA 12":"bio2","BIOL-UA 21":"mol_cell",
 "BIOL-UA 30":"genetics","CHEM-UA 125":"genchem1","CHEM-UA 126":"genchem2","CHEM-UA 225":"orgo1","CHEM-UA 226":"orgo2","MATH-UA 121":"calc1",
 "MATH-UA 122":"calc2","MATH-UA 123":"calc3","MATH-UA 140":"linalg","MATH-UA 262":"diffeq","MATH-UA 233":"probability","MATH-UA 235":"prob_stats"}

# Fictional institutions (synthetic catalogues)
HCC_NAME = "Harborview Community College (fictional)"
PCU_NAME = "Pacific Crest University (fictional)"
# code, title, program, credits, topic
HCC = [("CSC 110","Introduction to Programming (Python)","Computer Science",4,"intro_prog"),
 ("CSC 120","Computer Applications","Computer Science",3,"comp_apps"),
 ("CSC 215","Data Structures in Java","Computer Science",4,"data_structures"),
 ("MAT 090","Developmental Algebra","Mathematics",3,"dev_algebra"),
 ("MAT 140","Precalculus","Mathematics",4,"precalc"),
 ("MAT 151","Calculus I","Mathematics",4,"calc1"),
 ("MAT 152","Calculus II","Mathematics",4,"calc2"),
 ("MAT 210","Discrete Mathematics","Mathematics",3,"cc_disc_math"),
 ("MAT 220","Linear Algebra","Mathematics",3,"linalg"),
 ("STA 150","Elementary Statistics","Mathematics",3,"elem_stats"),
 ("ENG 101","English Composition I","English",3,"comp1"),
 ("ENG 102","English Composition II","English",3,"comp2"),
 ("ECO 201","Principles of Macroeconomics","Economics",3,"macro_intro"),
 ("ECO 202","Principles of Microeconomics","Economics",3,"micro_intro"),
 ("PSY 101","Introduction to Psychology","Psychology",3,"intro_psych"),
 ("PSY 210","Lifespan Development","Psychology",3,"lifespan"),
 ("BIO 121","General Biology I","Biology",4,"bio1"),
 ("BIO 122","General Biology II","Biology",4,"bio2"),
 ("CHM 121","General Chemistry I","Chemistry",4,"genchem1"),
 ("CHM 122","General Chemistry II","Chemistry",4,"genchem2"),
 ("HIS 111","U.S. History I","History",3,"us_hist"),
 ("HSP 101","Introduction to Hospitality Management","Hospitality",3,"hospitality"),
 ("COM 105","Public Speaking","Communication",3,"public_speaking")]
PCU = [("CSE 142","Computer Programming I","Computer Science",4,"q_prog1"),
 ("CSE 143","Computer Programming II","Computer Science",4,"q_prog2"),
 ("CSE 373","Data Structures and Algorithms","Computer Science",4,"q_dsa"),
 ("MATH 124","Calculus I","Mathematics",5,"q_calc1"),
 ("MATH 125","Calculus II","Mathematics",5,"q_calc2"),
 ("MATH 126","Calculus III","Mathematics",5,"q_calc3"),
 ("MATH 208","Matrix Algebra","Mathematics",3,"q_matrix"),
 ("STAT 311","Elements of Statistics","Mathematics",5,"elem_stats"),
 ("ECON 200","Introduction to Microeconomics","Economics",4,"micro_intro"),
 ("ECON 201","Introduction to Macroeconomics","Economics",4,"macro_intro"),
 ("PSYCH 101","Psychology as a Science","Psychology",5,"intro_psych"),
 ("BIOL 180","Introductory Biology I","Biology",5,"bio1"),
 ("CHEM 142","General Chemistry I","Chemistry",5,"genchem1"),
 ("CHEM 237","Organic Chemistry I","Chemistry",4,"q_orgo1")]
