#include <Python.h>
#include <string>
#include <stdlib.h>
#include <iostream>


int main (int argc, char *argv[] ){
	const char *scriptDirectoryName = "./pyutils";
	
	Py_SetProgramName(argv[0]);
	PyObject *pName, *pModule, *pDict, *pFunc, *pValue, *presult;
	
	
	// Initialize the Python Interpreter
	Py_Initialize();
	PyObject *sysPath = PySys_GetObject("path");
	PyObject *path = PyString_FromString(scriptDirectoryName);
	int result = PyList_Insert(sysPath, 0, path);
	pModule = PyImport_ImportModule("arbName");
	if (PyErr_Occurred())
		PyErr_Print();
//	printf("%p\n", pModule);
	
	
	
	// pDict is a borrowed reference
	pDict = PyModule_GetDict(pModule);
	
	// pFunc is also a borrowed reference
	pFunc = PyDict_GetItemString(pDict, (char*)"someFunction");
	
	if (PyCallable_Check(pFunc))
	{
		pValue=Py_BuildValue("(z)",(char*)"something");
		PyErr_Print();
		printf("Let's give this a shot!\n");
		presult=PyObject_CallObject(pFunc,pValue);
		PyErr_Print();
	} else
	{
		PyErr_Print();
	}
	printf("Result is %ld\n", PyInt_AsLong(presult));
	Py_DECREF(pValue);
	
	// Clean up
	Py_DECREF(pModule);
	
	
	// Finish the Python Interpreter
	Py_Finalize();
	
	return 0;
}
