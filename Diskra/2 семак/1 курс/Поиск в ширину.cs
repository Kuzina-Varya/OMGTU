namespace Поиск_в_ширину
{
    using System;
    using System.Collections.Generic;

    public class BreadthFirstSearch
    {
        private int numNodes;
        private List<int>[] adjacencyList; 

        public BreadthFirstSearch(int numNodes)
        {
            this.numNodes = numNodes;
            adjacencyList = new List<int>[numNodes + 1]; 
            for (int i = 1; i <= numNodes; i++)
            {
                adjacencyList[i] = new List<int>();
            }
        }

        public void AddEdge(int u, int v)
        {
            adjacencyList[u].Add(v);
            adjacencyList[v].Add(u); 
        }

        public void BreadthFirstTraversal(int startNode)
        {
            bool[] visited = new bool[numNodes + 1]; 
            Queue<int> queue = new Queue<int>(); 

            queue.Enqueue(startNode);
            visited[startNode] = true;

            while (queue.Count > 0)
            {
                int currentNode = queue.Dequeue();

                Console.Write(currentNode + " ");

                foreach (int neighbor in adjacencyList[currentNode])
                {
                    if (!visited[neighbor])
                    {
                        queue.Enqueue(neighbor);
                        visited[neighbor] = true;
                    }
                }
            }
        }
    }

    public class Program
    {
        public static void Main(string[] args)
        {
           
            int numNodes = 6;
            BreadthFirstSearch bfs = new BreadthFirstSearch(numNodes);

            bfs.AddEdge(1, 2);
            bfs.AddEdge(1, 3);
            bfs.AddEdge(2, 4);
            bfs.AddEdge(2, 5);
            bfs.AddEdge(3, 6);

            Console.WriteLine("Обход в ширину, начиная с вершины 1:");
            bfs.BreadthFirstTraversal(1);
            Console.WriteLine();
        }
    }

}
