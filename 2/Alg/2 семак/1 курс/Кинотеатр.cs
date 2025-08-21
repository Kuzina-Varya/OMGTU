class Kristal
{
    public string Film { get; set; }
    public double Time { get; set; }
    public double Time_start { get; set; }
    public double Time_end { get; set;}
    public int Bought_sits { get; set; }
    public int Free_sits { get; set; }
    public Kristal(string film, double time, double time_start, double time_end, int bought_sits,int free_sits)
    {
        Film = film;
        Time = time;
        Time_start = time_start;
        Time_end = time_end;
        Bought_sits=bought_sits;
        Free_sits=free_sits;
    }
}
namespace кинотеатр
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string[] films = { "Титаник", "Во все тяжкие", "Следствие ведут колобки", "Матье получает балл", "Узкоглазая шиншила" };
            double[] time = { 1.0, 2.0, 3.0, 4.0, 5.0 };
            double[] time_start = { 12.00, 13.00, 14.00, 15.00, 16.00 };
            double[] time_end = {13.00,15.00,17.00,19.00,21.00 };
            int[] bought_sits = {250,350,150,600,450 };
            int[] free_sits = {100,50,25,63,458};
            List<Kristal> kristal_list = new List<Kristal>();
            for(int i=0;i<films.Length;i++) 
            {
                Kristal kristal = new Kristal(films[i], time[i], time_start[i], time_end[i], bought_sits[i], free_sits[i]);
                kristal_list.Add(kristal);
            }
            var result1 = from l in kristal_list where (l.Bought_sits + l.Free_sits) * 0.5 < l.Bought_sits select l;
            var result2 = from k in kristal_list where k.Time_start > 15.00 select k;
            Console.WriteLine("Задание 1:");
            foreach(var l in result1)
            {
                Console.WriteLine(l.Film);
            }
            Console.WriteLine("Задание 2:");
            foreach (var k in result2) 
            {
                Console.WriteLine(k.Film);
            }

        }
    }
}
