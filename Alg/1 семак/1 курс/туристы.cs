namespace туристы
{
    internal class Program
    {
        static void Main(string[] args)
        {
            List<int> point_stop = new List<int>();
            Console.Write("длина пути "); int way = int.Parse(Console.ReadLine());
            Console.Write("время захода и восхода солнца ");
            string[] sun = Console.ReadLine().Split();
            Console.Write("скорость передвижения в км/ч "); float speed = float.Parse(Console.ReadLine());
            Console.Write("кол-во временных пунктов "); int count_points = int.Parse(Console.ReadLine());
            Console.Write("расстояние от начала пути до каждого пункта ");
            float[] distances = Console.ReadLine().Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries).Select(i => float.Parse(i)).ToArray<float>();
            for (int i = distances.Length - 1; i > 0; i--)
            {
                distances[i] = distances[i] - distances[i - 1];
            }
            int[] daytime = sun[0].Split(new char[] { ':' }, StringSplitOptions.RemoveEmptyEntries).Select(i => int.Parse(i)).ToArray<int>();
            int[] nighttime = sun[1].Split(new char[] { ':' }, StringSplitOptions.RemoveEmptyEntries).Select(i => int.Parse(i)).ToArray<int>();
            int acceptable_daytime = -daytime[0] * 60 - daytime[1] + nighttime[0] * 60 + nighttime[1];

            double var = 0;
            int j = 0;
            while (++j < distances.Length)
            {
                
                var += distances[j];
                while ((var / speed * 60 < acceptable_daytime) && (j + 1 != distances.Length))
                {
                    var += distances[++j];
                }
                point_stop.Add(j);
                var = 0;
            }
            point_stop.Add(distances.Length);
            Console.Write("места где туристы останавливались "); foreach (int h in point_stop) { Console.Write(h + " "); }
            Console.Write("\n");
            Console.WriteLine("туристы шли дней - " + point_stop.Count);
        }
    }
}