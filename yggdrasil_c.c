#include <Python.h>
#include <structmember.h>
#include <omp.h>

typedef struct {
    PyObject_HEAD
    PyObject *dict;  // Internal dictionary to store the data
} YggdrasilObject;

static void
Yggdrasil_dealloc(YggdrasilObject *self)
{
    Py_XDECREF(self->dict);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
Yggdrasil_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    YggdrasilObject *self;
    self = (YggdrasilObject *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->dict = PyDict_New();
        if (self->dict == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject *) self;
}

static int
Yggdrasil_init(YggdrasilObject *self, PyObject *args, PyObject *kwds)
{
    return 0;
}

static PyObject *
Yggdrasil_getitem(YggdrasilObject *self, PyObject *key)
{
    PyObject *value;

    // Check if key exists in the dictionary
    if (PyDict_Contains(self->dict, key)) {
        value = PyDict_GetItem(self->dict, key);
        Py_INCREF(value);
        return value;
    }

    // If key doesn't exist, create a new Yggdrasil instance
    PyObject *args = PyTuple_New(0);
    PyObject *new_yggdrasil = PyObject_CallObject((PyObject *) Py_TYPE(self), args);
    Py_DECREF(args);

    if (new_yggdrasil == NULL) {
        return NULL;
    }

    // Store the new Yggdrasil instance in the dictionary
    if (PyDict_SetItem(self->dict, key, new_yggdrasil) < 0) {
        Py_DECREF(new_yggdrasil);
        return NULL;
    }

    return new_yggdrasil;
}

static int
Yggdrasil_setitem(YggdrasilObject *self, PyObject *key, PyObject *value)
{
    // If value is None, just set it directly
    if (value == NULL || value == Py_None) {
        return PyDict_SetItem(self->dict, key, Py_None);
    }

    // Check if value is a list
    if (PyList_Check(value)) {
        Py_ssize_t list_size = PyList_Size(value);

        // If list is empty, set the key to None
        if (list_size == 0) {
            return PyDict_SetItem(self->dict, key, Py_None);
        }

        // Get the first item from the list
        PyObject *first_item = PyList_GetItem(value, 0);
        Py_INCREF(first_item);

        // If list has only one item, set the key to that item
        if (list_size == 1) {
            int result = PyDict_SetItem(self->dict, key, first_item);
            Py_DECREF(first_item);
            return result;
        }

        // If key doesn't exist, create a new Yggdrasil instance
        PyObject *sub_yggdrasil;
        if (!PyDict_Contains(self->dict, key)) {
            PyObject *args = PyTuple_New(0);
            sub_yggdrasil = PyObject_CallObject((PyObject *) Py_TYPE(self), args);
            Py_DECREF(args);

            if (sub_yggdrasil == NULL) {
                Py_DECREF(first_item);
                return -1;
            }

            if (PyDict_SetItem(self->dict, key, sub_yggdrasil) < 0) {
                Py_DECREF(first_item);
                Py_DECREF(sub_yggdrasil);
                return -1;
            }
        } else {
            sub_yggdrasil = PyDict_GetItem(self->dict, key);
            Py_INCREF(sub_yggdrasil);
        }

        // Create a new list with the remaining items
        PyObject *rest_list = PyList_New(list_size - 1);
        for (Py_ssize_t i = 1; i < list_size; i++) {
            PyObject *item = PyList_GetItem(value, i);
            Py_INCREF(item);
            PyList_SET_ITEM(rest_list, i - 1, item);
        }

        // Call __setitem__ on the sub_yggdrasil with the first_item and rest_list
        PyObject *result = PyObject_CallMethod(sub_yggdrasil, "__setitem__", "OO", first_item, rest_list);

        Py_DECREF(first_item);
        Py_DECREF(rest_list);
        Py_DECREF(sub_yggdrasil);

        if (result == NULL) {
            return -1;
        }

        Py_DECREF(result);
        return 0;
    }

    // For any other type of value, just set it directly
    return PyDict_SetItem(self->dict, key, value);
}

static PyObject *
Yggdrasil_add_fiber(YggdrasilObject *self, PyObject *args)
{
    PyObject *fiber;

    if (!PyArg_ParseTuple(args, "O", &fiber)) {
        return NULL;
    }

    if (!PyList_Check(fiber)) {
        PyErr_SetString(PyExc_TypeError, "fiber must be a list");
        return NULL;
    }

    Py_ssize_t list_size = PyList_Size(fiber);

    if (list_size == 0) {
        Py_RETURN_NONE;
    }

    // Get the first item from the list (sprout)
    PyObject *sprout = PyList_GetItem(fiber, 0);
    Py_INCREF(sprout);

    // Create a new list with the remaining items
    PyObject *rest_list = PyList_New(list_size - 1);
    for (Py_ssize_t i = 1; i < list_size; i++) {
        PyObject *item = PyList_GetItem(fiber, i);
        Py_INCREF(item);
        PyList_SET_ITEM(rest_list, i - 1, item);
    }

    // Call __setitem__ with the sprout and rest_list
    int result = Yggdrasil_setitem(self, sprout, rest_list);

    Py_DECREF(sprout);
    Py_DECREF(rest_list);

    if (result < 0) {
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject *
Yggdrasil_add_fibers_parallel(YggdrasilObject *self, PyObject *args)
{
    PyObject *fibers_list;
    int num_threads = omp_get_max_threads(); // Default to max available threads

    if (!PyArg_ParseTuple(args, "O|i", &fibers_list, &num_threads)) {
        return NULL;
    }

    if (!PyList_Check(fibers_list)) {
        PyErr_SetString(PyExc_TypeError, "fibers_list must be a list of fibers");
        return NULL;
    }

    Py_ssize_t num_fibers = PyList_Size(fibers_list);
    if (num_fibers == 0) {
        Py_RETURN_NONE;
    }

    // Ensure we don't use more threads than fibers
    if (num_threads > num_fibers) {
        num_threads = (int)num_fibers;  // Explicit cast to avoid warning
    }

    // Set the number of threads for OpenMP
    omp_set_num_threads(num_threads);

    // Save the current thread state
    PyThreadState *_save;

    // Process fibers in parallel
    Py_ssize_t i;

    // Release the GIL before starting parallel section
    _save = PyEval_SaveThread();

    #pragma omp parallel private(i)
    {
        // Each thread needs its own GIL state
        PyGILState_STATE gstate;

        #pragma omp for schedule(dynamic)
        for (i = 0; i < num_fibers; i++) {
            // Acquire the GIL for Python operations
            gstate = PyGILState_Ensure();

            PyObject *fiber = PyList_GetItem(fibers_list, i);

            // Skip if not a list or empty
            if (!PyList_Check(fiber) || PyList_Size(fiber) == 0) {
                PyGILState_Release(gstate);
                continue;
            }

            // Create a copy of the fiber to avoid modifying the original
            PyObject *fiber_copy = PyList_New(PyList_Size(fiber));
            for (Py_ssize_t j = 0; j < PyList_Size(fiber); j++) {
                PyObject *item = PyList_GetItem(fiber, j);
                Py_INCREF(item);
                PyList_SET_ITEM(fiber_copy, j, item);
            }

            // Get the first item from the list (sprout)
            PyObject *sprout = PyList_GetItem(fiber_copy, 0);
            Py_INCREF(sprout);

            // Create a new list with the remaining items
            PyObject *rest_list = PyList_New(PyList_Size(fiber_copy) - 1);
            for (Py_ssize_t j = 1; j < PyList_Size(fiber_copy); j++) {
                PyObject *item = PyList_GetItem(fiber_copy, j);
                Py_INCREF(item);
                PyList_SET_ITEM(rest_list, j - 1, item);
            }

            // Call __setitem__ with the sprout and rest_list
            // We need to use a mutex here to avoid race conditions
            #pragma omp critical
            {
                Yggdrasil_setitem(self, sprout, rest_list);
            }

            Py_DECREF(sprout);
            Py_DECREF(rest_list);
            Py_DECREF(fiber_copy);

            // Release the GIL after Python operations
            PyGILState_Release(gstate);
        }
    }

    // Restore the thread state and reacquire the GIL
    PyEval_RestoreThread(_save);
    Py_RETURN_NONE;
}

static PyObject *
Yggdrasil_print_tree(YggdrasilObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"prefix", "is_root", NULL};
    const char *prefix = "";
    int is_root = 1;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|sp", kwlist, &prefix, &is_root)) {
        return NULL;
    }

    // Get the keys from the dictionary
    PyObject *keys = PyDict_Keys(self->dict);
    if (keys == NULL) {
        return NULL;
    }

    Py_ssize_t num_keys = PyList_Size(keys);

    // If this is the root and there are no keys, print "Empty tree"
    if (is_root && num_keys == 0) {
        printf("Empty tree\n");
        Py_DECREF(keys);
        Py_RETURN_NONE;
    }

    // Process each key in the dictionary
    for (Py_ssize_t i = 0; i < num_keys; i++) {
        PyObject *key = PyList_GetItem(keys, i);
        int is_last = (i == num_keys - 1);

        // Create the connector string
        const char *connector = is_last ? "+-- " : "|-- ";

        // Print the current key with the appropriate connector
        PyObject *key_str = PyObject_Str(key);
        if (key_str == NULL) {
            Py_DECREF(keys);
            return NULL;
        }

        printf("%s%s%s\n", prefix, connector, PyUnicode_AsUTF8(key_str));
        Py_DECREF(key_str);

        // Get the value for this key
        PyObject *value = PyDict_GetItem(self->dict, key);
        if (value == NULL) {
            Py_DECREF(keys);
            return NULL;
        }

        // Determine the prefix for the next level
        char next_prefix[1024];
        if (is_last) {
            snprintf(next_prefix, sizeof(next_prefix), "%s    ", prefix);
        } else {
            snprintf(next_prefix, sizeof(next_prefix), "%s|   ", prefix);
        }

        // If the value is another Yggdrasil instance, recursively print it
        if (PyObject_TypeCheck(value, Py_TYPE(self))) {
            PyObject *args = PyTuple_New(0);
            PyObject *kwargs = PyDict_New();

            PyDict_SetItemString(kwargs, "prefix", PyUnicode_FromString(next_prefix));
            PyDict_SetItemString(kwargs, "is_root", Py_False);

            PyObject *result = PyObject_Call(PyObject_GetAttrString(value, "print_tree"), args, kwargs);

            Py_DECREF(args);
            Py_DECREF(kwargs);
            Py_XDECREF(result);
        }
        // Otherwise, print the value as a leaf node
        else if (value != Py_None) {
            PyObject *value_str = PyObject_Str(value);
            if (value_str == NULL) {
                Py_DECREF(keys);
                return NULL;
            }

            printf("%s+-- %s\n", next_prefix, PyUnicode_AsUTF8(value_str));
            Py_DECREF(value_str);
        }
    }

    Py_DECREF(keys);
    Py_RETURN_NONE;
}

static PyObject *
Yggdrasil_repr(YggdrasilObject *self)
{
    return PyObject_Repr(self->dict);
}

static PyObject *
Yggdrasil_str(YggdrasilObject *self)
{
    return PyObject_Str(self->dict);
}

static Py_ssize_t
Yggdrasil_len(YggdrasilObject *self)
{
    return PyDict_Size(self->dict);
}

static PyMappingMethods Yggdrasil_as_mapping = {
    (lenfunc)Yggdrasil_len,              /* mp_length */
    (binaryfunc)Yggdrasil_getitem,       /* mp_subscript */
    (objobjargproc)Yggdrasil_setitem,    /* mp_ass_subscript */
};

static PyMethodDef Yggdrasil_methods[] = {
    {"add_fiber", (PyCFunction)Yggdrasil_add_fiber, METH_VARARGS,
     "Add a fiber (path) to the tree"},
    {"add_fibers_parallel", (PyCFunction)Yggdrasil_add_fibers_parallel, METH_VARARGS,
     "Add multiple fibers (paths) to the tree in parallel using multiple cores"},
    {"print_tree", (PyCFunction)Yggdrasil_print_tree, METH_VARARGS | METH_KEYWORDS,
     "Print the tree structure like a directory tree with lines"},
    {NULL}  /* Sentinel */
};

static PyTypeObject YggdrasilType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "yggdrasil_c.Yggdrasil",
    .tp_doc = "Yggdrasil object",
    .tp_basicsize = sizeof(YggdrasilObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = Yggdrasil_new,
    .tp_init = (initproc)Yggdrasil_init,
    .tp_dealloc = (destructor)Yggdrasil_dealloc,
    .tp_methods = Yggdrasil_methods,
    .tp_as_mapping = &Yggdrasil_as_mapping,
    .tp_repr = (reprfunc)Yggdrasil_repr,
    .tp_str = (reprfunc)Yggdrasil_str,
};

static PyModuleDef yggdrasil_c_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "yggdrasil_c",
    .m_doc = "C extension for Yggdrasil data structure",
    .m_size = -1,
};

PyMODINIT_FUNC
PyInit_yggdrasil_c(void)
{
    PyObject *m;

    if (PyType_Ready(&YggdrasilType) < 0)
        return NULL;

    m = PyModule_Create(&yggdrasil_c_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&YggdrasilType);
    if (PyModule_AddObject(m, "Yggdrasil", (PyObject *) &YggdrasilType) < 0) {
        Py_DECREF(&YggdrasilType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
