namespace Алгоритм_Краскала
{

    using System;
    using System.Collections.Generic;
    using System.Linq;

    public class Edge : IComparable<Edge>
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

        public int CompareTo(Edge other)
        {
            return Weight.CompareTo(other.Weight);
        }
    }

    public class Kruskal
    {
        private int[] parent;

        public Kruskal(int numNodes)
        {
            parent = Enumerable.Range(0, numNodes + 1).ToArray();
        }

        private int Find(int node)
        {
            if (parent[node] != node)
            {
                parent[node] = Find(parent[node]);
            }
            return parent[node];
        }

        private void Union(int u, int v)
        {
            parent[Find(u)] = Find(v);
        }

        public List<Edge> FindMinimumSpanningTree(List<Edge> edges)
        {
            edges.Sort(); 
            List<Edge> mst = new List<Edge>(); 

            foreach (var edge in edges)
            {
                int u = edge.U;
                int v = edge.V;
                if (Find(u) != Find(v)) 
                {
                    Union(u, v); 
                    mst.Add(edge); 
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

          
            Kruskal kruskal = new Kruskal(numNodes);
            List<Edge> mst = kruskal.FindMinimumSpanningTree(edges);

           
            Console.WriteLine("Минимальное остовное дерево:");
            foreach (var edge in mst)
            {
                Console.WriteLine($"({edge.U}, {edge.V}) - {edge.Weight}");
            }
        }
    }
}
