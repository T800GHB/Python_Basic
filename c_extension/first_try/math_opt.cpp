#include <Python.h>
#include <iostream>
using namespace std;

static int add(int arg1 = 0, int arg2 = 0){
    return arg1 + arg2;
}
static PyObject *
add_wrap(PyObject *self, PyObject *args)
{
    int arg1;
    int arg2;

    if (!PyArg_ParseTuple(args, "ii", &arg1, &arg2))
        return NULL;
    int result = add(arg1, arg2);

    return (PyObject*)Py_BuildValue("i", result);
}

static int sub(int arg1 = 0, int arg2 = 0){
    return arg1 - arg2;
}
static PyObject *
sub_wrap(PyObject *self, PyObject *args)
{
    int arg1;
    int arg2;
    if (!PyArg_ParseTuple(args, "ii", &arg1, &arg2))
        return NULL;

    int result = sub(arg1, arg2);

    return (PyObject*)Py_BuildValue("i", result);
}

static PyMethodDef MathMethods[] = {

    {"add",  add_wrap, METH_VARARGS,
     "Execute add operation."},
    {"sub", sub_wrap, METH_VARARGS,
     "Execute subtraction operation."},

    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef math_module = {
   PyModuleDef_HEAD_INIT,
   "math_opt",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   MathMethods
};

PyMODINIT_FUNC
PyInit_math_opt(void)
{
    return PyModule_Create(&math_module);
}

//To add the module to the initialization table, use this block of code
// int main(int argc, char *argv[])
// {
//     wchar_t *program = Py_DecodeLocale(argv[0], NULL);
//     if (program == NULL) {
//         fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
//         exit(1);
//     }

//     /* Add a built-in module, before Py_Initialize */
//     PyImport_AppendInittab("math_opt", PyInit_math_opt);

//     /* Pass argv[0] to the Python interpreter */
//     Py_SetProgramName(program);

//     /* Initialize the Python interpreter.  Required. */
//     Py_Initialize();

//     /* Optionally import the module; alternatively,
//        import can be deferred until the embedded script
//        imports it. */
//     //PyImport_ImportModule("math_opt");

//     PyMem_RawFree(program);
//     return 0;
// }
