#Author-Hyunyoung Kim
#Description-MorpheesPlug script for Fusion 360
#Basic unit: cm, rad

import adsk.core, adsk.fusion, adsk.cam, traceback, math

_app = adsk.core.Application.cast(None)
_ui = adsk.core.UserInterface.cast(None)
_handlers = []
_inputs = adsk.core.CommandInputs.cast(None)


def run(context):
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        # Create the command definition. 
        cmdDef = _ui.commandDefinitions.itemById('morpheesPlug')
        if not cmdDef:
            cmdDef = _ui.commandDefinitions.addButtonDefinition('morpheesPlug','Morphees Plug','Create Morphees Plug shape-changing widgets','Resources')
        
        # Connect to the command created event.
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        # # Add the button the ADD-INS panel.
        # addInsPanel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        # addInsPanel.controls.addCommand(cmdDef)

        # Execute the command definition.
        cmdDef.execute()                # Remove for Add-in

        # Prevent this module from being terminated when the script returns, because we are waiting for event handlers to fire.
        adsk.autoTerminate(False)       # Remove for Add-in

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the commandCreated event.
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try: 
            global _inputs

            # Get the command that was created.
            cmd = adsk.core.Command.cast(args.command)

            # # Connect to the command destroyed event.     # Remove for Add-in
            onDestroy = MyCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            _handlers.append(onDestroy)

            # Connect to the input changed event.           
            onInputChanged = MyCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            _handlers.append(onInputChanged)    

            # Connect to command excute handler. 
            onExecute = MyExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)

            # Connect to a preview handler.
            onExecutePreview = MyExecutePreviewHandler()
            cmd.executePreview.add(onExecutePreview)
            _handlers.append(onExecutePreview)
            
            # Get the CommandInputs collection associated with the command.
            _inputs = cmd.commandInputs
            #inputs = cmd.commandInputs
            
            # Connect to command inputs.
            des = adsk.fusion.Design.cast(_app.activeProduct)
            um = des.unitsManager       # TODO. change the unit.
            dropDownInput = _inputs.addDropDownCommandInput('dropDown', 'Widget', adsk.core.DropDownStyles.LabeledIconDropDownStyle)
            dropDownInputItems = dropDownInput.listItems
            dropDownInputItems.add('Fold', True, 'Resources/Widget_Fold')
            dropDownInputItems.add('Spiral', False, 'Resources/Widget_Spiral')
            dropDownInputItems.add('Teeth', False, 'Resources/Widget_Teeth')
            dropDownInputItems.add('Bump', False, 'Resources/Widget_Bump')
            dropDownInputItems.add('Accordion', False, 'Resources/Widget_Accordion')
            dropDownInputItems.add('Auxetic', False, 'Resources/Widget_Auxetic')

            _inputs.addGroupCommandInput('groupInputs', 'Set Parameters')
            updateInputs(_inputs)
        except:
                _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



