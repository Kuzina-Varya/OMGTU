using Microsoft.VisualBasic;

namespace Сэты
{
    internal class Program
    {
        static void Main(string[] args)
        {
            List<int> set1 = new List<int>{ 1, 2, 3, 4, 5, 6, 5, 4, 3, 7 };
            int[] set2 = { 1, 4, 3, 9, 7, 8, 5, 4, 0, 7 };
            int[] set3 = { 3, 5, 3, 8, 5, 6, 9, 4, 8, 7 };
            IEnumerable<int> query1 = from intersection1 in set1.Intersect(set2)
                                        select intersection1;
            IEnumerable<int> query2 = from intersection2 in set1.Intersect(set3)
                                     select intersection2;
            IEnumerable<int> query3 = from intersection3 in query1.Intersect(query2)
                                     select intersection3;
            Console.Write("Пересечение: ");
            foreach (var str in query3)
            {
                Console.Write(str+" ");
            }
            Console.WriteLine();
            IEnumerable<int> query4 = from union1 in set1.Union(set2)
                                      select union1;
            IEnumerable<int> query5 = from union2 in set2.Union(set3)
                                      select union2;
            IEnumerable<int> query6 = from union3 in query4.Union(query5)
                                      select union3;
            Console.Write("Объединение: ");
            foreach (var str in query6)
            {
                Console.Write(str + " ");
            }
            Console.WriteLine();
            List<int> addition1 = new List<int>();
            List<int> addition2 = new List<int>();
            List<int> addition3 = new List<int>();
            for (int i = 0; i < query6.Count(); i++)
            {
                if (!set1.Contains(query6.ElementAt(i))) addition1.Add(query6.ElementAt(i));
                if (!set2.Contains(query6.ElementAt(i))) addition2.Add(query6.ElementAt(i));
                if (!set3.Contains(query6.ElementAt(i))) addition3.Add(query6.ElementAt(i));
            }
            Console.Write("Дополнение1: ");
            foreach (var str in addition1)
            {
                Console.Write(str + " ");
            }
            Console.WriteLine();
            Console.Write("Дополнение2: ");
            foreach (var str in addition2)
            {
                Console.Write(str + " ");
            }
            Console.WriteLine();
            Console.Write("Дополнение3: ");
            foreach (var str in addition3)
            {
                Console.Write(str + " ");
            }
            Console.WriteLine();
            
        }

    }
}
