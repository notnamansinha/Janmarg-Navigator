#!/usr/bin/env python3
"""
JANMARG NAVIGATOR - AHMEDABAD BRTS (data from official janmarg website)

"""

import os
import sys
import time
import random
from collections import deque
from datetime import datetime

# File Management Stuff 
ticket_folder = "janmarg_tickets"
ticket_counter_file = "ticket_counter.txt"

# Zone DataBase 
ZONES = {
    "Central": ["Kalupur", "Geeta Mandir", "Delhi Darwaja", "Kalupur Railway Station",
                "Town Hall", "Lal Darwaja", "ST Stand", "Dariapur", "Sarangpur",
                "Shah-e-Alam", "Camp Hanuman", "RTO Circle", "RTO"],
    "West": ["Vastrapur", "Bodakdev", "Satellite", "Paldi", "Ashram Road",
             "Mithakhali", "Navrangpura", "Jodhpur", "Thaltej", "Memnagar",
             "Gurukul", "Ambawadi", "Parimal Garden", "L D College"],
    "South-West": ["Sarkhej", "Makarba", "ISKCON Cross Road", "Shivranjani", "Nehrunagar",
                   "Bopal Approach", "South Bopal", "Ghuma Gam", "Bopal Gam", "Bopal ST",
                   "DCIS Circle", "Vasantnagar Township", "Amba Township", "Bopal Junction"],
    "North": ["Sabarmati", "Motera", "Motera Stadium", "Airport", "Chandkheda",
              "Sabarmati Police Station", "Sabarmati Power House", "Chandkheda Gam",
              "Chandkheda Police Station", "Subhash Bridge"],
    "North-West": ["Gota", "Kudasan", "Ranip", "Sola", "Sola Cross Roads", "Bhadaj Circle",
                   "Science City Approach", "Gota Cross Road", "Ranip Cross Roads",
                   "New Ranip", "Ranip GSRTC", "Vadaj", "Juna Vadaj", "Usmanpura",
                   "SGVP", "Shilaj", "Sola Bridge", "Sola Bhagwat", "AUDA Garden"],
    "East": ["Maninagar", "Maninagar Railway Station", "Anjali", "Isanpur", "Narol",
             "Vastral", "Nikol", "Odhav", "CTM", "CTM Cross Roads", "Odhav Ring Road",
             "Maninagar Depot", "Maninagar Terminus", "Isanpur Depot", "Ramol",
             "Memco", "Nirnay Nagar"],
    "North-East": ["Naroda", "Naroda Gam", "Dahegam Circle", "Naroda ST Workshop",
                   "Zundal Circle", "Vishwakarma Government Engineering College",
                   "Janta Nagar", "IOC Road", "Visat", "ONGC", "Chandranagar"],
    "South": ["Kankaria Lake", "Kankaria Zoo", "Khokhra", "Khodiyar Nagar",
              "Vasna", "IIM", "Gujarat University", "Commerce Six Roads"]
}

# Discount Categories
discount_categories = {
    "1": {"name": "Regular Citizen", "discount": 0, "description": "No discount"},
    "2": {"name": "Student", "discount": 25, "description": "25% discount with valid ID"},
    "3": {"name": "Senior Citizen", "discount": 50, "description": "50% discount (60+ years)"},
    "4": {"name": "Differently Abled", "discount": 50, "description": "50% discount"},
    "5": {"name": "Have a Monthly Pass", "discount": 30, "description": "30% discount"}
}

# All Stations
all_stations_list = {
    "RTO Circle", "Maninagar", "Anjali", "Naroda", "Ghuma Gam",
    "ISKCON Cross Road", "Bopal Approach", "Shivranjani", "Nehrunagar",
    "Kalupur", "Geeta Mandir", "Bhadaj Circle", "Amba Township",
    "Vasna", "Dahegam Circle", "Narol", "CTM Cross Roads",
    "Airport", "South Bopal", "DCIS Circle", "Vasantnagar Township",
    "Sola Cross Roads", "Jaymangal", "Delhi Darwaja", "Odhav Ring Road",
    "Camp Hanuman", "Kankaria Lake", "IIM", "Maninagar Railway Station",
    "Sabarmati", "Chandkheda", "Motera Stadium", "Sarkhej", "Thaltej",
    "Vastrapur", "Bodakdev", "Satellite", "Paldi", "Ashram Road",
    "Mithakhali", "Navrangpura", "Gujarat University", "Commerce Six Roads",
    "Vijay Nagar", "Jodhpur", "Gota", "Kudasan", "Ranip",
    "Makarba", "SGVP", "Shilaj", "Sola", "Ambawadi", "Memnagar",
    "Gurukul", "Isanpur", "Vastral", "Nirnay Nagar", "CTM",
    "Zundal Circle", "Vishwakarma Government Engineering College", "Janta Nagar",
    "IOC Road", "Visat", "ONGC", "Chandkheda Gam", "Sola Bhagwat",
    "Sola Bridge", "Science City Approach", "Ambali Road", "Swaminarayan Mandir",
    "AUDA Garden", "Bhavsar Hostel", "Bopal Gam", "Bopal ST",
    "BRTS Workshop", "Chandkheda Police Station", "Chandranagar", "Dariapur",
    "Dharnidhar", "Dilli Chakla", "Dindoli", "Drive-in Cinema",
    "Dudheshwar", "Gota Cross Road", "Gujcomasol", "Himmatlal Park",
    "Idgah", "India Colony", "Isanpur Depot", "Jashoda Nagar",
    "Jivanwadi", "Juna Vadaj", "Kalapinagar", "Kalupur Railway Station",
    "Kankaria Zoo", "Khokhra", "Khodiyar Nagar", "L D College",
    "Lal Darwaja", "Madhupura", "Maninagar Depot", "Maninagar Terminus",
    "Manmohan Park", "Memco", "MHS High School", "M J Library",
    "Motera", "Naranpura", "Naroda Gam", "Naroda ST Workshop",
    "New Ranip", "Nikol", "Nirant Cross Road", "Noble Nagar",
    "Odhav", "Ognaj", "Parasnagar", "Parimal Garden",
    "Patia", "Power House", "Rabari Colony", "Raipur",
    "Rakhial", "Ramdevnagar", "Ramol", "Ranip Cross Roads",
    "Ranip GSRTC", "RTO", "Sabarmati Police Station", "Sabarmati Power House",
    "Sahjanand College", "Sardar Patel Stadium", "Sarangpur", "Shah-e-Alam",
    "Shastri Nagar", "Shatabdi Hospital", "Shreyas", "Soni ni Chali",
    "ST Stand", "Subhash Bridge", "Swastik Cross Road", "Thakkarnagar",
    "Town Hall", "Usmanpura", "Vadaj", "Vallabh Vidyanagar",
    "Vatva", "Vatva Approach", "Vijay Mill", "Vivekanand",
    "Vyasvadi", "Zydus", "Akhbarnagar", "Amraiwadi",
    "Bage Firdos", "Bapunagar", "Bethak", "Bhulabhai Park",
    "Bhuyangdev", "Bopal Junction", "Gomtipur", "Himmatnagar",
    "Juna Wadaj Circle", "Kaligam", "Keshavbaug", "Lokmanya Tilak",
    "M K Shah College", "Panchvati", "Pragatinagar", "Shahwadi", "Sharda Mandir"
}

