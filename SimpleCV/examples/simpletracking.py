#!/usr/bin/python

from SimpleCV import *

c = Camera()
d = c.getImage().show()

color = ''
while not d.isDone():
  img = c.getImage()
  if color:
    blobs = img.colorDistance(color).invert().findBlobs(180)
    if blobs:
       blobs[-1].image = img
       blobs[-1].drawHull(width=5)
  elif (d.mouseLeft):
    color = img[d.mouseX, d.mouseY]
  img.save(d)