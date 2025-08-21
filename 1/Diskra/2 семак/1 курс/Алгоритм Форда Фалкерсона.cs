namespace Алгоритм_Форда_Фалкерсона
{
    using System;
    using System.Collections.Generic;

    public class FordFulkerson
    {
        
        public struct Edge
        {
            public int From { get; set; }
            public int To { get; set; }
            public int Capacity { get; set; }
            public int Flow { get; set; }
        }

        
        public class Graph
        {
            public int VerticesCount { get; private set; }
            public List<Edge> Edges { get; private set; }

            public Graph(int verticesCount)
            {
                VerticesCount = verticesCount;
                Edges = new List<Edge>();
            }

            
            public void AddEdge(int from, int to, int capacity)
            {
                Edges.Add(new Edge { From = from, To = to, Capacity = capacity, Flow = 0 });
            }
        }

       
        private static List<int> FindPath(Graph graph, int source, int sink, List<bool> visited)
        {
            
            Queue<int> queue = new Queue<int>();
            queue.Enqueue(source);
            visited[source] = true;

           
            Dictionary<int, int> predecessors = new Dictionary<int, int>();

          
            while (queue.Count > 0)
            {
                int current = queue.Dequeue();

                
                if (current == sink)
                {
                    List<int> path = new List<int>();
                    int vertex = sink;
                    while (vertex != source)
                    {
                        path.Add(vertex);
                        vertex = predecessors[vertex];
                    }
                    path.Add(source);
                    path.Reverse();
                    return path;
                }

               
                foreach (Edge edge in graph.Edges)
                {
                    if (edge.From == current && !visited[edge.To] && edge.Capacity > edge.Flow)
                    {
                        queue.Enqueue(edge.To);
                        visited[edge.To] = true;
                        predecessors[edge.To] = current;
                    }
                }
            }

           
            return null;
        }

        
        public static int MaxFlow(Graph graph, int source, int sink)
        {
            
            int maxFlow = 0;

           
            while (true)
            {
                
                List<bool> visited = new List<bool>(new bool[graph.VerticesCount]);
                List<int> path = FindPath(graph, source, sink, visited);
                if (path == null)
                {
                    break;
                }

               
                int minCapacity = int.MaxValue;
                for (int i = 1; i < path.Count; i++)
                {
                    foreach (Edge edge in graph.Edges)
                    {
                        if (edge.From == path[i - 1] && edge.To == path[i] && edge.Capacity > edge.Flow)
                        {
                            minCapacity = Math.Min(minCapacity, edge.Capacity - edge.Flow);
                            break;
                        }
                    }
                }

              
                for (int i = 1; i < path.Count; i++)
                {
                   
                    Edge edge = graph.Edges.Find(e => e.From == path[i - 1] && e.To == path[i]);

                   
                    if (edge.From != 0)
                    {
                        edge.Flow += minCapacity;
                    }
                    else
                    {
                        edge.Flow -= minCapacity;
                    }
                }


              
                maxFlow += minCapacity;
            }

           
            return maxFlow;
        }

        public static void Main(string[] args)
        {
           
            Graph graph = new Graph(6);
            graph.AddEdge(0, 1, 16);
            graph.AddEdge(0, 2, 13);
            graph.AddEdge(1, 2, 10);
            graph.AddEdge(1, 3, 12);
            graph.AddEdge(2, 1, 4);
            graph.AddEdge(2, 4, 14);
            graph.AddEdge(3, 2, 9);
            graph.AddEdge(3, 5, 20);
            graph.AddEdge(4, 3, 7);
            graph.AddEdge(4, 5, 4);

            
            int maxFlow = MaxFlow(graph, 0, 5);

            
            Console.WriteLine($"Максимальный поток: {maxFlow}");
        }
    }
}
