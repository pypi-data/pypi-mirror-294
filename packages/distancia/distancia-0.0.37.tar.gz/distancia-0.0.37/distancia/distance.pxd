# distance_function.pxd

#cdef double distance_function(double[:] point1, double[:] point2)
# distance_function.pxd
cdef double distance_function(list[float] point1, list[float] point2)
