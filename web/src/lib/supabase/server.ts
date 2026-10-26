import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { getSupabaseConfig } from "./config";

export async function supabaseServer() {
  const store = await cookies();
  const { url, key } = getSupabaseConfig();
  return createServerClient(url, key, {
    cookies: {
      getAll: () => store.getAll(),
      setAll: (list) => {
        try { list.forEach(({ name, value, options }) => store.set(name, value, options)); }
        catch { /* called from a Server Component: middleware refreshes the session */ }
      },
    },
  });
}

/** Returns the signed-in staff member, or null if not signed in / not staff. */
export async function getStaff() {
  const sb = await supabaseServer();
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return { sb, user: null, staff: null };
  const { data: staff } = await sb.from("staff_profiles").select("full_name, role, active").eq("user_id", user.id).maybeSingle();
  return { sb, user, staff: staff && staff.active ? staff : null };
}
