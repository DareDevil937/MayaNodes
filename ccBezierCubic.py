import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
 
class ccBezierCubic(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00000121)
 
    #MObject attribute
    aP1 = OpenMaya.MObject()
    aP2 = OpenMaya.MObject()
    aP3 = OpenMaya.MObject()
    aP4 = OpenMaya.MObject()
    
    aSum = OpenMaya.MObject()
    aBias = OpenMaya.MObject()
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
 
    def compute(self, plug, data):
        
        #get controls points as Vector
        p1 = data.inputValue(ccBezierCubic.aP1).asVector()
        p2 = data.inputValue(ccBezierCubic.aP2).asVector()
        p3 = data.inputValue(ccBezierCubic.aP3).asVector()
        p4 = data.inputValue(ccBezierCubic.aP4).asVector()
        t = data.inputValue(ccBezierCubic.aBias).asFloat()
        
        #sum of bezierCubic formula
        sum = p1*pow(1-t,3) + p2*3*t*pow(1-t,2) + p3*3*pow(t,2)*(1-t) + p4*pow(t,3)
        
        #set Output
        outputData = data.outputValue(ccBezierCubic.aSum)
        outputData.set3Double(sum[0], sum[1], sum[2])
        
        #set the MPlug clean
        data.setClean(plug)
  
def creator():
    return OpenMayaMPx.asMPxPtr(ccBezierCubic())
 
def initialize():
    #create MFnNumericAttribute
    nAttr = OpenMaya.MFnNumericAttribute()
    
    #create inputs  positions attribute
    ccBezierCubic.aP1 = nAttr.create('Point1', 'p1', OpenMaya.MFnNumericData.k3Double)
    ccBezierCubic.addAttribute(ccBezierCubic.aP1)
    
    ccBezierCubic.aP2 = nAttr.create('Point2', 'p2', OpenMaya.MFnNumericData.k3Double)
    ccBezierCubic.addAttribute(ccBezierCubic.aP2)
    
    ccBezierCubic.aP3 = nAttr.create('Point3', 'p3', OpenMaya.MFnNumericData.k3Double)
    ccBezierCubic.addAttribute(ccBezierCubic.aP3)
    
    ccBezierCubic.aP4 = nAttr.create('Point4', 'p4', OpenMaya.MFnNumericData.k3Double)
    ccBezierCubic.addAttribute(ccBezierCubic.aP4)
    
    #create output sum attribute
    ccBezierCubic.aSum = nAttr.create('SumBezier', 'sum', OpenMaya.MFnNumericData.k3Double)
    nAttr.setWritable(True)
    ccBezierCubic.addAttribute(ccBezierCubic.aSum)
    
    #create input bias attribute
    ccBezierCubic.aBias = nAttr.create('Bias', 't', OpenMaya.MFnNumericData.kFloat,0.)
    nAttr.setSoftMin = 0.
    nAttr.setSoftMax = 1.
    nAttr.setKeyable(True)
    nAttr.setWritable(True)
    ccBezierCubic.addAttribute(ccBezierCubic.aBias)
    
    #create input/output connections
    ccBezierCubic.attributeAffects(ccBezierCubic.aBias, ccBezierCubic.aSum)
    ccBezierCubic.attributeAffects(ccBezierCubic.aP1, ccBezierCubic.aSum)
    ccBezierCubic.attributeAffects(ccBezierCubic.aP2, ccBezierCubic.aSum)
    ccBezierCubic.attributeAffects(ccBezierCubic.aP3, ccBezierCubic.aSum)
    ccBezierCubic.attributeAffects(ccBezierCubic.aP4, ccBezierCubic.aSum)
    
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'cc', '1.0', 'Thinking3d')
    try:
        plugin.registerNode('ccBezierCubic', ccBezierCubic.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node'
 
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(ccBezierCubic.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node'
    
'''   
import maya.cmds as cmds
from math import *
cmds.file( newFile=True, force=True )
cmds.unloadPlugin( 'ccBezierCubic.py' )
cmds.loadPlugin( 'ccBezierCubic.py' )


l1 = cmds.spaceLocator(name='loc1')
cmds.xform(l1,t=(-6,0,-2),ws=True)
l2 = cmds.spaceLocator(name='loc2')
cmds.xform(l2,t=(-5,0,-6),ws=True)
l3 = cmds.spaceLocator(name='loc3')
cmds.xform(l3,t=(1,0,-6),ws=True)
l4 = cmds.spaceLocator(name='loc4')
cmds.xform(l4,t=(2,0,-2),ws=True)


for i in range(0,11):
    nodeName = 'ccBezierCubic'+str(i)
    sphereName = 'sphere'+str(i)
    sphere = cmds.sphere(name=sphereName, radius=0.5)
    cmds.createNode( 'ccBezierCubic', name=nodeName)
    cmds.connectAttr( 'loc1.translate', nodeName+'.Point1' )
    cmds.connectAttr( 'loc2.translate', nodeName+'.Point2' )
    cmds.connectAttr( 'loc3.translate', nodeName+'.Point3' )
    cmds.connectAttr( 'loc4.translate', nodeName+'.Point4' )
    cmds.connectAttr( nodeName+'.SumBezier', sphereName+'.translate' )
    cmds.setAttr(nodeName+'.Bias',i/1.0*0.1)
    



'''
