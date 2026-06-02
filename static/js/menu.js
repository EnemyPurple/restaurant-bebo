async function loadMenu() {
  const q = document.getElementById("menu-q")?.value.trim() || "";
  const category = document.getElementById("menu-category")?.value || "";
  const toggles = [...document.querySelectorAll(".bebo-menu-toggle.is-active")].map((el) => el.dataset.filter);
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
      <div class="card h-100 bebo-menu-card">
        ${d.photo ? `<img src="${d.photo}" class="card-img-top bebo-menu-card__img" alt="${d.name}">` : ""}
        <div class="card-body d-flex flex-column bebo-menu-card__body">
          <div class="bebo-menu-card__head">
            <h5 class="bebo-menu-card__title">${d.name}</h5>
            <span class="bebo-menu-card__price">${d.price}&nbsp;₽</span>
          </div>
          <p class="bebo-menu-card__desc">${(d.description || "").slice(0, 120)}</p>
          <div class="bebo-menu-card__badges d-flex gap-1 flex-wrap">
            ${d.is_spicy ? `<span class="badge text-bg-danger">Острое</span>` : ""}
            ${d.is_vegetarian ? `<span class="badge text-bg-success">Вегет.</span>` : ""}
            ${d.is_recommended ? `<span class="badge text-bg-warning">Реком.</span>` : ""}
          </div>
          <a class="btn btn-sm btn-outline-secondary bebo-menu-card__link mt-auto" href="/menu/dish/${d.slug}/">Подробнее</a>
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
document.querySelectorAll(".bebo-menu-toggle").forEach((toggle) => {
  toggle.addEventListener("click", () => {
    toggle.classList.toggle("is-active");
    loadMenu();
  });
});

loadMenu();