def updateInputs(commandInputs):
    inputs = adsk.core.CommandInputs.cast(commandInputs)
    group = inputs.itemById('groupInputs')
    groupInputs = group.children

    # Remove all previous command inputs in the group
    while groupInputs.count > 0:
        groupInputs.item(0).deleteMe()

    dropDownInput = inputs.itemById('dropDown')
    dropDownItem = dropDownInput.selectedItem

    if dropDownItem.name == 'Fold':
        groupInputs.addImageCommandInput('imgFold', '', 'Resources/Widget_Image/Fold.png')
        groupInputs.item(0).isFullWidth = True
        groupInputs.addTextBoxCommandInput('textDesc', '', 'Fold widget will elongate along the arrow direction when inflated.', 3, True)
        groupInputs.addIntegerSpinnerCommandInput('numFolds', '1. Number of Folds', 1, 10, 1, 1) # id, name, min, max, spinStep, initialValue
        groupInputs.addValueInput('height', '2. Height', 'cm', adsk.core.ValueInput.createByReal(2))
        groupInputs.addValueInput('length', '3. Length', 'cm', adsk.core.ValueInput.createByReal(4))
        groupInputs.addValueInput('width', '4. Thickness', 'cm', adsk.core.ValueInput.createByReal(0.5))
        groupInputs.addValueInput('gap', '5. Gap', 'cm', adsk.core.ValueInput.createByReal(0.5))
        
    elif dropDownItem.name == 'Spiral':
        groupInputs.addImageCommandInput('imgFold', '', 'Resources/Widget_Image/Spiral.png')
        groupInputs.item(0).isFullWidth = True
        groupInputs.addTextBoxCommandInput('textDesc', '', 'Spiral widget will unbend when inflated.', 3, True)
        groupInputs.addIntegerSpinnerCommandInput('numTurns', '1. Number of Turns', 1, 10, 1, 1) # id, name, min, max, spinStep, initialValue
        groupInputs.addValueInput('height', '2. Height', 'cm', adsk.core.ValueInput.createByReal(2))
        groupInputs.addValueInput('offset', '3. Central Offset', 'cm', adsk.core.ValueInput.createByReal(1))
        groupInputs.addValueInput('width', '4. Thickness', 'cm', adsk.core.ValueInput.createByReal(0.5))
        groupInputs.addValueInput('distBtwTurns', '5. Gap', 'cm', adsk.core.ValueInput.createByReal(0.5))

    elif dropDownItem.name == 'Teeth':
        groupInputs.addImageCommandInput('imgFold', '', 'Resources/Widget_Image/Teeth.png')
        groupInputs.item(0).isFullWidth = True
        groupInputs.addTextBoxCommandInput('textDesc', '', 'Teeth widget will bend to the direction of the arrow when inflated.', 3, True)
        groupInputs.addValueInput('width', '1. Length 1', 'cm', adsk.core.ValueInput.createByReal(10))
        groupInputs.addValueInput('width2', '2. Length 2', 'cm', adsk.core.ValueInput.createByReal(3))
        groupInputs.addValueInput('height', '3. Height', 'cm', adsk.core.ValueInput.createByReal(5))
        groupInputs.addValueInput('depth', '4. Thickness 1', 'cm', adsk.core.ValueInput.createByReal(0.5))
        groupInputs.addValueInput('thickness', '5. Thickness 2', 'cm', adsk.core.ValueInput.createByReal(0.5))
        groupInputs.addValueInput('gap', '6. Gap', 'cm', adsk.core.ValueInput.createByReal(0.5))
        groupInputs.addValueInput('angle', '7. Angle', 'deg', adsk.core.ValueInput.createByReal(0))

    elif dropDownItem.name == 'Bump':
        groupInputs.addImageCommandInput('imgFold', '', 'Resources/Widget_Image/Bump.png')
        groupInputs.item(0).isFullWidth = True
        groupInputs.addTextBoxCommandInput('textDesc', '', 'Bump widget will create bumps where the empty chambers are when inflated.', 3, True)
        groupInputs.addIntegerSpinnerCommandInput('numWidth', '1. Chambers on X Axis', 1, 30, 1, 2)
        groupInputs.addIntegerSpinnerCommandInput('numLength', '2. Chambers on Y Axis', 1, 30, 1, 2)
        groupInputs.addValueInput('width', '3. Length on X Axis', 'cm', adsk.core.ValueInput.createByReal(1))
        groupInputs.addValueInput('length', '4. Length on Y Axis', 'cm', adsk.core.ValueInput.createByReal(1))

    elif dropDownItem.name == 'Accordion':
        groupInputs.addImageCommandInput('imgFold', '', 'Resources/Widget_Image/Accordion.png')
        groupInputs.item(0).isFullWidth = True
        groupInputs.addTextBoxCommandInput('textDesc', '', 'Accordion widget will create a set of length-changing chambers. Each chamber can be inflated individually', 3, True)
        groupInputs.addIntegerSpinnerCommandInput('height', '1. Number of Layers', 1, 10, 1, 1) # id, name, min, max, spinStep, initialValue
        groupInputs.addIntegerSpinnerCommandInput('x_axis', '2. Chambers on X Axis', 1, 10, 1, 2) # id, name, min, max, spinStep, initialValue
        groupInputs.addIntegerSpinnerCommandInput('y_axis', '3. Chambers on Y Axis', 1, 10, 1, 2) # id, name, min, max, spinStep, initialValue
        groupInputs.addValueInput('width', '4. Length on X Axis', 'cm', adsk.core.ValueInput.createByReal(5))
        groupInputs.addValueInput('depth', '5. Length on Y Axis', 'cm', adsk.core.ValueInput.createByReal(5))

    elif dropDownItem.name == 'Auxetic':
        groupInputs.addImageCommandInput('imgFold', '', 'Resources/Widget_Image/Accordion.png')
        groupInputs.item(0).isFullWidth = True
        groupInputs.addTextBoxCommandInput('textDesc', '', 'Auxetic widget will change width when inflated.', 3, True)
        groupInputs.addValueInput('a', '1. Width', 'cm', adsk.core.ValueInput.createByReal(3.5))
        groupInputs.addValueInput('b', '2. Inner Gap', 'mm', adsk.core.ValueInput.createByReal(.3))
        groupInputs.addValueInput('c', '3. Outer Gap', 'mm', adsk.core.ValueInput.createByReal(.8))
        groupInputs.addValueInput('height', '4. Height', 'cm', adsk.core.ValueInput.createByReal(2.5))



# Event handler that reacts to any changes the user makes to any of the command inputs.
class MyCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            # inputs = eventArgs.inputs
            # cmdInput = eventArgs.input
            command = args.firingEvent.sender
            cmdInput = args.input
            # onInputChange for slider controller
            if cmdInput.id == 'dropDown':
                #updateInputs(inputs)
                updateInputs(args.inputs)
                
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



