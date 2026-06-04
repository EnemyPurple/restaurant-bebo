async function loadMenu() {
  const q = document.getElementById("menu-q")?.value.trim() || "";
  const category = document.getElementById("menu-category")?.value || "";
  const toggles = [...document.querySelectorAll(".wr-menu-toggle.is-active, .bebo-menu-toggle.is-active")].map((el) => el.dataset.filter);
  const params = new URLSearchParams();
  if (q) params.set("q", q);
  if (category) params.set("category", category);

  const root = document.getElementById("menu-results");
  const empty = document.getElementById("menu-empty");
  if (!root || !empty) return;

  root.innerHTML = "";

  try {
    const res = await fetch(`/api/menu/dishes/?${params.toString()}`, {
      headers: { Accept: "application/json" },
    });
    if (!res.ok) {
      throw new Error(`Menu API error: ${res.status}`);
    }
    const data = await res.json();

    const results = (data.results || []).filter((dish) => {
      if (toggles.includes("recommended") && !dish.is_recommended) return false;
      if (toggles.includes("vegetarian") && !dish.is_vegetarian) return false;
      if (toggles.includes("spicy") && !dish.is_spicy) return false;
      return true;
    });

    if (results.length === 0) {
      empty.classList.remove("d-none");
      return;
    }
    empty.classList.add("d-none");

    for (const d of results) {
      const col = document.createElement("div");
      col.className = "col-md-6 col-lg-4";
      col.innerHTML = `
      <div class="wr-menu-card h-100 d-flex flex-column">
        ${d.photo ? `<img src="${d.photo}" alt="${d.name}">` : ""}
        <div class="p-3 d-flex flex-column flex-grow-1">
          <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
            <h5 class="h6 mb-0 wr-serif">${d.name}</h5>
            <span class="small text-nowrap">${d.price}&nbsp;₽</span>
          </div>
          <p class="small text-muted flex-grow-1">${(d.description || "").slice(0, 120)}</p>
          <div class="d-flex gap-1 flex-wrap mb-2">
            ${d.is_spicy ? `<span class="badge rounded-0 text-bg-dark">Острое</span>` : ""}
            ${d.is_vegetarian ? `<span class="badge rounded-0 text-bg-secondary">Вегет.</span>` : ""}
            ${d.is_recommended ? `<span class="badge rounded-0 border">Реком.</span>` : ""}
          </div>
          <a class="wr-link-arrow small mt-auto" href="/menu/dish/${d.slug}/">Подробнее</a>
        </div>
      </div>
    `;
      root.appendChild(col);
    }
  } catch (error) {
    console.error("Failed to load menu:", error);
    empty.textContent = "Не удалось загрузить меню. Обновите страницу.";
    empty.classList.remove("d-none");
  }
}

document.getElementById("menu-apply")?.addEventListener("click", loadMenu);
document.getElementById("menu-q")?.addEventListener("keydown", (e) => {
  if (e.key === "Enter") loadMenu();
});
document.querySelectorAll(".wr-menu-toggle, .bebo-menu-toggle").forEach((toggle) => {
  toggle.addEventListener("click", () => {
    toggle.classList.toggle("is-active");
    loadMenu();
  });
});

loadMenu();

