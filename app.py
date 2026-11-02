from flask import Flask, render_template, jsonify, request
from collections import deque
import heapq

# --- ADSA CORE GRAPH ENGINE ---
class SocialGraph:
    def __init__(self):
        # 1. Hash Map: user_id -> set of friend_ids (O(1) average lookup)
        self.adj_list = {}
        # Hash Map: user_id -> profile metadata
        self.users = {}

    def add_user(self, user_id, name, department):
        if user_id not in self.adj_list:
            self.adj_list[user_id] = set()
            self.users[user_id] = {"id": user_id, "name": name, "department": department}

    def add_edge(self, u, v):
        """Adds an undirected edge between user u and user v."""
        if u in self.adj_list and v in self.adj_list:
            self.adj_list[u].add(v)
            self.adj_list[v].add(u)

    def get_direct_friends(self, user_id):
        """O(1) lookup using hash map."""
        return self.adj_list.get(user_id, set())

    def get_candidates_by_bfs(self, target_user, max_depth=2):
        """
        Feature 1: BFS to find candidates strictly within distance [2, max_depth].
        Distance 1 = already direct friends; Distance >= 2 = potential suggestions.
        Time Complexity: O(V + E)
        """
        if target_user not in self.adj_list:
            return {}

        visited_distance = {target_user: 0}
        queue = deque([target_user])
        candidates = {}  # candidate_id -> distance

        while queue:
            curr = queue.popleft()
            curr_dist = visited_distance[curr]

            if curr_dist >= max_depth:
                continue

            for neighbor in self.adj_list.get(curr, set()):
                if neighbor not in visited_distance:
                    dist = curr_dist + 1
                    visited_distance[neighbor] = dist
                    queue.append(neighbor)

                    if dist >= 2:
                        candidates[neighbor] = dist

        return candidates

    def recommend_friends_min_heap(self, target_user, max_depth=2, top_k=5):
        candidates = self.get_candidates_by_bfs(target_user, max_depth)
        target_friends = self.get_direct_friends(target_user)

        min_heap = []

        for cand_id, distance in candidates.items():
            cand_friends = self.get_direct_friends(cand_id)
            mutual_ids = target_friends.intersection(cand_friends)
            mutual_count = len(mutual_ids)

            # If distance is 2, mutual connections are direct friends (Distance 1)
            # If distance is 3, find the 2nd-degree friend who bridges the gap
            if distance == 2:
                connection_names = [self.users[m]["name"] for m in mutual_ids]
            else:
                # Find intermediate 2nd-degree friends connecting target to candidate
                intermediates = set()
                for tf in target_friends:
                    for cf in cand_friends:
                        if cf in self.get_direct_friends(tf):
                            intermediates.add(self.users[cf]["name"])
                connection_names = list(intermediates)

            u = self.users[cand_id]
            # Tuple priority: (mutual_count, -distance) so distance 2 ranks above distance 3
            item = (mutual_count, -distance, cand_id, u["name"], u["department"], distance, connection_names)

            if len(min_heap) < top_k:
                heapq.heappush(min_heap, item)
            elif (mutual_count, -distance) > (min_heap[0][0], min_heap[0][1]):
                heapq.heappushpop(min_heap, item)

        # Extract from heap and sort in descending order
        results = []
        while min_heap:
            count, neg_dist, cid, name, dept, dist, connections = heapq.heappop(min_heap)
            results.append({
                "id": cid,
                "name": name,
                "department": dept,
                "distance": dist,
                "mutual_count": count,
                "mutual_friends": connections
            })

        results.reverse()
        return results


# --- FLASK WEB SERVER SETUP ---
# template_folder='.' allows index.html to sit directly in the same directory
app = Flask(__name__, template_folder='.')
graph = SocialGraph()

def seed_data():
    sample_users = [
        (1, "Ram Kiran", "CSE"),
        (2, "Santhosh Reddy", "CSE"),
        (3, "Karun Peketi", "ECE"),
        (4, "Aditya Varma", "CSE"),
        (5, "Priya Sharma", "IT"),
        (6, "Bhavya Sri", "CSE"),
        (7, "Naveen Kumar", "Mechanical"),
        (8, "Kavya Rao", "IT")
    ]
    for uid, name, dept in sample_users:
        graph.add_user(uid, name, dept)

    edges = [
        (1, 2), (1, 3),        # Ram connects to Santhosh and Karun
        (2, 4), (2, 5), (2, 6), # Santhosh connects to Aditya, Priya, Bhavya
        (3, 4), (3, 7),        # Karun connects to Aditya, Naveen
        (4, 8),                # Aditya connects to Kavya (3 hops from Ram)
        (5, 6), (6, 8)
    ]
    for u, v in edges:
        graph.add_edge(u, v)

seed_data()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(list(graph.users.values()))

@app.route("/api/recommend", methods=["GET"])
def get_recommendations():
    user_id = int(request.args.get("user_id", 1))
    depth = int(request.args.get("depth", 2))
    top_k = int(request.args.get("top_k", 3))

    direct_friends = [
        {"id": fid, "name": graph.users[fid]["name"]}
        for fid in graph.get_direct_friends(user_id)
    ]
    
    recs = graph.recommend_friends_min_heap(user_id, depth, top_k)

    return jsonify({
        "direct_friends": direct_friends,
        "recommendations": recs
    })

if __name__ == "__main__":
    print("Flask ADSA Server running at http://127.0.0.1:5001")
    app.run(debug=True, port=5001)