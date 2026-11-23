// "The Daily Globe" — news-image-20261122.
// The entry image is drawn by draw_entry.py (PIL, deterministic) and held in
// this repository as entry.png. This program copies it to the output
// directory, byte for byte, so both grading runs write identical bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
