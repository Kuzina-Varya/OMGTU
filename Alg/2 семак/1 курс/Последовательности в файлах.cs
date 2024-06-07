using System.IO;
namespace Последовательности_в_файлах
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string file1 = @"C:\Users\Доктор Варвар\Desktop\_\алгоритмизация\Последовательность по возрастанию.txt";
            string file2 = @"C:\Users\Доктор Варвар\Desktop\_\алгоритмизация\Последовательность по убыванию.txt";

            using (StreamReader sr1 = new StreamReader(file1))
            {
                using (StreamReader sr2 = new StreamReader(file2))
                {
                    using (StreamWriter sw = new StreamWriter(File.Create("Up_Down.txt")))
                    {
                        sw.WriteLine(sr1.ReadToEnd());
                        sw.WriteLine(sr2.ReadToEnd());
                    }
                }


            }

        }
    }
}
