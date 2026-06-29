<div align="center">

# 🧪 Fragrantica Automation Engine — AromaForge

**An enterprise-grade Python web scraping and automation framework for extracting rich olfactory data and dynamic consumer metrics from Fragrantica.**

AromaForge programmatically bypasses dynamic frontend complexities to compile high-fidelity perfume profiles and translate live Vue.js data visualizations into responsive, offline-ready HTML/Tailwind CSS components.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-Styling-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

</div>

---

## 🎯 The Objective & Business Philosophy

In the competitive landscape of luxury fragrance e-commerce, **content velocity** and **user experience (UX)** are primary vectors for conversion. Traditionally, cataloging a single artisanal fragrance required hours of manual research, metadata entry, and graphic asset production.

**AromaForge** was engineered to redefine this workflow through the lens of continuous business optimization:

| Pillar | Impact |
|---|---|
| **Human Capital Reallocation** | Automates ingestion of complex technical profiles (olfactory notes, performance tracking, consumer sentiment), saving countless operational hours daily |
| **Strategic Focus** | Frees your core team from repetitive data entry to focus on high-value initiatives — user personas, digital gallery experiences, and long-term strategy |
| **Data Integrity as a Standard** | Extraction directly from a definitive reference source eliminates human transcription errors, producing instantly credible, standardized product technical sheets |

---

## ✨ Key Features

- **⚡ Dynamic Vue.js Component Extraction** — Intercepts and parses asynchronous UI states directly from Fragrantica's dynamic frontend layout.

- **📊 Offline Tailwind Component Compilation** — Automatically converts live voter data metrics (**Longevity, Sillage, Gender profiles, Seasonal behavior, and Olfactory Notes**) into beautiful, semantic, dependency-free HTML components pre-styled with Tailwind CSS.

- **🖊️ Automated SEO Content Generation Pipeline** — Compiles raw technical attributes into structured data packages ready to feed programmatic LLM copywriting workflows, generating rich, unique descriptions optimized for organic search rankings.

- **🛡️ Robust Automation Design** — Built on top of Playwright with advanced stealth practices to handle lazy-loaded elements, single-page application (SPA) state transitions, and asynchronous asset loading.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | [Python 3.10+](https://www.python.org/) | Clean, type-hinted data manipulation pipelines |
| **Browser Automation** | [Playwright for Python](https://playwright.dev/python/) | High-performance, asynchronous headless browser interaction |
| **Styling & UI Generation** | [Tailwind CSS Engine](https://tailwindcss.com/) | Highly optimized, responsive, modern card layouts and visualization bars |
| **Data Parsing** | [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) & Native JSON | Fast, reliable markup parsing and structured payload serialization |

---

## ⚙️ Prerequisites & Installation

Ensure you have **Python 3.10 or higher** installed on your environment.

### 1. Clone the Repository

```bash
git clone https://github.com/bardiaazvanian/fragrantica-data-scraper.git
cd fragrantica-data-scraper
```

### 2. Set Up a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\activate

# Activate on Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies & Playwright Browsers

```bash
# Install required Python packages
pip install -r requirements.txt

# Install headless browser binaries required by Playwright
playwright install chromium
```

---

## 🖥️ Usage

The system is split into **modular execution layers**, allowing you to either scrape raw data profiles or directly compile ready-to-use e-commerce frontend components.

### Ingesting Fragrantica Data Profiles

To target a specific perfume URL and export its raw structured profile data:

```bash
python run_scraper.py --url "https://www.fragrantica.com/perfume/Path-To-Target"
```

### Building the Gallery Frontend Components

To translate an ingested data profile into standalone, offline Tailwind CSS components:

```bash
python compile_components.py --source data/profiles/target-perfume.json --output components/
```

> This will generate independent, perfectly responsive blocks for your product tabs, including custom-drawn visual bars for **Longevity**, **Sillage**, and **Season breakdown**.

---

## 📁 Project Structure

```
fragrantica-automation-engine/
├── config/
│   └── settings.py          # Anti-bot profiles, viewport configurations, and stealth settings
├── core/
│   ├── scraper.py           # Core Playwright automation script and navigation logic
│   ├── parser.py            # Extracts dynamic data tables and serializes Vue.js state
│   └── compiler.py          # Translates raw metrics into beautiful HTML/Tailwind components
├── data/                    # Temporary or long-term local storage for extracted profiles
├── templates/
│   └── components/          # Semantic HTML templates mimicking modern, lightweight layouts
├── requirements.txt         # Package dependencies file
├── run_scraper.py           # CLI entrypoint for targeted scraping routines
└── compile_components.py    # CLI entrypoint for generation pipelines
```

**Module Responsibilities:**

- **`core/scraper.py`** — Handles browser initialization, stealth configuration, and dynamic content discovery.
- **`core/parser.py`** — Decodes web metrics (voter statistics for sillage, longevity, gender bias) into clean numerical arrays.
- **`core/compiler.py`** — Injects compiled metrics directly into standard HTML layouts using Tailwind CSS utility classes.

---

## 🤝 Contributing

Contributions are what make the open-source and developer automation communities such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

<div align="center">

Developed with 💡 by **Bardia Azvanian**

*Engineered for the intersection of luxury fragrance and intelligent automation.*

</div>
