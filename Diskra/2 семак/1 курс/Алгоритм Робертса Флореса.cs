namespace Алгоритм_Робертса_Флореса
{
    using System;
    using System.Collections.Generic;

    public class RobertsFloresAlgorithm
    {
        public static List<int> RobertsFlores(int[] array)
        {
           
            if (array.Length == 0)
            {
                return new List<int>();
            }

            
            List<int> result = new List<int>();

            
            result.Add(array[0]);

            
            for (int i = 1; i < array.Length; i++)
            {
               
                if (array[i] > array[i - 1])
                {
                    result.Add(array[i]);
                }
                
                else if (result.Count > 0 && array[i] > result[result.Count - 1])
                {
                    result.Add(array[i]);
                }
            }

           
            return result;
        }

        public static void Main(string[] args)
        {
            
            int[] array = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

           
            List<int> result = RobertsFlores(array);

            
            Console.WriteLine("Результат алгоритма Робертса Флореса:");
            foreach (int item in result)
            {
                Console.Write(item + " ");
            }
        }
    }

}
