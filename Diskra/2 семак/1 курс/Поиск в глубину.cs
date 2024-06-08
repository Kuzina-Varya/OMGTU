namespace Поиск_в_глубину
{
    using System;
    using System.Collections.Generic;

    public class DepthFirstSearch
    {
        private int numNodes;
        private List<int>[] adjacencyList; 

        public DepthFirstSearch(int numNodes)
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

        public void DepthFirstTraversal(int startNode)
        {
            bool[] visited = new bool[numNodes + 1]; 
            Stack<int> stack = new Stack<int>(); 

            stack.Push(startNode);

            while (stack.Count > 0)
            {
                int currentNode = stack.Pop();

                if (!visited[currentNode])
                {
                    Console.Write(currentNode + " ");
                    visited[currentNode] = true;

                   
                    foreach (int neighbor in adjacencyList[currentNode])
                    {
                        if (!visited[neighbor])
                        {
                            stack.Push(neighbor);
                        }
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
            DepthFirstSearch dfs = new DepthFirstSearch(numNodes);

            dfs.AddEdge(1, 2);
            dfs.AddEdge(1, 3);
            dfs.AddEdge(2, 4);
            dfs.AddEdge(2, 5);
            dfs.AddEdge(3, 6);

            Console.WriteLine("Обход в глубину, начиная с вершины 1:");
            dfs.DepthFirstTraversal(1);
            Console.WriteLine();
        }
    }

}
