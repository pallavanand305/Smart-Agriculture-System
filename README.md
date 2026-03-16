# Smart Agriculture System
**BCA Major Project | Academic Year 2024-2025**

Integrating IoT · Machine Learning · Advanced Data Structures

## Subjects Covered
- **AADS** — Max-Heap, Red-Black Tree, Dijkstra, Merge Sort
- **FML**  — Random Forest, Linear Regression, LSTM
- **IoT**  — ESP32 firmware (Arduino C++), MQTT protocol, relay control

## Quick Start

```bash
pip install -r requirements.txt
```

### 1. Generate Dataset
```bash
python data/generate_dataset.py
```

### 2. Train ML Models
```bash
python ml/train_crop.py
python ml/train_yield.py
python ml/train_lstm.py
```

### 3. Start Flask API
```bash
python api/app.py
```

### 4. Run Dashboard (new terminal)
```bash
streamlit run dashboard/app.py
```

### 5. (Optional) Simulate IoT Sensors
Requires a running Mosquitto MQTT broker on localhost:1883
```bash
python iot/simulator.py
python iot/subscriber.py
```

### 6. Generate PPT
```bash
python ppt/generate_ppt.py
```

## Project Structure
```
smart-agriculture-system/
├── iot/            ESP32 firmware + MQTT simulator/subscriber
├── aads/           Max-Heap, RB-Tree, Dijkstra, Merge Sort
├── ml/             Model training scripts
├── api/            Flask REST API
├── dashboard/      Streamlit web dashboard
├── database/       PostgreSQL schema
├── data/           Dataset generator
├── ppt/            Auto PPT generator
└── models/         Saved .pkl and .h5 model files (auto-created)
```

## No Hardware Required
All IoT concepts are implemented purely in software.
The ESP32 firmware (`iot/esp32_firmware.ino`) is provided for reference/report.
