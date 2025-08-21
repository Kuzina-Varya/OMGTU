using Microsoft.VisualBasic;

namespace Сэты
{
    internal class Program
    {
        static void Print(HashSet<int> addition1, HashSet<int> set1) 
        {
            for (int i = 0; i < set1.Count(); i++)
            {
                if (!addition1.Contains(set1.ElementAt(i)))
                {
                    addition1.Add(set1.ElementAt(i));
                }
                else
                {
                    addition1.Remove(set1.ElementAt(i));
                }

            }
            foreach (var str in addition1)
            {
                Console.Write(str + " ");
            }
            Console.WriteLine();
        }
        static void Main(string[] args)
        {
            HashSet<int> set1 = new HashSet<int>{ 1, 2, 3, 4, 5, 6, 4, 7 };
            HashSet<int> set2 = new HashSet<int> { 1, 4, 3, 9, 7, 8, 5, 4, 0, 7 };
            HashSet<int> set3 = new HashSet<int> { 3, 5, 3, 8, 5, 6, 9, 4, 8, 7 };
            set1.IntersectWith(set2);
            set1.IntersectWith(set3);
            Console.Write("Пересечение: ");
            foreach (var str in set1)
            {
                Console.Write(str+" ");
            }
            Console.WriteLine();
             set1 = new HashSet<int> { 1, 2, 3, 4, 5, 6, 4, 7 };
             set2 = new HashSet<int> { 1, 4, 3, 9, 7, 8, 5, 4, 0, 7 };
             set3 = new HashSet<int> { 3, 5, 3, 8, 5, 6, 9, 4, 8, 7 };
            set1.Union(set2);
            set1.Union(set3);
            Console.Write("Объединение: ");
            foreach (var str in set1)
            {
                Console.Write(str + " ");
            }
            Console.WriteLine();

            HashSet<int> addition1 = new HashSet<int> { 1, 2, 3, 4, 5, 6, 4, 7 };
            HashSet<int> addition2 = new HashSet<int> { 1, 4, 3, 9, 7, 8, 5, 4, 0, 7 };
            HashSet<int> addition3 = new HashSet<int> { 3, 5, 3, 8, 5, 6, 9, 4, 8, 7 };
            
            Console.Write("Дополнение1: ");
            Print(addition1, set1);
            Console.Write("Дополнение2: ");
            Print(addition2, set1);
            Console.Write("Дополнение3: ");
            Print(addition3, set1);
          
        }

    }
}
