# Social Network Friend Recommendation System

**Course:** Advanced Data Structures & Algorithms (ADSA)  
**UN Sustainable Development Goal:** SDG 9 (Industry, Innovation & Infrastructure)

---

## 📌 Problem Statement
Build a friend recommendation feature for a social network that suggests "People You May Know" based on mutual connections, social graph proximity, and network depth.

---

## 🛠️ Data Structures & Algorithms (ADSA) Used

| Component | Data Structure / Algorithm | Time Complexity | Purpose |
| :--- | :--- | :--- | :--- |
| **Graph Representation** | **Hash Map** (`dict` of `sets`) | $O(1)$ average lookup | Instant access to a user's direct friends without storing a sparse $V \times V$ matrix. |
| **Candidate Discovery** | **Breadth-First Search (BFS)** | $O(V + E)$ bounded to depth | Explores connections level-by-level to filter candidates strictly within distance 2 (friends of friends) or 3. |
| **Top-$K$ Ranking** | **Min-Heap** (`heapq`) | $O(N \log K)$ | Maintains a bounded priority queue of size $K$ to evict low-mutual candidates, outperforming a full $O(N \log N)$ sort. |

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8+
- Flask

### Installation & Execution
```bash
# 1. Install dependencies
pip install flask

# 2. Run the server
python app.py