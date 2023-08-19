# This is a sample Python script.
from vtk import *

def extract_isocontour(input_file, output_file, isovalue):
  
    reader = vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    data = reader.GetOutput()

    # Initialize a vtkCellArray object to store the contour segments
    contour_segments = vtkCellArray()

    # Initialize a vtkPoints object to store the vertices of the contour segments
    contour_points = vtkPoints()

    # Get the scalar range of the image data
    scalar_range = data.GetScalarRange()

    if isovalue < scalar_range[0] or isovalue > scalar_range[1]:
        print("Isovalue is not within the scalar_range of data")

    # Get the number of cells
    numCells = data.GetNumberOfCells()

    dataArr = data.GetPointData().GetArray('Pressure')

    for i in range(numCells):
        cell = data.GetCell(i)
        scalars = []
        pid1 = cell.GetPointId(0)
        pid2 = cell.GetPointId(1)
        pid3 = cell.GetPointId(3)
        pid4 = cell.GetPointId(2)
     
    #  Get the value at every vertices of cell
        val1 = dataArr.GetTuple1(pid1)
        val2 = dataArr.GetTuple1(pid2)
        val3 = dataArr.GetTuple1(pid3)
        val4 = dataArr.GetTuple1(pid4)
     
    #  append the value of vertices in scalars list
        scalars.append(val1)
        scalars.append(val2)
        scalars.append(val3)
        scalars.append(val4)

    # check the conditions here
        if (scalars[0] < isovalue and scalars[1] > isovalue) or (scalars[0] > isovalue and scalars[1] < isovalue):
            p1 = data.GetPoint(cell.GetPointId(0))
            p2 = data.GetPoint(cell.GetPointId(1))
            x = (val2 - isovalue) / (val2 - val1)
            x1 = x * (p1[0] - p2[0]) + p2[0]
            y1 = x * (p1[1] - p2[1]) + p2[1]
            contour_points.InsertNextPoint([x1, y1, 25.0])

        if (scalars[1] < isovalue and scalars[2] > isovalue) or (scalars[1] > isovalue and scalars[2] < isovalue):
            p2 = data.GetPoint(cell.GetPointId(1))
            p3 = data.GetPoint(cell.GetPointId(3))
            x = (val3 - isovalue) / (val3 - val2)
            x2 = x * (p2[0] - p3[0]) + p3[0]
            y2 = x * (p2[1] - p3[1]) + p3[1]
            contour_points.InsertNextPoint([x2, y2, 25.0])

        if (scalars[2] < isovalue and scalars[3] > isovalue) or (scalars[2] > isovalue and scalars[3] < isovalue):
            p3 = data.GetPoint(cell.GetPointId(3))
            p4 = data.GetPoint(cell.GetPointId(2))
            x = (val4 - isovalue) / (val4 - val3)
            x3 = x * (p3[0] - p4[0]) + p4[0]
            y3 = x * (p3[1] - p4[1]) + p4[1]
            contour_points.InsertNextPoint([x3, y3, 25.0])

        if (scalars[3] < isovalue and scalars[0] > isovalue) or (scalars[3] > isovalue and scalars[0] < isovalue):
            p4 = data.GetPoint(cell.GetPointId(2))
            p1 = data.GetPoint(cell.GetPointId(0))
            x = (val4 - isovalue) / (val4 - val1)
            x4 = x * (p1[0] - p4[0]) + p4[0]
            y4 = x * (p1[1] - p4[1]) + p4[1]
            contour_points.InsertNextPoint([x4, y4, 25.0])
    
    # create polyline
    i = 0
    polyLine = vtkPolyLine()
    while (i < contour_points.GetNumberOfPoints()):
        polyLine.GetPointIds().SetNumberOfIds(2)
        polyLine.GetPointIds().SetId(0, i)
        polyLine.GetPointIds().SetId(1, i + 1)
        i += 2
        contour_segments.InsertNextCell(polyLine)

    # Initialize vtkpolydata
        ####################
    pdata = vtkPolyData()

    ### Add points and cells to polydata
    ####################################
    pdata.SetPoints(contour_points)
    pdata.SetLines(contour_segments)

    # Write the vtkPolyData object to disk as a VTKPolyData file
    writer = vtkXMLPolyDataWriter()
    writer.SetFileName("isocontour.vtp")
    writer.SetInputData(pdata)
    writer.Write()


input_file = "Isabel_2D.vti"
output_file = "isocontour.vtp"            #output file
isovalue = input("Enter the isovalue:")   #take the input isovalue
isovalue=int(isovalue)

extract_isocontour(input_file, output_file, isovalue)
