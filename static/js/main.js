/**
 * Modular High-End Personal Portfolio - Main Frontend Script (Part 4)
 * Asynchronous Contact API Handling, Interactive CLI Terminal Modal,
 * Category Filtering, Live Clock, Spotlight Engine & UI Utilities.
 */

document.addEventListener("DOMContentLoaded", () => {
  initContactForm();
  initCliTerminalModal();
  initLiveClock();
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
 * 1. ASYNCHRONOUS CONTACT FORM HANDLING (PART 4)
 * Submits inquiries via fetch() to /api/contact with validation and feedback.
 * --------------------------------------------------------------------------
 */
function initContactForm() {
  const contactForm = document.getElementById("contact-form");
  const submitBtn = document.getElementById("contact-submit-btn");

  if (!contactForm || !submitBtn) return;

  contactForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = (document.getElementById("contact-name")?.value || "").trim();
    const email = (document.getElementById("contact-email")?.value || "").trim();
    const subject = (document.getElementById("contact-subject")?.value || "").trim();
    const message = (document.getElementById("contact-message")?.value || "").trim();

    // Client-side quick check
    if (!name || !email || !subject || !message) {
      showToast("Please fill in all required fields.");
      return;
    }

    const emailRegex = /^[\w\.-]+@[\w\.-]+\.\w{2,}$/;
    if (!emailRegex.test(email)) {
      showToast("Please enter a valid email address.");
      return;
    }

    // Set Loading State
    const originalBtnHtml = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <i class="fa-solid fa-circle-notch fa-spin text-sm"></i>
      <span>Transmitting Message...</span>
    `;

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({ name, email, subject, message })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showToast(data.message || "Message transmitted successfully! Expect a reply within 24h.");
        contactForm.reset();
      } else {
        showToast(data.error || "Submission error. Please try again.");
      }
    } catch (err) {
      console.error("Contact Form Fetch Error:", err);
      showToast("Network anomaly. Please contact via direct email.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnHtml;
    }
  });
}

/**
 * --------------------------------------------------------------------------
 * 2. INTERACTIVE CLI COMMAND TERMINAL MODAL (PART 4)
 * Key-bound (Ctrl + K) client-side interactive shell.
 * --------------------------------------------------------------------------
 */
function initCliTerminalModal() {
  const modal = document.getElementById("cli-modal");
  const openBtns = document.querySelectorAll(".open-cli-modal-btn");
  const closeBtn = document.getElementById("close-cli-modal-btn");
  const cliInput = document.getElementById("cli-command-input");
  const cliHistory = document.getElementById("cli-history-output");

  if (!modal || !cliInput || !cliHistory) return;

  const commandLog = [];
  let logPointer = -1;

  // Open / Close Controls
  const openModal = () => {
    modal.classList.add("open");
    document.body.style.overflow = "hidden";
    setTimeout(() => cliInput.focus(), 80);
  };

  const closeModal = () => {
    modal.classList.remove("open");
    document.body.style.overflow = "";
    cliInput.blur();
  };

  openBtns.forEach((btn) => btn.addEventListener("click", openModal));
  if (closeBtn) closeBtn.addEventListener("click", closeModal);

  // Close on backdrop click
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  // Global Keyboard Shortcuts (Ctrl + K or Cmd + K, Esc to close)
  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (modal.classList.contains("open")) {
        closeModal();
      } else {
        openModal();
      }
    } else if (e.key === "Escape" && modal.classList.contains("open")) {
      closeModal();
    }
  });

  // Available Terminal Commands
  const commands = {
    help: () => `
<div class="text-indigo-300 font-semibold mb-1">Available System Commands:</div>
<div class="grid grid-cols-2 gap-x-4 gap-y-1 text-slate-300">
  <div><span class="text-cyan-400 font-bold">about</span> - Background & engineering summary</div>
  <div><span class="text-cyan-400 font-bold">projects</span> - Shipped systems & live deployments</div>
  <div><span class="text-cyan-400 font-bold">skills</span> - Core languages & architecture stack</div>
  <div><span class="text-cyan-400 font-bold">hackathons</span> - Major achievements & research</div>
  <div><span class="text-cyan-400 font-bold">contact</span> - Direct communication coordinates</div>
  <div><span class="text-cyan-400 font-bold">clear</span> - Flush terminal view output</div>
  <div><span class="text-cyan-400 font-bold">exit</span> - Terminate CLI session & close modal</div>
</div>`,

    about: () => `
<div class="text-slate-300 space-y-1">
  <div class="text-white font-bold">Akash N | Full-Stack Systems Engineer & AI Developer</div>
  <p class="text-slate-400">Location: Bengaluru, India | Status: Available for Projects & Hackathons</p>
  <p>Passionate about low-latency distributed platforms, microservices, and glassmorphic UI architectures.</p>
</div>`,

    projects: () => `
<div class="text-slate-300 space-y-1.5">
  <div><span class="text-emerald-400 font-bold">• EchoRoute</span> - Urban acoustic noise-aware navigation (<a href="https://github.com/Akash04092006/echoroute" target="_blank" class="text-cyan-400 underline">GitHub</a>)</div>
  <div><span class="text-emerald-400 font-bold">• NexusPulse</span> - 50k metrics/sec distributed telemetry engine (<a href="https://github.com/Akash04092006/nexus-pulse" target="_blank" class="text-cyan-400 underline">GitHub</a>)</div>
  <div><span class="text-emerald-400 font-bold">• OmniScribe AI</span> - Multi-agent enterprise RAG platform (<a href="https://github.com/Akash04092006/omniscribe-ai" target="_blank" class="text-cyan-400 underline">GitHub</a>)</div>
  <div><span class="text-emerald-400 font-bold">• AuraPay</span> - Idempotent cryptographic ledger gateway (<a href="https://github.com/Akash04092006/aurapay-ledger" target="_blank" class="text-cyan-400 underline">GitHub</a>)</div>
</div>`,

    skills: () => `
<div class="text-slate-300 space-y-1">
  <div><span class="text-indigo-400 font-bold">Languages:</span> Python, JavaScript (ES6+), C / C++, SQL, Go</div>
  <div><span class="text-indigo-400 font-bold">Backend & AI:</span> Flask, FastAPI, PyTorch, LangChain, Celery, Redis</div>
  <div><span class="text-indigo-400 font-bold">Frontend:</span> Tailwind CSS, Jinja2, HTML5 Glassmorphism, WebSockets</div>
  <div><span class="text-indigo-400 font-bold">Cloud & DevOps:</span> Docker, Kubernetes, Vercel, Prometheus, Git</div>
</div>`,

    hackathons: () => `
<div class="text-slate-300 space-y-1">
  <div><span class="text-amber-400 font-bold">🏆 NITK Build for Billions</span> - Top 50 Finalist (300+ entries)</div>
  <div><span class="text-amber-400 font-bold">⚡ TEAM ASTRA Hackathon</span> - Project Lead & Lead Architect (EchoRoute)</div>
  <div><span class="text-amber-400 font-bold">📄 Explainable AI Paper</span> - Research published in adolescent screen addiction ML</div>
  <div><span class="text-amber-400 font-bold">🤖 Robofiesta @ RVITM</span> - Smart agriculture & warehouse inventory prototype</div>
</div>`,

    contact: () => `
<div class="text-slate-300 space-y-1">
  <div><span class="text-cyan-400 font-bold">Email:</span> akashgowdan2006@gmail.com</div>
  <div><span class="text-cyan-400 font-bold">GitHub:</span> <a href="https://github.com/Akash04092006" target="_blank" class="underline">https://github.com/Akash04092006</a></div>
  <div><span class="text-cyan-400 font-bold">LinkedIn:</span> <a href="https://linkedin.com/in/akash-n" target="_blank" class="underline">https://linkedin.com/in/akash-n</a></div>
  <div><span class="text-cyan-400 font-bold">WhatsApp:</span> <a href="https://wa.me/919876543210" target="_blank" class="underline">+91 98765 43210</a></div>
</div>`,

    clear: () => {
      cliHistory.innerHTML = "";
      return "";
    },

    exit: () => {
      closeModal();
      return "Session terminated.";
    }
  };

  // Command Execution Handler
  cliInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const rawInput = cliInput.value.trim();
      cliInput.value = "";
      if (!rawInput) return;

      commandLog.push(rawInput);
      logPointer = commandLog.length;

      const normalized = rawInput.toLowerCase();
      let outputHtml = "";

      if (commands[normalized]) {
        outputHtml = commands[normalized]();
      } else {
        outputHtml = `<span class="text-rose-400">Command not found: '${rawInput}'. Type <span class="text-cyan-300 font-bold">'help'</span> to inspect available directives.</span>`;
      }

      if (normalized !== "clear") {
        const entry = document.createElement("div");
        entry.className = "mb-3";
        entry.innerHTML = `
          <div class="flex items-center gap-2 text-xs text-slate-500 mb-1">
            <span class="text-emerald-400 font-bold">akash@core:~$</span>
            <span class="text-slate-200">${rawInput}</span>
          </div>
          <div class="pl-3 border-l-2 border-indigo-500/30 text-xs">${outputHtml}</div>
        `;
        cliHistory.appendChild(entry);
        cliHistory.scrollTop = cliHistory.scrollHeight;
      }
    } else if (e.key === "ArrowUp") {
      if (logPointer > 0) {
        logPointer--;
        cliInput.value = commandLog[logPointer] || "";
      }
    } else if (e.key === "ArrowDown") {
      if (logPointer < commandLog.length - 1) {
        logPointer++;
        cliInput.value = commandLog[logPointer] || "";
      } else {
        logPointer = commandLog.length;
        cliInput.value = "";
      }
    }
  });
}

/**
 * --------------------------------------------------------------------------
 * 3. LIVE FOOTER CLOCK (PART 4)
 * Displays live synchronized timestamp with IST time zone badge.
 * --------------------------------------------------------------------------
 */
function initLiveClock() {
  const clockEl = document.getElementById("footer-live-clock");
  if (!clockEl) return;

  const updateClock = () => {
    const now = new Date();
    // Format in IST (UTC+5:30)
    const options = {
      timeZone: "Asia/Kolkata",
      hour12: true,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit"
    };
    const timeStr = now.toLocaleTimeString("en-US", options);
    clockEl.textContent = `IST (UTC+5:30) • ${timeStr}`;
  };

  updateClock();
  setInterval(updateClock, 1000);
}

/**
 * --------------------------------------------------------------------------
 * 4. DYNAMIC PROJECTS CATEGORY FILTERING (PART 3)
 * --------------------------------------------------------------------------
 */
function initProjectCategoryFilter() {
  const filterTabs = document.querySelectorAll(".filter-tab");
  const projectCards = document.querySelectorAll(".project-card");
  const emptyState = document.getElementById("projects-empty-state");

  if (!filterTabs.length || !projectCards.length) return;

  filterTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      filterTabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      const selectedFilter = tab.getAttribute("data-filter") || "all";
      let matchCount = 0;

      projectCards.forEach((card) => {
        const cardCategory = card.getAttribute("data-category");

        if (selectedFilter === "all" || cardCategory === selectedFilter) {
          card.classList.remove("hidden");
          card.classList.remove("project-filter-animate");
          void card.offsetWidth;
          card.classList.add("project-filter-animate");
          matchCount++;
        } else {
          card.classList.add("hidden");
          card.classList.remove("project-filter-animate");
        }
      });

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
 * 5. COPY REPOSITORY URL TO CLIPBOARD (PART 3)
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
 * 6. GLOBAL GLASS TOAST NOTIFICATION UTILITY
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
 * 7. INTERACTIVE CURSOR SPOTLIGHT ENGINE
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
 * 8. ACTIVE NAVIGATION SCROLL-SPY
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
 * 9. STICKY NAVBAR ELEVATION
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
 * 10. MOBILE HAMBURGER MENU
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
 * 11. ONE-CLICK EMAIL CLIPBOARD
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
 * 12. FLOATING BACK-TO-TOP BUTTON
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
 * 13. SMOOTH ANCHOR SCROLLING WITH OFFSET
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

  console.log("%c⚡ Akash N | Glassmorphism Portfolio & Contact API Active.", styles);
  console.log("%cPress Ctrl + K anywhere to trigger the interactive CLI shell.", "color: #a5b4fc; font-size: 11px;");
}
