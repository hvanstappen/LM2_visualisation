# LM2_visualisation


# Apprentice-Master Network Dashboard
Single page visualization web app 

An interactive, multidimensional analytical dashboard designed to explore the relationships, lifespans, and travel histories of historical artists. 

This tool allows researchers and enthusiasts to seamlessly navigate through complex historical data across three synchronized dimensions: time (timeline), relationships (social network), and geography (interactive map).

## ✨ Key Features

* **Multidimensional Exploration**: Three primary visualizations work in perfect sync:
  * **Timeline**: Visualizes artist lifespans and specific travel events. Features smart inferences for unknown dates and visual fade effects for uncertain travel durations.
  * **Social Network**: A node-based graph showing relationships (e.g., teacher, student, influenced by).
  * **Travel Map**: A geographic overview of birthplaces and travel destinations.
* **Faceted Search & Filtering**: A persistent top navigation bar features smart, interconnected filters for **Name**, **Location**, and **Time Period** (using a dual-thumb slider). Selections dynamically update available options to prevent "zero result" dead ends.
* **Context-Aware Details Panel**: The information panel automatically adapts to your focus:
  * *Artist Focus*: Displays biographical data, name variants, roles, and external links (e.g., RKD).
  * *Location Focus*: Displays a chronological log of all artists who visited a specific city.
* **Synchronized Interactions**: 
  * Clicking a travel event on the timeline smoothly flies the map camera to that specific city.
  * Clicking a map marker pulls up the location's visitor log and allows you to instantly filter the entire dashboard by that city.
* **Floating Navigation Controls**: Built-in, accessible UI controls (zoom, pan, fit-to-screen, reset) for complex visualizations.

## 🛠️ Technologies Used

This project is built using standard web technologies (HTML, CSS, JavaScript) and relies on the following powerful open-source libraries:

* **[Vis-Timeline](https://visjs.github.io/vis-timeline/docs/timeline/)**: For handling complex, stacked temporal data.
* **[Cytoscape.js](https://js.cytoscape.org/)**: For rendering the interactive, physics-based social network graph.
* **[Leaflet.js](https://leafletjs.com/)**: For the interactive travel map.

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

## 📂 Project Structure

```text
├── index.html                  # Main application entry point
├── styles/
│   ├── lm_style2.css           # Custom dashboard styling, tooltips, and layout
│   ├── vis-timeline-graph2d.min.css
│   └── leaflet.css
├── libraries/                  # Local copies of external libraries
│   ├── vis-timeline-graph2d.min.js
│   ├── cytoscape.min.js
│   └── leaflet.js
└── source_data/
    └── leerling_meester_sourcedata.js # Contains the dataset (peopleData, travelsData, relationsData, Locations)
```

## 📊 Data Format

The dashboard expects data to be loaded via the `leerling_meester_sourcedata.js` file, structured into four main variables:
* `peopleData`: Array of objects containing artist biographies (id, name, birth, death, etc.).
* `travelsData`: Array of objects linking an artist to a location over a specific timeframe.
* `relationsData`: Array of objects defining relationships between two artist IDs (`source` and `target`).
* `Locations`: Array mapping location names to latitude and longitude coordinates.

You can create this .js file from the original data file source_data/Brugse_kunstenaars_in_het_buitenland.xlsx with scripts/csv_to_json.py

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License

This project is open-source and available under the MIT License.
