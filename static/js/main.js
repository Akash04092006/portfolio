/**
 * Modular High-End Personal Portfolio - Main Frontend Script (Part 3)
 * Dynamic category filtering, interactive spotlight engine, clipboard utilities & scroll-spy.
 */

document.addEventListener("DOMContentLoaded", () => {
  initProjectCategoryFilter();
  initCopyRepoUrls();
  initCardSpotlightLighting();
  initActiveNavTracking();
  initNavbarScroll();
  initMobileMenu();
  initCopyEmail();
  initBackToTop();
  initSmoothAnchorScroll();
  printConsoleBanner();
});

/**
 * --------------------------------------------------------------------------
 * 1. DYNAMIC PROJECTS CATEGORY FILTERING (PART 3)
 * Smoothly filters project cards by category without page reloads.
 * --------------------------------------------------------------------------
 */
function initProjectCategoryFilter() {
  const filterTabs = document.querySelectorAll(".filter-tab");
  const projectCards = document.querySelectorAll(".project-card");
  const emptyState = document.getElementById("projects-empty-state");

  if (!filterTabs.length || !projectCards.length) return;

  filterTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      // 1. Update active tab styling
      filterTabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      const selectedFilter = tab.getAttribute("data-filter") || "all";
      let matchCount = 0;

      // 2. Filter project cards with smooth animation
      projectCards.forEach((card) => {
        const cardCategory = card.getAttribute("data-category");

        if (selectedFilter === "all" || cardCategory === selectedFilter) {
          card.classList.remove("hidden");
          // Re-trigger CSS keyframe animation
          card.classList.remove("project-filter-animate");
          // Trigger DOM reflow
          void card.offsetWidth;
          card.classList.add("project-filter-animate");
          matchCount++;
        } else {
          card.classList.add("hidden");
          card.classList.remove("project-filter-animate");
        }
      });

      // 3. Handle empty state if no projects match
      if (emptyState) {
        if (matchCount === 0) {
          emptyState.classList.remove("hidden");
        } else {
          emptyState.classList.add("hidden");
        }
      }
    });
  });
}

/**
 * --------------------------------------------------------------------------
 * 2. COPY REPOSITORY URL TO CLIPBOARD (PART 3)
 * One-click copy for GitHub repo links with toast notification.
 * --------------------------------------------------------------------------
 */
function initCopyRepoUrls() {
  const copyRepoBtns = document.querySelectorAll(".copy-repo-btn");
  if (!copyRepoBtns.length) return;

  copyRepoBtns.forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const repoUrl = btn.getAttribute("data-repo-url");
      if (!repoUrl) return;

      try {
        await navigator.clipboard.writeText(repoUrl);
        showToast("Repository URL copied to clipboard!");
      } catch (err) {
        // Fallback for clipboard API
        const textarea = document.createElement("textarea");
        textarea.value = repoUrl;
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();
        try {
          document.execCommand("copy");
          showToast("Repository URL copied to clipboard!");
        } catch (subErr) {
          showToast(`Repo: ${repoUrl}`);
        }
        document.body.removeChild(textarea);
      }
    });
  });
}

/**
 * --------------------------------------------------------------------------
 * 3. GLOBAL GLASS TOAST NOTIFICATION UTILITY
 * --------------------------------------------------------------------------
 */
let toastTimeout;
function showToast(message) {
  const toast = document.getElementById("clipboard-toast");
  if (!toast) return;

  const msgEl = document.getElementById("toast-message");
  if (msgEl) msgEl.textContent = message;

  toast.classList.remove("hidden");
  requestAnimationFrame(() => {
    toast.classList.add("show");
  });

  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => {
      toast.classList.add("hidden");
    }, 350);
  }, 3200);
}

/**
 * --------------------------------------------------------------------------
 * 4. INTERACTIVE CURSOR SPOTLIGHT ENGINE
 * Dynamically calculates mouse coordinates relative to card boundaries
 * and updates CSS custom properties (--mouse-x, --mouse-y) in real time.
 * --------------------------------------------------------------------------
 */
function initCardSpotlightLighting() {
  const spotlightElements = document.querySelectorAll(".card-spotlight, .glass-card, .project-card");
  if (!spotlightElements.length) return;

  spotlightElements.forEach((card) => {
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      card.style.setProperty("--mouse-x", `${x}px`);
      card.style.setProperty("--mouse-y", `${y}px`);
    });

    card.addEventListener("mouseleave", () => {
      card.style.setProperty("--mouse-x", "-300px");
      card.style.setProperty("--mouse-y", "-300px");
    });
  });
}

/**
 * --------------------------------------------------------------------------
 * 5. ACTIVE NAVIGATION SCROLL-SPY
 * Highlights the header navbar links based on the active viewport section.
 * --------------------------------------------------------------------------
 */
