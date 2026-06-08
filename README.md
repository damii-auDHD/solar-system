# 🪐 Solar System Simulation

A 2D solar system simulation built with **Python** and **Pygame**. Planets orbit the Sun following Kepler's third law, with moons orbiting their parent planets — just like the real thing.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)

## ✨ Features

- **Accurate Kepler orbits** — orbital speeds derived from ω = √(GM/r³)
- **Hierarchical system** — the Moon orbits Earth, Io & Europa orbit Jupiter
- **Saturn's ring** rendered as a tilted ellipse
- **Sun glow** with a soft radial gradient
- **Fading orbit trails** that follow each body
- **Starfield background** for that deep-space feel
- **Speed controls** — slow down, speed up, or pause the simulation

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Pygame 2.x

### Install & Run

```bash
# Clone the repo
git clone https://github.com/damii-auDHD/solar-system.git
cd solar-system

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install pygame
pip install pygame

# Run the simulation
python app/main.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `↑` | Speed up simulation |
| `↓` | Slow down simulation |
| `Space` | Pause / unpause |

## 🗂️ Project Structure

```
app/
├── main.py           # Game loop, rendering, and input handling
├── planets.py        # Body class (orbital mechanics, drawing, trails)
└── solar_system.py   # Solar system data tree and Kepler speed generator
```

## 🌍 Bodies

| Body | Parent | Orbital Distance (px) |
|------|--------|-----------------------|
| ☀️ Sun | — | — |
| Mercury | Sun | 65 |
| Venus | Sun | 105 |
| 🌍 Earth | Sun | 165 |
| 🌙 Moon | Earth | 22 |
| Mars | Sun | 235 |
| Jupiter | Sun | 340 |
| Io | Jupiter | 28 |
| Europa | Jupiter | 36 |
| 🪐 Saturn | Sun | 440 |

## 🔮 Roadmap

- [ ] Migrate to 3D using **Ursina**
- [ ] Add Uranus & Neptune
- [ ] Asteroid belt between Mars and Jupiter
- [ ] Planet info panel on hover/click
- [ ] Zoom & pan controls

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
