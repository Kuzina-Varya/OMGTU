namespace интерфейсы_и_делегаты2_мойка_
{
    class Car
    {
        public int Id { get; set; }
        public string Color { get; set; }
        public bool Washed { get; set; }
        public Car(int id, string color, bool washed = false)
        {
            Id = id;
            Color = color;
            Washed = washed;
        }
    }
    delegate void Road(Car car);
    class Garage
    {
        public List<Car> Places { get; set; }
        public Garage()
        {
            Places = new List<Car>();
        }
        public void Add(Car car)
        {
            Places.Add(car);
        }
    }
    class Washing
    {

        static public void Wash(Car car)
        {
            Console.WriteLine($"Машина {car.Id} помыта");
            car.Washed = true;
        }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            string[] colors = { "красный", "желтый", "зеленый", "серый", "черный" };

            //Washing washing = new Washing();
            // List<Car> cars = new List<Car>();
            Garage list = new Garage();
            Road road;
            for (int i = 0; i < colors.Length; i++)
            {
                Car car = new Car(i, colors[i]);
                list.Add(car);

                road = Washing.Wash;
                road(list.Places[i]);


            }
        }
    }
}
