namespace Запросы
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int[] array = { 1, 5, 2, 3, 48, 59, 61, 25, 58, 74, 71, 72, 35, 65, 99 };
            List<int> list = new List<int>();
            int value;
            for (int i = 0; i < array.Length; i++) 
            {
                value = array[i];
                while (array[i] != 0)
                {
                    if (array[i]%10%2==0)
                    {
                  
                        list.Add(value);
                        break;
                    }
                    else
                    {
                        
                        array[i] /= 10;

                    }
                    
                }
            }
            var linq = from a1 in list
                       where a1 % 3 == 0
                       select a1 ;
            foreach (var a in linq)
            {
                Console.WriteLine(a);
            }
        }
    }
}

