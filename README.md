# 🏠 Smart Home Automation System

A Wi-Fi-based smart home automation system that allows users to remotely control electrical appliances (e.g., bulbs, fans) via an Android application. The system integrates ESP8266 microcontroller with a Django REST API backend and Firebase Realtime Database for real-time device state synchronization.

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [System Architecture](#️-system-architecture)
- [Hardware Components](#-hardware-components)
- [Software Requirements](#-software-requirements)
- [Project Setup](#️-project-setup)
- [How It Works](#-how-it-works)
- [Use Case Diagram](#-use-case-diagram)
- [Team Roles & Responsibilities](#-team-roles--responsibilities)
- [Installation Guide](#-installation-guide)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🔍 Project Overview

This project aims to simplify home automation using cost-effective and scalable components. It provides users with control over home appliances through an Android app, making the home smarter and more energy-efficient. The system leverages IoT principles to create a seamless, real-time control loop between user and device.

## ✨ Features

- **Remote Control**: ON/OFF control of appliances via Android app
- **Real-time Sync**: Live device status tracking and updates
- **Secure Communication**: API-based communication with authentication
- **Persistent State**: Firebase sync for reliable state management
- **Scalable Design**: Cost-efficient hardware integration
- **Modern UI**: Cross-platform interface using Jetpack Compose (Kotlin)
- **IoT Integration**: Seamless ESP8266 microcontroller integration

## 🏗️ System Architecture

```
[Android App] ⇄ [Django REST API] ⇄ [Firebase DB]
     ↓                                    ↑
  [HTTP Commands]       ⇄        [ESP8266 NodeMCU]
                              ↓
                      [Relay → Bulb/Fan]
```

## 🧰 Hardware Components

| Component | Description |
|-----------|-------------|
| **ESP8266 NodeMCU** | Wi-Fi-enabled microcontroller |
| **Relay Module** | Switches 220V AC appliances safely |
| **LED/Fan/Bulb** | Electrical appliance for testing/demo |
| **Breadboard** | For circuit prototyping |
| **Jumper Wires** | To connect circuit components |
| **Power Adapter** | 5V USB power supply for NodeMCU |

## 💻 Software Requirements

| Software/Tool | Purpose |
|---------------|---------|
| **Arduino IDE** | Programming the ESP8266 NodeMCU |
| **ESP8266 Board Package** | Enables ESP support in Arduino IDE |
| **Django (Python)** | REST API backend |
| **Firebase Realtime DB** | Stores device state and syncs with ESP |
| **Jetpack Compose** | Kotlin UI framework for Android App |
| **Postman** | Testing API endpoints |
| **Firebase Admin SDK** | Python module to access Firebase |

## 🛠️ Project Setup

### 1. ESP8266 Firmware
- Install ESP8266 board in Arduino IDE
- Connect to Wi-Fi and Firebase using Arduino code
- Listen for ON/OFF commands from Firebase and control relay

### 2. Django Backend
- Expose APIs: `/appliance/on`, `/appliance/off`, `/status`
- Authenticate requests and push commands to Firebase
- Use Django REST Framework for simplicity

### 3. Android App (Jetpack Compose)
- Login or register user
- UI buttons for each appliance (toggle state)
- API calls to Django endpoints
- Display real-time status using Firebase listeners

## 💡 ESP8266 Web Server - Bulb Controller

This example demonstrates a **standalone ESP8266 web server** that allows controlling a bulb (or LED) directly from a browser without needing the Django/Firebase stack.

### 🔧 Hardware Setup
1. **ESP8266 Board** (NodeMCU or Wemos D1 Mini)  
2. **Relay Module** (for AC bulb) OR LED with resistor  
3. **Jumper Wires**  

### ⚡ Wiring
- **Using Relay**  
  - ESP8266 **D1 (GPIO5)** → Relay IN pin  
  - ESP8266 **VIN** → Relay VCC  
  - ESP8266 **GND** → Relay GND  

- **Using LED (for testing)**  
  - ESP8266 **D1 (GPIO5)** → LED long leg (+)  
  - LED short leg (–) → 220Ω resistor → ESP8266 **GND**  

### 📲 How to Use
1. Update Wi-Fi credentials (`ssid`, `password`) in the Arduino sketch  
2. Set `bulbPin = D1` (GPIO5 by default)  
3. Upload the sketch via Arduino IDE  
4. Open **Serial Monitor** at **115200 baud** to see ESP’s IP address  
5. Access from browser (on same Wi-Fi):  
   - `http://<ESP_IP>/on` → Turn bulb **ON**  
   - `http://<ESP_IP>/off` → Turn bulb **OFF**  
   - `http://<ESP_IP>/` → Control panel with buttons  

---

## 🧩 How It Works

1. **User Interaction**: User opens the Android app and taps the appliance toggle
2. **API Request**: App sends a POST request to Django API with the command
3. **Database Update**: Django pushes command to Firebase Realtime Database
4. **Device Response**: ESP8266 listens for changes in Firebase node, reads the command
5. **Physical Control**: ESP8266 triggers relay module to control the appliance
6. **State Sync**: ESP8266 updates the device state back to Firebase
7. **UI Update**: App updates UI based on Firebase real-time changes

## 📊 Use Case Diagram

### Actors:
- **User** (Phone App)
- **ESP8266** (Controller)
- **Django Server** (API)
- **Firebase** (State DB)

### Use Cases:
- User logs in and sends command
- Server processes and stores the command
- ESP8266 reads from Firebase and toggles relay
- Device state updated and reflected back in app

## 👥 Team Roles & Responsibilities

### 1. **Pradeep Soni** – Backend & Android Developer
- Designed and implemented Android application with Jetpack Compose
- Developed Django backend with RESTful API for command handling
- Integrated Firebase Admin SDK with Django server

### 2. **Divyansh Sharma** – UI/UX & Embedded Developer
- Programmed ESP8266 to fetch and execute Firebase commands
- Managed app-to-server communication and error handling
- Built real-time UI using Firebase SDK

## 📦 Installation Guide

### Prerequisites
- Python 3.8+
- Arduino IDE
- Android Studio
- Firebase Project Setup

### Backend Setup
```bash
# Clone the repository
git clone <repository-url>
cd smart-home-automation

# Install Python dependencies
pip install -r requirements.txt

# Configure Firebase credentials
# Add your Firebase service account key to the project

# Run Django server
python manage.py runserver
```

### ESP8266 Setup
```cpp
// Install required libraries in Arduino IDE:
// - ESP8266WiFi
// - FirebaseESP8266
// - ArduinoJson

// Upload the firmware to ESP8266
```

### Android App Setup
```bash
# Open project in Android Studio
# Add Firebase configuration file (google-services.json)
# Build and install the APK
```

## 📋 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/appliance/on` | Turn appliance ON |
| POST | `/appliance/off` | Turn appliance OFF |
| GET | `/status` | Get current device status |

### Request/Response Examples

```json
// POST /appliance/on
{
  "device_id": "living_room_light",
  "user_id": "user123"
}

// Response
{
  "status": "success",
  "message": "Appliance turned ON",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🚀 Future Enhancements

- Voice control integration (Google Assistant/Alexa)
- Scheduling and automation rules
- Energy consumption monitoring
- Multiple user support
- Web dashboard interface
- Support for more device types

## 📞 Support

For support and questions, please contact:
- **Pradeep Soni**: [email/contact]
- **Divyansh Sharma**: [email/contact]

## ⭐ Acknowledgments

- ESP8266 Community for excellent documentation
- Firebase team for real-time database services
- Django REST Framework contributors

---

## ✅ Conclusion

This Smart Home Automation System is a low-cost, scalable, and intuitive solution built with modern technology stacks. It bridges IoT hardware and real-time software interfaces, enabling users to securely control home appliances from anywhere. The project showcases effective integration of microcontrollers, web APIs, mobile development, and cloud databases.

**Built with ❤️ by the Smart Home Team**
