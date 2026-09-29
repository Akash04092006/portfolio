"""
Main application backend for the modular high-end personal portfolio.
Designed for seamless local execution and instant serverless deployment on Vercel.
"""

import os
import re
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("portfolio")

# -----------------------------------------------------------------------------
# FLASK APP INITIALIZATION
# -----------------------------------------------------------------------------
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "akash-portfolio-secret-key-2026")

# -----------------------------------------------------------------------------
# DYNAMIC PORTFOLIO DATA CONFIGURATIONS
# Plug-and-play architecture: modify or append dictionaries to update the UI
# -----------------------------------------------------------------------------

PERSONAL_INFO = {
    "name": "Akash N",
    "role": "Full-Stack Engineer & AI Systems Developer",
    "tagline": "Building scalable distributed web applications, high-performance backends, and elegant human-centric digital experiences.",
    "short_bio": (
        "Passionate software engineer focused on crafting robust cloud platforms, intelligent "
        "microservices, and pixel-perfect interactive web interfaces. Driven by deep technical curiosity, "
        "athletic discipline, and continuous iteration."
    ),
    "location": "Bengaluru, India",
    "availability": "Available for Projects & Hackathons",
    "status_indicator": "Available for Projects & Hackathons",
    "email": "akashgowdan2006@gmail.com",
    "phone": "+91 98765 43210",
    "social": {
        "github": "https://github.com/Akash04092006",
        "linkedin": "https://linkedin.com/in/akash-n",
        "instagram": "https://instagram.com/akash_n",
        "twitter": "https://x.com/akash_n",
        "whatsapp": "https://wa.me/919876543210",
    },
    "quick_stats": [
        {"label": "Years Experience", "value": "3+"},
        {"label": "Projects Shipped", "value": "20+"},
        {"label": "Hackathon Wins", "value": "4x"},
        {"label": "Code Commits", "value": "1.5k+"},
    ]
}

LIFESTYLE_CARDS = [
    {
        "id": "volleyball",
        "title": "Volleyball",
        "category": "Athletics & Teamwork",
        "tagline": "Explosive Agility, On-Court Synergy & Tactical Focus",
        "description": (
            "Competitive spiker and court strategist. Playing high-intensity volleyball sharpens "
            "split-second decision making, spatial awareness, and synchronous communication under pressure."
        ),
        "icon": "fa-solid fa-volleyball",
        "accent_gradient": "from-amber-500/20 via-orange-500/10 to-transparent",
        "accent_border": "border-amber-500/30 hover:border-amber-400/60",
        "badge_color": "bg-amber-500/10 text-amber-300 border-amber-500/20",
        "stat_pill": "Competitive Spiker",
        "image_placeholder": "https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "gym",
        "title": "Gym & Strength",
        "category": "Discipline & Fitness",
        "tagline": "Progressive Overload, Mental Grit & Physical Conditioning",
        "description": (
            "Consistent daily resistance training and conditioning. Approaching strength and stamina "
            "with the exact same mindset as systems engineering: measured inputs, systematic recovery, and compounding gains."
        ),
        "icon": "fa-solid fa-dumbbell",
        "accent_gradient": "from-rose-500/20 via-red-500/10 to-transparent",
        "accent_border": "border-rose-500/30 hover:border-rose-400/60",
        "badge_color": "bg-rose-500/10 text-rose-300 border-rose-500/20",
        "stat_pill": "5-6 Days / Week",
        "image_placeholder": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "studying",
        "title": "Deep Learning",
        "category": "Intellectual Mastery",
        "tagline": "Systems Theory, Algorithms & Architectural Research",
        "description": (
            "Immersing in distributed architectures, database internals, compiler principles, and modern "
            "generative AI models. Relentless curiosity transforms theoretical foundations into real-world engineering power."
        ),
        "icon": "fa-solid fa-book-open-reader",
        "accent_gradient": "from-sky-500/20 via-blue-500/10 to-transparent",
        "accent_border": "border-sky-500/30 hover:border-sky-400/60",
        "badge_color": "bg-sky-500/10 text-sky-300 border-sky-500/20",
        "stat_pill": "Continuous Learner",
        "image_placeholder": "https://images.unsplash.com/photo-1532012164546-f432f2e3777f?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "coding",
        "title": "Software Engineering",
        "category": "Code Craftsmanship",
        "tagline": "High-Performance Backends, Cloud Services & Polished UI",
        "description": (
            "Designing and writing maintainable, tested, production-grade code. Obsessed with clean abstractions, "
            "sub-millisecond latency, robust developer tooling, and mesmerizing glassmorphic UI aesthetics."
        ),
        "icon": "fa-solid fa-code",
        "accent_gradient": "from-emerald-500/20 via-teal-500/10 to-transparent",
        "accent_border": "border-emerald-500/30 hover:border-emerald-400/60",
        "badge_color": "bg-emerald-500/10 text-emerald-300 border-emerald-500/20",
        "stat_pill": "1,500+ Commits",
        "image_placeholder": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80"
    }
]

