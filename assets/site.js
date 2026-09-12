(() => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("#site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  const q = document.querySelector("#q");
  const results = document.querySelector("#results");
  if (q && results) {
    let index = [];
    fetch("/data/search-index.json")
      .then((r) => r.json())
      .then((data) => {
        index = data;
        if (q.value) render(q.value);
      })
      .catch(() => {
        results.innerHTML = "<li>Search index unavailable.</li>";
      });

    const render = (term) => {
      const t = term.trim().toLowerCase();
      if (t.length < 2) {
        results.innerHTML = "";
        return;
      }
      const hits = [];
      for (const row of index) {
        const blob = `${row.title} ${row.author || ""} ${row.text || ""}`.toLowerCase();
        if (blob.includes(t)) hits.push(row);
        if (hits.length >= 40) break;
      }
      results.innerHTML = hits
        .map(
          (h) =>
            `<li><a href="${h.href}"><strong>${escapeHtml(h.title)}</strong><span>${escapeHtml(
              h.author || h.kind
            )}</span></a></li>`
        )
        .join("");
    };

    q.addEventListener("input", () => render(q.value));
  }

  document.querySelectorAll("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const el = document.querySelector(btn.getAttribute("data-copy") || "");
      if (!el) return;
      try {
        await navigator.clipboard.writeText(el.innerText);
        const old = btn.textContent;
        btn.textContent = "Copied";
        window.setTimeout(() => {
          btn.textContent = old;
        }, 1500);
      } catch {
        btn.textContent = "Select the prompt and copy";
      }
    });
  });

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
})();
