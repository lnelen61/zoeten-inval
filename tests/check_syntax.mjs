// Controle 1 (geen installatie nodig, alleen Node.js):
// leest index.html, haalt elk <script>-blok zonder src eruit en kijkt of de JavaScript syntactisch klopt.
// Gebruik (vanuit de projectmap):  node tests/check_syntax.mjs
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

// projectmap = één niveau boven de map tests (werkt op Windows en Linux)
const projectMap = join(dirname(fileURLToPath(import.meta.url)), "..");
const html = readFileSync(join(projectMap, "index.html"), "utf8");

// alle inline scripts (zonder src=)
const blokken = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (blokken.length === 0) { console.error("FOUT: geen inline script gevonden in index.html"); process.exit(1); }

let fouten = 0;
blokken.forEach((code, i) => {
  try { new Function(code); }           // alleen compileren, niet uitvoeren
  catch (e) { fouten++; console.error(`FOUT in script-blok ${i + 1}: ${e.message}`); }
});
if (fouten) process.exit(1);
console.log(`OK: ${blokken.length} script-blok(ken) syntactisch geldig`);