PROJECTS = [
    {
        "id": "echoroute",
        "title": "EchoRoute - Noise-Aware Navigation",
        "category": "ai-ml",
        "category_label": "AI & Data Science",
        "tagline": "Acoustic telemetry and urban noise-minimized routing algorithm",
        "description": (
            "Traditional GPS systems optimize solely for transit time, ignoring auditory pollution and urban stress. "
            "EchoRoute processes geospatial acoustic sensor streams using graph neural networks to compute quietest "
            "walking and cycling pathways. Deployed with sub-second path recalculation and live noise heatmaps."
        ),
        "tech_stack": ["Python", "FastAPI", "PyTorch", "Leaflet", "Tailwind CSS", "GeoPandas"],
        "tags": ["Python", "FastAPI", "PyTorch", "Leaflet", "Tailwind CSS", "GeoPandas"],
        "metrics": "94% Acoustic Accuracy",
        "metric": "94% Acoustic Accuracy",
        "github_url": "https://github.com/Akash04092006/echoroute",
        "github_link": "https://github.com/Akash04092006/echoroute",
        "demo_url": "https://echoroute.vercel.app",
        "live_link": "https://echoroute.vercel.app",
        "featured": True,
        "stars": "184",
        "icon": "fa-solid fa-route"
    },
    {
        "id": "nexus-pulse",
        "title": "NexusPulse - Telemetry Engine",
        "category": "systems",
        "category_label": "Systems & C",
        "tagline": "High-throughput distributed metrics ingestion and time-series aggregation",
        "description": (
            "Built to eliminate observability bottlenecks during high-throughput traffic spikes across microservices. "
            "Implements a zero-copy ring buffer with Kafka pipelining and Redis memory caching to ingest over 50,000 "
            "metrics per second. Delivers real-time anomaly alerts with sub-18ms p99 latency."
        ),
        "tech_stack": ["C / C++", "Python", "Kafka", "Redis", "Flask", "Docker"],
        "tags": ["C / C++", "Python", "Kafka", "Redis", "Flask", "Docker"],
        "metrics": "< 18ms p99 Latency",
        "metric": "< 18ms p99 Latency",
        "github_url": "https://github.com/Akash04092006/nexus-pulse",
        "github_link": "https://github.com/Akash04092006/nexus-pulse",
        "demo_url": "https://nexus-pulse.vercel.app",
        "live_link": "https://nexus-pulse.vercel.app",
        "featured": True,
        "stars": "142",
        "icon": "fa-solid fa-chart-line"
    },
    {
        "id": "omni-scribe-ai",
        "title": "OmniScribe AI - Document Intelligence",
        "category": "ai-ml",
        "category_label": "AI & Data Science",
        "tagline": "Enterprise multi-agent RAG engine for technical document synthesis",
        "description": (
            "Solves knowledge silos in complex enterprise codebases and regulatory filings. Couples hybrid "
            "vector-lexical search with autonomous verification agents that cross-examine retrieved citations "
            "before synthesis. Drastically reduces hallucination rates while indexing 100k+ documents."
        ),
        "tech_stack": ["Python", "LangChain", "Qdrant", "FastAPI", "Next.js", "Tailwind CSS"],
        "tags": ["Python", "LangChain", "Qdrant", "FastAPI", "Next.js", "Tailwind CSS"],
        "metrics": "100k+ Docs Indexed",
        "metric": "100k+ Docs Indexed",
        "github_url": "https://github.com/Akash04092006/omniscribe-ai",
        "github_link": "https://github.com/Akash04092006/omniscribe-ai",
        "demo_url": "https://omniscribe-ai.vercel.app",
        "live_link": "https://omniscribe-ai.vercel.app",
        "featured": True,
        "stars": "218",
        "icon": "fa-solid fa-brain"
    },
    {
        "id": "aurapay-ledger",
        "title": "AuraPay - Resilient Ledger Gateway",
        "category": "web-dev",
        "category_label": "Full Stack Web",
        "tagline": "Idempotent financial settlement gateway with automated reconciliation",
        "description": (
            "Engineered to prevent ledger drift in distributed micro-transaction ecosystems. Implements cryptographic "
            "audit trails, strict double-entry ledgering, and Celery background workers with automatic dead-letter "
            "queue recovery. Reconciles high-concurrency payment webhooks seamlessly."
        ),
        "tech_stack": ["Python", "Flask", "PostgreSQL", "Celery", "Tailwind CSS", "Redis"],
        "tags": ["Python", "Flask", "PostgreSQL", "Celery", "Tailwind CSS", "Redis"],
        "metrics": "Zero Drift Reconciliation",
        "metric": "Zero Drift Reconciliation",
        "github_url": "https://github.com/Akash04092006/aurapay-ledger",
        "github_link": "https://github.com/Akash04092006/aurapay-ledger",
        "demo_url": "https://aurapay.vercel.app",
        "live_link": "https://aurapay.vercel.app",
        "featured": False,
        "stars": "89",
        "icon": "fa-solid fa-shield-halved"
    },
    {
        "id": "cloud-vantage",
        "title": "CloudVantage - K8s Cost Optimizer",
        "category": "systems",
        "category_label": "Systems & C",
        "tagline": "Autonomous Kubernetes resource rightsizing daemon for cloud clusters",
        "description": (
            "Overprovisioned cloud workloads inflate cloud bills by billions annually. CloudVantage continuously "
            "monitors Prometheus pod telemetry, predicts workload peaks with time-series forecasting, and dynamically "
            "patches CPU and memory limits, reducing compute expenditure by 34%."
        ),
        "tech_stack": ["Go", "C", "Kubernetes", "Prometheus", "Python", "GraphQL"],
        "tags": ["Go", "C", "Kubernetes", "Prometheus", "Python", "GraphQL"],
        "metrics": "34% Cost Reduction",
        "metric": "34% Cost Reduction",
        "github_url": "https://github.com/Akash04092006/cloud-vantage",
        "github_link": "https://github.com/Akash04092006/cloud-vantage",
        "demo_url": "https://cloudvantage.vercel.app",
        "live_link": "https://cloudvantage.vercel.app",
        "featured": False,
        "stars": "310",
        "icon": "fa-solid fa-server"
    },
    {
        "id": "devlens-profiler",
        "title": "DevLens - Web Performance Profiler",
        "category": "web-dev",
        "category_label": "Full Stack Web",
        "tagline": "Full-stack browser DOM auditing & Core Web Vitals telemetry platform",
        "description": (
            "Developed to automate frontend performance regression detection during continuous delivery pipelines. "
            "Analyzes script execution bottlenecks, layout shifts, and WCAG accessibility standards in headless "
            "browser instances with interactive glassmorphic visual timelines."
        ),
        "tech_stack": ["Python", "Flask", "JavaScript", "Puppeteer", "Tailwind CSS", "Chart.js"],
        "tags": ["Python", "Flask", "JavaScript", "Puppeteer", "Tailwind CSS", "Chart.js"],
        "metrics": "Hackathon Winner",
        "metric": "Hackathon Winner",
        "github_url": "https://github.com/Akash04092006/devlens-profiler",
        "github_link": "https://github.com/Akash04092006/devlens-profiler",
        "demo_url": "https://devlens.vercel.app",
        "live_link": "https://devlens.vercel.app",
        "featured": False,
        "stars": "165",
        "icon": "fa-solid fa-gauge-high"
    }
]

