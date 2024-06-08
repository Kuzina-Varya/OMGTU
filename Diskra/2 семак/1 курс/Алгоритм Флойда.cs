namespace Алгоритм_Флойда
{
    using System;

    public class FloydWarshall
    {
        private int numNodes;
        private int[,] distances; 

        public FloydWarshall(int numNodes)
        {
            this.numNodes = numNodes;
            distances = new int[numNodes + 1, numNodes + 1]; 

            
            for (int i = 1; i <= numNodes; i++)
            {
                for (int j = 1; j <= numNodes; j++)
                {
                    distances[i, j] = int.MaxValue;
                }
            }

          
            distances[1, 2] = 4;
            distances[1, 3] = 2;
            distances[2, 3] = 3;
            distances[2, 4] = 6;
            distances[3, 4] = 5;
            distances[3, 5] = 7;
            distances[4, 5] = 8;

           
            for (int i = 1; i <= numNodes; i++)
            {
                distances[i, i] = 0;
            }
        }

        public void CalculateShortestPaths()
        {
            
            for (int k = 1; k <= numNodes; k++)
            {
                for (int i = 1; i <= numNodes; i++)
                {
                    for (int j = 1; j <= numNodes; j++)
                    {
                        if (distances[i, k] + distances[k, j] < distances[i, j])
                        {
                            distances[i, j] = distances[i, k] + distances[k, j];
                        }
                    }
                }
            }
        }

        public void PrintShortestPaths()
        {
            Console.WriteLine("Матрица кратчайших расстояний:");
            for (int i = 1; i <= numNodes; i++)
            {
                for (int j = 1; j <= numNodes; j++)
                {
                    if (distances[i, j] == int.MaxValue)
                    {
                        Console.Write("∞ ");
                    }
                    else
                    {
                        Console.Write($"{distances[i, j]} ");
                    }
                }
                Console.WriteLine();
            }
        }
    }

    public class Program
    {
        public static void Main(string[] args)
        {
            int numNodes = 5; 
            FloydWarshall floyd = new FloydWarshall(numNodes);

            floyd.CalculateShortestPaths();
            floyd.PrintShortestPaths();
        }
    }
}
