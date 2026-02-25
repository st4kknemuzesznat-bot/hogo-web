const body = document.body;

// Smooth load sequence.
const LOADER_MIN_MS = 1800;
const completeLoad = () => {
  body.classList.remove("is-loading");
  body.classList.add("page-ready");
};

if (document.readyState === "complete") {
  setTimeout(completeLoad, LOADER_MIN_MS);
} else {
  window.addEventListener("load", () => setTimeout(completeLoad, LOADER_MIN_MS));
}

// Transition overlay for page exits (ignores hash links/new tabs).
document.addEventListener("click", (e) => {
  const link = e.target.closest("a[href]");
  if (!link) return;

  const href = link.getAttribute("href") || "";
  const sameTab = !link.target || link.target === "_self";
  const isHash = href.startsWith("#");
  const isExternalProtocol = href.startsWith("mailto:") || href.startsWith("tel:") || href.startsWith("javascript:");

  if (!sameTab || isHash || isExternalProtocol || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) {
    return;
  }

  e.preventDefault();
  body.classList.add("is-transitioning");
  setTimeout(() => {
    window.location.href = href;
  }, 360);
});

// Smooth scrolling for internal anchors.
document.addEventListener("click", (e) => {
  const a = e.target.closest('a[href^="#"]');
  if (!a) return;
  const id = a.getAttribute("href");
  const el = document.querySelector(id);
  if (!el) return;
  e.preventDefault();
  el.scrollIntoView({ behavior: "smooth", block: "start" });
});

// Reveal sections on scroll.
const sections = document.querySelectorAll(".section");
if (sections.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.18 }
  );

  sections.forEach((section) => observer.observe(section));
}

// Single gallery slider driven by server-provided image list.
const sliderRoot = document.querySelector(".gallery-slider");
if (sliderRoot) {
  const slider = document.getElementById("sliderImage");
  const sliderLink = document.getElementById("sliderLink");
  const leftArrow = sliderRoot.querySelector(".gallery-arrow.left");
  const rightArrow = sliderRoot.querySelector(".gallery-arrow.right");

  let images = [];
  try {
    const raw = sliderRoot.getAttribute("data-gallery-images") || "[]";
    const parsed = JSON.parse(raw);
    images = Array.isArray(parsed) ? parsed.filter(Boolean) : [];
  } catch {
    images = [];
  }

  let index = 0;

  const render = () => {
    if (!images.length || !slider || !sliderLink) return;
    const src = images[index];
    slider.src = src;
    sliderLink.href = src;
  };

  const prev = () => {
    if (!images.length) return;
    index = (index - 1 + images.length) % images.length;
    render();
  };

  const next = () => {
    if (!images.length) return;
    index = (index + 1) % images.length;
    render();
  };

  if (leftArrow) leftArrow.addEventListener("click", prev);
  if (rightArrow) rightArrow.addEventListener("click", next);

  document.addEventListener("keydown", (e) => {
    if (!images.length) return;
    if (e.key === "ArrowLeft") prev();
    if (e.key === "ArrowRight") next();
  });

  render();
}

const finePointer = window.matchMedia("(pointer:fine)").matches;
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Gentle 3D parallax effect.
if (!reducedMotion && finePointer) {
  const layers = Array.from(document.querySelectorAll(".parallax-layer"));
  let pointerX = 0;
  let pointerY = 0;

  const clamp = (v, min, max) => Math.min(Math.max(v, min), max);

  const applyParallax = () => {
    layers.forEach((el) => {
      const depth = Number(el.getAttribute("data-parallax") || 10);
      const rect = el.getBoundingClientRect();
      const inView = rect.bottom > 0 && rect.top < window.innerHeight;
      if (!inView) return;

      const rotateX = clamp((-pointerY / window.innerHeight) * depth * 0.12, -4, 4);
      const rotateY = clamp((pointerX / window.innerWidth) * depth * 0.14, -5, 5);
      const offsetY = window.scrollY * (depth / 2800);

      el.style.transform = `translate3d(0, ${offsetY}px, 0) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });

    requestAnimationFrame(applyParallax);
  };

  window.addEventListener("mousemove", (e) => {
    pointerX = e.clientX - window.innerWidth / 2;
    pointerY = e.clientY - window.innerHeight / 2;
  });

  applyParallax();
}
