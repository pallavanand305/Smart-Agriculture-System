# SMART AGRICULTURE SYSTEM
## Integrating IoT · Machine Learning · Advanced Data Structures

**Bachelor of Computer Applications (BCA)**
**Major Project Report | Academic Year 2024–2025**

**Subjects Covered:**
- AADS — Algorithms & Advanced Data Structures
- FML — Fundamentals of Machine Learning
- IoT — Internet of Things

---

## Abstract

The Smart Agriculture System is a software project demonstrating the practical integration of three core computer science subjects: IoT, Machine Learning (FML), and Algorithms & Data Structures (AADS). The system helps farmers grow better crops by collecting soil and weather data through IoT sensors, managing tasks intelligently using AADS-based data structures, and providing smart recommendations through trained machine learning models.

IoT components — implemented in code using ESP32 microcontrollers and MQTT protocol — collect real-time readings of soil moisture, temperature, humidity, and NPK (Nitrogen, Phosphorus, Potassium) levels. The AADS layer uses a Max-Heap to prioritize irrigation tasks, a Red-Black Tree to index sensor logs by timestamp, and Dijkstra's algorithm to route farm vehicles between zones. The FML layer uses a Random Forest Classifier for crop recommendation, Linear Regression for yield prediction, and an LSTM neural network for 24-hour soil moisture forecasting.

The project achieves 98.4% crop recommendation accuracy and end-to-end sensor-to-dashboard latency under 200ms, demonstrating that the combination of IoT, AADS, and ML can produce a practical and efficient precision farming solution.

---

## Table of Contents

1. Introduction
2. Requirements & Objectives
3. Software Engineering Concepts
4. System Architecture
5. Data Flow Diagram (DFD)
6. Entity Relationship Diagram (ERD)
7. Dataset Description
8. Algorithms & Pseudocode (AADS)
9. Machine Learning Implementation (FML)
10. IoT Implementation (Code-Based)
11. Implementation Details & Code Snippets
12. Testing & Results
13. Conclusion & Future Scope
14. References

---

---

## Chapter 1: Introduction

### 1.1 Background

Agriculture employs more than half of India's workforce, yet traditional farming relies heavily on guesswork — fixed irrigation schedules, manual soil checks, and experience-based crop selection. The result is water overuse, soil degradation, and poor yields.

The Smart Agriculture System addresses this by building a fully software-implemented pipeline that collects sensor data, applies intelligent scheduling algorithms, and uses machine learning to provide actionable recommendations — all accessible through a web dashboard.

### 1.2 Problem Statement

- Irrigation runs on fixed schedules regardless of actual soil moisture levels, wasting water
- Farmers have no real-time visibility into soil nutrient (NPK) levels
- No data-driven system exists to recommend the right crop for current soil and weather conditions
- Farm tasks like fertilizing and pest control are not intelligently prioritized
- There is no forecasting tool to predict soil conditions 24 hours ahead

### 1.3 How All Three Subjects Are Used

| Subject | Concept Used | Applied To |
|---------|-------------|------------|
| AADS | Max-Heap Priority Queue | Scheduling irrigation & fertilization tasks by urgency |
| AADS | Red-Black Tree | Indexing sensor logs by timestamp for fast retrieval |
| AADS | Dijkstra's Algorithm | Finding shortest route between farm zones for drone/vehicle |
| AADS | Merge Sort | Sorting sensor history logs for trend analysis |
| FML | Random Forest Classifier | Recommending the best crop from soil & climate data |
| FML | Linear Regression | Predicting expected crop yield (quintals/hectare) |
| FML | LSTM Neural Network | Forecasting soil moisture 24 hours in advance |
| IoT | ESP32 + MQTT Protocol | Collecting & transmitting real-time sensor data wirelessly |
| IoT | Relay Module (Code Logic) | Automatically turning irrigation pump ON/OFF |

---

## Chapter 2: Requirements & Objectives

### 2.1 Project Objectives

1. Implement an IoT data collection layer in code that simulates sensor readings every 5 minutes
2. Use a Max-Heap priority queue to manage and schedule farm tasks by urgency score
3. Train a Random Forest model to recommend the correct crop with at least 95% accuracy
4. Build a Linear Regression model to predict crop yield
5. Implement an LSTM network to forecast soil moisture 24 hours ahead
6. Expose all predictions through a Flask REST API consumed by a Streamlit dashboard
7. Demonstrate auto-irrigation logic that triggers when soil moisture drops below 30%

### 2.2 Functional Requirements

**IoT Layer**
- The system shall publish sensor readings (temperature, humidity, moisture, NPK) as JSON over MQTT every 5 minutes
- The subscriber shall parse incoming messages and route them to the AADS scheduler
- The relay control module shall publish an irrigation ON command when moisture < 30%

**AADS Layer**
- A Max-Heap shall manage all pending tasks sorted by priority score
- A Red-Black Tree shall index all sensor readings by timestamp, supporting O(log n) range queries
- A weighted graph and Dijkstra's algorithm shall compute shortest drone route across all farm zones

**FML Layer**
- A Random Forest model (100 trees) shall classify the optimal crop from 7 input features
- A Linear Regression model shall predict yield from seasonal soil-climate averages
- An LSTM model shall accept a 24-hour window of readings and forecast next-hour soil moisture

### 2.3 Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Sensor to Dashboard Latency | < 200 ms end-to-end |
| Crop Recommendation Accuracy | ≥ 95% |
| Yield Prediction RMSE | ≤ 2.0 quintals/ha |
| LSTM Forecast RMSE | ≤ 3.0% soil moisture |
| API Response Time | < 100 ms per request |
| Database | PostgreSQL — retain 2 years of sensor history |

### 2.4 Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11 | Core backend language for ML and IoT logic |
| Flask | 3.0 | REST API to serve ML predictions |
| scikit-learn | 1.4 | Random Forest and Linear Regression models |
| TensorFlow / Keras | 2.15 | LSTM neural network training and inference |
| Mosquitto MQTT | 2.0 | Message broker for IoT sensor data |
| Paho-MQTT | 1.6 | Python MQTT client library |
| PostgreSQL | 16 | Relational database for sensor logs and predictions |
| Streamlit | 1.32 | Farmer-facing web dashboard |

---
