#!/usr/bin/env python
# coding: utf-8

# In[1]:


import vtk 
import numpy as np
import random
import time
from scipy.interpolate import griddata


# In[2]:


reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('Isabel_3D.vti')
reader.Update()
data=reader.GetOutput()


# In[3]:


total_values=data.GetPointData().GetScalars()
total_points = np.array([data.GetPoint(i) for i in range(data.GetNumberOfPoints())])
original_dim=data.GetDimensions()


# In[4]:


def srs_sampling(file_name, sampling_percentage, output_file):
    # create a reader for the vti file
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_name)
    reader.Update()

    # get the dimensions of the data set
    dims = reader.GetOutput().GetDimensions()
    
    # create a set to store the sampled points
    samples = set()
    
    # add the eight corner points to the set of sampled points
    corner_points = [(0, 0, 0), (dims[0]-1, 0, 0), (0, dims[1]-1, 0), (dims[0]-1, dims[1]-1, 0),
                     (0, 0, dims[2]-1), (dims[0]-1, 0, dims[2]-1), (0, dims[1]-1, dims[2]-1), (dims[0]-1, dims[1]-1, dims[2]-1)]
    samples.update(corner_points)
    
    # calculate the total number of points in the data set
    total_points = dims[0] * dims[1] * dims[2]

    # calculate the number of points to sample
    num_samples = int(sampling_percentage / 100 * total_points)
    
    # sample random points from the data set
    while len(samples) < num_samples:
        i = random.randint(0, dims[0]-1)
        j = random.randint(0, dims[1]-1)
        k = random.randint(0, dims[2]-1)
        samples.add((i, j, k))
    
    # create a vtkPoints object to store the sampled points
    points = vtk.vtkPoints()
    data_values = vtk.vtkIntArray()
    data_values.SetName("DataValues")
    for sample in samples:
        point_data = reader.GetOutput().GetPointData().GetScalars().GetTuple(sample[0] + sample[1]*dims[0] + sample[2]*dims[0]*dims[1])
        points.InsertNextPoint(sample)
        data_values.InsertNextTuple1(point_data[0])

    # create a vtkPolyData object to store the sampled points
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.GetPointData().AddArray(data_values)

    # write the vtkPolyData to a file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)
    writer.SetInputData(polydata)
    writer.Write()
    
    
    sampled_points = np.array([points.GetPoint(i) for i in range(points.GetNumberOfPoints())])

        
    return sampled_points,data_values


# In[5]:


def COMPUTE_SNR(arrgt,arr_recon):
    diff=arrgt-arr_recon
    sqd_max_diff=(np.max(arrgt)-np.min(arrgt))**2
    snr=10*np.log10(sqd_max_diff/np.mean(diff**2))
    return snr


# In[6]:


def reconstruct_volume(method,sampled_points,data_values,total_points):
    if method == 'nearest':
        start_time = time.time()
        interp = griddata(sampled_points, data_values, total_points, method='nearest')
        end_time = time.time()
        time_taken = end_time - start_time
        print("SNR for nearest:",COMPUTE_SNR(total_values,interp))
        print(f"Time taken for reconstruction for {sampling_percentage}%:", time_taken)
        
        
    elif method == 'linear':
        start_time = time.time()
        interp = griddata(sampled_points, data_values, total_points, method='linear')
        end_time = time.time()
        time_taken = end_time - start_time
        print("SNR for linear:",COMPUTE_SNR(total_values,interp))
        print(f"Time taken for reconstruction for {sampling_percentage}%:", time_taken)    
        
    # Create a vtkImageData object and set its dimensions, origin, and spacing
    imageData = vtk.vtkImageData()
    imageData.SetDimensions(original_dim)
    imageData.SetOrigin(0, 0, 0)
    imageData.SetSpacing(1, 1, 1)
    
    # create vtkDoubleArray 
    voxelValues = vtk.vtkDoubleArray()
    voxelValues.SetNumberOfComponents(1)
    
    for point in interp:
        voxelValues.InsertNextValue(point) 
        
    # set voxel values in vtkImageData object
    imageData.GetPointData().SetScalars(voxelValues)
    
    # write to file
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName('reconstructed_volume.vti')
    writer.SetInputData(imageData)
    writer.Write()


# In[7]:


sampling_percentage=int(input('Enter the sampling percentage %:'))
method = input("Enter the method for reconstruction:")
sampled_points,data_values = srs_sampling('Isabel_3D.vti', sampling_percentage,'output.vtp')
reconstruct_volume(method,sampled_points,data_values,total_points)


# In[ ]:




