namespace Линки_2
{
    class Workers
    {

        public int Employee_number { get; set; }
        public string Full_name { get; set; }
        public string Product_category { get; set; }
        public int Salary { get; set; }
        public int Number_of_goods_produced { get; set; }
        public int Price { get; set; }
        public Workers(int Employee_number, string Full_name, string Product_category, int Salary, int Number_of_goods_produced, int Price)
        {
            this.Employee_number = Employee_number;
            this.Full_name = Full_name;
            this.Product_category = Product_category;
            this.Salary = Salary;
            this.Number_of_goods_produced = Number_of_goods_produced;
            this.Price = Price;
        }

    }

    internal class Program
    {
        static void Main(string[] args)
        {
            string[] names = { "Ануфриев Глеб Андреевич", "Спиридонов Владислав Алексеевич", "Стяжкин Матвей Игоревич", "Эберт Роман Александрович", "Романов Александр Андреевич" };
            string[] categories = { "Еда ", "Бытовые товары", "Трусы" };
            List<Workers> workers = new List<Workers>();
            Random random = new Random();
            Workers worker;
            for (int i = 0; i < names.Length; i++)
            {
                worker = new Workers(random.Next(0, 20), names[i], categories[random.Next(3)], random.Next(100, 500), random.Next(1, 8), random.Next(100, 250));
                workers.Add(worker);

            }
            var numQuery1 = from employee in workers where (employee.Salary < employee.Number_of_goods_produced * employee.Price) select employee;
            Console.WriteLine($"Задание 1) работники, получающие меньше чем они зарабатывают:{numQuery1.Count()}");
            var numQuery23 = workers.GroupBy(work => work.Product_category);
            foreach (var item in numQuery23)
            {
                Console.WriteLine($"Задание 2) количество товара по {item.Key} категории:{item.Sum(p=>p.Number_of_goods_produced)}");
                Console.WriteLine($"Задание 3) объем товара по {item.Key} категории:{item.Sum(p => p.Price)* item.Sum(p => p.Number_of_goods_produced)}");
            }
            var numQuery4 = from employee in workers where (employee.Salary > (employee.Number_of_goods_produced * employee.Price)*1.5) select employee;
            Console.WriteLine($"Задание 4) работники, получающие больше 50% чем они зарабатывают:{numQuery4.Count()}");
        }
    }
}
