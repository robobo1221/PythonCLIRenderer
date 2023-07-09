import imp
from ShaderBase import ShaderBase
from vector.Vector2 import Vector2
from vector.Vector3 import Vector3
from util.math import *
import math
import time

MIN_DIST = 0.01
MAX_DIST = 20.0
SKY_INTENSITY = 1.
SKY_COLOR = Vector3(0.2, 0.5, 1.0) * 0.5
SUN_INTENSITY = 2.0

ID_FLOOR = 1
ID_SPHERE = 2

ALBEDO_FLOOR = Vector3(1.0, 1.0, 1.0)
ROUGHNESS_FLOOR = 0.3
F0_FLOOR = 0.1
ALBEDO_SPHERE = Vector3(1.0, 0.2, 0.3)
ROUGHNESS_SPHERE = 0.2
F0_SPHERE = 0.02

class SdfObject:
    def __init__(self, sdf, id) -> None:
        self.sdf = sdf
        self.id = id

    def __min__(self, other):
        newSdf = SdfObject(0, -1)

        if self.sdf < other.sdf:
            newSdf.id = self.id
            newSdf.sdf = self.sdf
        else:
            newSdf.id = other.id
            newSdf.sdf = other.sdf

        return newSdf

    def __lt__(self, other):
        return self.sdf < other.sdf

class Material:
    def __init__(self, albedo, roughness = 1.0, f0 = 0.02) -> None:
        self.albedo = albedo
        self.roughness = roughness
        self.f0 = f0

    def calculateMaterial(id):
        if id == ID_FLOOR:
            return Material(ALBEDO_FLOOR, ROUGHNESS_FLOOR, F0_FLOOR)
        if id == ID_SPHERE:
            return Material(ALBEDO_SPHERE, ROUGHNESS_SPHERE, F0_SPHERE)

        return Material(Vector3(1, 1, 1), 0.3, 0.02)

def sphereSdf(pos, radius):
    return pos.length() - radius

def planeSdf(pos, dir, height):
    return pos.dot(dir) - height

def cubeSdf(pos, boundary):
    dif = abs(pos) - boundary

    return Vector3(max(dif.x, 0), max(dif.y, 0), max(dif.z, 0)).length()

def sdf(pos):
    plane = SdfObject(planeSdf(pos, Vector3(0, 1, 0), -1.0), 1)
    sphere = SdfObject(sphereSdf(pos - Vector3(0, 0, 2), 1.0), 2)
    cube = SdfObject(cubeSdf(pos - Vector3(0, 0, 3), Vector3(1.0, 1.0, 1.0)), 2)

    return min(plane, sphere)

def march(ro, rd):
    steps = 256

    pos = ro
    totalDist = 0.0

    for i in range(steps):
        sdfObject = sdf(pos)
        totalDist += sdfObject.sdf

        if sdfObject.sdf < MIN_DIST:
            return True, totalDist, sdfObject.id

        if totalDist > MAX_DIST:
            return False, totalDist, sdfObject.id

        pos += sdfObject.sdf * rd

    return False, totalDist, -1

def calculateShadows(pos, direction, normal):
    hit, t, id = march(pos + normal * MIN_DIST * 2., direction)

    return float(not hit)

def calculateNormal(pos):
    delta = 0.001

    center = sdf(pos).sdf
    dx = center - sdf(pos - Vector3(delta, 0, 0)).sdf
    dy = center - sdf(pos - Vector3(0, delta, 0)).sdf
    dz = center - sdf(pos - Vector3(0, 0, delta)).sdf

    return Vector3(dx, dy, dz).normalize()

def calculateLighting(pos, lightVector, normal, material, shadows = False):
    NoL = normal.dot(lightVector)

    if not shadows:
        shadows = calculateShadows(pos, lightVector, normal)

    skyLight = calculateSkyIntensity(Vector3(0, 0.25, 0), lightVector, False) * (normal.y * 0.5 + 0.5) / math.pi
    
    return (skyLight + shadows * min(max(NoL, 0.0), 1.0) * SUN_INTENSITY) * material.albedo

