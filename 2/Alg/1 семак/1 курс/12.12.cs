using System.Net;
using System.Security.Cryptography;

namespace classessssss
{
    public class Library
    {
       

        public string Author { get; set; }//та же самая штука что и сверху + присвоение значения по дефолту
        public string Title { get; set; }
        public string Age { get; set; }

        private List<string> Date = new();

        public Library(string Author = "", string Title = "", string Age = "")
        {
            this.Author = Author;
            this.Title = Title;
            this.Age = Age;
        }
        public void DateAdd(string s)
        {
            Date.Add(s);
        }

        public List<string> DateGet() { return Date; }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            List<Library> lib = new();
            string Name = "";
            int j = 0;
            while (Name != "Загрузить книги")
            {
                Name = Console.ReadLine();
                if (Name != "Загрузить книги")
                {
                    lib.Add(new Library(Name, Console.ReadLine(), Console.ReadLine()));
                    string s = "1";
                    while (s != "")
                    {
                        s = Console.ReadLine();
                        if (s != "")
                        {
                            lib[j].DateAdd(s);
                        }
                    }
                    j++;
                }
            }
            Console.WriteLine("Введите условие для 2 задания: ");
            int year = Convert.ToInt32(Console.ReadLine());
            Console.WriteLine("Введите условие для 3 задания: ");
            string writer = Console.ReadLine();
            Console.WriteLine("Введите условие для 4 задания: ");
            string book = Console.ReadLine();
            for (int k = 0; k < lib.Count(); k++)
            {
                for (int i = 0; i < lib[k].DateGet().Count(); i++)
                {
                    Console.WriteLine($"1 задание: {lib[k].Author} - {lib[k].Title}: {lib[k].DateGet()[i]}");
                    if (lib[k].Title == book)
                    {
                        Console.WriteLine($"4 задание: {lib[k].Author} - {lib[k].Title} - {lib[k].Age}: {lib[k].DateGet()[i]}");
                    }
                }
                if (Convert.ToInt32(lib[k].Age) > year)
                {
                    Console.WriteLine($"2 задание: {lib[k].Author} - {lib[k].Title}: {lib[k].Age}");
                }
                if (lib[k].Author == writer)
                {
                    Console.WriteLine($"3 задание: {lib[k].Author} - {lib[k].Title}");
                }
            }
        }
    }
}
