cdef class NativeExecutionCursor:
    cdef int file
    cdef int line
    cdef str function_name

cdef class NativeVariables:
    cdef list variables

cdef class NativeStackFrame:
    cdef NativeStackFrame parent
    cdef NativeExecutionCursor cursor
    cdef int id

cdef class NativeCodeEvent:
    cpdef str event_name
    cdef NativeExecutionCursor cursor
    cdef NativeStackFrame stack
    cdef double ts
    cdef NativeVariables locals
    cdef NativeVariables input_variables
    cdef NativeVariables return_variables

cdef class NativeVariable:
    cdef str name
    cdef str value


