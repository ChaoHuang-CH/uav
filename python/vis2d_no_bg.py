import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import scene_pb2
import irispy
import scipy
import matplotlib.animation as animation
import sys, os

# default scenes file name
input_file_name = './scenes.txt'
if(len(sys.argv)==2):
    input_file_name = sys.argv[1]

fig = plt.figure(figsize=(6,14), dpi=80)

ax = fig.add_subplot(1, 1, 1)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
#ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position('zero')
ax.spines['bottom'].set_color('none')
#ax.yaxis.set_ticks_position('left')
#ax.spines['left'].set_position(('data',0))
ax.spines['left'].set_position('zero')
ax.spines['left'].set_color('none')

x_min = -8
x_max = 8
y_min = -8
y_max = 28
ax.set_xlim(x_min,x_max)
#ax.set_xticks(np.linspace(x_min,x_max,x_max-x_min+1,endpoint=True))
ax.set_xticks(np.array([]))
ax.set_ylim(y_min,y_max)
#ax.set_yticks(np.linspace(y_min,y_max,y_max-y_min+1,endpoint=True))
ax.set_yticks(np.array([]))

uavRadius = 1
uavsDirRadius = 0.2
gDirRadius = 0.2

# data Var
uavs = None
uavsDir = None
gDir = None
a = None
b = None
dos = None
sos = None
currCentroid = None
currFormation = None

# Ax Var
uavsAx = []
uavsDirAx = []
sosAx = []
dosAx = []
gDirAx = None
#lcpAx = None

fd = open(input_file_name, 'r')

DIM = 2

def updateData():
    global fd
    global DIM
    global uavs, uavsDir, gDir, a, b, dos, sos, currCentroid, currFormation
    # update data
    s = ''
    for line in fd:
        if(line[:-1]=='###'):
            scene = scene_pb2.Scene()
            scene.ParseFromString(s[:-1])
            #print (scene)
            #uavs
            uavsPb = scene.uavs.uav
            uavs = np.ones((len(uavsPb), DIM))
            for i, uavPb in enumerate(uavsPb):
                uavs[i, 0] = uavPb.x
                uavs[i, 1] = uavPb.y
            #uavsDir
            uavsDirPb = scene.uavsDir.uavDir
            uavsDir = np.ones((len(uavsDirPb), DIM))
            for i, pPb in enumerate(uavsDirPb):
                uavsDir[i, 0] = pPb.x
                uavsDir[i, 1] = pPb.y
            #gDir
            gDirPb = scene.gDir
            gDir = np.ones(DIM)
            gDir[0] = gDirPb.x
            gDir[1] = gDirPb.y
            #a
            aPb = scene.a
            a = np.ones(aPb.row * aPb.col)
            for i, dataPb in enumerate(aPb.data):
                a[i] = dataPb
            a.resize((aPb.row, aPb.col))
            #b
            bPb = scene.b
            b = np.ones(bPb.row)
            for i, dataPb in enumerate(bPb.data):
                b[i] = dataPb
            b.resize((bPb.row, 1))
            #if top is equal with bottom, only leave one 
            if(a.shape[0]%2==0):
                ab = np.hstack((a,b))
                abTop = np.split(ab,2)[0]
                abBot = np.split(ab,2)[1]
                if (np.allclose(abTop,abBot)):
                    ab = abTop
                    ab = np.hsplit(ab, np.array([2]))
                    a = ab[0]
                    b = ab[1]
            #sos
            sosPb = scene.sos.so
            sos = []
            for soPb in sosPb:
                so_temp = np.ones((len(soPb.point), DIM))
                for i, pPb in enumerate(soPb.point):
                    so_temp[i, 0] = pPb.x
                    so_temp[i, 1] = pPb.y
                sos.append(so_temp)
            #dos
            dosPb = scene.dos.do
            dos = []
            for doPb in dosPb:
                do_temp = np.ones((len(doPb.point), DIM))
                for i, pPb in enumerate(doPb.point):
                    do_temp[i, 0] = pPb.x
                    do_temp[i, 1] = pPb.y
                dos.append(do_temp)
            #currCentroid
            currCentroidPb = scene.currCentroid
            currCentroid = np.ones(DIM)
            currCentroid[0] = currCentroidPb.x
            currCentroid[1] = currCentroidPb.y
            #currFormation
            currFormation = scene.formation
            break;
        else:
            s += line

