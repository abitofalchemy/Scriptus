#include <Python.h>
#include <iostream>
#include <string>

int main(int argc, char* argv[])
{
    Py_Initialize();
    std::clog << "Type lines of text:" << std::endl;
    std::string input;
    while (true)
    {
        std::getline(std::cin, input);
        if (!std::cin.good())
        {
            break;
        }
        std::cout << input << std::endl;
    }
    Py_Finalize();
    return 0;
}
