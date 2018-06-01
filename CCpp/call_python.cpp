#include <Python.h>
#include <stdlib.h>

int main (int argc, char *argv[] ){
    // Set PYTHONPATH TO working directory
    setenv("PYTHONPATH",".",1);

    Py_SetProgramName(argv[0]);
    Py_Initialize();
    PyRun_SimpleString("from time import time,ctime\n"
                                 "print 'Today is',ctime(time())\n");
    Py_Finalize();
    
    return 0;
}
