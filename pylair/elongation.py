#    pyLair:  A geodesic dome calculator
#    Copyright (C) 2013  Emily Williams
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np

# Independent per-axis scale factors (fx, fy, fz). This stretches the
# sphere into a general axis-aligned ellipsoid with semi-axes
# (r*fx, r*fy, r*fz) for ceiling-height/footprint tradeoffs on any
# combination of axes -- chord/face connectivity is unaffected, since
# this is a pure per-vertex scale.


def elongate(vertices, factors):
  scale = np.array(factors, dtype=float)
  return [v * scale for v in vertices]
