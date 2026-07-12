#    pyDome:  A geodesic dome calculator
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

# Scale the Z axis only, matching the codebase's existing convention
# (Truncation.py already treats v[2] as "up"). This stretches the
# sphere into an axis-aligned ellipsoid with semi-axes (r, r, r*factor)
# for ceiling-height/footprint tradeoffs -- chord/face connectivity is
# unaffected, since this is a pure per-vertex scale.
_SCALE_AXIS = 2


def elongate(vertices, factor):
  scale = np.array([1., 1., 1.])
  scale[_SCALE_AXIS] = factor
  return [v * scale for v in vertices]
