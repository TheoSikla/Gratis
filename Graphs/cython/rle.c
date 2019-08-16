#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_RLEN 50

#include <Python.h>

/* Returns the Run Length Encoded string for the
   source string src */
char* encode(char* src)
{
    int rLen;
    char count[MAX_RLEN];
    int len = strlen(src);

    /* If all characters in the source string are different,
    then size of destination string would be twice of input string.
    For example if the src is "abcd", then dest would be "a1b1c1d1"
    For other inputs, size would be less than twice.  */
    char* dest = (char*)malloc(sizeof(char) * (len * 2 + 1));

    int i, j = 0, k;

    /* traverse the input string one by one */
    for (i = 0; i < len; i++) {

        /* Copy the first occurrence of the new character */
        dest[j++] = src[i];

        /* Count the number of occurrences of the new character */
        rLen = 1;
        while (i + 1 < len && src[i] == src[i + 1]) {
            rLen++;
            i++;
        }

        /* Store rLen in a character array count[] */
        sprintf(count, "%d", rLen);

        /* Copy the count[] to destination */
        for (k = 0; *(count + k); k++, j++) {
            dest[j] = count[k];
        }
    }

    /*terminate the destination string */
    dest[j] = '\0';
    return dest;
}


static PyObject* fib(PyObject* self,PyObject* args)
{
    char* n;
    if (!PyArg_ParseTuple(args,"s",&n))
        return NULL;
    return Py_BuildValue("s", encode(n));
}

static PyMethodDef module_methods[] = {
    {"fib",(PyCFunction) fib, METH_VARARGS,"calculates the fibonachi number"},
    {NULL,NULL,0,NULL}
};


static struct PyModuleDef demo =
{
    PyModuleDef_HEAD_INIT,
    "demo", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit_demo(void)
{
    return PyModule_Create(&demo);
}