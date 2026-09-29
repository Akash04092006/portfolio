"""
Main application backend for the modular high-end personal portfolio.
Designed for seamless local execution and instant serverless deployment on Vercel.
"""

import os
import re
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Load local environment variables if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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

# -----------------------------------------------------------------------------
# SKILLS & TECHNICAL ARSENAL DATA (PART 5)
# 5 Categorized Domains: Languages, Frameworks, AI/Data, Tools/DevOps, Systems
# -----------------------------------------------------------------------------

SKILLS = {
    "languages": [
        {
            "id": "c",
            "name": "C",
            "category": "languages",
            "category_label": "Languages",
            "proficiency": 88,
            "badge": "Advanced",
            "badge_color": "bg-sky-500/10 text-sky-300 border-sky-500/25",
            "icon": "fa-solid fa-c",
            "icon_color": "text-sky-400",
            "tagline": "Pointers, dynamic heap allocation, and POSIX concurrency",
            "projects": ["NexusPulse Buffer Engine", "LPC2148 Peripheral Drivers"],
            "concepts": ["Memory Layout & Struct Padding", "Pointers & Function Pointers", "Ring Buffers", "POSIX Threads"]
        },
        {
            "id": "cpp",
            "name": "C++",
            "category": "languages",
            "category_label": "Languages",
            "proficiency": 85,
            "badge": "Advanced",
            "badge_color": "bg-blue-500/10 text-blue-300 border-blue-500/25",
            "icon": "fa-solid fa-code",
            "icon_color": "text-blue-400",
            "tagline": "Modern OOP, STL containers, templates, and high-speed algorithms",
            "projects": ["NexusPulse Ingestion Core", "Graph Algorithms Solver"],
            "concepts": ["RAII & Smart Pointers", "STL Iterators & Maps", "Templates & Metaprogramming", "Competitive Problem Solving"]
        },
        {
            "id": "python",
            "name": "Python",
            "category": "languages",
            "category_label": "Languages",
            "proficiency": 95,
            "badge": "Expert",
            "badge_color": "bg-emerald-500/10 text-emerald-300 border-emerald-500/25",
            "icon": "fa-brands fa-python",
            "icon_color": "text-emerald-400",
            "tagline": "Backend microservices, asynchronous I/O, ML pipelines & scripting",
            "projects": ["EchoRoute Navigation Engine", "OmniScribe AI", "AuraPay Gateway"],
            "concepts": ["Decorators & Generators", "Asyncio Event Loops", "Metaclasses & Typing", "PyTest & Performance Profiling"]
        },
        {
            "id": "java",
            "name": "Java",
            "category": "languages",
            "category_label": "Languages",
            "proficiency": 82,
            "badge": "Proficient",
            "badge_color": "bg-amber-500/10 text-amber-300 border-amber-500/25",
            "icon": "fa-brands fa-java",
            "icon_color": "text-amber-400",
            "tagline": "Enterprise OOP architecture, JVM garbage collection & collections",
            "projects": ["Distributed Banking Simulator", "Multi-Threaded Queue Service"],
            "concepts": ["JVM Internals & GC", "Multithreading & Synchronization", "Generics & Collections", "Clean Architecture"]
        },
        {
            "id": "javascript",
            "name": "JavaScript (ES6+)",
            "category": "languages",
            "category_label": "Languages",
            "proficiency": 90,
            "badge": "Advanced",
            "badge_color": "bg-yellow-500/10 text-yellow-300 border-yellow-500/25",
            "icon": "fa-brands fa-js",
            "icon_color": "text-yellow-400",
            "tagline": "Event loops, asynchronous promises, DOM manipulation & modern web",
            "projects": ["Interactive Portfolio Engine", "DevLens Web Profiler UI"],
            "concepts": ["Closures & Prototypes", "Async/Await & Promises", "Intersection Observer API", "DOM Render Cycles"]
        },
        {
            "id": "html-css",
            "name": "HTML5 / CSS3",
            "category": "languages",
            "category_label": "Languages",
            "proficiency": 92,
            "badge": "Advanced",
            "badge_color": "bg-orange-500/10 text-orange-300 border-orange-500/25",
            "icon": "fa-brands fa-html5",
            "icon_color": "text-orange-400",
            "tagline": "Semantic layout, accessibility, hardware-accelerated animations & glassmorphism",
            "projects": ["Modular Portfolio Design", "DevLens Visual Dashboard"],
            "concepts": ["Semantic HTML5 Elements", "CSS Grid & Flexbox", "Backdrop Filters & Gradients", "WCAG AA Accessibility"]
        }
    ],

    "frameworks": [
        {
            "id": "flask",
            "name": "Flask",
            "category": "frameworks",
            "category_label": "Frameworks & Web",
            "proficiency": 94,
            "badge": "Advanced",
            "badge_color": "bg-indigo-500/10 text-indigo-300 border-indigo-500/25",
            "icon": "fa-solid fa-flask",
            "icon_color": "text-indigo-400",
            "tagline": "Lightweight WSGI routing, Jinja2 templating, blueprints & serverless Vercel runtime",
            "projects": ["Portfolio Web Platform", "AuraPay Microservices", "Robofiesta API"],
            "concepts": ["Application Factories", "Blueprints & Context Globals", "Jinja2 Macro Inheritance", "Vercel Serverless Wrappers"]
        },
        {
            "id": "fastapi",
            "name": "FastAPI",
            "category": "frameworks",
            "category_label": "Frameworks & Web",
            "proficiency": 90,
            "badge": "Advanced",
            "badge_color": "bg-teal-500/10 text-teal-300 border-teal-500/25",
            "icon": "fa-solid fa-bolt",
            "icon_color": "text-teal-400",
            "tagline": "Asynchronous high-throughput REST APIs with automatic OpenAPI & Pydantic typing",
            "projects": ["EchoRoute Routing Microservice", "OmniScribe Agent Server"],
            "concepts": ["Pydantic V2 Schemas", "Dependency Injection", "Async/Await Route Handlers", "OpenAPI Generation"]
        },
        {
            "id": "react",
            "name": "React",
            "category": "frameworks",
            "category_label": "Frameworks & Web",
            "proficiency": 84,
            "badge": "Proficient",
            "badge_color": "bg-cyan-500/10 text-cyan-300 border-cyan-500/25",
            "icon": "fa-brands fa-react",
            "icon_color": "text-cyan-400",
            "tagline": "Component lifecycle, functional hooks, state management & reactive rendering",
            "projects": ["OmniScribe Knowledge Console", "Interactive Map Explorer"],
            "concepts": ["Custom Hooks & useEffect", "Virtual DOM Reconciliation", "Context API", "Component Modularization"]
        },
        {
            "id": "nodejs",
            "name": "Node.js",
            "category": "frameworks",
            "category_label": "Frameworks & Web",
            "proficiency": 82,
            "badge": "Proficient",
            "badge_color": "bg-emerald-500/10 text-emerald-300 border-emerald-500/25",
            "icon": "fa-brands fa-node-js",
            "icon_color": "text-emerald-400",
            "tagline": "Non-blocking event-driven backend services and package scripting",
            "projects": ["DevLens Headless Runner", "Live WebSocket Hub"],
            "concepts": ["Event Loop Tick Phases", "Stream Buffers", "NPM Modules", "Child Processes"]
        },
        {
            "id": "express",
            "name": "Express",
            "category": "frameworks",
            "category_label": "Frameworks & Web",
            "proficiency": 80,
            "badge": "Proficient",
            "badge_color": "bg-slate-400/10 text-slate-300 border-slate-400/25",
            "icon": "fa-solid fa-server",
            "icon_color": "text-slate-300",
            "tagline": "Middleware pipelines, RESTful routing & microservice API gateways",
            "projects": ["Telemetry Relay Server", "DevLens Mock APIs"],
            "concepts": ["Middleware Chaining", "Route Parameter Binding", "Error Handling Handlers", "CORS & Security Headers"]
        },
        {
            "id": "tailwind",
            "name": "Tailwind CSS",
            "category": "frameworks",
            "category_label": "Frameworks & Web",
            "proficiency": 95,
            "badge": "Expert",
            "badge_color": "bg-cyan-500/10 text-cyan-300 border-cyan-500/25",
            "icon": "fa-solid fa-wind",
            "icon_color": "text-cyan-400",
            "tagline": "Utility-first modern styling, responsive breakpoints, custom theme config & dark mode",
            "projects": ["Portfolio Engine", "EchoRoute UI", "DevLens Profiler Dashboard"],
            "concepts": ["Custom Theme Extensions", "Dark Mode Classes", "Arbitrary Values & Filters", "JIT Engine Optimization"]
        },
        {
            "id": "bootstrap",
            "name": "Bootstrap",
            "category": "frameworks",
            "category_label": "Frameworks & Web",
            "proficiency": 85,
            "badge": "Proficient",
            "badge_color": "bg-purple-500/10 text-purple-300 border-purple-500/25",
            "icon": "fa-brands fa-bootstrap",
            "icon_color": "text-purple-400",
            "tagline": "Rapid prototype UI design, responsive grid systems & accessible components",
            "projects": ["Robofiesta Admin Console", "Hackathon Rapid Prototype"],
            "concepts": ["Grid Columns & Breakpoints", "Utility Classes", "Modal Components", "Form Controls"]
        }
    ],

    "ai_data": [
        {
            "id": "pytorch",
            "name": "PyTorch",
            "category": "ai_data",
            "category_label": "AI & Data Science",
            "proficiency": 86,
            "badge": "Advanced",
            "badge_color": "bg-rose-500/10 text-rose-300 border-rose-500/25",
            "icon": "fa-solid fa-fire",
            "icon_color": "text-rose-400",
            "tagline": "Deep learning tensors, autograd differentiation, custom neural nets & GNN models",
            "projects": ["EchoRoute Acoustic GNN", "Gaming Addiction ML Predictor"],
            "concepts": ["Custom nn.Module Layers", "Loss Optimization (AdamW)", "Tensor Board Visualization", "Model Evaluation Matrices"]
        },
        {
            "id": "scikit-learn",
            "name": "scikit-learn",
            "category": "ai_data",
            "category_label": "AI & Data Science",
            "proficiency": 90,
            "badge": "Advanced",
            "badge_color": "bg-orange-500/10 text-orange-300 border-orange-500/25",
            "icon": "fa-solid fa-brain",
            "icon_color": "text-orange-400",
            "tagline": "Supervised & unsupervised ML, regression, clustering & cross-validation",
            "projects": ["Explainable AI Research Paper", "Agricultural Price Estimator"],
            "concepts": ["Random Forests & XGBoost", "Pipeline Feature Unions", "GridSearchCV Hyperparameters", "SHAP Feature Attributions"]
        },
        {
            "id": "opencv",
            "name": "OpenCV",
            "category": "ai_data",
            "category_label": "AI & Data Science",
            "proficiency": 82,
            "badge": "Proficient",
            "badge_color": "bg-emerald-500/10 text-emerald-300 border-emerald-500/25",
            "icon": "fa-solid fa-eye",
            "icon_color": "text-emerald-400",
            "tagline": "Computer vision, image filtering, contour detection & frame processing",
            "projects": ["Warehouse Drone Inventory Counter", "Crop Disease Optical Filter"],
            "concepts": ["Color Space Transformations", "Edge & Contour Detection", "Morphological Operations", "Haar Cascades"]
        },
        {
            "id": "pandas",
            "name": "Pandas",
            "category": "ai_data",
            "category_label": "AI & Data Science",
            "proficiency": 92,
            "badge": "Advanced",
            "badge_color": "bg-indigo-500/10 text-indigo-300 border-indigo-500/25",
            "icon": "fa-solid fa-table",
            "icon_color": "text-indigo-400",
            "tagline": "DataFrames, time-series aggregations, vector indexing & exploratory analysis",
            "projects": ["CloudVantage Telemetry Processor", "Research Dataset Analysis"],
            "concepts": ["Multi-Index GroupBy Operations", "Rolling Window Telemetry", "Vectorized Mapping", "Missing Value Imputation"]
        },
        {
            "id": "numpy",
            "name": "NumPy",
            "category": "ai_data",
            "category_label": "AI & Data Science",
            "proficiency": 90,
            "badge": "Advanced",
            "badge_color": "bg-sky-500/10 text-sky-300 border-sky-500/25",
            "icon": "fa-solid fa-square-root-variable",
            "icon_color": "text-sky-400",
            "tagline": "N-dimensional array computations, linear algebra, Fourier transforms & broadcasting",
            "projects": ["Acoustic Signal Processing", "Vector Embedding Normalizer"],
            "concepts": ["Array Broadcasting Rules", "Matrix SVD & Eigenvectors", "Memory Contiguity (C vs Fortran)", "Vectorized Reductions"]
        },
        {
            "id": "langchain",
            "name": "LangChain",
            "category": "ai_data",
            "category_label": "AI & Data Science",
            "proficiency": 85,
            "badge": "Advanced",
            "badge_color": "bg-purple-500/10 text-purple-300 border-purple-500/25",
            "icon": "fa-solid fa-diagram-project",
            "icon_color": "text-purple-400",
            "tagline": "LLM orchestration, autonomous agent chains, hybrid RAG & vector store connectors",
            "projects": ["OmniScribe AI Platform", "Autonomous Code Review Bot"],
            "concepts": ["Retrieval-Augmented Generation", "Multi-Agent Reflection Loops", "Qdrant Vector Embeddings", "Custom Tool Binding"]
        }
    ],

    "tools_devops": [
        {
            "id": "git",
            "name": "Git",
            "category": "tools_devops",
            "category_label": "Tools & DevOps",
            "proficiency": 92,
            "badge": "Advanced",
            "badge_color": "bg-red-500/10 text-red-300 border-red-500/25",
            "icon": "fa-brands fa-git-alt",
            "icon_color": "text-red-400",
            "tagline": "Distributed version control, branch rebasing, cherry-picking & conflict resolution",
            "projects": ["All Portfolio Projects", "Open Source Contributions"],
            "concepts": ["Interactive Rebasing", "Git Hooks & Submodules", "Merge Conflict Architecture", "Reflog Recovery"]
        },
        {
            "id": "github",
            "name": "GitHub",
            "category": "tools_devops",
            "category_label": "Tools & DevOps",
            "proficiency": 94,
            "badge": "Advanced",
            "badge_color": "bg-slate-300/10 text-slate-200 border-slate-300/25",
            "icon": "fa-brands fa-github",
            "icon_color": "text-slate-200",
            "tagline": "CI/CD Actions pipelines, issue tracking, releases & pull request reviews",
            "projects": ["@Akash04092006 Repositories", "Automated Linting Actions"],
            "concepts": ["GitHub Actions Workflows", "Release Artifacts Packaging", "Branch Protection Rules", "Secrets Management"]
        },
        {
            "id": "vscode",
            "name": "VS Code",
            "category": "tools_devops",
            "category_label": "Tools & DevOps",
            "proficiency": 95,
            "badge": "Expert",
            "badge_color": "bg-blue-500/10 text-blue-300 border-blue-500/25",
            "icon": "fa-solid fa-code-compare",
            "icon_color": "text-blue-400",
            "tagline": "Tailored multi-language workspace, remote SSH debugging & container attachments",
            "projects": ["Primary IDE for All Software Work"],
            "concepts": ["Multi-Root Workspaces", "Remote Containers / SSH", "Launch Configs & Debuggers", "Snippet Automation"]
        },
        {
            "id": "docker",
            "name": "Docker",
            "category": "tools_devops",
            "category_label": "Tools & DevOps",
            "proficiency": 84,
            "badge": "Proficient",
            "badge_color": "bg-sky-500/10 text-sky-300 border-sky-500/25",
            "icon": "fa-brands fa-docker",
            "icon_color": "text-sky-400",
            "tagline": "Multi-stage Dockerfiles, compose clusters, volume management & image minimization",
            "projects": ["NexusPulse Cluster", "AuraPay Microservices"],
            "concepts": ["Multi-Stage Build Caching", "Docker Compose Networks", "Volume Isolation", "Alpine Minimal Runtimes"]
        },
        {
            "id": "jupyter",
            "name": "Jupyter",
            "category": "tools_devops",
            "category_label": "Tools & DevOps",
            "proficiency": 90,
            "badge": "Advanced",
            "badge_color": "bg-orange-500/10 text-orange-300 border-orange-500/25",
            "icon": "fa-solid fa-book",
            "icon_color": "text-orange-400",
            "tagline": "Interactive data exploration, visualization notebooks & ML prototype experimentation",
            "projects": ["XAI Research Paper Analysis", "Geospatial Noise Clustering"],
            "concepts": ["IPython Magic Commands", "Interactive Widget Sliders", "Kernel Memory Management", "Reproducible Data Pipelines"]
        },
        {
            "id": "keil",
            "name": "Keil uVision",
            "category": "tools_devops",
            "category_label": "Tools & DevOps",
            "proficiency": 80,
            "badge": "Proficient",
            "badge_color": "bg-indigo-500/10 text-indigo-300 border-indigo-500/25",
            "icon": "fa-solid fa-microchip",
            "icon_color": "text-indigo-400",
            "tagline": "Embedded ARM compilation, microcontroller simulation, registers & memory maps",
            "projects": ["LPC2148 Firmware Suite", "UART / Timer Driver"],
            "concepts": ["ARM7TDMI Architecture", "Peripheral Register Mapping", "In-Circuit Debugging", "Flash Programming"]
        },
        {
            "id": "ollama",
            "name": "Ollama",
            "category": "tools_devops",
            "category_label": "Tools & DevOps",
            "proficiency": 85,
            "badge": "Proficient",
            "badge_color": "bg-emerald-500/10 text-emerald-300 border-emerald-500/25",
            "icon": "fa-solid fa-laptop-code",
            "icon_color": "text-emerald-400",
            "tagline": "Local open-weights LLM deployment (Llama 3, Mistral, Qwen) with quantized inference",
            "projects": ["OmniScribe Offline Synthesis", "Local Code Reviewer"],
            "concepts": ["GGUF Quantization (4-bit/8-bit)", "Modelfile Customization", "Context Window Management", "REST Server Integration"]
        },
        {
            "id": "vercel",
            "name": "Vercel",
            "category": "tools_devops",
            "category_label": "Tools & DevOps",
            "proficiency": 92,
            "badge": "Advanced",
            "badge_color": "bg-slate-200/10 text-slate-100 border-slate-200/25",
            "icon": "fa-solid fa-triangle-circle-square",
            "icon_color": "text-slate-100",
            "tagline": "Serverless edge functions, Python builders, instant CI/CD preview deployments & routing",
            "projects": ["Personal Portfolio Web App", "EchoRoute Live Deployment"],
            "concepts": ["vercel.json Route Rewrites", "Python Serverless Runtimes", "Edge Caching Headers", "Environment Secrets"]
        }
    ],

    "systems_embedded": [
        {
            "id": "arm-assembly",
            "name": "ARM Assembly",
            "category": "systems_embedded",
            "category_label": "Systems & Embedded",
            "proficiency": 78,
            "badge": "Intermediate",
            "badge_color": "bg-amber-500/10 text-amber-300 border-amber-500/25",
            "icon": "fa-solid fa-microchip",
            "icon_color": "text-amber-400",
            "tagline": "Instruction sets, conditional execution, stack frames & register allocation",
            "projects": ["LPC2148 Bootloader Routine", "Hardware Delay Loop Assembly"],
            "concepts": ["Thumb vs ARM Mode", "Branch with Link (BL)", "Stack Pointer (SP) Alignment", "Status Register (CPSR) Flags"]
        },
        {
            "id": "lpc2148",
            "name": "LPC2148 Microcontrollers",
            "category": "systems_embedded",
            "category_label": "Systems & Embedded",
            "proficiency": 80,
            "badge": "Proficient",
            "badge_color": "bg-sky-500/10 text-sky-300 border-sky-500/25",
            "icon": "fa-solid fa-memory",
            "icon_color": "text-sky-400",
            "tagline": "ARM7TDMI-S architecture, GPIO, UART, Timer/Counters, PWM, ADC & DAC interfaces",
            "projects": ["Robofiesta Sensor Hub", "Telemetry Data Logger"],
            "concepts": ["Pin Connect Block Configuration", "UART Baud Rate Calculations", "Vectored Interrupt Controller (VIC)", "ADC Analog Polling"]
        },
        {
            "id": "operating-systems",
            "name": "Operating Systems",
            "category": "systems_embedded",
            "category_label": "Systems & Embedded",
            "proficiency": 88,
            "badge": "Advanced",
            "badge_color": "bg-indigo-500/10 text-indigo-300 border-indigo-500/25",
            "icon": "fa-solid fa-hard-drive",
            "icon_color": "text-indigo-400",
            "tagline": "Process scheduling, virtual memory, paging, concurrency, deadlocks & file systems",
            "projects": ["Custom Thread Pool & Scheduler", "Multi-Process Pipeline"],
            "concepts": ["Context Switching Overhead", "Page Replacement Algorithms", "Mutexes & Semaphores", "Inode Disk Structures"]
        },
        {
            "id": "computer-networks",
            "name": "Computer Networks",
            "category": "systems_embedded",
            "category_label": "Systems & Embedded",
            "proficiency": 85,
            "badge": "Advanced",
            "badge_color": "bg-emerald-500/10 text-emerald-300 border-emerald-500/25",
            "icon": "fa-solid fa-network-wired",
            "icon_color": "text-emerald-400",
            "tagline": "OSI 7-layer model, TCP/IP, WebSockets, DNS, routing algorithms & network security",
            "projects": ["Decentralized Emergency Mesh", "Real-Time Telemetry Stream"],
            "concepts": ["TCP 3-Way Handshake & Congestion", "DNS Resolution Protocols", "WebSocket Duplex Frames", "TLS Cryptographic Handshake"]
        },
        {
            "id": "dsa",
            "name": "Data Structures & Algorithms",
            "category": "systems_embedded",
            "category_label": "Systems & Embedded",
            "proficiency": 92,
            "badge": "Advanced",
            "badge_color": "bg-rose-500/10 text-rose-300 border-rose-500/25",
            "icon": "fa-solid fa-diagram-next",
            "icon_color": "text-rose-400",
            "tagline": "Graphs, dynamic programming, trees, amortized analysis & algorithmic optimization",
            "projects": ["EchoRoute Dijkstra / A* Routing", "NexusPulse Ring Buffer"],
            "concepts": ["Dijkstra & A* Pathfinding", "Dynamic Programming Memoization", "Segment & Trie Trees", "Amortized Big-O Bounds"]
        }
    ]
}

