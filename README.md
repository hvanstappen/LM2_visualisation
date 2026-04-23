# Apprentice-Master Network Dashboard

A JavaScript Single Page Application (SPA) designed to visualize, filter, and explore historical data concerning artists, their geographical movements, and their professional relationships. The application integrates three distinct visualization paradigms—chronological (Timeline), relational (Network), and geospatial (Map)—into a highly synchronized, interactive dashboard.
This page was developed as part of the [Leerling Meester project](https://www.museabrugge.be/collectie/onderzoek/leerling_meester_ii) by [Datable](http://datable.be). 

See the [user guide](https://github.com/hvanstappen/LM2_visualisation/blob/main/help.md) for instructions in Dutch/English

## 🚀 Features
* **Faceted Cross-Filtering:** Real-time filtering across time periods, geographical locations, and specific artist names.
* **Tri-modal Visualization:** Synchronized updates across a Timeline, a Force-Directed Network Graph, and an Interactive Map.
* **Global State Synchronization:** Clicking an entity in any panel focuses and zooms all other panels to the corresponding data.
* **Algorithmic Data Inference:** Automatically calculates and visualizes uncertain lifespans and travel dates using gradient fades and inferred bounds.
* **Dynamic i18n (Internationalization):** Zero-reload dictionary-based language toggling (English/Dutch).
* **CSS-driven Window Management:** Flexbox and absolute positioning-based maximization of individual panels without losing the context of the details pane.

## 🚀 Installation & Setup
This is a client-side application with no build steps or server required.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/apprentice-master-network.git](https://github.com/yourusername/apprentice-master-network.git)
   ```
2. **Navigate to the project directory:**
   ```bash
   cd apprentice-master-network
   ```
3. **Run the application:**
   Simply open the `index.html` in any modern web browser.

Or just go to the [dashboard](https://hvanstappen.github.io/LM2_visualisation/)

## 📂 Project Structure

```text
├── index.html                  # Main application entry point
├── styles/
│   ├── lm_style.css           # Custom dashboard styling, tooltips, and layout
│   ├── vis-timeline-graph2d.min.css
│   └── leaflet.css
├── libraries/                  # Local copies of external libraries
│   ├── vis-timeline-graph2d.min.js
│   ├── cytoscape.min.js
│   └── leaflet.js
├── scripts/                    # Extra tools
│   └── csv_to_json.py          # script to transform .xlsx to .js 
└── source_data/
    └── leerling_meester_sourcedata.js # Contains the dataset (peopleData, travelsData, relationsData, Locations)
    └── leerling_meester_sourcedata.xlsx # Contains the original dataset

```

## 🛠️ Technology Stack
This project operates entirely on the client side without the need for a build step or a backend framework.
* **Core:** HTML5, CSS3, ES6 JavaScript (Vanilla).
* **Timeline:** [Vis.js (Timeline/Graph2D)](https://visjs.github.io/vis-timeline/docs/timeline/) - Handles chronological events, ranges, and background lifespans.
* **Network:** [Cytoscape.js](https://js.cytoscape.org/) - Renders the nodes and edges using the `cose` (Compound Spring Embedder) physics layout.
* **Mapping:** [Leaflet.js](https://leafletjs.com/) - Renders geospatial data and handles bounding box animations.

## 📂 Data Architecture
Data is injected statically via `leerling_meester_sourcedata.js` and consists of three main JSON-like arrays:
1.  **`peopleData`:** Contains biographical metadata (birth/death dates, precision, nationality, RKD links) for each artist (nodes).
2.  **`travelsData`:** Contains chronological movement records (start/end dates, primary/secondary locations, funding sources). 
3.  **`relationsData`:** Defines the directed edges (source, target, relationship type) between artists in `peopleData`.
4.  **`Locations`:** A dictionary mapping city names to precise Latitude/Longitude coordinates for Leaflet.

You can create this .js file from the original data file source_data/Brugse_kunstenaars_in_het_buitenland.xlsx with scripts/csv_to_json.py

## ⚙️ Core Logic & State Management

### 1. The Filtering Engine (`applyFilters`)
The application uses a strict intersection logic (`AND` operator) across three main Sets:
* `checkedNames` (Set of artist IDs)
* `checkedLocations` (Set of city strings)
* `minYear` & `maxYear` (Integers derived from the range slider)

When `applyFilters()` is called, it iterates over `peopleData`. An artist is added to the `selectedArtists` Set only if they pass `matchesTime`, `matchesLocation`, and `matchesName`. The UI (checkboxes and visual libraries) is then re-rendered based strictly on the contents of the `selectedArtists` Set.

### 2. Data Aggregation (`buildLocationVisits`)
To optimize map and detail panel performance, travel events are pre-aggregated into a `globalLocationVisits` object. This function maps every unique location string to an array of objects containing the visitor's ID, name, and time spent there. It parses both primary `t.location` and arrays of `t.secondary_locations`, appending localized tags (e.g., "(secondary)") to the latter.

### 3. Global Synchronization (`setFocus`)
The `setFocus(artistId)` function handles cross-panel communication:
* **Details Panel:** Updates the DOM with HTML tables containing the artist's metadata.
* **Timeline:** Highlights the artist's label group (via CSS class toggling) and calls `timeline.focus()` to center the viewport on their active items.
* **Network:** Removes previous focus classes, applies a `.focused` CSS class to the specific Cytoscape node, and uses `cy.animate()` to zoom and center the canvas on the node.
* **Map:** Calculates a dynamic bounding box array containing the artist's birth place and all travel locations, then calls `map.fitBounds()` to frame the relevant geography.

## 📊 Visualization Specifics

### Vis.js Timeline
* **Inferred Lifespans:** Uses `type: 'background'` items to draw the lifespan. If birth or death dates are missing, the algorithm infers them based on the artist's travel history boundaries `+/- 15/70 years`.
* **Uncertainty Fades:** Travel events with uncertain start or end dates are assigned specific CSS classes (`fade-in`, `fade-out`, `fade-both`). CSS linear gradients are applied to visually communicate chronological uncertainty.
* **Native Tooltips:** Background items utilize HTML native `title` attributes wrapped in a 100% width/height `<div>` to ensure tooltips track the cursor accurately across horizontally expansive background items.

### Cytoscape.js Network
* **Node Sizing:** Node dimensions are dynamically calculated based on degree centrality (the total number of incoming and outgoing edges connected to the artist).
* **Edge Highlighting:** When an artist is filtered or selected, their connected edges receive an `.active` class, increasing opacity, changing color, and revealing the relationship label (e.g., "teacher").

### Leaflet.js Map
* **Dynamic Rendering:** Markers are continuously destroyed and redrawn based on the `selectedArtists` Set to maintain optimal performance.
* **Tooltip HTML:** Marker tooltips dynamically aggregate and display a list of all selected artists who visited the location and their respective dates.

## 🌐 Internationalization (i18n)
The application utilizes a lightweight, dictionary-based i18n implementation. 
* **Dictionary:** A global `translations` object stores key-value pairs for `nl` (Dutch) and `en` (English).
* **DOM Mapping:** Static HTML elements are tagged with `data-i18n`, `data-i18n-title`, or `data-i18n-placeholder`.
* **Execution:** `toggleLanguage()` iterates over these datasets, updating `innerHTML` and attributes natively. Dynamic strings inside JavaScript (e.g., timeline popups) retrieve their values from `translations[currentLang]` on the fly during rendering.

## 🎨 UI/UX & Layout Management
The dashboard is built using CSS Flexbox. Panel maximization (`toggleMaximize`) avoids expensive JavaScript resizing calculations by applying specific state classes (e.g., `.max-timeline`) to the root wrapper. These classes utilize `display: none !important` to hide non-active panels and absolute positioning (`calc(100% - 350px)`) to expand the active panel while preserving the fixed-width Details panel.

## 📄 License

This project is open-source and available under the MIT License.
