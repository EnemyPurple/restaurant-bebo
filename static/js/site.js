(() => {
  const header = document.querySelector(".wr-header");
  const hero = document.querySelector(".wr-hero");
  const cookie = document.getElementById("wrCookie");
  const cookieAccept = document.getElementById("wrCookieAccept");
  const modal = document.getElementById("wrBookingModal");
  const modalTriggers = document.querySelectorAll("[data-wr-booking-open]");
  const modalClose = document.querySelectorAll("[data-wr-booking-close]");

  if (header && hero) {
    const onScroll = () => {
      header.classList.toggle("is-scrolled", window.scrollY > 40);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  } else if (header) {
    header.classList.add("wr-header--solid", "is-scrolled");
  }

  const burger = document.getElementById("wrBurger");
  const mobileMenu = document.getElementById("wrMobileMenu");
  if (burger && mobileMenu) {
    const toggle = (open) => {
      mobileMenu.classList.toggle("is-open", open);
      document.body.style.overflow = open ? "hidden" : "";
    };
    burger.addEventListener("click", () => toggle(!mobileMenu.classList.contains("is-open")));
    mobileMenu.addEventListener("click", (e) => {
      if (e.target === mobileMenu) toggle(false);
    });
    mobileMenu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => toggle(false)));
  }

  if (cookie && cookieAccept) {
    const key = "wr_cookie_accept";
    if (!localStorage.getItem(key)) {
      requestAnimationFrame(() => cookie.classList.add("is-visible"));
    }
    cookieAccept.addEventListener("click", () => {
      localStorage.setItem(key, "1");
      cookie.classList.remove("is-visible");
    });
  }

  const openModal = () => {
    if (!modal) return;
    modal.classList.add("is-open");
    document.body.style.overflow = "hidden";
  };
  const closeModal = () => {
    if (!modal) return;
    modal.classList.remove("is-open");
    document.body.style.overflow = "";
  };

  modalTriggers.forEach((el) => el.addEventListener("click", (e) => {
    e.preventDefault();
    openModal();
  }));
  modalClose.forEach((el) => el.addEventListener("click", closeModal));
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeModal();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeModal();
    });
  }

  const heroSlides = document.querySelectorAll(".wr-hero__slide");
  if (heroSlides.length > 1) {
    let idx = 0;
    setInterval(() => {
      heroSlides[idx].classList.remove("is-active");
      idx = (idx + 1) % heroSlides.length;
      heroSlides[idx].classList.add("is-active");
    }, 5500);
  }
})();