function initActiveNavTracking() {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link[href^='#']");
  const mobileNavLinks = document.querySelectorAll(".mobile-nav-link[href^='#']");

  if (!sections.length || !navLinks.length) return;

  const observerOptions = {
    root: null,
    rootMargin: "-25% 0px -55% 0px",
    threshold: 0.15
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute("id");

        // Update Desktop Links
        navLinks.forEach((link) => {
          const href = link.getAttribute("href");
          if (href === `#${id}`) {
            link.classList.add("text-indigo-400", "font-semibold", "bg-white/5");
            link.classList.remove("text-slate-300");
          } else {
            link.classList.remove("text-indigo-400", "font-semibold", "bg-white/5");
            link.classList.add("text-slate-300");
          }
        });

        // Update Mobile Links
        mobileNavLinks.forEach((link) => {
          const href = link.getAttribute("href");
          if (href === `#${id}`) {
            link.classList.add("text-indigo-400", "font-semibold", "bg-white/10");
            link.classList.remove("text-slate-300");
          } else {
            link.classList.remove("text-indigo-400", "font-semibold", "bg-white/10");
            link.classList.add("text-slate-300");
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach((section) => observer.observe(section));
}

/**
 * --------------------------------------------------------------------------
 * 6. STICKY NAVBAR ELEVATION
 * Elevates navbar with intensified glass backdrop blur when scrolled.
 * --------------------------------------------------------------------------
 */
function initNavbarScroll() {
  const navbar = document.getElementById("main-nav");
  if (!navbar) return;

  let ticking = false;

  const handleScroll = () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        if (window.scrollY > 25) {
          navbar.classList.add("scrolled");
        } else {
          navbar.classList.remove("scrolled");
        }
        ticking = false;
      });
      ticking = true;
    }
  };

  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll();
}

/**
 * --------------------------------------------------------------------------
 * 7. MOBILE HAMBURGER MENU WITH SMOOTH BACKDROP BLUR
 * --------------------------------------------------------------------------
 */
function initMobileMenu() {
  const menuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  const mobileLinks = document.querySelectorAll(".mobile-nav-link");

  if (!menuBtn || !mobileMenu) return;

  const toggleMenu = () => {
    const isExpanded = menuBtn.getAttribute("aria-expanded") === "true";
    const newState = !isExpanded;

    menuBtn.setAttribute("aria-expanded", String(newState));
    mobileMenu.classList.toggle("hidden");

    const icon = menuBtn.querySelector("i");
    if (icon) {
      if (newState) {
        icon.classList.remove("fa-bars");
        icon.classList.add("fa-xmark");
      } else {
        icon.classList.remove("fa-xmark");
        icon.classList.add("fa-bars");
      }
    }
  };

  menuBtn.addEventListener("click", toggleMenu);

  mobileLinks.forEach((link) => {
    link.addEventListener("click", () => {
      if (!mobileMenu.classList.contains("hidden")) {
        toggleMenu();
      }
    });
  });

  document.addEventListener("click", (e) => {
    if (
      !mobileMenu.classList.contains("hidden") &&
      !mobileMenu.contains(e.target) &&
      !menuBtn.contains(e.target)
    ) {
      toggleMenu();
    }
  });
}

/**
 * --------------------------------------------------------------------------
 * 8. ONE-CLICK EMAIL CLIPBOARD WITH GLASS TOAST
 * --------------------------------------------------------------------------
 */
function initCopyEmail() {
  const copyBtns = document.querySelectorAll(".copy-email-btn");
  if (!copyBtns.length) return;

  copyBtns.forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const email = btn.getAttribute("data-email") || "akashgowdan2006@gmail.com";

      try {
        await navigator.clipboard.writeText(email);
        showToast(`Copied to clipboard: ${email}`);
      } catch (err) {
        const textarea = document.createElement("textarea");
        textarea.value = email;
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();
        try {
          document.execCommand("copy");
          showToast(`Copied to clipboard: ${email}`);
        } catch (fallbackErr) {
          showToast(`Email: ${email}`);
        }
        document.body.removeChild(textarea);
      }
    });
  });
}

/**
 * --------------------------------------------------------------------------
 * 9. FLOATING BACK-TO-TOP BUTTON
 * --------------------------------------------------------------------------
 */
function initBackToTop() {
  const bttBtn = document.getElementById("back-to-top");
  if (!bttBtn) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 450) {
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
 * --------------------------------------------------------------------------
 * 10. SMOOTH ANCHOR SCROLLING WITH OFFSET
 * --------------------------------------------------------------------------
 */
function initSmoothAnchorScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#" || targetId === "") return;

      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        const navHeight = 72;
        const elementPosition = targetEl.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - navHeight;

        window.scrollTo({
          top: offsetPosition,
          behavior: "smooth"
        });
      }
    });
  });
}

/**
 * Developer console greeting
 */
function printConsoleBanner() {
  const styles = [
    "color: #38bdf8",
    "font-size: 13px",
    "font-family: monospace",
    "font-weight: 700",
    "padding: 8px 12px",
    "background: #0f172a",
    "border-radius: 8px",
    "border: 1px solid #1e293b"
  ].join(";");

  console.log("%c⚡ Akash N | Projects Showcase Engine Active.", styles);
  console.log("%cGitHub: https://github.com/Akash04092006", "color: #94a3b8; font-size: 11px;");
}
