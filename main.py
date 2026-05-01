from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin, cos

# -------------------
# angles
# -------------------
earth_angle = 0
moon_angle = 0
camera_z = -18


# -------------------
# Fog
# -------------------
def setup_fog():
    glEnable(GL_FOG)

    fogColor = [0.0, 0.0, 0.08, 1.0]
    glFogfv(GL_FOG_COLOR, fogColor)

    glFogf(GL_FOG_MODE, GL_EXP)
    glFogf(GL_FOG_DENSITY, 0.04)


# -------------------
# Light / Shading
# -------------------
def setup_light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    light_pos = [0, 0, 0, 1]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    ambient = [0.25, 0.25, 0.25, 1]
    diffuse = [1, 1, 1, 1]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


# -------------------
# Blending
# -------------------
def setup_blend():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


# -------------------
# Sun
# -------------------
def draw_sun():
    glPushMatrix()

    # main sun
    glColor3f(1, 0.6, 0)
    glutSolidSphere(2, 50, 50)

    # glow effect (blending)
    glDisable(GL_LIGHTING)

    glColor4f(1, 0.8, 0.2, 0.25)
    glutSolidSphere(2.8, 40, 40)

    glEnable(GL_LIGHTING)

    glPopMatrix()


# -------------------
# Earth
# -------------------
def draw_earth():
    glPushMatrix()

    glRotatef(earth_angle, 0, 1, 0)
    glTranslatef(7, 0, 0)

    glColor3f(0, 0.3, 1)
    glutSolidSphere(0.9, 40, 40)

    glPopMatrix()


# -------------------
# Moon
# -------------------
def draw_moon():
    glPushMatrix()

    # Earth position
    glRotatef(earth_angle, 0, 1, 0)
    glTranslatef(7, 0, 0)

    # Moon orbit
    glRotatef(moon_angle, 0, 1, 0)
    glTranslatef(2, 0, 0)

    glColor3f(0.8, 0.8, 0.8)
    glutSolidSphere(0.35, 30, 30)

    glPopMatrix()


# -------------------
# Orbit line
# -------------------
def draw_orbit(radius):
    glDisable(GL_LIGHTING)

    glColor3f(1, 1, 1)

    glBegin(GL_LINE_LOOP)
    for i in range(100):
        ang = 2 * 3.1416 * i / 100
        glVertex3f(radius * cos(ang), 0, radius * sin(ang))
    glEnd()

    glEnable(GL_LIGHTING)


# -------------------
# Display
# -------------------
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(
        0, 6, camera_z,
        0, 0, 0,
        0, 1, 0
    )

    draw_orbit(7)

    draw_sun()
    draw_earth()
    draw_moon()

    glutSwapBuffers()


# -------------------
# Keyboard
# -------------------
def keyboard(key, x, y):
    global camera_z

    if key == b'w':
        camera_z += 1

    elif key == b's':
        camera_z -= 1

    glutPostRedisplay()


# -------------------
# Animation
# -------------------
def update(value):
    global earth_angle, moon_angle

    earth_angle += 0.8
    moon_angle += 3.5

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


# -------------------
# Init
# -------------------
def init():
    glClearColor(0, 0, 0.05, 1)

    glEnable(GL_DEPTH_TEST)

    setup_fog()
    setup_light()
    setup_blend()

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1, 1, 100)
    glMatrixMode(GL_MODELVIEW)


# -------------------
# Main
# -------------------
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutCreateWindow(b"3D Solar Eclipse Simulation")

init()

glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)
glutTimerFunc(0, update, 0)

glutMainLoop()