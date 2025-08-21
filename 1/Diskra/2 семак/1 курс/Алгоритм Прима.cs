namespace Алгоритм_Прима
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

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

    public class PrimsAlgorithm
    {
        public static List<Edge> FindMinimumSpanningTree(List<Edge> edges, int numNodes, int startNode)
        {
            List<Edge> mst = new List<Edge>(); 
            bool[] visited = new bool[numNodes + 1]; 
            PriorityQueue<Edge,int> priorityQueue = new PriorityQueue<Edge,int>(); 

            
            visited[startNode] = true;

          
            foreach (var edge in edges.Where(e => e.U == startNode || e.V == startNode))
            {
                priorityQueue.Enqueue(edge, edge.Weight);
            }

            while (priorityQueue.Count > 0)
            {
                
                Edge currentEdge = priorityQueue.Dequeue();

                
                if (!visited[currentEdge.V])
                {
                   
                    mst.Add(currentEdge);
                    visited[currentEdge.V] = true;

                    
                    foreach (var edge in edges.Where(e => e.U == currentEdge.V || e.V == currentEdge.V))
                    {
                        if (!visited[edge.U] || !visited[edge.V])
                        {
                            priorityQueue.Enqueue(edge, edge.Weight);
                        }
                    }
                }
            }

            return mst;
        }
    }

    public class Program
    {
        public static void Main(string[] args)
        {
           
            int numNodes = 5; 
            int startNode = 1; 
            List<Edge> edges = new List<Edge>()
        {
            new Edge(1, 2, 4),
            new Edge(1, 3, 2),
            new Edge(2, 3, 3),
            new Edge(2, 4, 6),
            new Edge(3, 4, 5),
            new Edge(3, 5, 7),
            new Edge(4, 5, 8)
        };

            
            List<Edge> mst = PrimsAlgorithm.FindMinimumSpanningTree(edges, numNodes, startNode);

            
            Console.WriteLine("Минимальное остовное дерево:");
            foreach (var edge in mst)
            {
                Console.WriteLine($"({edge.U}, {edge.V}) - {edge.Weight}");
            }
        }
    }
}