# All major BRTS routes with complete station lists
brts_routes = {
    "1": ["Ghuma Gam", "Bopal Gam", "Bopal ST", "South Bopal", "Bopal Approach", 
          "ISKCON Cross Road", "Shivranjani", "Bodakdev", "Vastrapur", "Memnagar",
          "Nehrunagar", "Paldi", "Ashram Road", "Anjali", "Geeta Mandir", 
          "Maninagar", "Maninagar Railway Station", "Maninagar Depot"],
    
    "2": ["Bhadaj Circle", "Science City Approach", "AUDA Garden", "Sola Bhagwat", 
          "Sola", "Sola Bridge", "Sola Cross Roads", "Jaymangal", "Navrangpura", 
          "Gujarat University", "Commerce Six Roads", "L D College", "Delhi Darwaja", 
          "Kalupur", "Kalupur Railway Station", "Lal Darwaja", "CTM Cross Roads", 
          "CTM", "Odhav Ring Road", "Odhav", "Rakhial"],
    
    "3": ["RTO Circle", "RTO", "Camp Hanuman", "Mithakhali", "Jaymangal", 
          "Navrangpura", "Ambawadi", "Parimal Garden", "Town Hall", "Kalupur", 
          "Geeta Mandir", "Dariapur", "Sarangpur", "Anjali", "Maninagar", 
          "Maninagar Depot", "Maninagar Terminus"],
    
    "4": ["Thaltej", "SGVP", "Shilaj", "Ognaj", "Bopal Junction", "Bopal ST", 
          "Bopal Gam", "Bopal Approach", "ISKCON Cross Road", "Shivranjani", 
          "Bodakdev", "Satellite", "Jodhpur", "Gurukul", "Memnagar"],
    
    "5": ["Vasna", "IIM", "Kankaria Lake", "Kankaria Zoo", "Khokhra", 
          "Khodiyar Nagar", "Paldi", "Ashram Road", "Anjali", "Geeta Mandir",
          "Maninagar", "Isanpur", "Isanpur Depot", "Narol", "Vastral", 
          "Memco", "Nikol", "Ramol", "Naroda", "Naroda Gam", "Dahegam Circle"],
    
    "6": ["Sarkhej", "Makarba", "DCIS Circle", "Vasantnagar Township", 
          "Amba Township", "ISKCON Cross Road", "Bodakdev", "Vastrapur", 
          "Memnagar", "Gurukul", "Nehrunagar", "Paldi", "Ashram Road", 
          "Ambawadi", "Geeta Mandir", "Kalupur"],
    
    "7": ["Airport", "Motera Stadium", "Motera", "Sabarmati", 
          "Sabarmati Police Station", "Sabarmati Power House", "Subhash Bridge",
          "Usmanpura", "Vadaj", "Juna Vadaj", "Naranpura", "Gujarat University",
          "ST Stand", "Town Hall", "Lal Darwaja", "Kalupur", "Geeta Mandir"],
    
    "8": ["Airport", "Chandkheda", "Chandkheda Gam", "Chandkheda Police Station",
          "Gota", "Gota Cross Road", "Kudasan", "Ranip", "Ranip Cross Roads",
          "New Ranip", "Ranip GSRTC", "Sola", "SGVP"],
    
    "9": ["Maninagar", "Maninagar Railway Station", "Anjali", "Isanpur",
          "Narol", "Vastral", "Nirnay Nagar", "CTM", "CTM Cross Roads",
          "Odhav", "Odhav Ring Road", "Nikol", "Naroda"],
    
    "10": ["Naroda", "Naroda Gam", "Naroda ST Workshop", "Zundal Circle",
           "Vishwakarma Government Engineering College", "Janta Nagar", 
           "IOC Road", "Visat", "ONGC", "Chandranagar"],
    
    "11": ["Kalupur", "Kalupur Railway Station", "Lal Darwaja", "Town Hall",
           "ST Stand", "Delhi Darwaja", "Shah-e-Alam", "Dariapur", "Sarangpur",
           "Geeta Mandir", "Anjali", "Maninagar"],
    
    "12": ["Satellite", "Jodhpur", "Gurukul", "Memnagar", "Vastrapur",
           "Bodakdev", "Nehrunagar", "Shivranjani", "Ambawadi", "Navrangpura"],
    
    "13": ["Vasna", "IIM", "Gujarat University", "Commerce Six Roads",
           "Kankaria Lake", "Kankaria Zoo", "Khokhra", "Maninagar"],
    
    "14": ["Ghuma Gam", "South Bopal", "DCIS Circle", "Vasantnagar Township",
           "Amba Township", "Bopal Junction", "Bopal Gam", "Bopal ST",
           "Bopal Approach", "ISKCON Cross Road"],
    
    "15": ["Thaltej", "Vastrapur", "Bodakdev", "Satellite", "Paldi",
           "Ashram Road", "Mithakhali", "Navrangpura", "RTO Circle"],
}

