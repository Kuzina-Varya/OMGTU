namespace Алгоритм_Дейкстры
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    public class Dijkstra
    {
        private int numNodes;
        private List<Edge>[] adjacencyList; 

        public Dijkstra(int numNodes)
        {
            this.numNodes = numNodes;
            adjacencyList = new List<Edge>[numNodes + 1]; 
            for (int i = 1; i <= numNodes; i++)
            {
                adjacencyList[i] = new List<Edge>();
            }
        }

        public void AddEdge(int u, int v, int weight)
        {
            adjacencyList[u].Add(new Edge(u, v, weight));
            adjacencyList[v].Add(new Edge(v, u, weight)); 
        }

        public int[] FindShortestPaths(int startNode)
        {
            int[] distances = Enumerable.Repeat(int.MaxValue, numNodes + 1).ToArray(); 
            distances[startNode] = 0; 

            PriorityQueue<int, int> priorityQueue = new PriorityQueue<int, int>(); 
            priorityQueue.Enqueue(startNode, 0); 

            while (priorityQueue.Count > 0)
            {
                int currentNode = priorityQueue.Dequeue();

                foreach (var edge in adjacencyList[currentNode])
                {
                    int neighbor = edge.V;
                    int newDistance = distances[currentNode] + edge.Weight;

                    if (newDistance < distances[neighbor])
                    {
                        distances[neighbor] = newDistance;
                        priorityQueue.Enqueue(neighbor, newDistance);
                    }
                }
            }

            return distances;
        }
    }

    public class Edge
    {
        public int U { get; set; }
        public int V { get; set; }
        public int Weight { get; set; }

        public Edge(int u, int v, int weight)
        {
            U = u;
            V = v;
            Weight = weight;
        }
    }

    public class Program
    {
        public static void Main(string[] args)
        {
           
            int numNodes = 6;
            Dijkstra dijkstra = new Dijkstra(numNodes);

            dijkstra.AddEdge(1, 2, 4);
            dijkstra.AddEdge(1, 3, 2);
            dijkstra.AddEdge(2, 3, 3);
            dijkstra.AddEdge(2, 4, 6);
            dijkstra.AddEdge(3, 4, 5);
            dijkstra.AddEdge(3, 5, 7);
            dijkstra.AddEdge(4, 5, 8);

            int startNode = 1;

            int[] shortestDistances = dijkstra.FindShortestPaths(startNode);

            Console.WriteLine($"Кратчайшие расстояния от вершины {startNode}:");
            for (int i = 1; i <= numNodes; i++)
            {
                Console.WriteLine($"Вершина {i}: {shortestDistances[i]}");
            }
        }
    }
}
