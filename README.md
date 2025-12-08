Primary Objectives
1. Intelligent Route Finding - Implement BFS algorithm to find optimal routes between 160+ BRTS stations
with interchange support
2. Digital Ticket Booking - Eliminate physical queues through paperless ticketing system
3. Fare Automation - Calculate distance-based fares with automated discount application for 5 passenger
categories
4. User Accessibility - Provide intuitive station search with autocomplete and zone-based browsing
5. Environmental Impact - Reduce paper waste and promote sustainable public transport usage

Secondary Objectives
● Real time navigation assistance with journey path visualization
● Persistent ticket storage and management system
● Comprehensive information services (maps, timings, emergency contacts)
● Cross-platform compatibility (Windows, macOS, Linux)

Problem Statement
Ahmedabad's BRTS serves 350,000+ daily commuters but faces challenges:
● Manual route planning causing 10-15 minute delays
● Time-consuming physical ticket booking (5-10 minute queues)
● Complex fare structures without transparent calculation
● Difficulty finding optimal routes with multiple interchanges
● No unified digital platform for commuter assistance


2. FUNCTIONALITY DEVELOPED
   
2.1 Route Finding Engine
The engine uses Breadth-First Search (BFS), which has a complexity of O(R \times S^2) (where R is routes and S
is stations), to efficiently calculate travel options.
● Direct Route Detection: Finds routes traveling in either direction along a single line.
● Optimal Path Finding: Determines the best route based on the fewest number of stops.
● Interchange Routing: Handles journeys requiring one or two changes between lines.
● Journey Visualization: Provides a clear display of the path, including arrows to simplify understanding.

2.2 Digital Ticket Booking System Summary
The system manages the ticket purchase and supports various passenger types with automatic discount calculation.
The tickets are generated digitally and stored persistently.
● Interactive Selection: Users select stations easily using an autocomplete feature.
● Automatic Fare Calculation: The system calculates the final fare immediately, applying the appropriate
discount based on the chosen category.
● Journey Preview: Before purchase, the user sees a complete path visualization of their planned journey.
● Digital Ticket: A unique ticket is generated with an "JM-" prefix for identification.
● Persistent Storage: All ticket records are saved reliably using file-based storage.

2.3 Station Autocomplete & Search Summary
The system uses fuzzy string matching with O(n) →complexity to provide fast, real-time station search and
identification, offering multiple ways for users to find their desired station from over 160 entries.
● Intelligent Matching: Employs case-insensitive substring matching for high accuracy, even with partial
input.
● Real-Time Results: Provides immediate search results with disambiguation to help users select the correct
station.
● Organized Browsing: Stations are grouped into 8 geographical zones for hierarchical navigation.
● Comprehensive Listing: Includes a directory of 160+ stations.
● Quick Selection: Allows for numeric quick-selection of stations from the displayed results.

2.4 Ticket Management Summary
The system is designed to handle the full lifecycle of digital tickets, using file-based persistence to ensure records are
uniquely generated, saved, and easily managed.
● Unique ID Generation: Automatically assigns unique, auto-incrementing ticket numbers (e.g., JM10001,
JM10002...).
● Persistent Storage: Saves each ticket as a formatted text file for reliable record-keeping.
● History & Review: Users can view a chronological history of all previously generated tickets.
● Data Maintenance: Allows users to delete old tickets to manage storage space.
● Encoding Support: Uses UTF-8 encoding to fully support Unicode characters in ticket details.

2.5 Information Services Summary
The system provides essential passenger information, ranging from network layout to operational details and support
services.
● Network Map: Displays the entire network, including 160 stations across 8 zones.
● Route Explorer: Details information for 15 major routes.
● Bus Timings: Provides operational times from 6:00 AM to 11:00 PM.
● Emergency Support: Offers immediate help via the Helpline: 1-800-233-2030.
● Educational Content: Includes engaging trivia presented with a typing animation.
● System Information: Provides comprehensive Help and About details.

2.6 User Interface Summary
The interface focuses on a clear, text-based, and cross-platform design for ease of use and navigation.
● Launch Experience: Features an ASCII art splash screen with a loading animation.
● Navigation: Uses clear hierarchical menus offering 13 distinct options.
● Visual Design: Leverages Unicode box-drawing for a visually appealing text-based layout.
● Usability: Ensures a clean display via cross-platform screen clearing.
● Intuitive Icons: Uses emoji icons to make navigation more intuitive.
● Formatting: Employs formatted headers and sections for readability.
