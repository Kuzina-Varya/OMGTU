using System.Linq;
namespace Линки_1
{
    class Ozon
    {
        public int vendor_code { get; set; }
        public string vendor_name { get; set; }
        public string category { get; set; }
        public int quantity { get; set; }
        public int price { get; set; }
        public int warehouse_number { get; set; }
        public Ozon(int vendor_code, string vendor_name, string category, int quantity, int price, int warehouse_number)
        {
            this.vendor_code = vendor_code;
            this.vendor_name = vendor_name;
            this.category = category;
            this.quantity = quantity;
            this.price = price;
            this.warehouse_number = warehouse_number;
        }

    }

    internal class Program
    {

        static void Main(string[] args)
        {
            string[] ventors = { "молоко", "хлеб", "стул", "стол", "юбка" };
            string[] categories = { "еда", "мебель", "одежда" };
            Random random = new Random();
            List<Ozon> list = new List<Ozon>();
            Ozon ozon;
            for (int i = 0; i < ventors.Length; i++)
            {
                if (ventors[i].StartsWith("ю"))
                {
                    ozon = new Ozon(random.Next(0, 100), ventors[i], categories[2], random.Next(1, 10), random.Next(100, 500), random.Next(0, 3));
                }
                else if (ventors[i].StartsWith("с"))
                {
                    ozon = new Ozon(random.Next(0, 100), ventors[i], categories[1], random.Next(1, 10), random.Next(100, 500), random.Next(0, 3));
                }
                else
                {
                    ozon = new Ozon(random.Next(0, 100), ventors[i], categories[0], random.Next(1, 10), random.Next(100, 500), random.Next(0, 3));
                }
                list.Add(ozon);
            }
            var numQuery1 = from l in list.GroupBy(l => l.warehouse_number) select l;
            Console.WriteLine("Задание 1 и 4:");
            foreach (var items in numQuery1)
            {
                Console.WriteLine($"1) На {items.Key} складе:{items.Sum(p => p.quantity * p.price)}");
                var numQuery4 = items.Min(p => p.price);
                foreach (var item in items)
                {
                    if (item.price == numQuery4)
                    {
                        Console.WriteLine($"4) На {items.Key} складе самый дешевый товар:{item.vendor_name}");
                    }

                }

            }
            var numQuery23 = from l in list.GroupBy(l => l.category) select l;
            Console.WriteLine("Задание 2 и 3:");
            foreach (var items in numQuery23)
            {
                Console.WriteLine($"2) В {items.Key} категории максимальная цена товара:{items.Max(p => p.price)}");
                Console.WriteLine($"3) В {items.Key} категории средняя цена товаров:{items.Average(p => p.price)}");
            }
        }
    }
}