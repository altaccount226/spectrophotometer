import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

SHIFT = 100
PADDING = 0
THRESHOLD = 2

#Take given image, average all its pixels on vertical axies, and save to .csv
def process_image(filename):

    #Read and average all pixel columns in image
    img = cv2.imread(os.path.join(os.getcwd(), 'pics', filename), 0)
    avg = img.mean(axis=0)
    pxl = np.linspace(0, len(avg), num=640)

    #Save the data to a .csv file in the format ImageJ saves it
    data = np.array(list(zip(pxl, avg)))
    df = pd.DataFrame(data, columns=['Distance_(pixels)','Gray_Value'])
    df.to_csv(os.path.join(os.getcwd(), 'data', filename[:-4] + '.csv'))
    
    print("Processed " + filename + " and dumped data in data/" + filename[:-4] + '.csv')

#Open .csv file, obtain callibrated .csv data, and plot the data
def set_plot(filename):
    df = pd.read_csv(os.path.join(os.getcwd(), 'data', filename + '.csv'))
    intensity, wavelength = align_to_callibration(df['Gray_Value'])

    plt.plot(wavelength, intensity, label=filename)
    #df.plot(kind='line',x='Distance_(pixels)',y='Gray_Value')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.grid(visible=True)

#Unused
def set_subplot(filenames):
    for i in range(len(filenames)):
        plt.subplot(4, int(len(filenames) / 4 + 1), i + 1)
        set_plot(filenames[i])

#Open the callibration data file, transform the data, and return the x & y axes
def align_to_callibration(avg):
    #Obtain callibration data
    with open("callibration.dat", "r") as cal:
        x1 = int(cal.readline())
        x2 = int(cal.readline())

    avg = avg[SHIFT:]
    #Read and average all pixel columns in
    avg = avg[x1:x2]
    wavelength = np.linspace(390, 700, num=len(avg))

    return (avg, wavelength)

#Take a chosen file and set the callibration config aligned to that data (will erase old callibration data)
def callibrate(filename):

    img = cv2.imread(os.path.join(os.getcwd(), 'pics', filename + '.png'), 0)
    avg = img.mean(axis=0)
    avg = avg[SHIFT:]
    where = np.where(avg > THRESHOLD)

    #print(('Callibrated x1 and x2 to: %d and %d') % {int(where[0][0]), int(where[0][-1])})
    with open('callibration.dat', 'w') as cal:
        cal.write(str(where[0][0] - PADDING) + '\n' + str(where[0][-1] + PADDING))

#Delete all files in pics/ & data/ or delete specified pair of files
def delete(filename):
    if filename == '-1':
        x = input('Are you sure you want to delete all images? [y/n] ')
        if x != 'y':
            print("Aborting deletion!")
            return
        pics = os.path.join(os.getcwd(), 'pics')
        data = os.path.join(os.getcwd(), 'data')
        for f in os.listdir(pics):
            if f[-4:] == '.png':
                os.remove(os.path.join(pics, f))
        for f in os.listdir(data):
            if f[-4:] == '.csv':
                os.remove(os.path.join(data, f))
    else:
        x = input('Are you sure you want to delete image ' + filename + '? [y/n] ')
        if x != 'y':
            print("Aborting deletion!")
            return
        os.remove(os.path.join(os.getcwd(), 'pics', filename + '.png'))
        os.remove(os.path.join(os.getcwd(), 'data', filename + '.csv'))