# Now I feel this handler is not necessary, because the preview handler does the job I need.
class MyExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            
            dropDownInput = _inputs.itemById('dropDown')
            dropDownItem = dropDownInput.selectedItem
            #_ui.messageBox(dropDownItem.name)

            if dropDownItem.name == 'Fold':
                numFolds = _inputs.itemById('numFolds').value
                width = _inputs.itemById('width').value
                length = _inputs.itemById('length').value
                height = _inputs.itemById('height').value
                gap = _inputs.itemById('gap').value
                modelFold(numFolds, width, length, height, gap)

            elif dropDownItem.name == 'Spiral':
                numTurns = _inputs.itemById('numTurns').value
                distBtwTurns = _inputs.itemById('distBtwTurns').value
                width = _inputs.itemById('width').value
                height = _inputs.itemById('height').value
                offset = _inputs.itemById('offset').value
                modelSpiral(numTurns, distBtwTurns, width, height, offset)

            elif dropDownItem.name == 'Teeth':
                width = _inputs.itemById('width').value
                width2 = _inputs.itemById('width2').value
                depth = _inputs.itemById('depth').value
                thickness = _inputs.itemById('thickness').value
                gap = _inputs.itemById('gap').value
                height = _inputs.itemById('height').value
                angle = _inputs.itemById('angle').value
                modelTeeth(width, width2, depth, height, angle, thickness, gap)

            elif dropDownItem.name == 'Bump':
                width = _inputs.itemById('width').value
                length = _inputs.itemById('length').value
                numWidth = _inputs.itemById('numWidth').value
                numLength = _inputs.itemById('numLength').value
                modelBump(width, length, numWidth, numLength)

            elif dropDownItem.name == 'Accordion':
                width = _inputs.itemById('width').value
                depth = _inputs.itemById('depth').value
                height = _inputs.itemById('height').value
                x_axis = _inputs.itemById('x_axis').value
                y_axis = _inputs.itemById('y_axis').value
                modelAccordion(width, depth, height, x_axis, y_axis)

            elif dropDownItem.name == 'Auxetic':
                a = _inputs.itemById('a').value
                b = _inputs.itemById('b').value
                c = _inputs.itemById('c').value
                height = _inputs.itemById('height').value
                modelAuxetic(a, b, c, height)

        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



class MyExecutePreviewHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            
            dropDownInput = _inputs.itemById('dropDown')
            dropDownItem = dropDownInput.selectedItem
            #_ui.messageBox(dropDownItem.name)

            if dropDownItem.name == 'Fold':
                numFolds = _inputs.itemById('numFolds').value
                width = _inputs.itemById('width').value
                length = _inputs.itemById('length').value
                height = _inputs.itemById('height').value
                gap = _inputs.itemById('gap').value
                modelFold(numFolds, width, length, height, gap)

            elif dropDownItem.name == 'Spiral':
                numTurns = _inputs.itemById('numTurns').value
                distBtwTurns = _inputs.itemById('distBtwTurns').value
                width = _inputs.itemById('width').value
                height = _inputs.itemById('height').value
                offset = _inputs.itemById('offset').value
                modelSpiral(numTurns, distBtwTurns, width, height, offset)

            elif dropDownItem.name == 'Teeth':
                width = _inputs.itemById('width').value
                width2 = _inputs.itemById('width2').value
                depth = _inputs.itemById('depth').value
                thickness = _inputs.itemById('thickness').value
                gap = _inputs.itemById('gap').value
                height = _inputs.itemById('height').value
                angle = _inputs.itemById('angle').value
                modelTeeth(width, width2, depth, height, angle, thickness, gap)

            elif dropDownItem.name == 'Bump':
                width = _inputs.itemById('width').value
                length = _inputs.itemById('length').value
                numWidth = _inputs.itemById('numWidth').value
                numLength = _inputs.itemById('numLength').value
                modelBump(width, length, numWidth, numLength)

            elif dropDownItem.name == 'Accordion':
                width = _inputs.itemById('width').value
                depth = _inputs.itemById('depth').value
                height = _inputs.itemById('height').value
                x_axis = _inputs.itemById('x_axis').value
                y_axis = _inputs.itemById('y_axis').value
                modelAccordion(width, depth, height, x_axis, y_axis)

            elif dropDownItem.name == 'Auxetic':
                a = _inputs.itemById('a').value
                b = _inputs.itemById('b').value
                c = _inputs.itemById('c').value
                height = _inputs.itemById('height').value
                modelAuxetic(a, b, c, height)
            eventArgs.isValidResult = True

        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



# Event handler that reacts to when the command is destroyed. This terminates the script. 
#      # Remove for Add-in           
class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # When the command is done, terminate the script
            # This will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



