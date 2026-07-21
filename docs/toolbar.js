// Injects the shared top toolbar (logo + nav) on every docs page.
// The logo SVGs are loaded from files (yp_logo.svg / yp_logo_mark.svg) and
// inlined into the DOM so the wordmark can inherit the toolbar color via
// `currentColor` (readable in light and dark). The full lockup shows on wide
// screens; the mark-only variant shows on narrow screens (see styles.css).

(function () {
  const GITHUB = `<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>`;

  const REPO = "https://github.com/YoungAgency/youngplatform_api_docs";

  const links = [
    { label: "Home", href: "./index.html", match: (p) => p.endsWith("/index.html") || p.endsWith("/") },
    { label: "Guides", href: "./guide.html?doc=overview", match: (p) => p.endsWith("/guide.html") },
    { label: "API Spec", href: "./openapi.html", match: (p) => p.endsWith("/openapi.html") },
  ];

  const path = location.pathname;
  const navHtml = links
    .map(
      (l) =>
        `<a href="${l.href}"${l.match(path) ? ' class="active"' : ""}>${l.label}</a>`
    )
    .join("");

  const header = document.createElement("header");
  header.className = "toolbar";
  header.innerHTML =
    `<a class="brand" href="./index.html" aria-label="YoungPlatform"></a>` +
    `<nav>${navHtml}` +
    `<a class="icon-link" href="${REPO}" target="_blank" rel="noopener" aria-label="GitHub repository">${GITHUB}</a>` +
    `</nav>`;

  document.body.prepend(header);

  // Load the logo files and inline the returned <svg> so `currentColor` works.
  const brand = header.querySelector(".brand");
  Promise.all([
    loadSvg("./yp_logo.svg", "logo-full"),
    loadSvg("./yp_logo_mark.svg", "logo-mark"),
  ]).then(([full, mark]) => {
    if (full) brand.appendChild(full);
    if (mark) brand.appendChild(mark);
    if (!full && !mark) brand.textContent = "YoungPlatform"; // fetch failed — text fallback
  });

  async function loadSvg(url, className) {
    try {
      const res = await fetch(url);
      if (!res.ok) return null;
      // Parse via HTML innerHTML so the node belongs to this document and can be
      // appended directly; the HTML parser preserves SVG attribute casing (viewBox).
      const tmp = document.createElement("div");
      tmp.innerHTML = (await res.text()).trim();
      const svg = tmp.querySelector("svg");
      if (svg) svg.classList.add(className);
      return svg;
    } catch (_) {
      return null;
    }
  }
})();
