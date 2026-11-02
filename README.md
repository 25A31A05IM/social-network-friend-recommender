# 🌐 Social Network Friend Recommendation System

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Render-brightgreen?style=for-the-badge&logo=render)](https://social-network-friend-recommender.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Framework-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Course](https://img.shields.io/badge/Course-ADSA-orange?style=for-the-badge)](#)
[![SDG](https://img.shields.io/badge/UN%20SDG-9%3A%20Industry%2C%20Innovation%20%26%20Infrastructure-blue?style=for-the-badge)](https://sdgs.un.org/goals/goal9)

> An algorithmic implementation of a "People You May Know" recommendation system for social networks using Breadth-First Search (BFS), Hash Maps, and a Bounded Min-Heap.

---

## 🔗 Live Deployment

- **Web Application:** [https://social-friend-recommender.onrender.com](https://social-friend-recommender.onrender.com)  
*(Note: Replace with your exact Render service URL if customized)*

---

## 📌 Problem Statement & SDG Alignment

### Problem Statement
In large-scale social networks, recommending relevant connections based on structural network proximity is a fundamental problem. This project implements a recommendation engine that suggests potential friends based on **mutual connections**, **network hop distance**, and **bounded priority ranking**.

### SDG 9: Industry, Innovation & Infrastructure
Large-scale graph computations demand significant memory and compute resources. By applying asymptotic optimizations:
- Replacing matrix traversals with **Hash Map adjacency sets** saves $O(V^2)$ space.
- Replacing global sorting ($O(N \log N)$) with a **bounded Min-Heap ($O(N \log K)$)** reduces compute overhead.  
This aligns with **SDG 9** by building efficient, scalable, and sustainable digital information infrastructure.

---

## 🧠 Data Structures & Asymptotic Complexity

| Component | Chosen Data Structure / Algorithm | Time Complexity | Space Complexity | Technical Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Graph Representation** | **Hash Map** (`dict` of `set`s) | **$O(1)$** avg lookup | **$O(V + E)$** | Avoids sparse $O(V^2)$ adjacency matrix overhead and enables $O(\min(d_A, d_B))$ mutual friend set intersection. |
| **Candidate Discovery** | **Breadth-First Search (BFS)** | **$O(V + E)$** (bounded to depth) | **$O(V)$** | Traverses level-by-level to guarantee shortest path discovery for distance 2 (friends of friends) and distance 3 hops. |
| **Top-$K$ Ranking** | **Min-Heap** (`heapq`) | **$O(N \log K)$** | **$O(K)$** | Bounded priority queue of size $K$. Automatically evicts low-mutual candidates, outperforming a full $O(N \log N)$ sort. |

---

## ⚙️ How the Algorithm Works

```text
[ Target User ]
       │
       ▼
1. Hash Map Lookup ────────► Get Direct Friends (Distance = 1)
       │
       ▼
2. BFS Traversal ──────────► Explore Level 2 (Friends-of-Friends) & Level 3
       │
       ▼
3. Intersection ───────────► Compute Mutual Connection Count: |Friends(Target) ∩ Friends(Candidate)|
       │
       ▼
4. Bounded Min-Heap ───────► If heap.size < K: push(candidate)
                             Else if candidate.score > heap.root:
                                 heappushpop(candidate)
       │
       ▼
[ Top-K Ranked Recommendations ]
