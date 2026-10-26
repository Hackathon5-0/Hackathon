import Link from "next/link";

export default function Home() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <section className="card md:col-span-2">
        <h1 className="text-2xl font-bold">Thinking of transferring to Boston University?</h1>
        <p className="mt-2 max-w-2xl text-slate-600">
          See how your completed courses would likely transfer: which BU courses they match, how many units you keep,
          and what still needs a department review. Nothing is submitted or saved.
        </p>
        <Link href="/check" className="btn mt-4">Check my courses</Link>
      </section>
      <section className="card">
        <h2 className="font-semibold">Ready to send your transcript?</h2>
        <p className="mt-1 text-sm text-slate-600">After admission, email your transcript to the Credit Evaluation office. Official copies must come from your college's registrar.</p>
      </section>
      <section className="card">
        <h2 className="font-semibold">Evaluators</h2>
        <p className="mt-1 text-sm text-slate-600">Review incoming transcripts and the engine's recommendations.</p>
        <Link href="/admin" className="btn-ghost mt-3">Evaluator login</Link>
      </section>
    </div>
  );
}
