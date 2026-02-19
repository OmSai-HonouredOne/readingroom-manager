# rrm/layout.py
import numpy as np

# This will hold your layout in memory
layoutnp = None

def init_layout(query_all):
    global layoutnp, layoutDB
    layoutDB = np.array(query_all(
        "SELECT y_coordinate, x_coordinate, box_no, is_laptop FROM boxes"
    ))
    
    layoutnp2d = np.zeros((12,12), dtype=[('box_no', np.int32), ('regno', np.int64), ('is_laptop', np.bool_)])
    y = layoutDB[:, 0] - 1
    x = layoutDB[:, 1] - 1
    layoutnp2d['box_no'][y, x] = layoutDB[:, 2]
    layoutnp2d['is_laptop'][y, x] = layoutDB[:, 3]
    layoutnp2d['regno'][y, x] = 1

    layoutnp = layoutnp2d.ravel()