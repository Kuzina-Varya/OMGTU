using System.Xml.Linq;

namespace цеха
{
    internal class Program
    {
       
        class Workshop
        {
            private String Name;
            private int Year;
            private int ValueOfProduction;

            public Workshop(String Name, int Year, int ValueOfProduction)
            {
                this.Name = Name;
                this.Year = Year;
                this.ValueOfProduction = ValueOfProduction;
            }

            public String getName(Workshop workshop)
            {
                return workshop.Name;
            }

            public int getYear(Workshop workshop)
            {
                return workshop.Year;
            }

            public int getValueOfProduction(Workshop workshop)
            {
                return workshop.ValueOfProduction;
            }

            public void setName(Workshop workshop, String name)
            {
                workshop.Name = name;
            }
            public void setYear(Workshop workshop, int year)
            {
                workshop.Year = year;
            }
            public void setValueOfProduction(Workshop workshop, int valueOfProduction)
            {
                workshop.ValueOfProduction = valueOfProduction;
            }

            public int getSumOfProduction(String name, Workshop[] workshops)
            {
                int sum = 0;
                for (int i = 0; i < workshops.Length; i++)
                {
                    if (workshops[i].getName(workshops[i]) == name)
                    {
                        sum = sum + workshops[i].getValueOfProduction(workshops[i]);
                    }
                }
                return sum;
            }

            public String getProductionByYear(String name, Workshop[] workshops)
            {
                String productionByYear = "" + name + ": \n";
                for (int i = 0; i < workshops.Length; i++)
                {
                    if (workshops[i].getName(workshops[i]) == name)
                    {
                        productionByYear = productionByYear + workshops[i].getYear(workshops[i]) + ": " + workshops[i].getValueOfProduction(workshops[i]) + "\n";
                    }
                }
                return productionByYear;
            }
        }
        static void Main(string[] args)
        {
            String name1 = "Цех 1", name2 = "Цех 2", name3 = "Объединенный заводческий цех города Кушкек";

            Workshop[] workshops = new Workshop[15];
            workshops[0] = new Workshop(name1, 2010, 100);
            workshops[1] = new Workshop(name2, 2011, 1100);
            workshops[2] = new Workshop(name3, 2010, 800);
            workshops[3] = new Workshop(name1, 2012, 90);
            workshops[4] = new Workshop(name2, 2012, 1200);
            workshops[5] = new Workshop(name3, 2012, 600);
            workshops[6] = new Workshop(name1, 2013, 200);
            workshops[7] = new Workshop(name2, 2013, 300);
            workshops[8] = new Workshop(name3, 2013, 400);
            workshops[9] = new Workshop(name1, 2015, 100);
            workshops[10] = new Workshop(name2, 2015, 350);
            workshops[11] = new Workshop(name3, 2015, 700);
            workshops[12] = new Workshop(name1, 2017, 130);
            workshops[13] = new Workshop(name2, 2017, 700);
            workshops[14] = new Workshop(name3, 2017, 900);

            Console.WriteLine("Суммарный объем выпуска образования " + name1 + ": " + workshops[0].getSumOfProduction(name1, workshops));
            Console.WriteLine("Суммарный объем выпуска образования " + name2 + ": " + workshops[0].getSumOfProduction(name2, workshops));
            Console.WriteLine("Суммарный объем выпуска образования " + name3 + ": " + workshops[0].getSumOfProduction(name3, workshops));
            Console.WriteLine("Интенсивность производства по годам для образования " + workshops[0].getProductionByYear(name1, workshops));
            Console.WriteLine("Интенсивность производства по годам для образования " + workshops[0].getProductionByYear(name2, workshops));
            Console.WriteLine("Интенсивность производства по годам для образования " + workshops[0].getProductionByYear(name3, workshops));
        }
    }
}