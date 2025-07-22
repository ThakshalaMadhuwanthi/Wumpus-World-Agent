# 🧠 Wumpus World - Logic-Based Agent (CSCI 22052 Project)

## 🎓 Bachelor of Science Honours in Computer Science  
**University of Kelaniya, Faculty of Computing and Technology**  
**Course**: CSCI 22052 – Introduction to Artificial Intelligence  
**Student**: H.G. Thakshala Madhuwanthi  
**Enrollment ID**: CS/2021/002  

---

## 📌 Project Overview

This project simulates a logic-based agent navigating the **Wumpus World**, a 4x4 grid-based environment filled with hidden dangers such as **pits** and a **Wumpus**. The agent uses **propositional logic** and **knowledge representation** to safely explore, find the gold, and return to the starting position.

The system is built with **Python** and **Pygame** for graphical visualization, allowing real-time tracking of the agent's decisions based on percepts like:

- **Breeze** (nearby pit)
- **Stench** (nearby Wumpus)
- **Glitter** (gold in current cell)
- **Bump** (wall collision)
- **Scream** (Wumpus has been killed)

---

## 🧠 Agent Features

- Percept-based knowledge updates and logical inference.
- Maintains `safe`, `unsafe`, `visited`, and `frontier` sets.
- Applies deduction rules to infer safe/dangerous cells.
- Uses **Breadth-First Search (BFS)** for safe backtracking.
- Optionally shoots the Wumpus when its location is deduced.
- Real-time Pygame visualization of agent movement and world state.

---

## 📽️ Video Demonstration

🎥 **Watch the simulation in action:**  
[![Watch on YouTube](https://img.shields.io/badge/YouTube-Video-red?logo=youtube)](https://youtu.be/lsDk-XHUqK0?si=QU2JEUCgU5y8on-S)

---

## ✅ Testing and Evaluation

- The simulation was tested on 10 randomly generated Wumpus Worlds.
- Each environment contains:
  - 1 Wumpus
  - 1 Gold
  - 2–3 Pits (randomly placed)
- The agent starts at position `(0, 0)` and tries to find the gold and return safely.

### ✔️ Strengths:
- Accurate deduction of safe zones using logical rules.
- Efficient backtracking and correct use of the arrow.

### ⚠️ Limitations:
- In high-uncertainty areas, the agent may be forced to make risky moves.
- No heuristic preference when multiple frontier cells are equally safe.

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Pygame** – for GUI-based grid simulation and agent movement

