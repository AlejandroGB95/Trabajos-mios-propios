document.addEventListener("DOMContentLoaded", () => {
  // Animaciones intro
  gsap.to(".intro-text", {
    scale: 1,
    opacity: 1,
    duration: 1.2,
    ease: "expo.out"
  });

  gsap.to(".subtitle", {
    opacity: 1,
    delay: 1,
    duration: 1,
    ease: "power2.out"
  });

  // Animar barras de habilidades al hacer scroll
  gsap.utils.toArray(".fill").forEach((bar) => {
    gsap.to(bar, {
      scrollTrigger: {
        trigger: bar,
        start: "top 90%",
      },
      width: bar.style.width,
      duration: 1,
      ease: "power2.out"
    });
  });

  // Animar proyectos al hacer scroll
  gsap.utils.toArray(".project-card").forEach((card, i) => {
    gsap.to(card, {
      scrollTrigger: {
        trigger: card,
        start: "top 95%",
      },
      opacity: 1,
      scale: 1,
      delay: i * 0.2,
      duration: 0.8,
      ease: "back.out(1.7)"
    });
  });

  // Modo claro/oscuro
  const toggle = document.getElementById("mode-toggle");
  toggle.addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
  });
});