def initVar():
    #global uavsAx, uavsDirAx, gDirAx, lcpAx, sosAx, dosAx
    global uavsAx, uavsDirAx, gDirAx, sosAx, dosAx
    # uavs
    for pos in uavs:
        circle = plt.Circle(pos, uavRadius, color='r')
        uavAx = ax.add_artist(circle)
        uavsAx.append(uavAx)
    # uavsDir
    for pos in uavsDir:
        circle = plt.Circle(pos, uavsDirRadius, color='g')
        uavDirAx = ax.add_artist(circle)
        uavsDirAx.append(uavDirAx)
    # gDir
    circle = plt.Circle(gDir, gDirRadius, color='r')
    gDirAx = ax.add_artist(circle)
    # lcp
    lcp = irispy.Polyhedron(a, b)
    #lcp = irispy.Polyhedron(a.astype(np.float16).astype(np.float64), b.astype(np.float16).astype(np.float64))
    #lcp = irispy.Polyhedron(a[:a.shape[0]/2,:],b[:b.shape[0]/2,:])
    #lcpPoints = lcp.getDrawingVertices()
    #lcpHull = scipy.spatial.ConvexHull(lcpPoints)
    #polygon = Polygon(lcpPoints[lcpHull.vertices], True, color='g', alpha=0.3)
    #lcpAx = ax.add_patch(polygon)
    # sos
    for so in sos:
        polygon = Polygon(so, True, color='b')    
        patchSo = ax.add_patch(polygon)
        sosAx.append(patchSo)
    # dos
    for do in dos:
        polygon = Polygon(do, True, color='b')
        patchDo = ax.add_patch(polygon)
        dosAx.append(patchDo)

def updateVar():
    #global uavsAx, uavsDirAx, gDirAx, lcpAx, sosAx, dosAx
    global uavsAx, uavsDirAx, gDirAx, sosAx, dosAx
    global uavs, uavsDir, gDir, a, b, sos, dos
    #uavs
    for i, uavAx in enumerate(uavsAx):
        uavAx.center = uavs[i]
    #uavsDir
    for i, uavDirAx in enumerate(uavsDirAx):
        uavDirAx.center = uavsDir[i]
    #gDirAx
    gDirAx.center = gDir
    #lcp
    lcp = irispy.Polyhedron(a, b)
    #lcp = irispy.Polyhedron(a.astype(np.float16).astype(np.float64), b.astype(np.float16).astype(np.float64))
    #lcp = irispy.Polyhedron(a[:a.shape[0]/2,:],b[:b.shape[0]/2,:])
#    print (lcp.getA())
#    print (lcp.getB())
    #lcpPoints = lcp.getDrawingVertices()
    #lcpHull = scipy.spatial.ConvexHull(lcpPoints)
    #lcpAx.set_xy(lcpPoints[lcpHull.vertices] + currCentroid)
    #dos
    for i, doAx in enumerate(dosAx):
        doAx.set_xy(dos[i])
    #sos
    for i, soAx in enumerate(sosAx):
        soAx.set_xy(sos[i])

count = 0 # to specify intialization
def update(frame):
    global count
    #global uavsAx, uavsDirAx, gDirAx, lcpAx, sosAx, dosAx
    global uavsAx, uavsDirAx, gDirAx, sosAx, dosAx
    updateData()
    if(count == 0):
        initVar()
    updateVar()
    count += 1
    print(count)
    print('currFormation: ' + str(currFormation))
    # Return the modified object
    #return uavsAx, uavsDirAx, gDirAx, lcpAx, sosAx, dosAx 
    return uavsAx, uavsDirAx, gDirAx, sosAx, dosAx 

animation = animation.FuncAnimation(fig, update, interval=100, blit=False, frames=range(150), repeat=False)
#animation.save('rain.gif', writer='imagemagick', fps=8, dpi=80)
    
# Show result on screen
plt.show()

#ta = np.array([[  1.00000000e+00  ,-1.30826602e-08], 
# [ -1.00000000e+00  ,-1.29587610e-08],
# [  1.00000000e+00  , 0.00000000e+00],
# [  0.00000000e+00  , 1.00000000e+00],
# [ -1.00000000e+00  ,-0.00000000e+00],
# [ -0.00000000e+00  ,-1.00000000e+00]])
#tb = np.array([[  1.99999073e+00], 
# [  2.00000924e+00],
# [  1.00000000e+04],
# [  1.00000000e+04],
# [  1.00000000e+04],
# [  1.00000000e+04]])
#
#ta = np.array([[  1.00000000e+00  , 1.42614081e-08], 
# [ -1.00000000e+00  ,-4.23160801e-08],
# [  1.00000000e+00  , 0.00000000e+00],
# [  0.00000000e+00  , 1.00000000e+00],
# [ -1.00000000e+00  ,-0.00000000e+00],
# [ -0.00000000e+00  ,-1.00000000e+00]])
#tb = np.array([[  2.00000665e+00], 
# [  1.99999317e+00],
# [  1.00000000e+04],
# [  1.00000000e+04],
# [  1.00000000e+04],
# [  1.00000000e+04]])
#
#for i in range(11):
#    updateData()
#    if(i == 0):
#        initVar()
#    if(i == 10):
#        print(a)
#        print(b)
#        lcp = irispy.Polyhedron(ta, tb)
#        lcp = irispy.Polyhedron(ta.astype(np.float16).astype(np.float64), tb.astype(np.float16).astype(np.float64))
#        print(lcp.getDrawingVertices())


fd.close()
