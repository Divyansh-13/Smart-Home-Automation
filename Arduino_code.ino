#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

//  CHANGE THESE TO YOUR WIFI DETAIL
const char* ssid     = "WIFI NAME";
const char* password = "WIFI PASSWORD";

// Dual channel relay pins
// IN1 → D1 (GPIO5) → Bulb 1
// IN2 → D2 (GPIO4) → Bulb 2
#define RELAY_CH1  5   // D1
#define RELAY_CH2  4   // D2

// Bulb states
bool state1 = false;  // Bulb 1
bool state2 = false;  // Bulb 2

ESP8266WebServer server(80);

// Active LOW relay: LOW = ON, HIGH = OFF
void applyRelays() {
  digitalWrite(RELAY_CH1, state1 ? HIGH : LOW);
  digitalWrite(RELAY_CH2, state2 ? HIGH : LOW);
}

// Build HTML Page ───────────────────────────────────────
String buildPage() {
  String pg = R"html(
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Smart Bulb Control</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #0f0f1a;
      color: #eee;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 30px 16px;
    }
    h1 { font-size: 1.7rem; color: #f5a623; margin-bottom: 4px; }
    .subtitle { color: #888; font-size: 0.85rem; margin-bottom: 28px; }
    .cards {
      display: flex;
      flex-direction: column;
      gap: 16px;
      width: 100%;
      max-width: 380px;
    }
    .card {
      background: #1c1c2e;
      border-radius: 14px;
      padding: 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border: 1.5px solid #2a2a40;
    }
    .card-left { display: flex; align-items: center; gap: 14px; }
    .icon { font-size: 2.2rem; }
    .name { font-size: 1rem; font-weight: 600; }
    .pin-tag { font-size: 0.72rem; color: #555; margin-top: 2px; }
    .state { font-size: 0.82rem; margin-top: 4px; font-weight: bold; }
    .on-txt  { color: #4caf50; }
    .off-txt { color: #e94560; }
    .toggle {
      padding: 11px 22px;
      border: none;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: bold;
      cursor: pointer;
      text-decoration: none;
    }
    .btn-turnon  { background: #4caf50; color: #fff; }
    .btn-turnoff { background: #e94560; color: #fff; }
    .all-row {
      display: flex;
      gap: 12px;
      margin-top: 20px;
      width: 100%;
      max-width: 380px;
    }
    .all-row a {
      flex: 1;
      text-align: center;
      padding: 13px;
      border-radius: 10px;
      font-weight: bold;
      font-size: 0.95rem;
      text-decoration: none;
    }
    .all-on  { background: #f5a623; color: #000; }
    .all-off { background: #2a2a3e; color: #aaa; }
  </style>
</head>
<body>
  <h1>&#127968; Smart Bulb Panel</h1>
  <p class="subtitle">Dual Channel Relay &mdash; NodeMCU ESP8266</p>
  <div class="cards">
)html";

  const char* names[]  = {"Bulb 1",       "Bulb 2"};
  const char* pins[]   = {"D1 / GPIO5",   "D2 / GPIO4"};
  const char* onURL[]  = {"/r1/on",       "/r2/on"};
  const char* offURL[] = {"/r1/off",      "/r2/off"};
  bool states[]        = {state1, state2};

  for (int i = 0; i < 2; i++) {
    pg += "<div class='card'>";
    pg += "<div class='card-left'>";
    pg += "<div class='icon'>";
    pg += states[i] ? "&#128161;" : "&#9899;";
    pg += "</div><div>";
    pg += "<div class='name'>" + String(names[i]) + "</div>";
    pg += "<div class='pin-tag'>" + String(pins[i]) + "</div>";
    pg += "<div class='state ";
    pg += states[i] ? "on-txt'>● ON" : "off-txt'>● OFF";
    pg += "</div></div></div>";

    if (states[i]) {
      pg += "<a class='toggle btn-turnoff' href='" + String(offURL[i]) + "'>Turn OFF</a>";
    } else {
      pg += "<a class='toggle btn-turnon'  href='" + String(onURL[i])  + "'>Turn ON</a>";
    }
    pg += "</div>";
  }

  pg += R"html(
  </div>
  <div class="all-row">
    <a class="all-on"  href="/all/on">ALL ON</a>
    <a class="all-off" href="/all/off">ALL OFF</a>
  </div>
</body>
</html>
)html";
  return pg;
}

// Route handlers ────────────────────────────────────────
void redirect() { server.sendHeader("Location", "/"); server.send(302); }

void handleRoot() { server.send(200, "text/html", buildPage()); }

void r1on()  { state1 = true;  applyRelays(); redirect(); }
void r1off() { state1 = false; applyRelays(); redirect(); }
void r2on()  { state2 = true;  applyRelays(); redirect(); }
void r2off() { state2 = false; applyRelays(); redirect(); }

void allOn()  { state1 = state2 = true;  applyRelays(); redirect(); }
void allOff() { state1 = state2 = false; applyRelays(); redirect(); }

// Setup ─────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);

  pinMode(RELAY_CH1, OUTPUT);
  pinMode(RELAY_CH2, OUTPUT);
  applyRelays();  // Both OFF at boot

  Serial.print("\nConnecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
  Serial.print("Open in browser: http://");
  Serial.println(WiFi.localIP());

  server.on("/",        handleRoot);
  server.on("/r1/on",   r1on);  server.on("/r1/off", r1off);
  server.on("/r2/on",   r2on);  server.on("/r2/off", r2off);
  server.on("/all/on",  allOn);
  server.on("/all/off", allOff);

  server.begin();
  Serial.println("Server started!");
}

// Loop ──────────────────────────────────────────────────
void loop() {
  server.handleClient();
}
