namespace _04._10
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int n = Convert.ToInt32(Console.ReadLine());
            int[] array = new int[n];
            int sumb = 0;
            int countb = 0;
            int sum_countb = 0;
            int countarr = 0;
            int countс = 0;
            bool c = false;
            int countd = 0;
            int d = 0;//сумма цифр
            bool flag = false;
            for (int i = 0; i < array.Length; i++)
            {
                array[i] = Convert.ToInt32(Console.ReadLine());
            }
            for (int i = 0; i < array.Length; i++)
            {

                string array2 = Convert.ToString(array[i]);

                char[] Array2 = array2.ToCharArray();

                for (int j = 0; j < Array2.Length; j++)
                {


                    int b = Convert.ToInt32(Array2[j] - '0');//правильная конвертация в инт чаровского числа

                    if (b % 2 == 0)
                    {
                        sumb += b;
                    }

                    if ((sumb % 16 == 0) && (sumb >= 16))
                    {
                        countb += 1;
                    }
                    else
                    {
                        countb = 0;
                    }
                    sum_countb += countb;

                    int arr = Convert.ToInt32(Array2[0] - '0');
                    if (((arr % 3) == (arr % 5)) && ((arr % 7) == (arr % 3)))
                    {
                        countarr += 1;
                    }
                    d += b;


                }

                if (d % 2 == 0)
                {
                    countd += 1;
                    d = 0;
                }
                else
                {
                    countd = 0;
                }
                if (countd == n)
                {
                    flag = true;
                }
                c = array2.Contains("5");
                if (c == true)
                {
                    countс += array[i];
                }

            }
            Console.WriteLine("Количество кратное 16:" + sum_countb);
            Console.WriteLine("Количество элементов,которые при переводе в 3ю,5ю,7ю СС имеют на конце 1:" + countarr);
            Console.WriteLine("Сумма элементов в которых содержится 5:" + countс);
            if (flag == true)
            {
                Console.WriteLine("Все элементы имеют четную сумму цифр");
            }
            else
            {
                Console.WriteLine("Не все элементы имеют четную сумму цифр");
            }
        }
    }
}