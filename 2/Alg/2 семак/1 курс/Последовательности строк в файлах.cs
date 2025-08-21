
using System;
using System.IO;
using System.Linq;




namespace Последовательность_срок_в_файлах
{





    public class Program
    {
        public static void Main(string[] args)
        {
           
            string[] lines = File.ReadAllLines(@"C:\Users\Доктор Варвар\Desktop\_\алгоритмизация\Последовательность строк.txt");
            string shortestSubsequence = lines
                .Select(line => new { Line = line, Count = line.Count(c => c == 'a') })
            .OrderBy(x => x.Count)
            .First()
            .Line;

            Console.WriteLine($"Самая короткая подстрока из 'a': {shortestSubsequence}");
        }

      
        private static int GetShortestSubsequenceLength(string line, char targetChar)
        {
            int minLength = int.MaxValue;
            int currentLength = 0;

            foreach (char c in line)
            {
                if (c == targetChar)
                {
                    currentLength++;
                }
                else
                {
                    minLength = Math.Min(minLength, currentLength);
                    
                }
            }
            
            return minLength;
        }
    }
}

    