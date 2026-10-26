import type { Config } from "tailwindcss";
export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: { extend: { colors: { brand: { DEFAULT: "#CC0000", dark: "#990000" }, ink: "#1F2937" } } },
  plugins: [],
} satisfies Config;
