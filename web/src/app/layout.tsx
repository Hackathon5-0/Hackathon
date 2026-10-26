import "./globals.css";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = { title: "Transfer Credit Check", description: "BU transfer credit evaluation (hackathon prototype, synthetic data)" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <header className="border-b border-slate-200 bg-white">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
            <Link href="/" className="flex items-center gap-2 font-bold">
              <span className="grid h-8 w-8 place-items-center rounded-md bg-brand text-white">TC</span>
              <span>Transfer Credit</span>
            </Link>
            <nav className="flex items-center gap-4 text-sm">
              <Link href="/check" className="hover:text-brand">Transfer Check</Link>
              <Link href="/admin" className="hover:text-brand">Evaluator login</Link>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
        <footer className="mx-auto max-w-6xl px-4 pb-8 text-xs text-slate-500">
          Hackathon prototype. All data is synthetic. Results are estimates; academic departments make the final decision.
        </footer>
      </body>
    </html>
  );
}
