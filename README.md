# 🔥 Fire Escape Route Agent using AI Search Algorithms

## 📌 Project Overview

“Fire Escape Route Agent” is a pathfinding problem, which studies and aims to the find the fastest and most safe path to take in a mall in case of a fire. The environment of the study is a 3D maze of size 25x30 and the actor is an agent that routes the maze through different AI algorithms in order to find the fastest and most safe path to the goal and select the AI algorithm that led it to this path in the shortest time as the best algorithm. Depending on the results of the study, a Surviving Trolley that transports people will take the optimal path towards the exit of the mall safely.

---

## 🎯 Project Objective

* Implement and compare classical **AI search algorithms**
* Simulate a realistic **evacuation scenario**
* Identify the **most efficient algorithm** for guiding people safely to exits
* Evaluate algorithms based on efficiency and optimality

---

## 🤖 Scenario Description

* The environment is represented as a **3D grid-based maze**
* Walls represent blocked areas
* The agent starts from a predefined position
* The goal is a **safe exit gate**
* Only **one algorithm runs per experiment**
* The simulation visualizes:
  * Exploration phase
  * Final escape path
* This setup allows observing algorithm behavior under **hard and constrained conditions**

---

## 🧠 Implemented Search Algorithms

| Algorithm                            | Description                                                               |
| ------------------------------------ | ------------------------------------------------------------------------- |
| **Breadth First Search (BFS)**       | Tries to reach the goal by exploring all neighboring nodes level by level |
| **Depth First Search (DFS)**         | Explores one path deeply before backtracking                              |
| **Iterative Deepening Search (IDS)** | Combines DFS depth limits with BFS completeness                           |
| **Uniform Cost Search (UCS)**        | Expands the node with the lowest cumulative cost                          |
| **A* Search**                        | Uses path cost and heuristic function to efficiently reach the goal       |
| **Hill Climbing**                    | Greedy approach that selects the closest neighbor to the goal             |

---

## 📊 Algorithms Comparison & Evaluation

```
--------------------------------------------------------------------------------------------------------------
|      Metric      |     BFS      |     DFS      |     UCS      |      A*      |     IDS      |     Hill     |
--------------------------------------------------------------------------------------------------------------
| Discovered nodes |        333   |        241   |        326   |        322   |        324   |         56   |
| Moves            |       6582   |        328   |       8814   |       9014   |      18103   |         56   |
| Final path       |         50   |        116   |         50   |         50   |         74   |          0   |
| Viz Time (s)     |     994.80   |      66.60   |    1329.60   |    1359.60   |    2726.55   |       8.40   |
--------------------------------------------------------------------------------------------------------------
```

### 🔍 Evaluation Metrics

* **Discovered nodes:** Number of explored states
* **Moves:** Total agent movements
* **Final path:** Length of the path to the exit
* **Visualization time:** Time taken to visualize the process

---

## 🏆 Algorithm Ranking (Best → Worst)

Based on **path optimality, exploration efficiency, and suitability for emergency evacuation**, the algorithms are ranked as follows:

1. **A*** – Optimal path with heuristic guidance
2. **Uniform Cost Search (UCS)** – Optimal but impractical for real-time fire escape scenarios
3. **Breadth First Search (BFS)** – Optimal path but inefficient for fire escape scenarios
4. **Iterative Deepening Search (IDS)** – Complete but inefficient in large environments
5. **Depth First Search (DFS)** – Fast but non-optimal
6. **Hill Climbing** – Incomplete

---

## 🛠 Technologies Used

* **Python 3**
* **PyOpenGL** (OpenGL, GLU, GLUT)
* 3D Maze Visualization
* Standard Python libraries

---

## 📁 Project Structure

```
Project_code/
│
├── main.py
├── maze.py
├── search_algo.py
│
├── project Report.pdf
└── project presentation.pdf

```

---

## ▶ How to Run the Project

### 1️⃣ Clone the repository

```bash
git clone https://github.com/DevMohamedNasser/FireEscapeRouteAgent
cd Project_code
```

### 2️⃣ Install required libraries

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### 3️⃣ Run the program

```bash
python main.py
```

Then choose one of the following options **inside the program**:

`bfs` | `dfs` | `ucs` | `astar` | `ids` | `hill` | `compare`

---

## 👥 Team Members

* Heba Ahmed Ibrahim Agamy
* Maram Hazem Fouad Ismail Ahmed
* Menna Ahmed Ibrahim Agamy
* Mohamed Elsayed Mohamed Ahmed Aboelsoud
* Mohamed Khaled El-Daheesh Ahmed
* Mohamed Refat Mustafa Abd-Elmajid Nasser
* Wessam Mohamed El-Sayed Al-Hanafy