HACKATHONS = [
    {
        "id": "nitk-build-for-billions",
        "event_name": "NITK Build for Billions Hackathon",
        "role_badge": "Selected Finalist",
        "badge_color": "bg-emerald-500/10 text-emerald-300 border-emerald-500/30",
        "date": "January 2026",
        "location": "NITK Surathkal, India",
        "highlight": "Top 50 / 300+ National Teams",
        "description": (
            "Selected in the Top 50 engineering teams out of 300+ nationwide entries. Architected a decentralized "
            "offline-first emergency supply chain mesh network with WebSockets and edge SQLite synchronization."
        ),
        "tech_tags": ["Python", "Decentralized Mesh", "FastAPI", "WebSockets"],
        "link": "https://github.com/Akash04092006",
        "icon": "fa-solid fa-trophy"
    },
    {
        "id": "team-astra-echoroute",
        "event_name": "EchoRoute - TEAM ASTRA Hackathon",
        "role_badge": "Team Lead",
        "badge_color": "bg-cyan-500/10 text-cyan-300 border-cyan-500/30",
        "date": "October 2025",
        "location": "Bengaluru, India",
        "highlight": "Lead Architect & Project Lead",
        "description": (
            "Served as project lead and primary systems architect for EchoRoute, an acoustic telemetry and urban noise-aware "
            "navigation platform. Coordinated a 4-person team to deliver geospatial ML path computation under 36-hour sprint constraints."
        ),
        "tech_tags": ["FastAPI", "PyTorch", "Graph Neural Networks", "Leaflet"],
        "link": "https://github.com/Akash04092006/echoroute",
        "icon": "fa-solid fa-route"
    },
    {
        "id": "xai-gaming-research",
        "event_name": "Explainable AI Gaming Addiction Research Paper",
        "role_badge": "Research Published",
        "badge_color": "bg-purple-500/10 text-purple-300 border-purple-500/30",
        "date": "August 2025",
        "location": "Peer-Reviewed Publication",
        "highlight": "XAI Interpretability Study",
        "description": (
            "Authored and evaluated machine learning predictive models exploring adolescent screen behaviors and gaming vulnerability. "
            "Applied SHAP (Shapley Additive Explanations) and LIME surrogate trees to demystify complex neural decisions for clinical practitioners."
        ),
        "tech_tags": ["Python", "Scikit-Learn", "SHAP", "XAI", "Pandas"],
        "link": "https://github.com/Akash04092006",
        "icon": "fa-solid fa-newspaper"
    },
    {
        "id": "robofiesta-rvitm",
        "event_name": "Robofiesta Hackathon @ RVITM",
        "role_badge": "Participant",
        "badge_color": "bg-amber-500/10 text-amber-300 border-amber-500/30",
        "date": "March 2025",
        "location": "RVITM Bengaluru, India",
        "highlight": "Agri-Tech Prototype",
        "description": (
            "Engineered a connected smart agri-marketplace and automated warehouse inventory allocation engine. "
            "Integrated sensor data with localized crop market analytics to optimize post-harvest storage efficiency."
        ),
        "tech_tags": ["IoT", "Flask", "SQLite", "Tailwind CSS"],
        "link": "https://github.com/Akash04092006",
        "icon": "fa-solid fa-robot"
    }
]

