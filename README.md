🧪 Fragrantica Automation Engine (AromaForge)An enterprise-grade Python web scraping and automation framework designed to extract rich olfactory data and dynamic consumer metrics from Fragrantica. This engine programmatically bypasses dynamic frontend complexities to compile high-fidelity perfume profiles and translate live Vue.js data visualizations into responsive, offline-ready HTML/Tailwind CSS components.🎯 The Objective & Business PhilosophyIn the competitive landscape of luxury fragrance e-commerce, content velocity and user experience (UX) are primary vectors for conversion. Traditionally, cataloging a single artisanal fragrance required hours of manual research, metadata entry, and graphic asset production.AromaForge was engineered to redefine this workflow through the lens of continuous business optimization:Human Capital Reallocation: By automating the ingestion of complex technical profiles (olfactory notes, performance tracking, consumer sentiment), this framework saves countless operational hours daily.Strategic Focus: Instead of executing repetitive data entry, your core team is empowered to focus entirely on high-value initiatives—refining user personas, designing immersive digital gallery experiences, optimizing customer support funnels, and building long-term business strategies.Data Integrity as a Standard: Automating extraction directly from a definitive reference source eliminates human transcription errors, providing your store with instantly credible, highly standardized product technical sheets.🚀 Key Features⚡ Dynamic Vue.js Component Extraction: Intercepts and parses asynchronous UI states directly from Fragrantica's dynamic frontend layout.📊 Offline Tailwind Component Compilation: Automatically converts live voter data metrics (Longevity, Sillage, Gender profiles, Seasonal behavior, and Olfactory Notes) into beautiful, semantic, dependency-free HTML components pre-styled with Tailwind CSS.✍️ Automated SEO Content Generation Pipeline: Compiles raw technical attributes into structured data packages ready to feed programmatic LLM copywriting workflows, generating rich, unique descriptions optimized for organic search rankings.🛡️ Robust Automation Design: Built on top of Playwright with advanced stealth practices to handle lazy-loaded elements, single-page application (SPA) state transitions, and asynchronous asset loading.🛠️ Tech StackLanguage: Python 3.10+ – Leveraged for clean, type-hinted data manipulation pipelines.Browser Automation: Playwright for Python – High-performance, asynchronous headless browser interaction.Styling & UI Generation: Tailwind CSS Engine – For generating highly optimized, responsive, modern card layouts and visualization bars.Data Parsing: BeautifulSoup4 & Native JSON – Fast, reliable markup parsing and structured payload serialization.⚙️ Prerequisites & InstallationEnsure you have Python 3.10 or higher installed on your environment.1. Clone the Repositorygit clone https://github.com/yourusername/fragrantica-automation-engine.git
cd fragrantica-automation-engine
2. Set Up a Virtual Environment# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\activate

# Activate on Linux/macOS
source venv/bin/activate
3. Install Dependencies & Playwright Browsers# Install required Python packages
pip install -r requirements.txt

# Install headless browser binaries required by Playwright
playwright install chromium
💻 UsageThe system is split into modular execution layers allowing you to either scrape raw data profiles or directly compile ready-to-use e-commerce frontend components.Ingesting Fragrantica Data ProfilesTo target a specific perfume URL and export its raw structured profile data:python run_scraper.py --url "https://www.fragrantica.com/perfume/Path-To-Target-Perfume.html" --output data/profiles/
Building the Gallery Frontend ComponentsTo translate an ingested data profile into standalone, offline Tailwind CSS components:python compile_components.py --source data/profiles/target-perfume.json --output dist/components/
This will spit out independent, perfectly responsive blocks for your product tabs, including custom-drawn visual bars for Longevity, Sillage, and Season breakdown.📁 Project Structure├── config/
│   └── settings.py          # Anti-bot profiles, viewport configurations, and selector maps.
├── core/
│   ├── scraper.py           # Core Playwright automation script and navigation layers.
│   ├── parser.py            # Extracts dynamic data tables and serializes Vue.js states.
│   └── compiler.py          # Translates raw metrics into beautiful HTML/Tailwind structures.
├── data/                    # Temporary or long-term local storage for extracted JSON assets.
├── templates/
│   └── components/          # Semantic HTML templates mimicking modern, lightweight chart layouts.
├── requirements.txt         # Package dependencies file.
├── run_scraper.py           # CLI entrypoint for targeted scraping routines.
└── compile_components.py    # CLI entrypoint for generation pipelines.
core/scraper.py: Handles browser initialization, stealth configuration, and dynamic content discovery.core/parser.py: Decodes web metrics (voter statistics for sillage, longevity, gender bias) into clean numerical arrays.core/compiler.py: Inject compiled metrics directly into standard HTML layouts using Tailwind CSS utility classes.🤝 ContributingContributions are what make the open-source and developer automation communities such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.Fork the ProjectCreate your Feature Branch (git checkout -b feature/AmazingFeature)Commit your Changes (git commit -m 'Add some AmazingFeature')Push to the Branch (git push origin feature/AmazingFeature)Open a Pull Request📄 LicenseDistributed under the MIT License. See LICENSE for more information.
