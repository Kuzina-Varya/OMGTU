using System.Runtime.InteropServices;

namespace CodeTest
{
    internal class Program
    {
        static void Main(string[] args)
        {

            string path = "input.txt";
            StreamReader reader = new StreamReader(path);

            int[][] mass = new int[2][];

            for (int i = 0; i < 2; i++)
            {
                mass[i] = Array.ConvertAll(reader.ReadLine().Split(' ', '\n').ToArray(), int.Parse);
            }

            int dim = mass[0][0];
            int kolvo = mass[0][1];

            int start_X = mass[1][0];
            int start_Y = mass[1][1];
            int start_Z = mass[1][2];


            int[][] vrasheniya = new int[kolvo][];

            for (int i = 0; i < kolvo; i++)
            {
                string str = reader.ReadLine();

                if (str[0] == 'Z')
                {
                    str = str.Replace('Z', '3');
                }
                else if (str[0] == 'Y')
                {
                    str = str.Replace('Y', '2');
                }
                else if (str[0] == 'X')
                {
                    str = str.Replace('X', '1');
                }

                vrasheniya[i] = Array.ConvertAll(str.Split(' ', '\n').ToArray(), int.Parse);
            }

            Console.WriteLine($"{start_X} {start_Y} {start_Z}");



            for (int main_I = 0; main_I < kolvo; main_I++)
            {



                if (vrasheniya[main_I][0] == 1 && vrasheniya[main_I][1] == start_X) //////////////////////// X
                {


                    if (vrasheniya[main_I][2] == -1)
                    {


                        int a = 0;
                        for (int i = dim; i > 0; i--, a++)
                            if (start_Y == i)
                                break;

                        int b = 0;
                        for (int j = dim; j > 0; j--, b++)
                            if (start_Z == j)
                                break;

                        start_Y = 1 + b;
                        start_Z = (dim) - a;

                    }
                    else if (vrasheniya[main_I][2] == 1)
                    {


                        int a = 0;
                        for (int i = 1; i <= dim; i++, a++)
                            if (start_Y == i)
                                break;

                        int b = 0;
                        for (int j = 1; j <= dim; j++, b++)
                            if (start_Z == j)
                                break;

                        start_Y = 1 + b;
                        start_Z = (dim) - a;
                    }
                }
                else if (vrasheniya[main_I][0] == 2 && vrasheniya[main_I][1] == start_Y) ///////////////////////// Y
                {


                    if (vrasheniya[main_I][2] == -1)
                    {


                        int a = 0;
                        for (int i = dim; i > 0; i--, a++)
                            if (start_X == i)
                                break;

                        int b = 0;
                        for (int j = dim; j > 0; j--, b++)
                            if (start_Z == j)
                                break;

                        start_X = 1 + b;
                        start_Z = (dim) - a;
                    }
                    else if (vrasheniya[main_I][2] == 1)
                    {


                        int a = 0;
                        for (int i = 1; i <= dim; i++, a++)
                            if (start_X == i)
                                break;

                        int b = 0;
                        for (int j = 1; j <= dim; j++, b++)
                            if (start_Z == j)
                                break;

                        start_X = 1 + b;
                        start_Z = (dim) - a;
                    }
                }
                else if (vrasheniya[main_I][0] == 3 && vrasheniya[main_I][1] == start_Z) ///////////////////////// Z
                {




                    if (vrasheniya[main_I][2] == -1)
                    {

                        int a = 0;
                        for (int i = dim; i > 0; i--, a++)
                            if (start_X == i)
                                break;

                        int b = 0;
                        for (int j = dim; j > 0; j--, b++)
                            if (start_Y == j)
                                break;

                        start_X = 1 + b;
                        start_Y = (dim) - a;

                    }
                    else if (vrasheniya[main_I][2] == 1)
                    {


                        int a = 0;
                        for (int i = 1; i <= dim; i++, a++)
                            if (start_X == i)
                                break;

                        int b = 0;
                        for (int j = 1; j <= dim; j++, b++)
                            if (start_Y == j)
                                break;

                        start_X = 1 + b;
                        start_Y = (dim) - a;
                    }

                }



            }

            Console.WriteLine($"{start_X} {start_Y} {start_Z}");

            Console.ReadKey();
        }
    }
}