#include <Python.h>

static PyObject *InvalidByteValue;

static PyObject* lower(PyObject* self, PyObject* args) {
    int byte_value;

    // Parse the input Python object (int in this case)
    if (!PyArg_ParseTuple(args, "i", &byte_value)) {
        return NULL;
    }

    // Check for invalid byte range (example condition)
    if (byte_value < 0x00 || byte_value > 0xFF) {
        PyErr_SetString(InvalidByteValue, "Byte value must be in the range 0-255.");
        return NULL;  // Return NULL to signal an exception
    }

    // Check if the byte_value is within the ASCII uppercase range
    if (!(byte_value < 0x41 || byte_value > 0x5A)) {
        byte_value += 0x20;  // Convert to lowercase
    }

    return PyLong_FromLong(byte_value);
}

// Define the methods for this module
static PyMethodDef OperationsMethods[] = {
    {"lower", lower, METH_VARARGS, "Convert a byte to lowercase."},
    {NULL, NULL, 0, NULL}
};

// Define the module itself
static struct PyModuleDef operationsmodule = {
    PyModuleDef_HEAD_INIT,
    "bytetools.operations",  // Name of the module
    NULL,                    // Module documentation (optional)
    -1,                      // Size of per-interpreter state of the module
    OperationsMethods
};

// Initialize the module and set up the custom exception
PyMODINIT_FUNC PyInit_operations(void) {
    PyObject *m;

    // Create the module
    m = PyModule_Create(&operationsmodule);
    if (m == NULL) {
        return NULL;
    }

    // Import the custom InvalidByteValue exception from the bytetools package
    PyObject *bytetools = PyImport_ImportModule("bytetools");
    if (bytetools == NULL) {
        // Set an appropriate error message
        PyErr_SetString(PyExc_ImportError, "Could not import 'bytetools' module.");
        return NULL;
    }

    // Get the InvalidByteValue exception from bytetools
    InvalidByteValue = PyObject_GetAttrString(bytetools, "InvalidByteValue");
    if (InvalidByteValue == NULL) {
        // Set an appropriate error message
        PyErr_SetString(PyExc_AttributeError, "Could not get 'InvalidByteValue' from 'bytetools'.");
        Py_DECREF(bytetools);
        return NULL;
    }

    // Decrement the reference to the bytetools module
    Py_DECREF(bytetools);

    // Return the module
    return m;
}
