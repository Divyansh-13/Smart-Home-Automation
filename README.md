<div align="center">

<img src="https://img.shields.io/badge/NodeMCU-ESP8266-blue?style=for-the-badge&logo=arduino&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/MediaPipe-Hand%20Gesture-FF6F00?style=for-the-badge&logo=google&logoColor=white"/>
<img src="https://img.shields.io/badge/OpenCV-Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>
<img src="https://img.shields.io/badge/IoT-Smart%20Home-green?style=for-the-badge"/>

<br/><br/>

# Hand Gesture–Controlled Smart Home Automation Prototype (Two-Bulb System)

### Control two AC bulbs with hand gestures — no physical switch needed.
### NodeMCU ESP8266 + Dual Channel Relay + Python MediaPipe + WiFi

<br/>

> **Show a gesture → Python detects it → HTTP request over WiFi → NodeMCU fires relay → Bulb switches**

<br/>

</div>

---

## Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Hardware Used](#-hardware-used)
- [Circuit Diagram](#-circuit-diagram)
- [Wiring Table](#-wiring-table)
- [Gesture Map](#-gesture-map)
- [Software Stack](#-software-stack)
- [Project Structure](#-project-structure)
- [Setup Guide](#-setup-guide)
- [How It Works](#-how-it-works)
- [Demo](#-demo)
- [Future Improvements](#-future-improvements)

---

## Overview

This project builds a **contactless smart lighting system** using computer vision and IoT hardware. A Python script running on a PC detects hand gestures in real time using **MediaPipe**. Each gesture maps to a command that is sent over **WiFi** as an HTTP request to a **NodeMCU ESP8266** board. The NodeMCU hosts a lightweight web server and controls two AC bulbs through a **dual channel relay module**.

No cloud. No app. Just your hand.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PC / Laptop                              │
│                                                                 │
│   ┌──────────┐    ┌──────────────┐    ┌─────────────────────┐  │
│   │  Webcam  │───▶│  OpenCV      │───▶│  MediaPipe          │  │
│   │          │    │  (capture)   │    │  (hand landmarks)   │  │
│   └──────────┘    └──────────────┘    └────────┬────────────┘  │
│                                                │               │
│                                    ┌───────────▼─────────────┐ │
│                                    │  Finger counter          │ │
│                                    │  Gesture → command map   │ │
│                                    └───────────┬─────────────┘ │
│                                                │               │
│                                    ┌───────────▼─────────────┐ │
│                                    │  HTTP GET request        │ │
│                                    │  requests.get(ESP_IP)    │ │
│                                    └───────────┬─────────────┘ │
└────────────────────────────────────────────────┼───────────────┘
                                                 │  WiFi (same network)
                                    ┌────────────▼────────────────┐
                                    │     NodeMCU ESP8266          │
                                    │   ESP8266WebServer (port 80) │
                                    │   Routes: /r1/on  /r2/on     │
                                    │           /r1/off /r2/off    │
                                    │           /all/on /all/off   │
                                    └──────┬──────────┬───────────┘
                                           │D1        │D2
                                    ┌──────▼──────────▼───────────┐
                                    │   Dual Channel Relay (5V)    │
                                    │   IN1 (CH1)    IN2 (CH2)     │
                                    └──────┬──────────┬───────────┘
                                           │          │
                                    ┌──────▼──┐  ┌───▼──────┐
                                    │ Bulb 1  │  │  Bulb 2  │
                                    │  AC     │  │  AC      │
                                    └─────────┘  └──────────┘
```

---

## Hardware Used

| Component | Specification | Purpose |
|---|---|---|
| **NodeMCU ESP8266** | ESP-12E, 3.3V logic, built-in WiFi | Microcontroller + web server |
| **Dual Channel Relay Module** | 5V coil, 10A/250VAC contacts | Switch AC bulbs electronically |
| **AC Bulb × 2** | Any standard bulb (LED/CFL) | Output — the loads being controlled |
| **Jumper wires** | Male-to-female | Connect NodeMCU pins to relay |
| **USB Cable** | Micro USB | Power NodeMCU + upload code |
| **PC with Webcam** | Python 3.10, USB/built-in cam | Run gesture detection |
| **WiFi Hotspot** | Mobile hotspot or router | Connect PC and NodeMCU |

---

## Circuit Diagram

```
                    ┌─────────────────────────────────────┐
                    │         NodeMCU ESP8266              │
                    │                                      │
                    │  VIN  ──────────────── 5V ──────┐   │
                    │  GND  ──────────────── GND ──┐  │   │
                    │  D1 (GPIO5) ─────── IN1 ──┐  │  │   │
                    │  D2 (GPIO4) ─────── IN2 ┐ │  │  │   │
                    │                         │ │  │  │   │
                    └─────────────────────────┼─┼──┼──┼───┘
                                              │ │  │  │
                               ┌──────────────┘ │  │  │
                               │  ┌─────────────┘  │  │
                               │  │  ┌─────────────┘  │
                               │  │  │  ┌─────────────┘
                               ▼  ▼  ▼  ▼
                    ┌──────────────────────────────────────┐
                    │       Dual Channel Relay Module       │
                    │                                       │
                    │  IN1   IN2   GND   VCC                │
                    │                                       │
                    │  ┌───────────┐   ┌───────────┐       │
                    │  │ Relay CH1 │   │ Relay CH2 │       │
                    │  │ COM1 NO1  │   │ COM2 NO2  │       │
                    └──┼───┬──┬───┼───┼───┬──┬────┼───────┘
                         │  │  │       │  │  │
                         │  │  └──┐    │  │  └──┐
                 LIVE ───┴──┘     │    ┴──┘     │
                 (AC)         ┌───┘         ┌───┘
                              │             │
                           ┌──▼──┐       ┌──▼──┐
                           │Bulb1│       │Bulb2│
                           └──┬──┘       └──┬──┘
                              │             │
                 NEUTRAL ──────┴─────────────┘
                 (AC, direct)
```

> **WARNING:** Always wire the AC side with the power completely disconnected. 220V is lethal. Double-check COM and NO terminals before powering on.

---

## 🔗 Wiring Table

### DC Side — NodeMCU to Relay (safe, low voltage)

| NodeMCU Pin | Wire Color | Relay Pin | Notes |
|---|---|---|---|
| VIN | Orange | VCC | 5V power to relay |
| GND | Black | GND | Common ground |
| D1 (GPIO5) | Blue | IN1 | Controls Bulb 1 |
| D2 (GPIO4) | Green | IN2 | Controls Bulb 2 |

### AC Side — Relay to Bulbs (mains voltage — wire with power OFF)

| From | To | Notes |
|---|---|---|
| Wall LIVE | COM1 | AC live input to relay CH1 |
| COM1 → COM2 | Jumper | Bridge live to both channels |
| NO1 | Bulb 1 wire A | Switched live to Bulb 1 |
| NO2 | Bulb 2 wire A | Switched live to Bulb 2 |
| Wall NEUTRAL | Bulb 1 wire B | Direct neutral — no switch |
| Wall NEUTRAL | Bulb 2 wire B | Direct neutral — no switch |

> **Key concept:** Neutral goes directly to both bulbs. Only the LIVE wire is switched by the relay. When the relay closes, it completes the circuit and the bulb lights.

---

## Gesture Map

| Gesture | Fingers Up | Command | Result |
|---|---|---|---|
| ✊ Fist | 0 | `/all/off` | Both bulbs OFF |
| ☝️ Index only | 1 | `/r1/on` | Bulb 1 ON |
| ✌️ Two fingers | 2 | `/r2/on` | Bulb 2 ON |
| 🤟 Three fingers | 3 | `/all/on` | Both bulbs ON |
| 🖐️ Open hand | 5 | `/all/on` | Both bulbs ON |

> The system only sends a new command when the gesture **changes** — preventing spam requests to the NodeMCU.

---

## 💻 Software Stack

| Layer | Technology | Version | Role |
|---|---|---|---|
| Gesture detection | MediaPipe | 0.10.9 | Detect 21 hand landmarks |
| Image capture | OpenCV | 4.x | Read webcam frames |
| HTTP client | Python requests | latest | Send commands to NodeMCU |
| Microcontroller | Arduino (ESP8266) | latest | Web server + GPIO control |
| Web server lib | ESP8266WebServer | built-in | Handle HTTP routes |
| Network | WiFi (local) | — | NodeMCU ↔ PC communication |

---

## 📁 Project Structure

```
hand-gesture-smart-bulbs/
│
├── arduino/
│   └── dual_relay_2bulb.ino      # NodeMCU web server code
│
├── python/
│   └── gesture_control.py        # Hand gesture detection + HTTP control
│
├── assets/
│   └── circuit_diagram.png       # Circuit wiring diagram
│
└── README.md
```

---

## 🚀 Setup Guide

### Step 1 — Flash the NodeMCU

1. Install [Arduino IDE](https://www.arduino.cc/en/software)
2. Add ESP8266 board support:
   - Go to **File → Preferences**
   - Add this URL to Additional Board Manager URLs:
     ```
     http://arduino.esp8266.com/stable/package_esp8266com_index.json
     ```
3. Go to **Tools → Board → Board Manager** → search `esp8266` → install
4. Select board: **NodeMCU 1.0 (ESP-12E Module)**
5. Open `arduino/dual_relay_2bulb.ino`
6. Update your WiFi credentials:
   ```cpp
   const char* ssid     = "YOUR_WIFI_NAME";
   const char* password = "YOUR_WIFI_PASSWORD";
   ```
7. Upload → open **Serial Monitor at 115200 baud**
8. Note the IP address printed:
   ```
   WiFi Connected!
   Open in browser: http://10.x.x.x
   ```

---

### Step 2 — Set up Python environment

```bash
# Requires Python 3.10 — not 3.12+
py -3.10 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install opencv-python mediapipe==0.10.9 requests
```

---

### Step 3 — Configure and run

1. Open `python/gesture_control.py`
2. Update the NodeMCU IP:
   ```python
   ESP_IP = "http://10.x.x.x"   # IP from Serial Monitor
   ```
3. Make sure your PC and NodeMCU are on the **same WiFi network**
4. Run:
   ```bash
   python gesture_control.py
   ```

---

### Step 4 — Test

A webcam window opens. Show gestures to the camera:
- Your hand skeleton is drawn in real time
- Bulb status (ON/OFF) is shown at the bottom of the window
- Press `ESC` to quit

---

## ⚙️ How It Works

### Gesture detection
MediaPipe returns 21 landmark coordinates for each detected hand. The script compares each fingertip Y-coordinate against its base knuckle — if the tip is higher (lower Y value) the finger is considered raised. The thumb uses X-axis comparison instead.

### Command deduplication  
The `last_command` variable stores the most recently sent command. A new HTTP request is only triggered when the gesture changes, preventing hundreds of identical requests per second flooding the NodeMCU.

### NodeMCU relay logic
Most relay modules are **active-LOW** — they trigger when the signal pin goes LOW. The code uses:
```cpp
digitalWrite(RELAY_CH1, state1 ? LOW : HIGH);
```
If your relays behave inverted, swap `LOW` and `HIGH`.

---

## 🔮 Future Improvements

- [ ] Firebase integration for cloud control (control from anywhere)
- [ ] Blynk mobile app dashboard
- [ ] Add more relay channels for more appliances
- [ ] Voice control integration with `SpeechRecognition`
- [ ] OTA (Over The Air) firmware updates
- [ ] Schedule-based automation (turn lights off at 10 PM)
- [ ] MQTT protocol for faster response

---

## Safety Notice

This project involves **mains AC voltage (220V/110V)** which is extremely dangerous.

- Always disconnect power before touching AC wiring
- Use insulated wire for all AC connections
- Keep AC wiring well away from the NodeMCU and relay signal side
- Do not touch COM/NO terminals while the circuit is powered
- If unsure, ask someone with electrical experience to help with the AC side

---

<div align="center">

Built with NodeMCU ESP8266 + Python MediaPipe

Star this repo if you found it useful!

</div>