trivia_facts = [
    "Did you know? 'Janmarg' means 'The People's Way' in Gujarati.",
    "Did you know? The Ahmedabad BRTS has over 160 stations!",
    "Did you know? Ahmedabad BRTS was India's first full-scale BRTS system!",
    "Did you know? Janmarg won the 'Sustainable Transport Award' in 2010!",
    "Did you know? It was designed by CEPT in Ahmedabad.",
    "Did you know? Janmarg was the first bus service in India to launch a smart card system.",
    "Did you know? Janmarg includes around 150 fully electric buses, helping to reduce pollution.",
    "Did you know? Due to E-buses, Total saved fuel 15433147.90L, GHG emission reduction per day 15503.40 Kg CO2e!",
]

current_language = "English"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def print_box(text):
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    print("╔" + "═" * (max_len + 2) + "╗")
    for line in lines:
        print(f"║ {line.ljust(max_len)} ║")
    print("╚" + "═" * (max_len + 2) + "╝")

def pause(message="Press Enter to continue...."):
    print()
    input(message)

def get_ticket_number():
    try:
        with open(ticket_counter_file, 'r') as f:
            counter = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        counter = 10000
    counter += 1
    try:
        with open(ticket_counter_file, 'w') as f:
            f.write(str(counter))
    except IOError as e:
        print(f"Warning: Could not update ticket counter: {e}")
    return f"JM{counter}"

def ensure_ticket_folder():
    if not os.path.exists(ticket_folder):
        try:
            os.makedirs(ticket_folder)
        except OSError as e:
            print(f"Error creating ticket folder: {e}")

