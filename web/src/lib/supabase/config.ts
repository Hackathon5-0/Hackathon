export function getSupabaseConfig() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_ANON_KEY;

  if (!url || !key) {
    throw new Error("Set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.");
  }

  return { url, key };
}

export function getClientSupabaseConfig(): { url: string; key: string } {
  // Values are injected at runtime by the server layout via a <script> tag.
  const config = (globalThis as unknown as { __supabaseConfig?: { url: string; key: string } }).__supabaseConfig;
  if (!config?.url || !config?.key) {
    throw new Error("Supabase client config not available.");
  }
  return config;
}
