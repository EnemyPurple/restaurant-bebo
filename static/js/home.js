(() => {
  const root = document.querySelector(".bebo-countdown");
  if (!root) return;

  const targetRaw = root.getAttribute("data-countdown-target");
  if (!targetRaw) return;

  const target = new Date(targetRaw).getTime();
  if (Number.isNaN(target)) return;

  const daysEl = root.querySelector("[data-unit='days']");
  const hoursEl = root.querySelector("[data-unit='hours']");
  const minutesEl = root.querySelector("[data-unit='minutes']");
  if (!daysEl || !hoursEl || !minutesEl) return;

  const pad = (value) => String(value).padStart(2, "0");

  const render = () => {
    const now = Date.now();
    const diff = Math.max(0, target - now);

    const totalMinutes = Math.floor(diff / 60000);
    const days = Math.floor(totalMinutes / (60 * 24));
    const hours = Math.floor((totalMinutes % (60 * 24)) / 60);
    const minutes = totalMinutes % 60;

    daysEl.textContent = pad(days);
    hoursEl.textContent = pad(hours);
    minutesEl.textContent = pad(minutes);

    if (diff === 0) {
      root.classList.add("bebo-countdown--done");
    }
  };

  render();
  setInterval(render, 30000);
})();