# Flattened list for seamless iteration and global lookups
ALL_SKILLS = [skill for group in SKILLS.values() for skill in group]

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
        skills=SKILLS,
        all_skills=ALL_SKILLS,
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
# SECURITY & PERFORMANCE HEADERS
# -----------------------------------------------------------------------------

@app.after_request
def add_security_and_cache_headers(response):
    """
    Applies recommended HTTP security headers and cache policies
    for production deployment readiness.
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

    # Cache policies: immutable long cache for static assets, no-cache for dynamic app routes
    if request.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    elif "Cache-Control" not in response.headers:
        response.headers["Cache-Control"] = "no-cache, must-revalidate"

    return response

# -----------------------------------------------------------------------------
# ERROR HANDLERS (404, 500)
# -----------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):
    """User-friendly 404 handler supporting both JSON API calls and glassmorphic UI."""
    if request.path.startswith("/api/") or request.is_json or "application/json" in request.headers.get("Accept", ""):
        return jsonify({
            "success": False,
            "error": "The requested API endpoint was not found.",
            "status_code": 404
        }), 404

    return render_template(
        "404.html",
        personal_info=PERSONAL_INFO,
        current_year=datetime.now().year,
        error_title="Coordinates Not Found",
        error_message="The requested sector or endpoint is not mapped in this deployment architecture."
    ), 404

@app.errorhandler(500)
def internal_server_error(error):
    """User-friendly 500 handler supporting both JSON API calls and glassmorphic UI."""
    logger.error(f"Internal Server Anomaly on {request.path}: {error}")
    if request.path.startswith("/api/") or request.is_json or "application/json" in request.headers.get("Accept", ""):
        return jsonify({
            "success": False,
            "error": "Internal server disturbance encountered. Diagnostics logged.",
            "status_code": 500
        }), 500

    return render_template(
        "500.html",
        personal_info=PERSONAL_INFO,
        current_year=datetime.now().year,
        error_title="System Anomaly Encountered",
        error_message="A temporary disturbance occurred within the backend service. Self-healing protocols are active."
    ), 500

# -----------------------------------------------------------------------------
# ENTRY POINT FOR LOCAL DEVELOPMENT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