# Model a fold widget with the given parameters.
def modelFold(numFolds, width, length, height, gap):
    try:
        design = adsk.fusion.Design.cast(_app.activeProduct)
        root = design.rootComponent
        sketches = root.sketches
        features = root.features
        
        ### 1. Draw sketch lines, path.
        sketchPath = sketches.add(root.xYConstructionPlane)
        lines = sketchPath.sketchCurves.sketchLines
        lineCollection = adsk.core.ObjectCollection.create()
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = length

        line = lines.addByTwoPoints(adsk.core.Point3D.create(0, -width/2, 0), adsk.core.Point3D.create(0, 0, 0))
        lineCollection.add(line)

        for i in range(numFolds):
            x1 = (gap + width) * 2 * i
            y1 = 0
            x2 = (gap + width) * 2 * i
            y2 = length
            line = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))
            lineCollection.add(line)

            x1 = x2
            y1 = y2
            x2 = x2 + (gap + width)
            y2 = y2
            line = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))
            lineCollection.add(line)

            x1 = x2
            y1 = y2
            x2 = x2
            y2 = 0
            line = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))
            lineCollection.add(line)

            x1 = x2
            y1 = y2
            x2 = x2 + (gap + width)
            y2 = y2
            line = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))
            lineCollection.add(line)

        x1 = x2
        y1 = y2
        y2 = length + width/2
        line = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))
        lineCollection.add(line)

        chainedOption = adsk.fusion.ChainedCurveOptions.connectedChainedCurves
        path = adsk.fusion.Path.create(lineCollection, chainedOption)   # Actually the value of chainedOption does not matter when input ObjectCollection.


        ### 2. Create a profile for sweep.
        # Create a sketch
        xzPlane = root.xZConstructionPlane
        sketchProfile = sketches.add(xzPlane)

        # Create two points to create a rectangle.
        center = xzPlane.geometry.origin
        center = sketchProfile.modelToSketchSpace(center)

        sketchPoints = sketchProfile.sketchPoints
        point = adsk.core.Point3D.create(width/2, height/2, 0)
        sketchPoint = sketchPoints.add(point)

        # Create a rectangular profile with the created two points.
        lines = sketchProfile.sketchCurves.sketchLines
        rect = lines.addCenterPointRectangle(center, sketchPoint)
        prof = sketchProfile.profiles.item(0)
        
        # 3. Sweep.
        sweeps = root.features.sweepFeatures
        sweepInput = sweeps.createInput(prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        sweep = sweeps.add(sweepInput)

    except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



# Model a spiral widget with the given parameters.
def modelSpiral(numTurns, distanceBetweenTurns, width, height, offset):
    try: 
        #_ui.messageBox('Test 01')

        design = adsk.fusion.Design.cast(_app.activeProduct)
        root = design.rootComponent
        sketches = root.sketches
        features = root.features

        ### Create a spiral path.
        # Create a new sketch.
        sketchPath = sketches.add(root.xYConstructionPlane)

        # Create a series of points along the spiral using the spiral equation.
        # r = a + (beta * theta) --> r = offset + (distanceBetweenTurns * theta)
        points = adsk.core.ObjectCollection.create()
        pointsPerTurn = 20
        theta = 0
        offset = offset + width/2
        for i in range(pointsPerTurn * numTurns + 1):
            r = offset + ((distanceBetweenTurns + width) * theta/(math.pi*2)) 
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.add(adsk.core.Point3D.create(x,y,0))
            
            theta += (math.pi*2) / pointsPerTurn

        splines = sketchPath.sketchCurves.sketchFittedSplines.add(points)
        path = features.createPath(splines)
        
        ### Create a profile.
        # Create a plane normal to the splines.
        planes = root.constructionPlanes
        planeInput = planes.createInput()
        planeInput.setByDistanceOnPath(splines, adsk.core.ValueInput.createByReal(0))
        plane = planes.add(planeInput)
        
        # Create two points to create a rectangle.
        sketchProfile = sketches.add(plane)
        center = plane.geometry.origin
        center = sketchProfile.modelToSketchSpace(center)

        sketchPoints = sketchProfile.sketchPoints
        point = adsk.core.Point3D.create(width/2, height/2, 0)
        sketchPoint = sketchPoints.add(point)

        # Create a rectangular profile with the created two points.
        lines = sketchProfile.sketchCurves.sketchLines
        rect = lines.addCenterPointRectangle(center, sketchPoint)
        prof = sketchProfile.profiles.item(0) # Make a profile

        ### Create a spiral widget.
        # Sweep
        sweeps = root.features.sweepFeatures
        sweepInput = sweeps.createInput(prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        sweep = sweeps.add(sweepInput)

    except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



# Model a widget that has teeth (previously called wrinkles) on one side.
def modelTeeth(width, width2, depth, height, angle, thickness, gap):
    try:
        design = adsk.fusion.Design.cast(_app.activeProduct)
        root = design.rootComponent
        sketches = root.sketches
        features = root.features

        # Internal parameters.
        wrinkleWidth = thickness
        wrinkleGap = gap
        wrinkleLength = width2

        # ### 1. Make a wall to put wrinkles.
        # # Draw a box for wall and teeth 
        # sketchWall = sketches.add(root.xYConstructionPlane)
        # lines = sketchWall.sketchCurves.sketchLines
        # _ = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, -depth, 0), adsk.core.Point3D.create(width, wrinkleLength, 0))
        # prof = sketchWall.profiles.item(0)

        # # Extrude
        # extrudes = features.extrudeFeatures
        # distance = adsk.core.ValueInput.createByReal(height)
        # _ = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # ### 2. Make wrinkles.
        # # Create a new sketch
        # planes = root.constructionPlanes
        # planeInput = planes.createInput()
        # planeInput.setByAngle(root.yConstructionAxis, angle, prof)
        # teethPlane = planes.add(planeInput)
        # sketchTeeth = sketches.add(teethPlane)
        # lines = sketchTeeth.sketchCurves.sketchLines

        ### 1. Make a wall to put wrinkles.
        # Draw the wall
        sketchWall = sketches.add(root.xZConstructionPlane)
        lines = sketchWall.sketchCurves.sketchLines
        _ = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(width, height, 0))
        prof = sketchWall.profiles.item(0)

        # Extrude
        extrudes = features.extrudeFeatures
        distance = adsk.core.ValueInput.createByReal(-depth)
        _ = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        ### 2. Make wrinkles.
        # Create a new sketch
        planes = root.constructionPlanes
        planeInput = planes.createInput()
        sketchTeeth = sketches.add(root.xZConstructionPlane)
        lines = sketchTeeth.sketchCurves.sketchLines

        if angle == 0:
            # Draw wrinkles
            startPointX = 0
            endPointX = wrinkleWidth
            while endPointX < width:
                rect = lines.addTwoPointRectangle(adsk.core.Point3D.create(startPointX, 0, 0), adsk.core.Point3D.create(endPointX, height, 0))
                startPointX = endPointX + wrinkleGap
                endPointX = startPointX + wrinkleWidth

        else:
            # Draw first triangle
            xTiltedRect = wrinkleWidth / math.cos(angle)
            #_ui.messageBox("width:"+str(wrinkleWidth)+"   x:"+str(xTiltedRect))
            lines.addByTwoPoints(adsk.core.Point3D.create(0, height, 0), adsk.core.Point3D.create(xTiltedRect, height, 0))
            lines.addByTwoPoints(adsk.core.Point3D.create(xTiltedRect, height, 0), adsk.core.Point3D.create(0, height-wrinkleWidth/math.sin(angle), 0))
            lines.addByTwoPoints(adsk.core.Point3D.create(0, height-wrinkleWidth/math.sin(angle), 0), adsk.core.Point3D.create(0, height, 0))

            # Draw parallelograms
            topX1 = 2 * xTiltedRect
            topX2 = topX1 + xTiltedRect
            bottomX1 = topX1 - height / math.tan(math.pi/2 - angle)
            bottomX2 = bottomX1 + xTiltedRect
            while topX2 < width:
                if bottomX1 >= 0:
                    lines.addByTwoPoints(adsk.core.Point3D.create(topX1, height, 0), adsk.core.Point3D.create(topX2, height, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(topX2, height, 0), adsk.core.Point3D.create(bottomX2, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(bottomX2, 0, 0), adsk.core.Point3D.create(bottomX1, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(bottomX1, 0, 0), adsk.core.Point3D.create(topX1, height, 0))

                elif bottomX1 < 0 and bottomX2 > 0:
                    lines.addByTwoPoints(adsk.core.Point3D.create(topX1, height, 0), adsk.core.Point3D.create(topX2, height, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(topX2, height, 0), adsk.core.Point3D.create(bottomX2, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(bottomX2, 0, 0), adsk.core.Point3D.create(0, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, height - topX1 / math.tan(angle), 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(0, height - topX1 / math.tan(angle), 0), adsk.core.Point3D.create(topX1, height, 0))
                    
                else: # bottomX2 <= 0
                    lines.addByTwoPoints(adsk.core.Point3D.create(topX1, height, 0), adsk.core.Point3D.create(topX2, height, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(topX2, height, 0), adsk.core.Point3D.create(0, height - topX2 / math.tan(angle), 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(0, height - topX2 / math.tan(angle), 0), adsk.core.Point3D.create(0, height - topX1 / math.tan(angle), 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(0, height - topX1 / math.tan(angle), 0), adsk.core.Point3D.create(topX1, height, 0))

                topX1 += 2 * xTiltedRect
                topX2 = topX1 + xTiltedRect
                bottomX1 += 2 * xTiltedRect
                bottomX2 = bottomX1 + xTiltedRect

            counter = 1

            while bottomX1 < width:
                if topX1 < width:
                    lines.addByTwoPoints(adsk.core.Point3D.create(topX1, height, 0), adsk.core.Point3D.create(width, height, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(width, height, 0), adsk.core.Point3D.create(width, height - (topX2 - width) / math.tan(angle), 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(width, height - (topX2 - width) / math.tan(angle), 0), adsk.core.Point3D.create(bottomX2, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(bottomX2, 0, 0), adsk.core.Point3D.create(bottomX1, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(bottomX1, 0, 0), adsk.core.Point3D.create(topX1, height, 0))

                elif bottomX2 < width:
                    lines.addByTwoPoints(adsk.core.Point3D.create(width, height - (topX1 - width) / math.tan(angle), 0), adsk.core.Point3D.create(width, height - (topX2 - width) / math.tan(angle), 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(width, height - (topX2 - width) / math.tan(angle), 0), adsk.core.Point3D.create(bottomX2, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(bottomX2, 0, 0), adsk.core.Point3D.create(bottomX1, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(bottomX1, 0, 0), adsk.core.Point3D.create(width, height - (topX1 - width) / math.tan(angle), 0))

                else: #bottomX2 >= width
                    lines.addByTwoPoints(adsk.core.Point3D.create(width, height - (topX1 - width) / math.tan(angle), 0), adsk.core.Point3D.create(width, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(width, 0, 0), adsk.core.Point3D.create(bottomX1, 0, 0))
                    lines.addByTwoPoints(adsk.core.Point3D.create(bottomX1, 0, 0), adsk.core.Point3D.create(width, height - (topX1 - width) / math.tan(angle), 0))

                topX1 += 2 * xTiltedRect
                topX2 = topX1 + xTiltedRect
                bottomX1 += 2 * xTiltedRect
                bottomX2 = bottomX1 + xTiltedRect
                counter += 1

        # Make profiles.
        profileCollection = adsk.core.ObjectCollection.create()
        for i in range(sketchTeeth.profiles.count):
            profileCollection.add(sketchTeeth.profiles.item(i))

        # Extrude.
        distance = adsk.core.ValueInput.createByReal(wrinkleLength)
        _ = extrudes.addSimple(profileCollection, distance, adsk.fusion.FeatureOperations.JoinFeatureOperation)

    except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



# Model a Bump widget with the given parameters.
def modelBump(width, length, numWidth, numLength):
    try:
        design = adsk.fusion.Design.cast(_app.activeProduct)
        root = design.rootComponent
        sketches = root.sketches
        features = root.features

        # # user parameters
        # width = 1
        # length = 1
        # numWidth = 2
        # numLength = 3

        # internal parameters
        gap = 0.2
        heightTop = 0.06
        heightBottom = 0.2
        heightChamber = 0.3
        totalWidth = (gap + width) * numWidth + gap
        totalLength = (gap + length) * numLength + gap
        
        ### 1. Extrude for the top layer and chambers.
        # Draw a rectangle for the top layer (top layer where bumps will go up will be printed at the bottom.)
        sketchTop = sketches.add(root.xYConstructionPlane)
        lines = sketchTop.sketchCurves.sketchLines
        rect = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(totalWidth, totalLength, 0))
        prof = sketchTop.profiles.item(0)

        # Extrude
        extrudes = features.extrudeFeatures
        distance = adsk.core.ValueInput.createByReal(heightTop + heightChamber)
        extrude1 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        ### 2. Draw and extrude chambers
        # Create a new sketch
        planes = root.constructionPlanes
        planeInput = planes.createInput()
        planeInput.setByOffset(root.xYConstructionPlane, distance)
        planeChamber = planes.add(planeInput)
        sketchChamber = sketches.add(planeChamber)
        lines = sketchChamber.sketchCurves.sketchLines

        # Draw chambers
        for i in range(numWidth):
            for j in range(numLength):
                xCorner = gap + (width + gap) * i
                yCorner = gap + (length + gap) * j
                lines.addTwoPointRectangle(adsk.core.Point3D.create(xCorner, yCorner, 0), adsk.core.Point3D.create(xCorner + width, yCorner + length, 0))

        # Extrude chambers
        profileCollection = adsk.core.ObjectCollection.create()
        for i in range(sketchChamber.profiles.count):
            profileCollection.add(sketchChamber.profiles.item(i))

        distance = adsk.core.ValueInput.createByReal(-heightChamber)
        extrude2 = extrudes.addSimple(profileCollection, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)

        ### 3. Draw and extrude bottom layer.
        # Draw a rectangle
        sketchBottom = sketches.add(planeChamber)
        lines = sketchBottom.sketchCurves.sketchLines
        rect = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(totalWidth, totalLength, 0))
        prof = sketchBottom.profiles.item(0)

        # Extrude.
        distance = adsk.core.ValueInput.createByReal(heightBottom)
        extrude3 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.JoinFeatureOperation)

    except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



def modelAccordion(width, depth, height, x_axis, y_axis):
    # Internal widget values:
    wrinkle_height = 0.5
    wrinkle_spacing = 1
    shell_thickness = .1

    try:
        design = adsk.fusion.Design.cast(_app.activeProduct)
        root = design.rootComponent
        sketches = root.sketches
        features = root.features
        planes = root.constructionPlanes

        for i in range(int(x_axis)):
            for j in range(int(y_axis)):
                bodies = adsk.core.ObjectCollection.create()
                target_body = None
                for k in range(int(height)):
                    # Creating planes
                    offsetValue = adsk.core.ValueInput.createByReal(k * wrinkle_height * 2)
                    planeInput = planes.createInput()
                    planeInput.setByOffset(root.xYConstructionPlane, offsetValue)
                    p = planes.add(planeInput)
                    # Sketching
                    s = sketches.add(p)
                    lines = s.sketchCurves.sketchLines
                    _ = lines.addTwoPointRectangle(adsk.core.Point3D.create(i * width, j * depth, 0), adsk.core.Point3D.create((i * width) + width, (j * depth) + depth, 0))
                    prof = s.profiles.item(0)
                    # Extruding
                    extrudes = features.extrudeFeatures
                    distance = adsk.core.ValueInput.createByReal(wrinkle_height)
                    base = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                    if k == 0:
                        target_body = base.bodies.item(0)
                    else:
                        bodies.add(base.bodies.item(0))

                    faces = base.endFaces
                    s = sketches.add(faces.item(0))
                    lines = s.sketchCurves.sketchLines
                    _ = lines.addTwoPointRectangle(adsk.core.Point3D.create((i * width) + wrinkle_spacing, (j * depth) + wrinkle_spacing, 0), adsk.core.Point3D.create((i * width) + width - wrinkle_spacing, (j * depth) + depth - wrinkle_spacing, 0))
                    prof = s.profiles.item(1)
                    # Extruding
                    extrudes = features.extrudeFeatures
                    distance = adsk.core.ValueInput.createByReal(wrinkle_height)
                    wrinkle = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                    bodies.add(wrinkle.bodies.item(0))
                combineFeatures = features.combineFeatures
                combineFeatureInput = combineFeatures.createInput(target_body, bodies)
                combineFeatureInput.operation = 0
                combineFeatureInput.isKeepToolBodies = False
                combineFeatureInput.isNewComponent = False
                _ = combineFeatures.add(combineFeatureInput).bodies.item(0)

                # Shelling
                shellFeats = features.shellFeatures
                isTangentChain = True
                #e = adsk.core.ObjectCollection.create()
                #bodies.add(bodies.endFaces.item(0))
                shellFeatureInput = shellFeats.createInput(bodies, isTangentChain)
                thickness = adsk.core.ValueInput.createByReal(.1)
                shellFeatureInput.insideThickness = thickness
                shellFeats.add(shellFeatureInput)

    except:
        _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def modelAuxetic(a, b, c, height):
    theta = 0.523599 # 30 degrees in radians

    try: 
        design = adsk.fusion.Design.cast(_app.activeProduct)
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        features = rootComp.features
        s = sketches.add(xyPlane)
    
        # # Sketching
        lines = s.sketchCurves.sketchLines
        p2x = a * math.cos(theta)
        p2y = a * math.sin(theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(p2x, p2y, 0))
        p3x = p2x + b * math.cos(theta + theta)
        p3y = p2y + b * math.sin(theta + theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p2x, p2y, 0), adsk.core.Point3D.create(p3x, p3y,0))
        p4x = p3x + a * math.cos(2 * theta + theta)
        p4y = p3y + a * math.sin(2 * theta + theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p3x, p3y,0), adsk.core.Point3D.create(p4x, p4y, 0))
        p5x = p4x + (a - c) * math.cos(3 * theta + 4 * theta)
        p5y = p4y + (a - c) * math.sin(3 * theta + 4 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p4x, p4y, 0), adsk.core.Point3D.create(p5x, p5y, 0))
        p6x = p5x + b * math.cos(7 * theta - 3 * theta)
        p6y = p5y + b * math.sin(7 * theta - 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p5x, p5y, 0), adsk.core.Point3D.create(p6x, p6y, 0))
        p7x = p6x + (a - c) * math.cos(4 * theta - 3 * theta)
        p7y = p6y + (a - c) * math.sin(4 * theta - 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p6x, p6y, 0), adsk.core.Point3D.create(p7x, p7y, 0))
        p8x = p7x + a * math.cos(theta + 4 * theta)
        p8y = p7y + a * math.sin(theta + 4 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p7x, p7y, 0), adsk.core.Point3D.create(p8x, p8y, 0))
        p9x = p8x + b * math.cos(5 * theta + theta)
        p9y = p8y + b * math.sin(5 * theta + theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p8x, p8y, 0), adsk.core.Point3D.create(p9x, p9y, 0))
        p10x = p9x + a * math.cos(6 * theta + theta)
        p10y = p9y + a * math.sin(6 * theta + theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p9x, p9y, 0), adsk.core.Point3D.create(p10x, p10y, 0))
        p11x = p10x + (a - c) * math.cos(7 * theta + 4 * theta)
        p11y = p10y + (a - c) * math.sin(7 * theta + 4 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p10x, p10y, 0), adsk.core.Point3D.create(p11x, p11y, 0))
        p12x = p11x + b * math.cos(11 * theta - 3 * theta)
        p12y = p11y + b * math.sin(11 * theta - 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p11x, p11y, 0), adsk.core.Point3D.create(p12x, p12y, 0))
        p13x = p12x + (a - c) * math.cos(8 * theta - 3 * theta)
        p13y = p12y + (a - c) * math.sin(8 * theta - 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p12x, p12y, 0), adsk.core.Point3D.create(p13x, p13y, 0))
        p14x = p13x + a * math.cos(5 * theta + 4 * theta)
        p14y = p13y + a * math.sin(5 * theta + 4 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p13x, p13y, 0), adsk.core.Point3D.create(p14x, p14y, 0))
        p15x = p14x + b * math.cos(9 * theta + theta)
        p15y = p14y + b * math.sin(9 * theta + theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p14x, p14y, 0), adsk.core.Point3D.create(p15x, p15y, 0))
        p16x = p15x + a * math.cos(10 * theta + theta)
        p16y = p15y + a * math.sin(10 * theta + theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p15x, p15y, 0), adsk.core.Point3D.create(p16x, p16y, 0))
        p17x = p16x + (a - c) * math.cos(11 * theta + 4 * theta)
        p17y = p16y + (a - c) * math.sin(11 * theta + 4 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p16x, p16y, 0), adsk.core.Point3D.create(p17x, p17y, 0))
        p18x = p17x + b * math.cos(15 * theta - 3 * theta)
        p18y = p17y + b * math.sin(15 * theta - 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p17x, p17y, 0), adsk.core.Point3D.create(p18x, p18y, 0))
        p19x = p18x + (a - c) * math.cos(12 * theta - 3 * theta)
        p19y = p18y + (a - c) * math.sin(12 * theta - 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p18x, p18y, 0), adsk.core.Point3D.create(p19x, p19y, 0))
        prof = s.profiles.item(0)
        # Extruding
        extrudes = features.extrudeFeatures
        distance = adsk.core.ValueInput.createByReal(height)
        _ = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        # Interior design
        p2x = 0 + (a - c) * math.cos(-theta)
        p2y = a + (a - c) * math.sin(-theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(0, a, 0), adsk.core.Point3D.create(p2x, p2y, 0))
        p3x = p2x + b * math.cos(-theta + 3 * theta)
        p3y = p2y + b * math.sin(-theta + 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p2x, p2y, 0), adsk.core.Point3D.create(p3x, p3y, 0))
        p4x = p3x + (a - c) * math.cos(2 * theta + 3 * theta)
        p4y = p3y + (a - c) * math.sin(2 * theta + 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p3x, p3y, 0), adsk.core.Point3D.create(p4x, p4y, 0))
        p5x = p4x + b * math.cos(5 * theta - theta)
        p5y = p4y + b * math.sin(5 * theta - theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p4x, p4y, 0), adsk.core.Point3D.create(p5x, p5y, 0))
        p6x = p5x + (a - c) * math.cos(4 * theta - theta)
        p6y = p5y + (a - c) * math.sin(4 * theta - theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p5x, p5y, 0), adsk.core.Point3D.create(p6x, p6y, 0))
        p7x = p6x + b * math.cos(3 * theta + 3 * theta)
        p7y = p6y + b * math.sin(3 * theta + 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p6x, p6y, 0), adsk.core.Point3D.create(p7x, p7y, 0))
        p8x = p7x + (a - c) * math.cos(6 * theta + 3 * theta)
        p8y = p7y + (a - c) * math.sin(6 * theta + 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p7x, p7y, 0), adsk.core.Point3D.create(p8x, p8y, 0))
        p9x = p8x + b * math.cos(9 * theta - theta)
        p9y = p8y + b * math.sin(9 * theta - theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p8x, p8y, 0), adsk.core.Point3D.create(p9x, p9y, 0))
        p10x = p9x + (a - c) * math.cos(8 * theta - theta)
        p10y = p9y + (a - c) * math.sin(8 * theta - theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p9x, p9y, 0), adsk.core.Point3D.create(p10x, p10y, 0))
        p11x = p10x + b * math.cos(7 * theta + 3 * theta)
        p11y = p10y + b * math.sin(7 * theta + 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p10x, p10y, 0), adsk.core.Point3D.create(p11x, p11y, 0))
        p12x = p11x + (a - c) * math.cos(10 * theta + 3 * theta)
        p12y = p11y + (a - c) * math.sin(10 * theta + 3 * theta)
        lines.addByTwoPoints(adsk.core.Point3D.create(p11x, p11y, 0), adsk.core.Point3D.create(p12x, p12y, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(p12x, p12y, 0), adsk.core.Point3D.create(0, a, 0))
        prof = s.profiles.item(1)
        # Extruding
        extrudes = features.extrudeFeatures
        distance = adsk.core.ValueInput.createByReal(height)
        _ = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)

    except:
        _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))