/**
 * Modular High-End Personal Portfolio - Main Frontend Script
 * Handles dynamic interactions, glassmorphism lighting effects, and UI utilities.
 */

document.addEventListener("DOMContentLoaded", () => {
  initNavbarScroll();
  initMobileMenu();
  initCardSpotlightLighting();
  initCopyEmail();
  initActiveNavTracking();
  initBackToTop();
  printConsoleBanner();
});

/**
 * Elevates navbar with darker background and border when scrolled
 */
function initNavbarScroll() {
  const navbar = document.getElementById("main-nav");
  if (!navbar) return;

  const handleScroll = () => {
    if (window.scrollY > 20) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  };

  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll();
}

/**
 * Mobile responsive menu drawer toggle
 */
function initMobileMenu() {
  const menuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  const mobileLinks = document.querySelectorAll(".mobile-nav-link");

  if (!menuBtn || !mobileMenu) return;

  const toggleMenu = () => {
    const isExpanded = menuBtn.getAttribute("aria-expanded") === "true";
    menuBtn.setAttribute("aria-expanded", String(!isExpanded));
    mobileMenu.classList.toggle("hidden");

    // Toggle icon animation
    const icon = menuBtn.querySelector("i");
    if (icon) {
      if (mobileMenu.classList.contains("hidden")) {
        icon.classList.remove("fa-xmark");
        icon.classList.add("fa-bars");
      } else {
        icon.classList.remove("fa-bars");
        icon.classList.add("fa-xmark");
      }
    }
  };

  menuBtn.addEventListener("click", toggleMenu);

  mobileLinks.forEach(link => {
    link.addEventListener("click", () => {
      mobileMenu.classList.add("hidden");
      menuBtn.setAttribute("aria-expanded", "false");
      const icon = menuBtn.querySelector("i");
      if (icon) {
        icon.classList.remove("fa-xmark");
        icon.classList.add("fa-bars");
      }
    });
  });
}

/**
 * Subtle dynamic spotlight lighting effect that follows mouse cursor over cards
 */
function initCardSpotlightLighting() {
  const cards = document.querySelectorAll(".card-spotlight");
  if (!cards.length) return;

  cards.forEach(card => {
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      card.style.setProperty("--mouse-x", `${x}px`);
      card.style.setProperty("--mouse-y", `${y}px`);
    });
  });
}

/**
 * Interactive one-click copy email button with sleek toast notification
 */
function initCopyEmail() {
  const copyBtns = document.querySelectorAll(".copy-email-btn");
  const toast = document.getElementById("clipboard-toast");
  let toastTimeout;

  if (!copyBtns.length) return;

  copyBtns.forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const emailToCopy = btn.getAttribute("data-email") || "akashgowdan2006@gmail.com";

      try {
        await navigator.clipboard.writeText(emailToCopy);
        showToast("Email copied to clipboard!");
      } catch (err) {
        // Fallback for older browsers or restricted permissions
        const textArea = document.createElement("textarea");
        textArea.value = emailToCopy;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
          document.execCommand("copy");
          showToast("Email copied to clipboard!");
        } catch (subErr) {
          showToast("Press Ctrl+C to copy: " + emailToCopy);
        }
        document.body.removeChild(textArea);
      }
    });
  });

  function showToast(message) {
    if (!toast) return;
    const msgEl = document.getElementById("toast-message");
    if (msgEl) msgEl.textContent = message;

    toast.classList.remove("hidden");
    // Trigger CSS transition
    requestAnimationFrame(() => {
      toast.classList.add("show");
    });

    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => {
        toast.classList.add("hidden");
      }, 350);
    }, 3000);
  }
}

/**
 * Tracks current active section using IntersectionObserver to highlight navbar items
 */
function initActiveNavTracking() {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link[href^='#']");

  if (!sections.length || !navLinks.length) return;

  const observerOptions = {
    root: null,
    rootMargin: "-20% 0px -60% 0px",
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute("id");
        navLinks.forEach(link => {
          if (link.getAttribute("href") === `#${id}`) {
            link.classList.add("text-indigo-400", "font-semibold");
            link.classList.remove("text-slate-300");
          } else {
            link.classList.remove("text-indigo-400", "font-semibold");
            link.classList.add("text-slate-300");
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach(section => observer.observe(section));
}

/**
 * Floating Back-to-Top Button
 */
function initBackToTop() {
  const bttBtn = document.getElementById("back-to-top");
  if (!bttBtn) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 400) {
      bttBtn.classList.remove("opacity-0", "pointer-events-none", "translate-y-4");
      bttBtn.classList.add("opacity-100", "translate-y-0");
    } else {
      bttBtn.classList.add("opacity-0", "pointer-events-none", "translate-y-4");
      bttBtn.classList.remove("opacity-100", "translate-y-0");
    }
  }, { passive: true });

  bttBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/**
 * Console developer greeting
 */
function printConsoleBanner() {
  const styles = [
    "color: #818cf8",
    "font-size: 13px",
    "font-family: monospace",
    "font-weight: bold",
    "padding: 6px 10px",
    "background: #0f172a",
    "border-radius: 6px",
    "border: 1px solid #334155"
  ].join(";");

  console.log("%c⚡ Akash N | Full-Stack Engineer Portfolio Initialized.", styles);
  console.log("%cCurious about the codebase? Inspect the clean Flask + Tailwind architecture.", "color: #94a3b8; font-size: 11px;");
}