def save_ticket_to_file(ticket_data):
    ensure_ticket_folder()
    ticket_number = ticket_data['ticket_number']
    filename = os.path.join(ticket_folder, f"{ticket_number}.txt")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("╔" + "═" * 78 + "╗\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("║" + "JANMARG BRTS - DIGITAL TICKET".center(78) + "║\n")
            f.write("║" + "Ahmedabad Bus Rapid Transit System".center(78) + "║\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("╚" + "═" * 78 + "╝\n\n")
            
            f.write("TICKET INFORMATION\n")
            f.write("─" * 80 + "\n")
            f.write(f"Ticket Number:          {ticket_data['ticket_number']}\n")
            f.write(f"Booking Date & Time:    {ticket_data['booking_time']}\n")
            f.write(f"Status:                 {ticket_data['status']}\n")
            f.write(f"Valid Until:            {ticket_data['booking_time'][:10]} 23:59:59\n\n")
            
            f.write("PASSENGER DETAILS\n")
            f.write("─" * 80 + "\n")
            f.write(f"Name:                   {ticket_data['passenger_name']}\n")
            f.write(f"Phone:                  {ticket_data['passenger_phone']}\n")
            f.write(f"Passenger Category:     {ticket_data['category']}\n\n")
            
            f.write("JOURNEY DETAILS\n")
            f.write("─" * 80 + "\n")
            f.write(f"From Station:           {ticket_data['from']}\n")
            f.write(f"To Station:             {ticket_data['to']}\n")
            f.write(f"Route Number:           {ticket_data['route']}\n")
            f.write(f"Total Stops:            {ticket_data['stops']}\n")
            
            if 'journey_path' in ticket_data and ticket_data['journey_path']:
                f.write(f"\nJourney Path:\n")
                for i, station in enumerate(ticket_data['journey_path']):
                    if i == 0:
                        f.write(f"   ▶ {station}\n")
                    elif i == len(ticket_data['journey_path']) - 1:
                        f.write(f"   ■ {station}\n")
                    else:
                        f.write(f"   │ {station}\n")
            
            f.write("\n")
            
            f.write("FARE DETAILS\n")
            f.write("─" * 80 + "\n")
            f.write(f"Base Fare:              ₹{ticket_data.get('base_fare', ticket_data['fare']):.2f}\n")
            if ticket_data.get('discount', 0) > 0:
                discount_percent = (ticket_data['discount'] / ticket_data['base_fare']) * 100
                f.write(f"Discount ({discount_percent:.0f}%):          -₹{ticket_data['discount']:.2f}\n")
                f.write(f"{'─' * 40}\n")
            f.write(f"TOTAL FARE:             ₹{ticket_data['fare']:.2f}\n\n")
            
            f.write("╔" + "═" * 78 + "╗\n")
            f.write("║" + "TERMS & CONDITIONS".center(78) + "║\n")
            f.write("╠" + "═" * 78 + "╣\n")
            f.write("║  • This ticket is valid for SINGLE JOURNEY only" + " " * 29 + "║\n")
            f.write("║  • Please show this ticket to the conductor when requested" + " " * 18 + "║\n")
            f.write("║  • Keep this ticket with you until you exit the bus" + " " * 26 + "║\n")
            f.write("║  • Ticket is non-transferable and non-refundable" + " " * 29 + "║\n")
            f.write("║  • This is a computer-generated digital ticket" + " " * 31 + "║\n")
            f.write("╠" + "═" * 78 + "╣\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("║" + "HELPLINE: 1-800-233-2030 | www.ahmedabadbrts.org".center(78) + "║\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("║" + "Thank you for choosing Janmarg! Have a safe journey!".center(78) + "║\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("╚" + "═" * 78 + "╝\n")
        
        return True, filename
    except IOError as e:
        return False, f"File error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def load_all_tickets():
    ensure_ticket_folder()
    tickets = []
    try:
        for filename in os.listdir(ticket_folder):
            if filename.endswith('.txt'):
                tickets.append({'ticket_number': filename.replace('.txt', ''),
                              'filename': filename,
                              'filepath': os.path.join(ticket_folder, filename)})
    except OSError as e:
        print(f"Error loading tickets: {e}")
    return sorted(tickets, key=lambda x: x['ticket_number'], reverse=True)

def show_splash_screen():
    clear_screen()
    print("""
     ██╗ █████╗ ███╗   ██╗███╗   ███╗ █████╗ ██████╗  ██████╗ 
     ██║██╔══██╗████╗  ██║████╗ ████║██╔══██╗██╔══██╗██╔════╝ 
     ██║███████║██╔██╗ ██║██╔████╔██║███████║██████╔╝██║  ███╗
██   ██║██╔══██║██║╚██╗██║██║╚██╔╝██║██╔══██║██╔══██╗██║   ██║
╚█████╔╝██║  ██║██║ ╚████║██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╔╝
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
                                                                
    ███╗   ██╗ █████╗ ██╗   ██╗██╗ ██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
    ████╗  ██║██╔══██╗██║   ██║██║██╔════╝ ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    ██╔██╗ ██║███████║██║   ██║██║██║  ███╗███████║   ██║   ██║   ██║██████╔╝
    ██║╚██╗██║██╔══██║╚██╗ ██╔╝██║██║   ██║██╔══██║   ██║   ██║   ██║██╔══██╗
    ██║ ╚████║██║  ██║ ╚████╔╝ ██║╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║
    ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

                     🚌 The People's Way 🚌
             Ahmedabad Bus Rapid Transit System
                         2025 Edition 
    """)
    time.sleep(1)
    print("                         Loading", end='')
    for _ in range(9):
        print(".", end='', flush=True)
        time.sleep(0.2)
    print("\n                      ✓ Ready!\n")
    time.sleep(0.5)

def search_by_zone():
    print_header("SEARCH STATIONS BY ZONE")
    zone_list = list(ZONES.keys())
    for i, zone in enumerate(zone_list, 1):
        print(f"{i}. {zone:20s} ({len(ZONES[zone])} stations)")
    print()
    choice = input("Select zone number: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(zone_list):
        print("\n❌ Invalid zone!")
        return None
    selected_zone = zone_list[int(choice) - 1]
    stations = sorted(ZONES[selected_zone])
    print(f"\n📍 Stations in {selected_zone}:")
    print("-" * 50)
    for i, station in enumerate(stations, 1):
        print(f"{i:3d}. {station}")
    print()
    station_choice = input("Select station number (or Enter to go back): ").strip()
    if station_choice.isdigit():
        idx = int(station_choice) - 1
        if 0 <= idx < len(stations):
            return stations[idx]
    return None

def autocomplete_station(prompt):
    print(prompt)
    print("(Type station name, 'list' for all, or 'zone' for zone search)")
    while True:
        user_input = input(">>> ").strip()
        if user_input.lower() == 'zone':
            station = search_by_zone()
            if station:
                print(f"✓ Selected: {station}")
                return station
            continue
        if user_input.lower() == 'list':
            stations_list = sorted(all_stations_list)
            print("\n📍 ALL STATIONS:")
            for i, station in enumerate(stations_list, 1):
                if i % 3 == 1:
                    print()
                print(f"{i:3d}. {station:30s}", end='')
            print("\n")
            continue
        if not user_input:
            print("Please enter something.")
            continue
        if user_input.isdigit():
            stations_list = sorted(all_stations_list)
            idx = int(user_input) - 1
            if 0 <= idx < len(stations_list):
                return stations_list[idx]
            else:
                print(f"Invalid. Enter 1-{len(stations_list)}")
                continue
        matches = [s for s in all_stations_list if user_input.lower() in s.lower()]
        if not matches:
            print(f"No match for '{user_input}'.")
            continue
        if len(matches) == 1:
            print(f"✓ Selected: {matches[0]}")
            return matches[0]
        print(f"\n🔍 Found {len(matches)} matches:")
        for i, station in enumerate(matches, 1):
            print(f"{i}. {station}")
        choice = input("Select number (or Enter to search again): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(matches):
                print(f"✓ Selected: {matches[idx]}")
                return matches[idx]

def find_route(start_station, end_station):
    if start_station not in all_stations_list or end_station not in all_stations_list:
        return None, False
    
    # Check for direct routes (including both directions)
    for route_num, stations in brts_routes.items():
        if start_station in stations and end_station in stations:
            start_idx = stations.index(start_station)
            end_idx = stations.index(end_station)
            
            
            if start_idx < end_idx:
                path = stations[start_idx:end_idx + 1]
                return {
                    'type': 'direct',
                    'route_num': route_num,
                    'path': path,
                    'stops': len(path) - 1
                }, True
            elif start_idx > end_idx:
                path = list(reversed(stations[end_idx:start_idx + 1]))
                return {
                    'type': 'direct',
                    'route_num': route_num,
                    'path': path,
                    'stops': len(path) - 1
                }, True
    
    # Routes with interchanges (up to 2 interchanges)
    queue = deque([(start_station, [start_station], [], [])])
    visited = {(start_station, tuple())}
    
    while queue:
        current, path, routes_used, interchanges = queue.popleft()
        
        if len(interchanges) > 2:
            continue
        
        for route_num, stations in brts_routes.items():
            if current not in stations:
                continue
            
            current_idx = stations.index(current)
            
            for direction in [1, -1]:
                idx = current_idx + direction
                while 0 <= idx < len(stations):
                    next_station = stations[idx]
                    
                    route_tuple = tuple(routes_used + [route_num])
                    if (next_station, route_tuple) in visited:
                        idx += direction
                        continue
                    
                    new_path = path + [next_station]
                    new_routes = routes_used.copy()
                    new_interchanges = interchanges.copy()
                    
                    if not new_routes or new_routes[-1] != route_num:
                        new_routes.append(route_num)
                        if len(new_routes) > 1:
                            new_interchanges.append(current)
                    
                    if next_station == end_station:
                        if len(new_interchanges) == 0:
                            return {
                                'type': 'direct',
                                'route_num': route_num,
                                'path': new_path,
                                'stops': len(new_path) - 1
                            }, True
                        elif len(new_interchanges) == 1:
                            interchange_idx = new_path.index(new_interchanges[0])
                            return {
                                'type': 'interchange',
                                'first_route': new_routes[0],
                                'first_path': new_path[:interchange_idx + 1],
                                'interchange': new_interchanges[0],
                                'second_route': new_routes[1],
                                'second_path': new_path[interchange_idx:],
                                'stops': len(new_path) - 1
                            }, False
                        else:
                            return {
                                'type': 'multi_interchange',
                                'routes': new_routes,
                                'path': new_path,
                                'interchanges': new_interchanges,
                                'stops': len(new_path) - 1
                            }, False
                    
                    visited.add((next_station, route_tuple))
                    queue.append((next_station, new_path, new_routes, new_interchanges))
                    
                    idx += direction
    
    return None, False

def calculate_fare(stops, discount_percent=0):
    full_fare = max(5, (stops // 3) * 2 + 5)
    discount_amount = (full_fare * discount_percent) / 100
    return {'full_fare': full_fare, 'discount_percent': discount_percent,
            'discount_amount': discount_amount, 'final_fare': full_fare - discount_amount}

def book_ticket():
    clear_screen()
    print_header("🎫 TICKET BOOKING")
    start = autocomplete_station("🚩 Starting station:")
    print()
    end = autocomplete_station("🏁 Destination station:")
    if start == end:
        print("\n❌ Same station!")
        pause()
        return
    print("\n🔍 Finding route...")
    time.sleep(1)
    route_info, is_direct = find_route(start, end)
    if not route_info:
        print("\n❌ No route found between these stations.")
        print("Please check the station names or try alternative routes.")
        pause()
        return
    
    if route_info['type'] == 'direct':
        stops = route_info['stops']
        route_num = route_info['route_num']
        journey_path = route_info['path']
    elif route_info['type'] == 'interchange':
        first_path = route_info['first_path']
        second_path = route_info['second_path']
        stops = route_info['stops']
        route_num = f"{route_info['first_route']}-{route_info['second_route']}"
        journey_path = first_path + second_path[1:]
    else:
        stops = route_info['stops']
        route_num = "-".join(route_info['routes'])
        journey_path = route_info['path']
    
    clear_screen()
    print_header("💳 PASSENGER DETAILS")
    print("Categories:")
    for key, value in discount_categories.items():
        print(f"[{key}] {value['name']:20s} - {value['description']}")
    print()
    discount_choice = input("Select category [1]: ").strip() or "1"
    if discount_choice not in discount_categories:
        discount_choice = "1"
    category = discount_categories[discount_choice]
    print(f"\n✓ {category['name']}\n")
    passenger_name = input("Name: ").strip() or "Anonymous"
    passenger_phone = input("Phone (optional): ").strip() or "N/A"
    fare_info = calculate_fare(stops, category['discount'])
    
    clear_screen()
    print_header("🎫 CONFIRMATION")
    ticket_number = get_ticket_number()
    booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Ticket: {ticket_number}")
    print(f"Date: {booking_time}")
    print(f"Passenger: {passenger_name}")
    print(f"Category: {category['name']}\n")
    print(f"Journey: {start} → {end}")
    print(f"Route: {route_num} | Stops: {stops}\n")
    
    if route_info['type'] == 'interchange':
        print(f"⚠️  1 Interchange at: {route_info['interchange']}\n")
    elif route_info['type'] == 'multi_interchange':
        print(f"⚠️  {len(route_info['interchanges'])} Interchanges at:")
        for ic in route_info['interchanges']:
            print(f"    → {ic}")
        print()
    
    print("Journey Path:")
    for i, station in enumerate(journey_path):
        if i == 0:
            print(f"   ▶ {station}")
        elif i == len(journey_path) - 1:
            print(f"   ■ {station}")
        else:
            if route_info['type'] in ['interchange', 'multi_interchange']:
                interchanges = [route_info['interchange']] if route_info['type'] == 'interchange' else route_info['interchanges']
                if station in interchanges:
                    print(f"   🔄 {station} (INTERCHANGE)")
                else:
                    print(f"   │ {station}")
            else:
                print(f"   │ {station}")
    
    print(f"\nBase Fare: ₹{fare_info['full_fare']:.2f}")
    if fare_info['discount_percent'] > 0:
        print(f"Discount ({fare_info['discount_percent']}%): -₹{fare_info['discount_amount']:.2f}")
    print(f"TOTAL: ₹{fare_info['final_fare']:.2f}")
    
    confirm = input("\nType 'YES' to confirm: ").strip().upper()
    if confirm != 'YES':
        print("\n❌ Cancelled.")
        pause()
        return
    
    ticket_data = {
        'ticket_number': ticket_number,
        'booking_time': booking_time,
        'passenger_name': passenger_name,
        'passenger_phone': passenger_phone,
        'category': category['name'],
        'from': start,
        'to': end,
        'route': route_num,
        'stops': stops,
        'base_fare': fare_info['full_fare'],
        'fare': fare_info['final_fare'],
        'discount': fare_info['discount_amount'],
        'status': 'Active',
        'journey_path': journey_path
    }
    
    success, result = save_ticket_to_file(ticket_data)
    if success:
        print(f"\n✓ Booked! Saved: {result}")
        print(f"📱 Ticket: {ticket_number}")
        print(f"📂 Location: {os.path.abspath(ticket_folder)}")
    else:
        print(f"\n⚠️ Error: {result}")
    pause()

def view_tickets():
    clear_screen()
    print_header("📋 MY TICKETS")
    tickets = load_all_tickets()
    if not tickets:
        print("No tickets found.")
        pause()
        return
    print(f"Total: {len(tickets)}\n")
    for i, ticket in enumerate(tickets, 1):
        print(f"{i}. {ticket['ticket_number']} - {ticket['filename']}")
    print(f"\n📂 Folder: {os.path.abspath(ticket_folder)}")
    print("\n[V] View  [D] Delete  [Enter] Back")
    choice = input("\nChoice: ").strip().upper()
    if choice == 'V':
        ticket_num = input("Ticket number: ").strip()
        filepath = os.path.join(ticket_folder, f"{ticket_num}.txt")
        if os.path.exists(filepath):
            clear_screen()
            print_header("TICKET DETAILS")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    print(f.read())
            except IOError as e:
                print(f"Error reading ticket: {e}")
            pause()
        else:
            print("Not found!")
            pause()
    elif choice == 'D':
        ticket_num = input("Ticket number: ").strip()
        filepath = os.path.join(ticket_folder, f"{ticket_num}.txt")
        if os.path.exists(filepath):
            confirm = input("Type 'DELETE': ").strip().upper()
            if confirm == 'DELETE':
                try:
                    os.remove(filepath)
                    print("\n✓ Deleted!")
                except OSError as e:
                    print(f"\n❌ Error deleting: {e}")
            else:
                print("\n❌ Cancelled.")
            pause()
        else:
            print("Not found!")
            pause()

def feature_find_route():
    clear_screen()
    print_header("🗺️  ROUTE FINDER")
    start = autocomplete_station("🚩 Starting station:")
    print()
    end = autocomplete_station("🏁 Destination station:")
    if start == end:
        print("\n❌ Same station!")
        pause()
        return
    print("\n🔍 Searching...")
    time.sleep(1)
    route_info, is_direct = find_route(start, end)
    if not route_info:
        print("\n❌ No route found between these stations.")
        print("Please check the station names or try alternative routes.")
        pause()
        return
    clear_screen()
    print_header("🎉 ROUTE FOUND")
    
    if route_info['type'] == 'direct':
        print(f"✓ DIRECT ROUTE\n🚌 Route {route_info['route_num']}")
        print(f"📍 {start} → 🏁 {end}")
        print(f"🛑 Stops: {route_info['stops']}\n")
        for i, station in enumerate(route_info['path']):
            symbol = "▶" if i == 0 else ("■" if i == len(route_info['path'])-1 else "│")
            print(f"   {symbol} {station}")
    elif route_info['type'] == 'interchange':
        print("🔄 ROUTE WITH INTERCHANGE\n")
        first_path = route_info['first_path']
        second_path = route_info['second_path']
        print(f"1️⃣ FIRST LEG:")
        print(f"   🚌 Route {route_info['first_route']} from {first_path[0]}")
        print(f"   🛑 {len(first_path) - 1} stops")
        for station in first_path[1:-1]:
            print(f"      → {station}")
        print(f"   🔄 INTERCHANGE at {route_info['interchange']}\n")
        print(f"2️⃣ SECOND LEG:")
        print(f"   🚌 Route {route_info['second_route']} from {second_path[0]}")
        print(f"   🛑 {len(second_path) - 1} stops")
        for station in second_path[1:-1]:
            print(f"      → {station}")
        print(f"   ✓ Arrive at {end}")
    else:
        print(f"🔄 ROUTE WITH {len(route_info['interchanges'])} INTERCHANGES\n")
        print(f"📍 {start} → 🏁 {end}")
        print(f"🛑 Total Stops: {route_info['stops']}\n")
        print("Complete Journey:")
        for i, station in enumerate(route_info['path']):
            if i == 0:
                print(f"   ▶ {station} (START)")
            elif i == len(route_info['path']) - 1:
                print(f"   ■ {station} (END)")
            elif station in route_info['interchanges']:
                print(f"   🔄 {station} (INTERCHANGE)")
            else:
                print(f"   │ {station}")
        print(f"\n🚌 Routes: {' → '.join(route_info['routes'])}")
    
    estimated_time = route_info['stops'] * 2.5
    print(f"\n⏱️  Estimated Time: ~{estimated_time:.0f} minutes")
    pause()

def feature_list_all_stations():
    clear_screen()
    print_header("📍 ALL STATIONS")
    stations_list = sorted(all_stations_list)
    print(f"Total: {len(stations_list)}\n")
    cols = 3
    rows = (len(stations_list) + cols - 1) // cols
    for row in range(rows):
        line = ""
        for col in range(cols):
            idx = row + col * rows
            if idx < len(stations_list):
                line += f"{idx + 1:3d}. {stations_list[idx]:25s}  "
        print(line)
    print()
    pause()

def feature_zone_wise_stations():
    clear_screen()
    print_header("🗺️  ZONE-WISE STATIONS")
    zone_list = list(ZONES.keys())
    for i, zone in enumerate(zone_list, 1):
        print(f"[{i}] {zone:20s} ({len(ZONES[zone])} stations)")
    print()
    choice = input("Select zone (or Enter to go back): ").strip()
    if not choice:
        return
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(zone_list):
        print("\n❌ Invalid!")
        pause()
        return
    selected_zone = zone_list[int(choice) - 1]
    stations = sorted(ZONES[selected_zone])
    clear_screen()
    print_header(f"📍 {selected_zone.upper()} ZONE")
    print(f"Total: {len(stations)}\n")
    for i, station in enumerate(stations, 1):
        if i % 2 == 1:
            print(f"{i:3d}. {station:35s}", end='')
        else:
            print(f"{i:3d}. {station}")
    if len(stations) % 2 == 1:
        print()
    print()
    pause()

def feature_show_map():
    clear_screen()
    print_header("🗺️  BRTS NETWORK MAP")
    print("""
══════════════════════════════════════════════════════════════════════
                           NORTH-EAST ZONE
══════════════════════════════════════════════════════════════════════

         [ONGC]───[Visat]───[IOC Road]───[Janta Nagar]
            |                                   |
      [Chandranagar]              [Vishwakarma Govt Engineering College]
                                                |
                                        [Zundal Circle]
                                                |
                                    [Naroda ST Workshop]
                                                |
                            [Naroda Gam]────[Naroda]────[Dahegam Circle]
                                    |           |
                                [Nikol]     [Ramol]
                                    |           |
                            [Odhav Ring Road]  [Memco]
                                    |           |
                                [Odhav]─────[Vastral]
                                    |           |
                                [Rakhial]   [Narol]
                                    |           |
                            [CTM]──[CTM Cross Roads]──[Nirnay Nagar]
                              |                           |
                        [Lal Darwaja]              [Isanpur Depot]
                              |                           |
                        [Town Hall]                  [Isanpur]
                              |                           |
══════════════════════════════════════════════════════════════════════
                          NORTH ZONE
══════════════════════════════════════════════════════════════════════

                          [Airport]
                              |
                      [Motera Stadium]
                              |
                          [Motera]
                              |
                        [Sabarmati]
                              |
              [Sabarmati Police Station]
                              |
              [Sabarmati Power House]
                              |
                      [Subhash Bridge]
                              |
    [Chandkheda]──[Chandkheda Gam]──[Chandkheda Police Station]
         |
      [Gota]──[Gota Cross Road]──[Kudasan]
         |                            |
      [Ranip]──[Ranip Cross Roads]──[New Ranip]──[Ranip GSRTC]
                                                        |
══════════════════════════════════════════════════════════════════════
                        NORTH-WEST ZONE
══════════════════════════════════════════════════════════════════════

    [Bhadaj Circle]──[Science City Approach]──[AUDA Garden]
                                    |
                            [Sola Bhagwat]
                                    |
                    [Sola Bridge]──[Sola]──[Sola Cross Roads]
                            |       |              |
                        [SGVP]  [Shilaj]     [Jaymangal]
                            |       |              |
                       [Thaltej] [Ognaj]    [Navrangpura]
                            |                      |
                       [Vastrapur]          [Usmanpura]
                            |                      |
                                            [Vadaj]──[Juna Vadaj]
                                                |
                                        [Juna Wadaj Circle]
                                                |
══════════════════════════════════════════════════════════════════════
                    WEST ZONE (EXPANDED)
══════════════════════════════════════════════════════════════════════

    [Vastrapur]──[Bodakdev]──[Satellite]
         |            |            |
    [Memnagar]──[Gurukul]──[Jodhpur]──[Vijay Nagar]
         |            |            |
    [Nehrunagar]──[Ambawadi]──[Panchvati]
         |            |            |
      [Paldi]────[Mithakhali]──[Parimal Garden]
         |            |            |
    [Ashram Road]  [RTO Circle]──[RTO]──[Camp Hanuman]
         |            |                       |
    [Kankaria Lake]  [Naranpura]      [Bhavsar Hostel]
         |                  |                |
    [Kankaria Zoo]   [Gujarat University]  [Akhbarnagar]
         |                  |                |
      [Khokhra]      [Commerce Six Roads]  [Pragatinagar]
         |                  |                |
    [Khodiyar Nagar] [L D College]    [Shastrinagar]
         |                  |                |
    [Amraiwadi]         [ST Stand]     [M K Shah College]
         |                  |                |
══════════════════════════════════════════════════════════════════════
                        CENTRAL ZONE (DETAILED)
══════════════════════════════════════════════════════════════════════

                        [Town Hall]
                              |
                    [Kalupur Railway Station]
                              |
                        [Kalupur]
                /             |              \
         [Geeta Mandir]  [Lal Darwaja]  [Shah-e-Alam]
               |              |                |
           [Anjali]     [Delhi Darwaja]   [Dariapur]
               |              |                |
         [Maninagar]    [Soni ni Chali]  [Sarangpur]
               |              |                |
    [Maninagar Railway]  [Idgah]        [Camp Hanuman]
         Station         |                    |
               |      [Dudheshwar]       [RTO Circle]
               |         |
    [Maninagar Depot]──[Maninagar Terminus]
               |
         [Bapunagar]──[Amraiwadi]
               |
         [Bage Firdos]──[Gomtipur]

══════════════════════════════════════════════════════════════════════
                    SOUTH & SOUTH-WEST ZONE (COMPLETE)
══════════════════════════════════════════════════════════════════════

         [Vasna]──[IIM]──[Keshavbaug]
                   |
              [Lokmanya Tilak]
                   |
         [Shivranjani]──[ISKCON Cross Road]──[Bopal Approach]
              |                  |                   |
         [Bodakdev]      [Amba Township]      [Bopal Junction]
                                |                   |
                        [Vasantnagar Township]  [Bopal Gam]
                                |                   |
                          [DCIS Circle]         [Bopal ST]
                                |                   |
                           [Makarba]          [South Bopal]
                                |                   |
                           [Sarkhej]           [Ghuma Gam]


 ══════════════════════════════════════════════════════════════════════
                    MAJOR INTERCHANGE STATIONS
══════════════════════════════════════════════════════════════════════

 KALUPUR: 6+ routes (Largest Hub + Railway Connection)
 NAVRANGPURA: 5 routes (Major West-North Connector)
 MANINAGAR: 5 routes (Eastern Hub)
 VASTRAPUR: 4 routes (Western Hub)
 PALDI: 4 routes (West-Central Link)
 ANJALI: 4 routes (Central-East Connector)
 SABARMATI: 3 routes (Northern Hub)
 SOLA: 3 routes (NW Connector)
 ISKCON: 3 routes (SW Hub)

══════════════════════════════════════════════════════════════════════
                    NETWORK STATISTICS (2025)
══════════════════════════════════════════════════════════════════════

Total Routes:                15 major routes
Total Stations:              150+ stations across 8 zones
Network Coverage:            ~160 km operational
Daily Ridership:             ~350,000+ passengers
Fleet Size:                  220+ buses (AC & Non-AC)
Operational Hours:           05:30 AM - 11:00 PM
Average Frequency:           5-15 minutes (peak), 15-30 min (off-peak)
Fare Range:                  ₹5 - ₹50 (based on distance)


    """)
    print_box("""🌐 Official Interactive Map:
   https://www.ahmedabadbrts.org/plan/

📱 Scan QR at any BRTS station""")
    pause()

def feature_explore_route():
    clear_screen()
    print_header("🚍 ROUTE EXPLORER")
    print("Available Routes:")
    for route_num in sorted(brts_routes.keys(), key=lambda x: int(x)):
        stations = brts_routes[route_num]
        print(f"  Route {route_num:2s}: {stations[0]} ↔ {stations[-1]} ({len(stations)} stations)")
    print()
    route_choice = input("Enter route number: ").strip()
    if route_choice not in brts_routes:
        print("\n❌ Invalid!")
        pause()
        return
    clear_screen()
    print_header(f"🚍 ROUTE {route_choice} JOURNEY")
    stations = brts_routes[route_choice]
    print(f"Total Stops: {len(stations)}\n")
    time.sleep(0.5)
    for i, station in enumerate(stations):
        indent = "  " * (i % 3)
        print(f"🚌 Route {route_choice}: {indent}→ {station}")
        time.sleep(0.3)
    print("\n✓ Journey complete!")
    pause()

def feature_fare_calculator():
    clear_screen()
    print_header("💰 FARE CALCULATOR")
    start = autocomplete_station("🚩 Starting:")
    print()
    end = autocomplete_station("🏁 Destination:")
    if start == end:
        print("\n❌ Same station!")
        pause()
        return
    route_info, _ = find_route(start, end)
    if not route_info:
        print("\n❌ No route found.")
        pause()
        return
    stops = route_info['stops']
    clear_screen()
    print_header("💳 SELECT CATEGORY")
    for key, value in discount_categories.items():
        print(f"[{key}] {value['name']:20s} - {value['description']}")
    print()
    category_choice = input("Category [1]: ").strip() or "1"
    if category_choice not in discount_categories:
        category_choice = "1"
    category = discount_categories[category_choice]
    fare_info = calculate_fare(stops, category['discount'])
    clear_screen()
    print_header("💳 FARE BREAKDOWN")
    print(f"📍 From: {start}")
    print(f"🏁 To: {end}")
    print(f"🛑 Stops: {stops}")
    print(f"👤 Category: {category['name']}\n")
    print("-" * 60)
    print(f"Base Fare:              ₹{fare_info['full_fare']:.2f}")
    if fare_info['discount_percent'] > 0:
        print(f"Discount ({fare_info['discount_percent']}%):           -₹{fare_info['discount_amount']:.2f}")
    print("=" * 60)
    print(f"TOTAL:                  ₹{fare_info['final_fare']:.2f}")
    print("=" * 60)
    if fare_info['discount_percent'] > 0:
        print(f"\n💰 You save ₹{fare_info['discount_amount']:.2f}!")
    pause()

def feature_trivia():
    clear_screen()
    print_header("💡 JANMARG TRIVIA")
    fact = random.choice(trivia_facts)
    for char in fact:
        print(char, end='', flush=True)
        time.sleep(0.03)
    print("\n")
    pause()

def feature_bus_timings():
    clear_screen()
    print_header("🕐 BUS TIMINGS")
    print_box("""Most BRTS services run:

🌅 First Bus: 6:00 AM
🌙 Last Bus: 11:00 PM

⏱️  Frequency: Every 10-15 minutes

Check official sources for exact timings.""")
    print("\n📞 Helpline: 1-800-233-2030")
    pause()

def feature_help_about():
    clear_screen()
    print_header("ℹ️  HELP & ABOUT")
    print("JANMARG NAVIGATOR v3.2 - Features:\n")
    features = [
        ("1", "Find Route", "Best route between stations"),
        ("2", "List Stations", "All 162 BRTS stations"),
        ("3", "Zone Stations", "Browse by zone"),
        ("4", "Show Map", "Network map"),
        ("5", "Explore Route", "All stops on route"),
        ("6", "Fare Calculator", "Calculate with discounts"),
        ("7", "Trivia", "BRTS facts"),
        ("8", "Bus Timings", "Schedule info"),
        ("9", "Help/About", "This screen"),
        ("10", "Book Ticket", "Digital ticket booking"),
        ("11", "View Tickets", "Ticket history"),
        ("12", "Emergency", "Helpline numbers"),
    ]
    for num, name, desc in features:
        print(f"[{num:>2s}] {name:20s} - {desc}")
    print("\n" + "=" * 80)
    print("Enhanced BRTS navigation with comprehensive routing & ticket booking")
    print("Created with ❤️ for Ahmedabad")
    print("=" * 80)
    pause()

def feature_emergency_contacts():
    clear_screen()
    print_header("📞 EMERGENCY CONTACTS")
    print_box("""🚌 Janmarg Helpline:
   1-800-233-2030 (Toll-free, 24/7)

🚨 City Emergency Services:
   Police: 100
   Ambulance: 108
   Fire: 101

🏥 Medical Emergency: 108

👮 Women's Helpline: 1091

🚔 Traffic Police: 103""")
    print("\n⚠️  Save these numbers!")
    pause()

def show_main_menu():
    clear_screen()
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + "JANMARG NAVIGATOR v3.2".center(78) + "║")
    print("║" + "Ahmedabad Bus Rapid Transit System".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    menu_items = [
        ("1", "🗺️  Find Route (Start → End)"),
        ("2", "📍 List All 162 Stations"),
        ("3", "🗺️  Zone-Wise Station Browser"),
        ("4", "🗺️  Show BRTS Network Map"),
        ("5", "🚍 Explore a Route"),
        ("6", "💰 Fare Calculator with Discounts"),
        ("7", "💡 Janmarg Trivia"),
        ("8", "🕐 First/Last Bus Timings"),
        ("9", "ℹ️  Help / About"),
        ("10", "🎫 Book Digital Ticket"),
        ("11", "📋 View My Tickets"),
        ("12", "📞 Emergency Contacts"),
        ("Q", "🚪 Quit"),
    ]
    print("    MAIN MENU")
    print("    " + "─" * 70)
    print()
    for num, name in menu_items:
        print(f"    [{num:>2s}]  {name}")
    print()
    print("    " + "─" * 70)
    print(f"    Language: {current_language} | Routes: 15 | Stations: {len(all_stations_list)}")
    print("    " + "═" * 70)
    print()

def main():
    show_splash_screen()
    while True:
        show_main_menu()
        choice = input("    Enter choice: ").strip().upper()
        if choice == "1":
            feature_find_route()
        elif choice == "2":
            feature_list_all_stations()
        elif choice == "3":
            feature_zone_wise_stations()
        elif choice == "4":
            feature_show_map()
        elif choice == "5":
            feature_explore_route()
        elif choice == "6":
            feature_fare_calculator()
        elif choice == "7":
            feature_trivia()
        elif choice == "8":
            feature_bus_timings()
        elif choice == "9":
            feature_help_about()
        elif choice == "10":
            book_ticket()
        elif choice == "11":
            view_tickets()
        elif choice == "12":
            feature_emergency_contacts()
        elif choice == "Q":
            clear_screen()
            print()
            print("╔" + "═" * 78 + "╗")
            print("║" + " " * 78 + "║")
            print("║" + "Thank you for using Janmarg Navigator!".center(78) + "║")
            print("║" + " " * 78 + "║")
            print("║" + "🚌 Have a safe journey! 🚌".center(78) + "║")
            print("║" + " " * 78 + "║")
            print("║" + "જય જનમાર્ગ! (Jay Janmarg!)".center(78) + "║")
            print("║" + " " * 78 + "║")
            print("╚" + "═" * 78 + "╝")
            print()
            time.sleep(1)
            break
        else:
            print("\n    ❌ Invalid choice!")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + "Program interrupted by user".center(78) + "║")
        print("║" + "Thank you for using Janmarg Navigator!".center(78) + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please report this issue.")
        print()
        sys.exit(1)
