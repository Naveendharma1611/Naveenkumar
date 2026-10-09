import { createClient } from "@supabase/supabase-js";

const url =
  import.meta.env.VITE_SUPABASE_URL ||
  "https://yijjamxxovaguxfeenuy.supabase.co";
const anonKey =
  import.meta.env.VITE_SUPABASE_ANON_KEY ||
  "sb_publishable_A_dpT1pxY_BLr6jG4BlTIQ_WkMshgdI";

if (!url || !anonKey) {
  // eslint-disable-next-line no-console
  console.warn(
    "Missing VITE_SUPABASE_URL / VITE_SUPABASE_ANON_KEY. Copy .env.example to .env and fill in your Supabase project's values."
  );
}

export const supabase = createClient(url, anonKey);

export const DIFFICULTY_POINTS = { easy: 10, medium: 20, hard: 30 };
export const MAX_ATTEMPTS_BEFORE_HELP = 3;
