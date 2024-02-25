using System.Collections;

namespace _18_02
{
    class Menu
    {
        public string Minu = "Meню:";
        public string Array = "1.Array";
        public string Arraylist = "2.ArrayList";
        public string Sortedlist = "3.SortedList";
        public string Exit = "4.Выход";
        public void Start()
        {
            Console.WriteLine(Minu);
            Console.WriteLine(Array);
            Console.WriteLine(Arraylist);
            Console.WriteLine(Sortedlist);
            Console.WriteLine(Exit);
        }
        public void First()
        {
            Console.WriteLine("1. Count");
            Console.WriteLine("2. BinSearch");
            Console.WriteLine("3. Copy");
            Console.WriteLine("4. Find");
            Console.WriteLine("5. FindLast");
            Console.WriteLine("6. IndexOf");
            Console.WriteLine("7. Reverse");
            Console.WriteLine("8. Resize");
            Console.WriteLine("9. Sort");
            Console.WriteLine("10. Выход");

        }
        public void Second()
        {
            Console.WriteLine("1. Count");
            Console.WriteLine("2. BinSearch");
            Console.WriteLine("3. Copy");
            Console.WriteLine("4. IndexOf");
            Console.WriteLine("5. Insert");
            Console.WriteLine("6. Reverse");
            Console.WriteLine("7. Sort");
            Console.WriteLine("8. Add");
            Console.WriteLine("9. Выход");
        }
        public void Third()
        {
            Console.WriteLine("1. Add");
            Console.WriteLine("2. IndexOf(по значению)");
            Console.WriteLine("3. IndexOf(по ключу)");
            Console.WriteLine("4. Вывод ключа по индексу");
            Console.WriteLine("5. Вывод значения по индексу");
            Console.WriteLine("6. Выход");
        }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            Menu newmenu = new Menu();
            newmenu.Start();
            Console.WriteLine("Введите с чем хотите работать:");
            int operation = Convert.ToInt32(Console.ReadLine());

