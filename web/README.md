# Web app (Next.js 15 + Supabase)

## Run locally
```bash
cd web
npm install
cp .env.example .env.local   # skip if .env.local is already filled in
npm run dev                  # http://localhost:3000
```
Requires Node 20+.

| Page | Who | What |
|------|-----|------|
| `/check` | Public, no login | Transfer Check: pick courses, see likely BU equivalents, units, flags and programme coverage. Nothing saved. |
| `/login` | Evaluators | Email + password (Supabase Auth). Only users in `staff_profiles` get in. |
| `/admin` | Evaluators | Dashboard. Inbox / Review / Manual entry come in steps 4–5. |

## Rules engine
`src/lib/engine.ts` is the deterministic engine (R1–R12) used by the Transfer Check now and by the evaluation pipeline in step 5.
`npm run test:engine` scores it against the synthetic Answer Key (currently 35/35).

## Deploy to Vercel
1. Push this repo to GitHub, then import it in Vercel with **Root Directory = `web`**.
2. Add env vars `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
3. In Supabase → Authentication → URL Configuration, set **Site URL** to your Vercel URL.
