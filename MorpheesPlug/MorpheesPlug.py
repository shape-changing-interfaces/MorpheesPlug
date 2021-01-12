#Author-Hyunyoung Kim
#Description-MorpheesPlug add-in for Fusion 360

import adsk.core, adsk.fusion, adsk.cam, traceback

_app = adsk.core.Application.cast(None)
_ui = adsk.core.UserInterface.cast(None)
_handlers = []

def run(context):
    try:
        global _app, _ui
        _app= adsk.core.Application.get()
        _ui= _app.userInterface

        # Create the command definition. 
        cmdDef = _ui.commandDefinitions.addButtonDefinition('morpheesPlug','Morphees Plug','Create Morphees Plug shape-changing widgets','Resources')

        # Connect to the command created event.
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        # Add the button the ADD-INS panel.
        addInsPanel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        addInsPanel.controls.addCommand(cmdDef)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        cmdDef = _ui.commandDefinitions.itemById('morpheesPlug')
        if cmdDef:
            cmdDef.deleteMe()
            
        addInsPanel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        control = addInsPanel.controls.itemById('morpheesPlug')
        if control:
            control.deleteMe()
            
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the commandCreated event.
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try: 
            # Get the command that was created.
            cmd = adsk.core.Command.cast(args.command)

            # # Connect to the command destroyed event.
            # onDestroy = MyCommandDestroyHandler()
            # cmd.destroy.add(onDestroy)
            # _handlers.append(onDestroy)

            # Connect to the input changed event.           
            onInputChanged = MyCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            _handlers.append(onInputChanged)    
            
            # Get the CommandInputs collection associated with the command.
            inputs = cmd.commandInputs
            
            # Connect to command inputs.
            des = adsk.fusion.Design.cast(_app.activeProduct)
            um = des.unitsManager
            dropDownInput = inputs.addDropDownCommandInput('dropDown', 'Widget/Connector', adsk.core.DropDownStyles.LabeledIconDropDownStyle)
            dropDownInputItems = dropDownInput.listItems
            dropDownInputItems.add('Folded', True, 'Resources/Widget_Length')
            dropDownInputItems.add('Spiral', False, 'Resources/Widget_Spiral')
            
        except:
                _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler that reacts to any changes the user makes to any of the command inputs.
class MyCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            inputs = eventArgs.inputs
            cmdInput = eventArgs.input
            # onInputChange for slider controller
            if cmdInput.id == "dropDown":
                
                dropDownInput = inputs.itemById('dropDown')
                dropDownItem = dropDownInput.selectedItem

                #_ui.messageBox(dropDownItem.name + " Selected.")

                if dropDownItem.name == "Spiral":
                    _ui.messageBox("Spiral Selected.")
                    inputs.addValueInput('numTurns', "Number of Turns", 'mm', adsk.core.ValueInput.createByReal(1))
                    
                    
          
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# # Input parametersfor shape
# pipeRadius = 2.5
# pipeThickness = '5mm'

# # Assigning variables
# radius = 5


# def run(context):
#     ui = None
    
#     try:
        
#         app = adsk.core.Application.get()
#         ui  = app.userInterface
#         ui.messageBox('Test 01')

        

 
#         des = adsk.fusion.Design.cast(app.activeProduct)
#         root = des.rootComponent

#         # Create a new sketch.
#         sk = root.sketches.add(root.xYConstructionPlane)

#         # Create a series of points along the spiral using the spiral equation.
#         # r = a + (beta * theta)
#         pnts = adsk.core.ObjectCollection.create()
#         numTurns = 5
#         pointsPerTurn = 20
#         distanceBetweenTurns = 5  # beta
#         theta = 0
#         offset = 5                # a
#         for i in range(pointsPerTurn * numTurns + 1):
#             r = offset + (distanceBetweenTurns * theta) 
#             x = r * math.cos(theta)
#             y = r * math.sin(theta)
#             pnts.add(adsk.core.Point3D.create(x,y,0))
            
#             theta += (math.pi*2) / pointsPerTurn

#         sk.sketchCurves.sketchFittedSplines.add(pnts) 