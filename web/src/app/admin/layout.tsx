import Link from "next/link";
import { redirect } from "next/navigation";
import { getStaff } from "@/lib/supabase/server";

export const dynamic = "force-dynamic";

const NAV = [
  { href: "/admin", label: "Dashboard" },
  { href: "/admin/inbox", label: "Inbox", soon: true },
  { href: "/admin/review", label: "Review queue", soon: true },
  { href: "/admin/new", label: "Manual entry / upload", soon: true },
];

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const { user, staff } = await getStaff();
  if (!user) redirect("/login?next=/admin");
  if (!staff) redirect("/login?error=" + encodeURIComponent("This account is not set up as an evaluator."));
  return (
    <div className="grid gap-6 md:grid-cols-[220px_1fr]">
      <aside className="card h-fit space-y-1 p-3">
        <div className="px-2 pb-2">
          <div className="text-sm font-semibold">{staff.full_name}</div>
          <div className="text-xs capitalize text-slate-500">{staff.role}</div>
        </div>
        {NAV.map((n) => (
          <Link key={n.href} href={n.href} className="flex items-center justify-between rounded-md px-2 py-1.5 text-sm hover:bg-slate-100">
            {n.label}{n.soon && <span className="chip bg-slate-100 text-slate-500">soon</span>}
          </Link>
        ))}
        <form action="/auth/signout" method="post" className="pt-2">
          <button className="btn-ghost w-full">Sign out</button>
        </form>
      </aside>
      <section>{children}</section>
    </div>
  );
}
