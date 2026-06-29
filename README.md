🌸 AromaFlow: Automated Perfume Data & Chart Pipeline

Welcome to AromaFlow — a high-performance Python web scraping and automation toolkit designed to extract accurate, high-quality perfume data and dynamic visual charts from Fragrantica, the definitive reference database for fragrance enthusiasts.

💡 Why We Built This (And Why Your Business Needs It)

The Problem: The Data Entry Bottleneck

In modern e-commerce, time is the ultimate leverage. For boutique and scale-up perfume galleries alike, sourcing accurate product data and translating complex, dynamic charts into usable web elements is traditionally a slow, human-intensive process. Teams easily sink dozens of hours weekly into copy-pasting olfactory notes, translating graphics, and manually formatting specifications for new catalog entries. This manual workflow is highly error-prone, challenging to scale, and distracts high-value talent from core business activities.

The Solution: Strategic Automation

We built AromaFlow to completely eliminate this operational friction. By programmatically interface-scraping dynamic Vue.js web applications, the script instantly extracts structured fragrance datasets. It handles the heavy lifting, turning an outdated multi-step editorial workflow into a single, automated, and deterministic software pipeline.

The Immediate Benefits

⏱️ Unmatched Time & Resource Optimization: Turns hours of repetitive manual data entry into a fast execution script that compiles an entire product's profile in seconds.

📈 Programmatic SEO Generation: Automates the drafting of rich, keyword-optimized content derived directly from factual olfactory pyramids, elevating search rankings effortlessly.

✨ Seamless Visual Assets: Extracts complex frontend visual charts (such as Longevity, Sillage, Seasons, and Gender) and renders them as localized Tailwind CSS/HTML components. This adds interactive, high-fidelity customer-facing visual guides to your website out-of-the-box.

Why Every Modern Business Needs Pipelines Like This

No modern brand can scale if its human talent is acting as human middleware between databases. Implementing custom automation pipelines like AromaFlow transforms information-gathering from an overhead cost into a scalable programmatic asset. By offloading data collection, compilation, and standard visual rendering to intelligent scrapers, businesses can re-invest their valuable hours where it matters most: honing the Customer Experience (CX), crafting brand narratives, building strategic partnerships, and accelerating sales.

🚀 Key Features

🧠 Automated SEO Content Generation: Programmatically parses scraped olfactory profiles to generate detailed, keyword-rich copy for perfume product listings.

📊 Dynamic Chart Extraction & Conversion: Hooks into client-side Vue.js app states, extracting raw values for Longevity, Sillage, Gender, Seasons, and Notes to generate offline Tailwind CSS components.

🖼️ Visual Product Enhancement: Instantly outputs beautiful, self-contained interactive visual widgets ready to drop directly into your gallery's custom product pages.

⚡ Resilient Dynamic Scraping: Built on top of Playwright to gracefully navigate single-page application (SPA) environments, asynchronous API calls, and heavy dynamic rendering.

🛠️ Tech Stack

Python 3.9+ - Scripting engine, file system management, and structured data serialization.

Playwright - Headless browser automation framework utilized to fetch dynamically loaded assets.

Tailwind CSS - Modern utility-first styling system used to render beautiful, responsive visual offline charts.

JavaScript - Custom injected evaluation layers to extract raw state objects directly from client-side DOM.

⚙️ Prerequisites & Installation

To get started, make sure you have Python 3.9 or higher installed on your machine.

Clone the repository:

git clone https://github.com/yourusername/aromaflow.git
cd aromaflow


Set up a virtual environment (Recommended):

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Install Playwright headless browser binaries:

playwright install chromium


💻 Usage

AromaFlow provides a straightforward command-line interface. Run the pipeline against a specific product page URL:

python main.py --url "https://www.fragrantica.com/perfume/Brand/Perfume-Name.html" --output-dir ./product_data


Expected Output

Upon successful execution, the script automatically exports production-ready visual components and structured content directly into your output directory:

product_data/
├── seo_description.md       # Tailored markdown description for your e-shop
├── seo_metadata.json        # Structured JSON with key olfactory metadata
└── components/
    ├── longevity_chart.html # Responsive, standalone Tailwind CSS component
    ├── sillage_chart.html   # Standalone Sillage HTML visual component
    └── notes_pyramid.html   # Clean HTML representation of top, middle, & base notes


📁 Project Structure

├── main.py                # Primary entry point & CLI controller
├── scraper/
│   ├── engine.py          # Playwright initialization & web drivers
│   └── extractors.py      # Target scrapers parsing text, ratings, and parameters
├── chart_converter/
│   ├── vue_parser.py      # Injects evaluation layers to extract Vue.js component states
│   └── tailwind_gen.py    # Translates states to responsive Tailwind HTML code
├── content_generator/
│   └── seo_builder.py     # Parses text data to assemble SEO-ready copy
├── requirements.txt       # Python dependency declarations
└── README.md              # Project documentation


🤝 Contributing

We welcome contributions to expand AromaFlow's automation capabilities. If you have suggestions for improved parsers, additional component templates, or scraper performance tuning:

Fork the project repository.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📄 License

Distributed under the MIT License. See LICENSE for more details.

Built with precision to let you focus on the art of perfumery. 🌹
