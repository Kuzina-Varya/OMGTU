namespace Алгоритм_Форд_Беллмана
{
    using System;
    using System.Collections.Generic;

    public class BellmanFord
    {
        private int numNodes;
        private List<Edge>[] adjacencyList; 

        public BellmanFord(int numNodes)
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
            
        }

        public int[] FindShortestPaths(int startNode)
        {
            int[] distances = new int[numNodes + 1]; 
            for (int i = 1; i <= numNodes; i++)
            {
                distances[i] = int.MaxValue; 
            }
            distances[startNode] = 0; 

           
            for (int i = 1; i <= numNodes - 1; i++) 
            {
                for (int u = 1; u <= numNodes; u++)
                {
                    foreach (var edge in adjacencyList[u])
                    {
                        int v = edge.V;
                        int weight = edge.Weight;
                        if (distances[u] != int.MaxValue && distances[u] + weight < distances[v])
                        {
                            distances[v] = distances[u] + weight;
                        }
                    }
                }
            }

            
            for (int u = 1; u <= numNodes; u++)
            {
                foreach (var edge in adjacencyList[u])
                {
                    int v = edge.V;
                    int weight = edge.Weight;
                    if (distances[u] != int.MaxValue && distances[u] + weight < distances[v])
                    {
                        throw new Exception("Граф содержит отрицательный цикл!");
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
            
            int numNodes = 5; 
            BellmanFord bellmanFord = new BellmanFord(numNodes);

            bellmanFord.AddEdge(1, 2, -1);
            bellmanFord.AddEdge(1, 3, 4);
            bellmanFord.AddEdge(2, 4, 3);
            bellmanFord.AddEdge(3, 5, 2);
            bellmanFord.AddEdge(4, 5, -2);

            int startNode = 1; 

            try
            {
                int[] shortestDistances = bellmanFord.FindShortestPaths(startNode);

                Console.WriteLine($"Кратчайшие расстояния от вершины {startNode}:");
                for (int i = 1; i <= numNodes; i++)
                {
                    Console.WriteLine($"Вершина {i}: {shortestDistances[i]}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }
    }
}
