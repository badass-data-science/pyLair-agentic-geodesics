pyLair
======

A geodesic dome calculator written in Python.

pyLair calculates vertices and chords of Class One geodesic domes of arbitrary size. Domes created by pyLair can be truncated to facilitate structure design. The program produces DXF for easy import into CAD programs, and VRML output for easy display.

The overall method used to produce the geodesic domes is described below:

## Method

Start with an icosahedron:

![](edited_icosahedron1.png)

Divide each face into smaller, equal-sized triangles:

![](edited_4_unprojected1.png)

Project the points (triangle intersections) created in the last step onto the unit sphere while preserving the chord pattern:

![](edited_4_projected1.png)

Truncate the sphere at the equator:

![](edited_truncated.png)

Load into CAD:

![](../sample_image.png)

### Angles Between Chords and the Hub Tangent Plane

The angle between a chord and the plane tangent to the sphere at the chord's hub measures the amount of inward deflection a hub spoke for that chord must make. The following diagram illustrates this idea:

![](tangent_angle_image_CROPPED.png)

In this image, the view is directly facing the side of the tangent plane, so that it appears as a line. Two chords are shown here for illustrative purposes, but there are actually either five or six chords for a hub depending on the hub's position in the geodesic sphere.

The program now reports these angles for each hub as part of the standard output:

![](STDOUT_tangent_angles.png)

As expected, these are small angles.

### Angles of Chords Around the Hub

The other hub angles considered here are the angles between chords centered around a hub. Here we first project the chords onto the tangent plane, then select one of the chords as a reference, and then report the angle between the projected reference chord and each other projected chord. I call these angles "spoke" angles. The following image illustrates the idea:

![](spoke_angle_image_CROPPED.png)

Here the view is orthogonal to the sphere's tangent plane defined at the hub. (This is the same tangent plane as that used above).

The program reports these angles in its standard output:

![](STDOUT_spoke_angles.png)