            while (operation != 4)
            {

                switch (operation)
                {
                    case 1:
                        Console.WriteLine("Введите диапазон значений, с которым хотите работать:");
                        int n = Convert.ToInt32(Console.ReadLine());
                        int[] array = new int[n];
                        Console.WriteLine("Введите числовые значения:");
                        for (int i = 0; i < n; i++)
                        {
                            array[i] = Convert.ToInt32(Console.ReadLine());
                        }
                        newmenu.First();
                        Console.WriteLine("Введите операцию:");
                        int procedure = Convert.ToInt32(Console.ReadLine());
                        while (procedure != 10)
                        {
                            switch (procedure)
                            {
                                case 1:
                                    Console.WriteLine("Введите значение, чтобы узнать сколько элементов с этим значение содержится в массиве:");
                                    int value1 = Convert.ToInt32(Console.ReadLine());
                                    Console.WriteLine(array.Count(p => p == value1));
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.First();
                                    procedure = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 2:
                                    Console.WriteLine("Введите значение, индекс котрого хотите узнать:");
                                    int value2 = Convert.ToInt32(Console.ReadLine());
                                    Array.Sort(array);
                                    int index = Array.BinarySearch(array, value2);
                                    Console.WriteLine(index);
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.First();
                                    procedure = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 3:
                                    int[] myarray = new int[10];
                                    Console.WriteLine("Вставим ваш масси в данный:");
                                    for (int i = 0; i < 10; i++)
                                    {
                                        myarray[i] = i;
                                        Console.WriteLine(myarray[i]);
                                    }
                                    Console.WriteLine("_________________________________________________________________________");

                                    Array.Copy(array, myarray, array.Length);
                                    for (int i = 0; i < myarray.Length; i++)
                                    {
                                        Console.WriteLine(myarray[i]);
                                    }
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.First();
                                    procedure = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 4:
                                    Console.WriteLine("Введите элемент, наличие которого вы хотите проверить в массиве(если вывелось это значение, значит элемент содершится в массиве, если 0-то не содлержится:");
                                    int element1 = Convert.ToInt32(Console.ReadLine());
                                    Console.WriteLine(Array.Find(array, p => p == element1));
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.First();
                                    procedure = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 5:
                                    Console.WriteLine("Введите элемент,наличие котрого вы хотите проверить в массиве:");
                                    int element2 = Convert.ToInt32(Console.ReadLine());
                                    Console.WriteLine(Array.FindLast(array, p => p == element2));
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.First();
                                    procedure = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 6:
                                    Console.WriteLine("Введите значение элемента, индекс первого вхождения которого вы хотите узнать:");
                                    int element3 = Convert.ToInt32(Console.ReadLine());
                                    Console.WriteLine(Array.IndexOf(array, element3));
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.First();
                                    procedure = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 7:
                                    Console.WriteLine("------------------------------------------------------");
                                    Array.Reverse(array);
                                    for (int i = 0; i < array.Length; i++)
                                    {
                                        Console.WriteLine(array[i]);
                                    }
                                    Console.WriteLine("-------------------------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.First();
                                    procedure = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 8:
                                    Console.WriteLine("Введите значение, до которого хотите увеличить вместимость массива:");
                                    int capacity = Convert.ToInt32(Console.ReadLine());
                                    Array.Resize(ref array, capacity);
                                    Console.WriteLine(array.Length);
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.First();
                                    procedure = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 9:

                                    Array.Sort(array);
                                    Console.WriteLine("Отсортированный массив:");
                                    for (int i = 0; i < array.Length; i++)
                                    {
                                        Console.WriteLine(array[i]);
                                    }
                                    Console.WriteLine("---------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.First();
                                    procedure = Convert.ToInt32(Console.ReadLine());
                                    break;
                            }

                        }
                        Console.WriteLine("Введите с чем хотите работать:");
                        newmenu.Start();
                        operation = Convert.ToInt32(Console.ReadLine());
                        break;
                    case 2:
                        Console.WriteLine("Создан ArrayList:");
                        ArrayList list = new ArrayList();
                        list.Add(2.0);
                        list.Add(2.5);
                        list.Add(5.6);
                        list.Add(4.5);
                        list.Add(7.2);
                        list.Add(9.1);
                        list.Add(4.1);
                        list.Add(8.0);
                        for (int i = 0; i < list.Count; i++)
                        {
                            Console.WriteLine(list[i]);
                        }
                        Console.WriteLine("--------------------------------");
                        Console.WriteLine("Введите операцию:");
                        newmenu.Second();
                        int variable = Convert.ToInt32(Console.ReadLine());
                        while (variable != 9)
                        {
                            switch (variable)
                            {
                                case 1:
                                    Console.WriteLine("Число элементов,содержащееся в списке:");
                                    Console.WriteLine(list.Count);
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Second();
                                    variable = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 2:
                                    Console.WriteLine("Введите значение, индекс котрого хотите узнать:");
                                    double meaning = Convert.ToDouble(Console.ReadLine());
                                    Console.WriteLine(list.BinarySearch(meaning));


                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Second();
                                    variable = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 3:
                                    Console.WriteLine("Вставим ваш список в данный массив:");
                                    double[] arr = new double[10];

                                    for (int i = 0; i < 10; i++)
                                    {
                                        Console.WriteLine(arr[i] = i);
                                    }
                                    Console.WriteLine("--------------------------------");
                                    list.CopyTo(arr);
                                    for (int i = 0; i < arr.Length; i++)
                                    {
                                        Console.WriteLine(arr[i]);
                                    }
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Second();
                                    variable = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 4:
                                    Console.WriteLine("Введите значение, идекс которого хотите узнать(в формате double):");
                                    double meaning1 = Convert.ToDouble(Console.ReadLine());
                                    Console.WriteLine(list.IndexOf(meaning1));
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Second();
                                    variable = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 5:
                                    Console.WriteLine("Введите значение, которое хотите установить:");
                                    double import = Convert.ToDouble(Console.ReadLine());
                                    Console.WriteLine("Введите индекс, по которому установить значение:");
                                    int number = Convert.ToInt32(Console.ReadLine());
                                    list.Insert(number, import);
                                    for (int i = 0; i < list.Count; i++)
                                    {
                                        Console.WriteLine(list[i]);
                                    }
                                    Console.WriteLine("-----------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Second();
                                    variable = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 6:
                                    list.Reverse();
                                    for (int i = 0; i < list.Count; i++)
                                    {
                                        Console.WriteLine(list[i]);
                                    }
                                    Console.WriteLine("-----------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Second();
                                    variable = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 7:
                                    list.Sort();
                                    Console.WriteLine("Отсортированный список:");
                                    for (int i = 0; i < list.Count; i++)
                                    {
                                        Console.WriteLine(list[i]);
                                    }
                                    Console.WriteLine("-----------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Second();
                                    variable = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 8:
                                    Console.WriteLine("Введите значение, которое хотите поместить в список:");
                                    var import2 = Console.ReadLine();
                                    list.Add(import2);
                                    Console.WriteLine("Новый список:");
                                    for (int i = 0; i < list.Count; i++)
                                    {
                                        Console.WriteLine(list[i]);
                                    }
                                    Console.WriteLine("-----------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Second();
                                    variable = Convert.ToInt32(Console.ReadLine());
                                    break;
                            }
                        }
                        Console.WriteLine("Введите с чем хотите работать:");
                        newmenu.Start();
                        operation = Convert.ToInt32(Console.ReadLine());
                        break;
                    case 3:
                        Console.WriteLine("Создан SortedList:");
                        SortedList sortedList = new SortedList();
                        sortedList.Add("first",5);
                        sortedList.Add("second", 8);
                        sortedList.Add("third", 7);
                        sortedList.Add("fourth", 4);
                        sortedList.Add("fifth", 7);
                        sortedList.Add("sixth", 9);
                        sortedList.Add("seventh", 6);
                        sortedList.Add("neighth", 2);
                        for(int i=0;i<sortedList.Count;i++)
                        {
                            Console.WriteLine(sortedList.GetKey(i)+" "+sortedList.GetByIndex(i));
                        }
                        
                        Console.WriteLine("--------------------------------");
                        Console.WriteLine("Введите операцию:");
                        newmenu.Third();
                        int show = Convert.ToInt32(Console.ReadLine());
                        while (show != 6)
                        {
                            
                            switch(show)
                            {
                                case 1:
                                    Console.WriteLine("Введите элемент, который нужно добавить:");
                                    int x=Convert.ToInt32(Console.ReadLine());
                                    Console.WriteLine("Введите ключ,по которому нужно добавить:");
                                    string key = Console.ReadLine();
                                    sortedList.Add(key, x);
                                    for(int i=0;i<sortedList.Count;i++)
                                    {
                                        Console.WriteLine(sortedList.GetKey(i)+" "+sortedList.GetByIndex(i));
                                    }
                                    Console.WriteLine("-----------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Third();
                                    show = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 2:
                                    Console.WriteLine("Введите значение,индекс первого вхождения котрого хотите узнать:");
                                    int x2=Convert.ToInt32(Console.ReadLine());
                                    Console.WriteLine(sortedList.IndexOfValue(x2));
                                    Console.WriteLine("-----------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Third();
                                    show = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 3:
                                    Console.WriteLine("Введите ключ элемента,индекс первого вхождения котрого хотите узнать:");
                                    string key2 = Console.ReadLine();
                                    Console.WriteLine(sortedList.IndexOfKey(key2));
                                    Console.WriteLine("-----------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Third();
                                    show = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 4:
                                    Console.WriteLine("Введите индекс, ключ которого хотите узнать:");
                                    int index=Convert.ToInt32(Console.ReadLine());
                                    Console.WriteLine(sortedList.GetKey(index));
                                    Console.WriteLine("-----------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Third();
                                    show = Convert.ToInt32(Console.ReadLine());
                                    break;
                                case 5:
                                    Console.WriteLine("Введите индекс, значение которого хотите узнать");
                                    int index2=Convert.ToInt32(Console.ReadLine());
                                    Console.WriteLine(sortedList.GetByIndex(index2));
                                    Console.WriteLine("-----------------------------------------");
                                    Console.WriteLine("Введите операцию:");
                                    newmenu.Third();
                                    show = Convert.ToInt32(Console.ReadLine());
                                    break;
                            }
                                

                            
                        }
                        Console.WriteLine("Введите с чем хотите работать:");
                        newmenu.Start();
                        operation = Convert.ToInt32(Console.ReadLine());
                        break;
                }

            }
        }
    }
}