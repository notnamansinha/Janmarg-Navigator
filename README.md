# JANMARG NAVIGATOR 🚌

## 📖 Project Overview

**Janmarg Navigator** is a self-contained, high-performance Command Line Interface (CLI) application developed to simulate and optimize the passenger experience on the **Ahmedabad Bus Rapid Transit System (BRTS)**.

This utility serves as a powerful demonstration of graph traversal algorithms, data modeling using Python dictionaries, and robust file management for persistence—all implemented without relying on external libraries.

### 🎯 Key Challenges Addressed
1.  **Complex Connectivity:** Mapping the multi-route network to find the shortest path, including necessary interchanges.
2.  **State Management:** Persisting user-specific transaction data (tickets) without a formal database.
3.  **Real-World Logic:** Implementing distance-based fare calculation and dynamic discount application.

---

## 🏗️ System Architecture and Data Model

The application architecture is logically separated into three core components: Data Layer, Logic Layer, and Presentation Layer.

### 1. Data Layer: Graph Modeling
The entire BRTS network is modeled as a collection of routes, where each route is an ordered list of stations.

* `all_stations_list` (Set): Provides $O(1)$ average-case lookup time for station existence and validation.
* `brts_routes` (Dictionary): The core adjacency model. Keys are the BRTS route numbers (`"1"`, `"2"`, etc.), and values are ordered lists of stations defining the path.
* `ZONES` (Dictionary): Used for the geographical browsing feature.

### 2. Logic Layer: The Route Finder Engine
The primary logic is handled by the `find_route(start, end)` function, which leverages **Breadth-First Search (BFS)** to guarantee the shortest path in terms of the number of stops/segments.

#### **Algorithm Details**
| Feature | Implementation | Time Complexity |
| :--- | :--- | :--- |
| **Pathfinding** | Iterative BFS using `collections.deque` | $O(R \cdot S^2)$ worst-case, where $R$ is routes and $S$ is stations per route. Highly efficient on sparse real-world transit graphs. |
| **Interchange Logic** | Path-tracking within BFS queue to detect switches between routes | Up to two interchanges are supported to maintain usability and computation speed. |
| **Fare Calculation** | Linear function of stops (`(stops // 3) * 2 + 5`) | $O(1)$ |



### 3. Persistence and File Management
Ticket records are managed using a lightweight flat-file system within the dedicated `janmarg_tickets/` directory.

* `get_ticket_number()`: Manages an auto-incrementing counter (`ticket_counter.txt`) for unique ID generation (e.g., `JM10001`).
* `save_ticket_to_file()`: Writes comprehensive ticket data into a human-readable, formatted `.txt` file, ensuring portability and auditability.

---

## ⚙️ How to Run

This project requires only a standard Python 3.x installation and uses zero third-party dependencies.

### Prerequisites
* Python 3.6+

### Installation and Execution

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/janmarg-navigator.git](https://github.com/yourusername/janmarg-navigator.git)
    cd janmarg-navigator
    ```

2.  **Run the Application:**
    ```bash
    python3 janmarg_navigator.py
    ```
    *(For Windows users, use `python janmarg_navigator.py`)*

---

## 🚀 Core Features Showcase

### 1. Smart Route Navigation (`find_route`)
The system provides detailed journey breakdowns:

| Route Type | Example Start $\to$ End | Output Detail |
| :--- | :--- | :--- |
| **Direct** | Ghuma Gam $\to$ Maninagar | Route #1, Total Stops: 15 |
| **Single Interchange** | Airport $\to$ Vastrapur | Route #7 ($\to$ Juna Vadaj) $\to$ Route #15 ($\to$ Vastrapur) |
| **Multi Interchange** | Sabarmati $\to$ Ramol | Pathing through 3+ routes with a warning message. |

### 2. Ticket & Fare Automation

The `book_ticket` workflow seamlessly combines all calculated data:

```text
================================================================================
🎫 CONFIRMATION
================================================================================

Ticket: JM10001
Date: 2025-12-15 23:00:00
Passenger: Yash Patel
Category: Student

Journey: Sabarmati → Ramol
Route: 7-5 | Stops: 25

Journey Path:
    ▶ Sabarmati
    │ Subhash Bridge
    ...
    🔄 Geeta Mandir (INTERCHANGE)   <- Highlights transfer point
    │ Maninagar
    ...
    ■ Ramol

Base Fare: ₹25.00
Discount (25%): -₹6.25
TOTAL: ₹18.75
3. Station Autocompletion and Search
The autocomplete_station utility enhances user experience by providing quick lookups:

Fuzzy Matching: Type "vas" to see matches like Vasna, Vastrapur, Vasantnagar.

Numerical Selection: Select stations by number from a refined list.

Zone Browsing: Option to filter stations geographically (e.g., list all 14 stations in the South-West zone).

🗺️ Roadmap and Future Development
The current architecture is highly modular and ready for external integration. Proposed enhancements include:

Integration with Live Feeds: Using the requests library (an external dependency) to fetch real-time bus locations or estimated time of arrival (ETA) data from the official BRTS API.

Advanced Pathfinding: Implementation of the A* search algorithm to prioritize routes not just by stops, but by perceived travel time, potentially using a time-based heuristic.

Containerization: Packaging the application within a Docker container to ensure environment consistency across all deployment targets.

Database Migration: Moving the data model from hardcoded dictionaries and flat files to a lightweight SQLite database for more complex query support.

🤝 Contributing
We welcome contributions! Please refer to the Code of Conduct and Contribution Guidelines (to be added) before submitting pull requests.

Fork the Project.

Create your Feature Branch (git checkout -b feature/advanced-search).

Commit your Changes (git commit -m 'feat: added a\* search heuristic').

Push to the Branch (git push origin feature/advanced-search).

Open a Pull Request.

📄 License
Distributed under the MIT License. See LICENSE.txt for more information.
