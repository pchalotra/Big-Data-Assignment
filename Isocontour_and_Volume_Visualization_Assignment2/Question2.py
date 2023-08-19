from vtk import *
# Load the 3D data
reader =vtkXMLImageDataReader()
reader.SetFileName("Isabel_3D.vti")
reader.Update()

# Create instances of vtkColorTransferFunction and vtkPiecewiseFunction
color_transfer_function = vtkColorTransferFunction()
opacity_transfer_function = vtkPiecewiseFunction()

# Set up color transfer function
color_transfer_function.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
color_transfer_function.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
color_transfer_function.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)
color_transfer_function.AddRGBPoint(-1027.16 , 1.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(-298.031  , 1.0, 0.4, 0.0)
color_transfer_function.AddRGBPoint(2594.97  , 1.0, 1.0, 0.0)

# Set up opacity transfer function
opacity_transfer_function.AddPoint(-4931.54 , 1.0)
opacity_transfer_function.AddPoint(101.815, 0.002)
opacity_transfer_function.AddPoint(2594.97, 0.0)

# Use vtkSmartVolumeMapper to perform the volume rendering
volume_mapper = vtkSmartVolumeMapper()
volume_mapper.SetInputData(reader.GetOutput())

# Create a volume
volume_property = vtkVolumeProperty()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)


# Use vtkOutlineFilter to add an outline to the volume rendered data
outline = vtkOutlineFilter()
outline.SetInputData(reader.GetOutput())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
# outline_actor.GetProperty().SetColor(255, 255, 0)



# Take input from the user to determine if Phong shading should be used
use_phong = input("Do you want to use Phong shading (yes/no)? ")

if use_phong.lower() == "yes":
    # Set Phong shading parameters
    volume.GetProperty().ShadeOn()
    volume.GetProperty().SetAmbient(0.5)
    volume.GetProperty().SetDiffuse(0.5)
    volume.GetProperty().SetSpecular(0.5)

# Create a render window
renderer = vtkRenderer()
renderer.SetBackground(1,1,1)
renderer.AddVolume(volume)
renderer.AddActor(outline_actor)

render_window = vtkRenderWindow()
render_window.SetSize(1000, 1000)
render_window.AddRenderer(renderer)

# Start the rendering
render_window.Render()

# Set up an interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
# interactor.Initialize()
interactor.Start()