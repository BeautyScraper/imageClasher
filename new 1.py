@cuda.jit
def cuda_histogram(x, xmin, xmax, histogram_out):
    '''Increment bin counts in histogram_out, given histogram range [xmin, xmax).'''
    nbins = histogram_out.shape[0]
    bin_width = (xmax - xmin) / nbins
    
    start = cuda.grid(1)
    stride = cuda.gridsize(1)
    
    for i in range(start,x.shape[0], stride):
        bin_number = np.int32((x[i] - xmin)/bin_width)
        if bin_number >= 0 and bin_number < histogram_out.shape[0]:
            cuda.atomic.add(histogram_out, bin_number, 1)

            
import numpy as np
from numba import cuda, types
@cuda.jit
def mm_shared(a, b, c):
    column, row = cuda.grid(2)
    sum = 0

    # `a_cache` and `b_cache` are already correctly defined
    a_cache = cuda.shared.array(block_size, types.int32)
    b_cache = cuda.shared.array(block_size, types.int32)

    # TODO: use each thread to populate one element each a_cache and b_cache
    
    for i in range(a.shape[1]):
        # TODO: calculate the `sum` value correctly using values from the cache 
        sum += a_cache[0][0] * b_cache[0][0]
        
    c[row][column] = sum
    
import numpy as np
from numba import cuda, types
@cuda.jit
def mm_shared(a, b, c):
    sum = 0

    # `a_cache` and `b_cache` are already correctly defined
    a_cache = cuda.shared.array(block_size, types.int32)
    b_cache = cuda.shared.array(block_size, types.int32)

    # TODO: use each thread to populate one element each a_cache and b_cache
    x,y = cuda.grid(2)
    tx = cuda.threadIdx.x
    ty = cuda.threadIdx.y
    bpg = cuda.gridDim.x
    n = int(N)
    
    for i in range(a.shape[1] / n):
        y1 = ty + i * n
        x1 = tx + i * n
        a_cache[tx, ty] = a[x, y1]
        b_cache[tx, ty] = b[x1, y]
    
    cuda.syncthreads()
    for j in range(n):#a.shape[1]):
        # TODO: calculate the `sum` value correctly using values from the cache 
        sum += a_cache[tx][j] * b_cache[j][ty]
    cuda.syncthreads()    
    c[x][y] = sum
