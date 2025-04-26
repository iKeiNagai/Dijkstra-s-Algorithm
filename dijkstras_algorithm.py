from pyspark import SparkContext

sc = SparkContext("spark://<master-ip>:7077", "DijkstraApp")

source_node = 0

# Read edges
lines = sc.textFile("hdfs:///graph/weighted_graph.txt")
valid_lines = lines.filter(lambda line: len(line.strip().split()) >= 3)

# Parse input into (source, (dest, weight))
edges = (valid_lines
         .map(lambda line: line.strip().split())
         .map(lambda tokens: (int(tokens[0]), (int(tokens[1]), int(tokens[2])))))
print(edges.take(5))

# Create adjacency list: (source, [(dest, weight)])
adj = edges.groupByKey().mapValues(list).cache()

# Initialize distances: (node, distance)
nodes = adj.flatMap(lambda x: [x[0]] + [n for n, _ in x[1]]).distinct()
distances = nodes.map(lambda x: (x, float("inf")))
distances = distances.map(lambda x: (x[0], 0) if x[0] == source_node else x).cache()

for i in range(10):  # max 10 iterations
    # Join distances with adjacency list
    joined = distances.join(adj)
    
    # Generate possible new distances
    new_distances = joined.flatMap(
        lambda x: [(nbr, x[1][0] + weight) for nbr, weight in x[1][1]]
    )
    
    # Combine minimum distances
    all_distances = distances.union(new_distances)
    distances = all_distances.reduceByKey(min).cache()

# Collect results
result = distances.collect()
for node, dist in sorted(result):
    print(f"Node {node}: Distance {dist}")


print("Job completed. Stopping SparkContext.")
sc.stop()