# In-memory storage for logged contact submissions
CONTACT_INQUIRIES = []

# -----------------------------------------------------------------------------
# APPLICATION ROUTES & CONTROLLERS
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    """Renders the main high-end portfolio landing page with all contextual data."""
    return render_template(
        "index.html",
        personal_info=PERSONAL_INFO,
        lifestyle_cards=LIFESTYLE_CARDS,
        projects=PROJECTS,
        hackathons=HACKATHONS,
        current_year=datetime.now().year
    )

@app.route("/api/contact", methods=["POST"])
def contact_api():
    """
    Asynchronous contact endpoint handling JSON and form payloads.
    Performs server-side validation and logs inquiries with structured timestamps.
    """
    # Accept both JSON payloads and standard multipart/urlencoded form data
    if request.is_json:
        payload = request.get_json() or {}
    else:
        payload = request.form.to_dict() or {}

    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip()
    subject = payload.get("subject", "").strip()
    message = payload.get("message", "").strip()

    # Server-Side Validation: Check required fields
    if not name or not email or not subject or not message:
        logger.warning(f"Contact submission rejected: missing required fields. Payload: {payload}")
        return jsonify({
            "success": False,
            "error": "All fields (Name, Email, Subject, Message) are strictly required."
        }), 400

    # Server-Side Validation: Email format check
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not re.match(email_regex, email):
        logger.warning(f"Contact submission rejected: invalid email format: {email}")
        return jsonify({
            "success": False,
            "error": "Please provide a valid, well-formed email address."
        }), 400

    # Structured inquiry record
    inquiry_record = {
        "timestamp": datetime.utcnow().isoformat(),
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "ip_address": request.headers.get("X-Forwarded-For", request.remote_addr)
    }

    CONTACT_INQUIRIES.append(inquiry_record)
    logger.info(f"Incoming Contact Inquiry [{inquiry_record['timestamp']}]: From='{name}' <{email}> Subject='{subject}'")

    return jsonify({
        "success": True,
        "message": f"Transmission received, {name}! Your message has been routed to Akash N. Expect a response within 24 hours.",
        "inquiry_id": f"INQ-{len(CONTACT_INQUIRIES):04d}",
        "timestamp": inquiry_record["timestamp"]
    }), 200

@app.route("/health")
def health_check():
    """Lightweight health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "portfolio-backend",
        "inquiries_received": len(CONTACT_INQUIRIES),
        "timestamp": datetime.utcnow().isoformat()
    }, 200

# -----------------------------------------------------------------------------
# ERROR HANDLERS (404, 500)
# -----------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):
    """User-friendly glassmorphic 404 Not Found view."""
    return render_template(
        "404.html",
        personal_info=PERSONAL_INFO,
        current_year=datetime.now().year,
        error_title="Page Not Found",
        error_message="The coordinate or page you requested does not exist in this sector."
    ), 404

@app.errorhandler(500)
def internal_server_error(error):
    """User-friendly glassmorphic 500 Internal Server Error view."""
    return render_template(
        "500.html",
        personal_info=PERSONAL_INFO,
        current_year=datetime.now().year,
        error_title="Internal System Anomaly",
        error_message="An unexpected condition was encountered. Our monitoring agents have been notified."
    ), 500

# -----------------------------------------------------------------------------
# ENTRY POINT FOR LOCAL DEVELOPMENT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
