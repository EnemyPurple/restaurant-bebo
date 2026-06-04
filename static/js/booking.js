async function refreshAvailability(form) {
  const date = form.querySelector("[name='date']")?.value;
  const time = form.querySelector("[name='time']")?.value;
  const guests = form.querySelector("[name='guests']")?.value;
  const hint = form.querySelector(".js-booking-availability");
  const tableSelect = form.querySelector("[name='table']");

  if (!date || !time || !guests || !hint || !tableSelect) return;
  hint.textContent = "Проверяем доступность...";

  const params = new URLSearchParams({ date, time, guests });
  const res = await fetch(`/api/booking/availability/?${params.toString()}`, { headers: { "Accept": "application/json" } });
  const data = await res.json();

  tableSelect.innerHTML = "";
  if (!data.results || data.results.length === 0) {
    hint.textContent = "Нет доступных столиков на выбранные дату/время.";
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = "Нет доступных столиков";
    tableSelect.appendChild(opt);
    return;
  }
  hint.textContent = `Доступно: ${data.results.length}`;
  for (const t of data.results) {
    const opt = document.createElement("option");
    opt.value = t.id;
    opt.textContent = `#${t.number} — ${t.seats} мест (${t.location})`;
    tableSelect.appendChild(opt);
  }
}

document.querySelectorAll("form").forEach((form) => {
  if (!form.querySelector("[name='date'], [name='table']")) return;
  const handler = () => refreshAvailability(form);
  ["date", "time", "guests"].forEach((name) => {
    form.querySelector(`[name='${name}']`)?.addEventListener("change", handler);
  });
});

