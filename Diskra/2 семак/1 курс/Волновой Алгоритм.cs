namespace Волновой_Алгоритм
{
    using System;
    using System.Collections.Generic;

    public class WaveAlgorithm
    {
        private int[,] grid; 
        private int rows;
        private int cols;

        public WaveAlgorithm(int[,] grid)
        {
            this.grid = grid;
            this.rows = grid.GetLength(0);
            this.cols = grid.GetLength(1);
        }

        public void FindPath(int startX, int startY, int endX, int endY)
        {
           
            if (startX < 0 || startX >= rows || startY < 0 || startY >= cols ||
                endX < 0 || endX >= rows || endY < 0 || endY >= cols)
            {
                Console.WriteLine("Неверные координаты.");
                return;
            }

          
            if (grid[startX, startY] != 0 || grid[endX, endY] != 0)
            {
                Console.WriteLine("Стартовая или конечная точка недоступна.");
                return;
            }

           
            int[,] waveMatrix = new int[rows, cols];
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    waveMatrix[i, j] = -1; 
                }
            }

          
            waveMatrix[startX, startY] = 0;

           
            Queue<(int, int)> queue = new Queue<(int, int)>();
            queue.Enqueue((startX, startY));

          
            while (queue.Count > 0)
            {
                (int x, int y) = queue.Dequeue();

               
                foreach (var (dx, dy) in new (int, int)[] { (-1, 0), (1, 0), (0, -1), (0, 1) })
                {
                    int newX = x + dx;
                    int newY = y + dy;

                    
                    if (newX >= 0 && newX < rows && newY >= 0 && newY < cols && grid[newX, newY] == 0 && waveMatrix[newX, newY] == -1)
                    {
                       
                        waveMatrix[newX, newY] = waveMatrix[x, y] + 1;
                        queue.Enqueue((newX, newY));
                    }
                }
            }

           
            Console.WriteLine("Волновая матрица:");
            PrintMatrix(waveMatrix);

            
            if (waveMatrix[endX, endY] == -1)
            {
                Console.WriteLine("Конечная точка недостижима.");
                return;
            }

           
            List<(int, int)> path = ReconstructPath(waveMatrix, endX, endY);

          
            Console.WriteLine("Путь:");
            foreach (var (x, y) in path)
            {
                Console.WriteLine($"({x}, {y})");
            }
        }

        
        private List<(int, int)> ReconstructPath(int[,] waveMatrix, int endX, int endY)
        {
            List<(int, int)> path = new List<(int, int)>();
            path.Add((endX, endY));

            int currentWave = waveMatrix[endX, endY];
            (int x, int y) = (endX, endY);

            while (currentWave > 0)
            {
                
                foreach (var (dx, dy) in new (int, int)[] { (-1, 0), (1, 0), (0, -1), (0, 1) })
                {
                    int newX = x + dx;
                    int newY = y + dy;

                    
                    if (newX >= 0 && newX < rows && newY >= 0 && newY < cols && waveMatrix[newX, newY] == currentWave - 1)
                    {
                        path.Add((newX, newY));
                        x = newX;
                        y = newY;
                        currentWave--;
                        break;
                    }
                }
            }

            return path;
        }

        
        private void PrintMatrix(int[,] matrix)
        {
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    Console.Write($"{matrix[i, j],3} ");
                }
                Console.WriteLine();
            }
        }
    }

    public class Program
    {
        public static void Main(string[] args)
        {
            
            int[,] grid = new int[,]
            {
            {0, 0, 0, 0, 0},
            {0, 1, 1, 1, 0},
            {0, 1, 0, 1, 0},
            {0, 1, 0, 0, 0},
            {0, 0, 0, 0, 0}
            };

            WaveAlgorithm waveAlgorithm = new WaveAlgorithm(grid);
            waveAlgorithm.FindPath(0, 0, 4, 4);
        }
    }
}
