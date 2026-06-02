async function loadMenu() {
  const q = document.getElementById("menu-q").value.trim();
  const category = document.getElementById("menu-category").value;
  const toggles = [...document.querySelectorAll(".bebo-menu-toggle.is-active")].map((el) => el.dataset.filter);
  const params = new URLSearchParams();
  if (q) params.set("q", q);
  if (category) params.set("category", category);

  const res = await fetch(`/api/menu/dishes/?${params.toString()}`, { headers: { "Accept": "application/json" } });
  const data = await res.json();

  const root = document.getElementById("menu-results");
  const empty = document.getElementById("menu-empty");
  root.innerHTML = "";

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
      <div class="card h-100">
        ${d.photo ? `<img src="${d.photo}" class="card-img-top" alt="${d.name}">` : ""}
        <div class="card-body d-flex flex-column">
          <div class="d-flex justify-content-between">
            <h5 class="card-title mb-1">${d.name}</h5>
            <span class="badge text-bg-primary">${d.price} ₽</span>
          </div>
          <div class="text-muted small mb-2">${d.category.name}</div>
          <div class="card-text small text-muted">${(d.description || "").slice(0, 120)}</div>
          <div class="mt-2 d-flex gap-1 flex-wrap">
            ${d.is_spicy ? `<span class="badge text-bg-danger">Острое</span>` : ""}
            ${d.is_vegetarian ? `<span class="badge text-bg-success">Вегет.</span>` : ""}
            ${d.is_recommended ? `<span class="badge text-bg-warning">Реком.</span>` : ""}
          </div>
          <a class="btn btn-sm btn-outline-secondary mt-auto" href="/menu/dish/${d.slug}/">Подробнее</a>
        </div>
      </div>
    `;
    root.appendChild(col);
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

