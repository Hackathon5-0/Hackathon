"use client";
import { createBrowserClient } from "@supabase/ssr";
import { getClientSupabaseConfig } from "./config";

export const supabaseBrowser = () => {
  const { url, key } = getClientSupabaseConfig();
  return createBrowserClient(url, key);
};
