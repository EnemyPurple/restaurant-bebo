async function refreshAvailability() {
  const date = document.getElementById("id_date")?.value;
  const time = document.getElementById("id_time")?.value;
  const guests = document.getElementById("id_guests")?.value;
  const hint = document.getElementById("booking-availability");
  const tableSelect = document.getElementById("id_table");

  if (!date || !time || !guests) return;
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

["id_date", "id_time", "id_guests"].forEach((id) => {
  document.getElementById(id)?.addEventListener("change", refreshAvailability);
});

