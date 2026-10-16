// Wraps src/artifact.html (the fragment Claude's Artifact tool publishes)
// in a real HTML document so the same source also runs as a plain web page.
const fs = require("fs");
const body = fs.readFileSync("src/artifact.html", "utf8");
const page = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
  :root { color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  body { margin: 0; font: 14px system-ui, sans-serif; }
  img { max-width: 100%; }
  [hidden] { display: none !important; }
</style>
</head>
<body>
${body}
</body>
</html>
`;
fs.writeFileSync("index.html", page);
console.log("wrote index.html (" + page.length + " bytes)");
