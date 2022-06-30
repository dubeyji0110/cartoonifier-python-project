# required imports
import matplotlib.pyplot as plt
import tkinter as tk
import easygui
import sys
import cv2
import os

from tkinter import *

# creating main window
window = Tk()
window.geometry('400x400')
window.title('Cartoonify your Image')
window.configure(background='white')
label = Label(window, background='#cdcdcd', font=('calibri', 20, 'bold'))


# getting image path
def getImage():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):
    originalImage = cv2.imread(ImagePath)
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
    # print(originalImage)

    # if image is not found
    if originalImage is None:
        print('Cannot find any image at given path')
        sys.exit()

    ReSizedImage1 = cv2.resize(originalImage, (960, 960))

    # converting image to grayscale
    grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    ReSizedImage2 = cv2.resize(grayScaleImage, (960, 960))

    # smoothning of grayscale image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSizedImage3 = cv2.resize(smoothGrayScale, (960, 960))

    # highlighting the outlines of the image
    getEdge = cv2.adaptiveThreshold(
        smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    ReSizedImage4 = cv2.resize(getEdge, (960, 960))

    # applying filter on original image
    colorImage = cv2.bilateralFilter(originalImage, 9, 300, 300)
    ReSizedImage5 = cv2.resize(colorImage, (960, 960))

    # merging originalImage with outlinedImage
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSizedImage6 = cv2.resize(cartoonImage, (960, 960))

    images = [ReSizedImage1, ReSizedImage2, ReSizedImage3,
              ReSizedImage4, ReSizedImage5, ReSizedImage6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={
                             'xticks': [], 'yticks': []}, gridspec_kw=dict(hspace=0.1, wspace=0.1))

    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    # creating save button
    saveBtn = Button(window, text='Save Image',
                     command=lambda: saveImage(ImagePath=ImagePath, ReSizedImage6=ReSizedImage6))
    saveBtn.configure(background='#364156', foreground='white',
                      font=('calibri', 10, 'bold'))
    saveBtn.pack(side=TOP, pady=50)

    plt.show()


# saving the cartoonified image
def saveImage(ReSizedImage6, ImagePath):
    newName = 'cartoonified_Image'
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSizedImage6, cv2.COLOR_RGB2BGR))
    msg = "Image saved by name " + newName + " at " + path
    tk.messagebox.showinfo(title=None, message=msg)


# creating upload button
uploadBtn = Button(window, text='Cartoonify an Image',
                   command=getImage, padx=10, pady=5)
uploadBtn.configure(background='#364156', foreground='white',
                    font=('calibri', 10, 'bold'))
uploadBtn.pack(side=TOP, pady=50)


if __name__ == "__main__":
    window.mainloop()
