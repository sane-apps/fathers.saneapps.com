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

  // Reader Contents: highlight the passage currently in view.
  const tocRoot = document.querySelector(".reader-rail .toc, #contents .toc");
  if (tocRoot) {
    const links = [...tocRoot.querySelectorAll('a[href*="#s"]')];
    const entries = links
      .map((link) => {
        const hash = (link.getAttribute("href") || "").split("#")[1];
        if (!hash) return null;
        const target = document.getElementById(hash);
        return target ? { link, target } : null;
      })
      .filter(Boolean);

    const setCurrent = (active) => {
      for (const { link } of entries) {
        const on = link === active;
        link.classList.toggle("is-current", on);
        if (on) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      }
      if (active && tocRoot.closest(".reader-rail")) {
        const rail = tocRoot;
        const row = active.closest("li");
        if (!row) return;
        const rowTop = row.offsetTop;
        const rowBottom = rowTop + row.offsetHeight;
        const viewTop = rail.scrollTop;
        const viewBottom = viewTop + rail.clientHeight;
        if (rowTop < viewTop + 8) rail.scrollTop = Math.max(0, rowTop - 12);
        else if (rowBottom > viewBottom - 8) rail.scrollTop = rowBottom - rail.clientHeight + 12;
      }
    };

    if (entries.length) {
      const pick = () => {
        const probe = window.scrollY + Math.min(160, window.innerHeight * 0.28);
        let current = entries[0];
        for (const entry of entries) {
          const top = entry.target.getBoundingClientRect().top + window.scrollY;
          if (top <= probe) current = entry;
          else break;
        }
        setCurrent(current.link);
      };

      let ticking = false;
      const onScroll = () => {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(() => {
          pick();
          ticking = false;
        });
      };
      window.addEventListener("scroll", onScroll, { passive: true });
      window.addEventListener("resize", onScroll, { passive: true });
      pick();

      tocRoot.addEventListener("click", (ev) => {
        const a = ev.target.closest('a[href*="#s"]');
        if (!a || !tocRoot.contains(a)) return;
        setCurrent(a);
      });
    }
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
})();
