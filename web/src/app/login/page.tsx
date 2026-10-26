"use client";
import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { supabaseBrowser } from "@/lib/supabase/client";

function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(params.get("error"));
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault(); setBusy(true); setError(null);
    const sb = supabaseBrowser();
    const { data, error } = await sb.auth.signInWithPassword({ email, password });
    if (error || !data.user) { setError(error?.message ?? "Sign-in failed"); setBusy(false); return; }
    const { data: staff } = await sb.from("staff_profiles").select("active").eq("user_id", data.user.id).maybeSingle();
    if (!staff?.active) {
      await sb.auth.signOut();
      setError("This account is not set up as an evaluator. Ask an admin to add you."); setBusy(false); return;
    }
    router.replace(params.get("next") || "/admin"); router.refresh();
  }

  return (
    <form onSubmit={onSubmit} className="card mx-auto mt-6 max-w-sm space-y-4">
      <div>
        <h1 className="text-xl font-bold">Evaluator sign in</h1>
        <p className="text-sm text-slate-500">For Credit Evaluation staff and department evaluators.</p>
      </div>
      <div><label className="label" htmlFor="email">Email</label>
        <input id="email" type="email" required autoComplete="username" className="input" value={email} onChange={(e) => setEmail(e.target.value)} /></div>
      <div><label className="label" htmlFor="pw">Password</label>
        <input id="pw" type="password" required autoComplete="current-password" className="input" value={password} onChange={(e) => setPassword(e.target.value)} /></div>
      {error && <p className="rounded-md bg-red-50 p-2 text-sm text-red-700">{error}</p>}
      <button className="btn w-full" disabled={busy}>{busy ? "Signing in…" : "Sign in"}</button>
      <p className="text-xs text-slate-500">Accounts are created by an admin. There is no public sign-up.</p>
    </form>
  );
}
export default function LoginPage() { return <Suspense><LoginForm /></Suspense>; }
