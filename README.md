pyDome
======

A geodesic dome calculator written in Python.

pyDome calculates vertices and chords of Class One geodesic domes of arbitrary size. Domes created by pyDome can be truncated to facilitate structure design. The program produces DXF for easy import into CAD programs, and VRML output for easy display.

The overall method used to produce the geodesic domes is described below:

## Method

Start with an icosahedron:

![](https://github.com/badassdatascience/pyDome/blob/master/images/edited_icosahedron1.png)

Divide each face into smaller, equal-sized triangles:

![](https://github.com/badassdatascience/pyDome/blob/master/images/edited_4_unprojected1.png)

Project the points (triangle intersections) created in the last step onto the unit sphere while preserving the chord pattern:

![](https://github.com/badassdatascience/pyDome/blob/master/images/edited_4_projected1.png)

Truncate the sphere at the equator:

![](https://github.com/badassdatascience/pyDome/blob/master/images/edited_truncated.png)

Load into CAD:

![](https://github.com/badassdatascience/pyDome/blob/master/sample_image.png)

### Angles Between Chords and the Hub Tangent Plane

The angle between a chord and the plane tangent to the sphere at the chord's hub measures the amount of inward deflection a hub spoke for that chord must make. The following diagram illustrates this idea:

<!--a href="http://badassdatascience.com/2014/06/15/pydome-updates-hub-angles/tangent_angle_image_cropped/" rel="attachment wp-att-1923"><img class="alignnone size-full wp-image-1923" src="http://badassdatascience.com/badassdatascience/wp-content/uploads/2014/06/tangent_angle_image_CROPPED.png" alt="tangent_angle_image_CROPPED" width="880" height="736" /></a-->

![](https://github.com/badassdatascience/pyDome/blob/master/images/tangent_angle_image_CROPPED.png)

In this image, the view is directly facing the side of the tangent plane, so that it appears as a line. Two chords are shown here for illustrative purposes, but there are actually either five or six chords for a hub depending on the hub's position in the geodesic sphere.

The program now reports these angles for each hub as part of the standard output:

<!--a href="http://badassdatascience.com/2014/06/15/pydome-updates-hub-angles/stdout_tangent_angles/" rel="attachment wp-att-1924"><img class="alignnone size-full wp-image-1924" src="http://badassdatascience.com/badassdatascience/wp-content/uploads/2014/06/STDOUT_tangent_angles.png" alt="STDOUT_tangent_angles" width="623" height="480" /></a-->

![](https://github.com/badassdatascience/pyDome/blob/master/images/STDOUT_tangent_angles.png)

As expected, these are small angles.

### Angles of Chords Around the Hub

The other hub angles considered here are the angles between chords centered around a hub. Here we first project the chords onto the tangent plane, then select one of the chords as a reference, and then report the angle between the projected reference chord and each other projected chord. I call these angles "spoke" angles. The following image illustrates the idea:

<!--a href="http://badassdatascience.com/2014/06/15/pydome-updates-hub-angles/spoke_angle_image_cropped/" rel="attachment wp-att-1925"><img class="alignnone size-full wp-image-1925" src="http://badassdatascience.com/badassdatascience/wp-content/uploads/2014/06/spoke_angle_image_CROPPED.png" alt="spoke_angle_image_CROPPED" width="672" height="603" /></a-->

![](https://github.com/badassdatascience/pyDome/blob/master/images/spoke_angle_image_CROPPED.png)

Here the view is orthogonal to the sphere's tangent plane defined at the hub. (This is the same tangent plane as that used above).

The program reports these angles in its standard output:

<!--a href="http://badassdatascience.com/2014/06/15/pydome-updates-hub-angles/stdout_spoke_angles/" rel="attachment wp-att-1926"><img class="alignnone size-full wp-image-1926" src="http://badassdatascience.com/badassdatascience/wp-content/uploads/2014/06/STDOUT_spoke_angles.png" alt="STDOUT_spoke_angles" width="623" height="480" /></a-->

![](https://github.com/badassdatascience/pyDome/blob/master/images/STDOUT_spoke_angles.png)