def calculateReflections(pos, rd, normal, lightVector):
    reflectedVector = rd.reflect(normal)

    hit, t, id = march(pos + normal * MIN_DIST * 2, reflectedVector)

    if hit:
        material = Material.calculateMaterial(id)
        reflectedPos = pos + reflectedVector * t
        reflectedNormal = calculateNormal(reflectedPos)
        return calculateLighting(reflectedPos, lightVector, reflectedNormal, material)

    return calculateSkyIntensity(reflectedVector, lightVector, False)

def calculateFresnel(LoH, f0):
    return pow(1.0 - LoH, 5.0) * (1.0 - f0) + f0

def calculateSkyIntensity(rd, lightVector, isCamera = True):
    color = mix(SKY_COLOR, Vector3(0.8, 0.9, 1.0) * 4.0, math.exp(-max(rd.y * 10.0, 0.0)))

    if isCamera:
        color += calculateSunSpot(rd, lightVector)

    return color

def calculateSpecularHighlight(N, V, L, roughness, F0):
    alpha = roughness*roughness
    H = (L - V).normalize()
    dotLH = max(0.0, L.dot(H))
    dotNH = max(0.0, N.dot(H))
    dotNL = max(0.0, N.dot(L))

    alphaSqr = alpha * alpha
    denom = dotNH * dotNH * (alphaSqr - 1.0) + 1.0
    D = alphaSqr / (3.141592653589793 * denom * denom)
    F = calculateFresnel(dotLH, F0)
    k = 0.5 * alpha
    k2 = k * k

    return dotNL * D * F / (dotLH*dotLH*(1.0-k2)+k2)


def calculateSunSpot(rd, lightVector):
    return float(rd.dot(lightVector) > 0.999) * 100.0

def Bayer2(a):
    a = Vector2(math.floor(a.x), math.floor(a.y))
    return math.fmod(a.x / 2. + a.y * a.y * .75, 1.0)

def Bayer4(a):
    return Bayer2(0.5 * a) * 0.25 + Bayer2(a)

def Bayer8(a):
    return Bayer4(0.5 * a) * 0.25 + Bayer2(a)

def Bayer16(a):
    return Bayer8(0.5 * a) * 0.25 + Bayer2(a)

class TestShader(ShaderBase):
    def main(self):
        lightVector = Vector3(0.5, 0.3, 1.0).normalize()

        viewWidth = self.getUniform("viewWidth")
        viewHeight = self.getUniform("viewHeight")

        pixelSize = Vector2(viewWidth, viewHeight)
        
        uv = self.position / pixelSize

        worldUv = (uv * 2.0 - 1.0) * Vector2((pixelSize.x / pixelSize.y) * 0.5, 1.0)
        rd = Vector3(worldUv.x, worldUv.y, 1.0).normalize()
        ro = Vector3(0, -0.0, -2)

        rayHit, t, id = march(ro, rd)

        if (rayHit):
            material = Material.calculateMaterial(id)

            pos = ro + rd * t
            normal = calculateNormal(pos)

            shadows = calculateShadows(pos, lightVector, normal)

            light = calculateLighting(pos, lightVector, normal, material, shadows)
            reflections = calculateReflections(pos, rd, normal, lightVector)
            
            fresnel = calculateFresnel(rd.dot(-normal), material.f0)
            geometry = (1.0 - material.roughness * material.roughness * material.roughness * material.roughness)
            fresnel *= geometry + material.f0 * (1.0 - geometry)

            highlight = calculateSpecularHighlight(normal, rd, lightVector, material.roughness, material.f0) * shadows

            color = (reflections + highlight) * fresnel + light * (1.0 - fresnel)
        else:
            color = calculateSkyIntensity(rd, lightVector)

        color *= 2.0

        color /= color + 1.0
        color = pow(color, 1.0 / 2.2)

        color += Bayer8(self.position) / 255.

        return color