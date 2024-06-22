import mahotas as mh
import mahotas.demos
import numpy as np
from pylab import imshow, show

f = mh.demos.nuclear_image()
f =f[:, :, 0]
imshow(f)
show()  