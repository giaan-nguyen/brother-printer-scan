#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:17:17 2020
@author: giaannguyen

This program is compatible with scans made by the printer model, Brother MFC-J430W.
Functions include:
    1) Obtaining BMP images from PDFs
    2) Darkening such BMP images
    3) Restoring BMP size after editing
    4) Compiling BMP (or any image format) files into a single PDF
    5) Compress PDFs if possible
"""
import PyPDF2, os, time, cv2
from PIL import Image
import numpy as np

def importfile(file_mode):
    import tkinter as tk
    from tkinter import filedialog
    # GUI
    root = tk.Tk()
    root.withdraw()
    if file_mode in [1,6]: files = filedialog.askopenfilename() # select one file
    else: files = filedialog.askopenfilenames() # select multiple files
    root.update()
    return files

def jpg_from_pdf(pdf_filename):
    pdf_file = open(pdf_filename, 'rb')
    cond_scan_reader = PyPDF2.PdfFileReader(pdf_file)
    jpg_files = []
    offset = 0
    while os.path.exists(os.getcwd() + "/Im" + str(offset) + ".bmp"): offset += 1
    for i in range(0, cond_scan_reader.getNumPages()):
        page = cond_scan_reader.getPage(i)
        xObject = page['/Resources']['/XObject'].getObject()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                if '/DCTDecode' in xObject[obj]['/Filter']:
                    data = xObject[obj]._data
                    jpg_str = "Im" + str(i + offset) # obj[1:]
                    img = open(jpg_str + ".jpg", "wb")
                    jpg_files.append(jpg_str + ".jpg")
                    img.write(data)
                    img.close()
                else: print('Error: no .jpg files were detected.')
            else: print('Error: no images were detected.')
    pdf_file.close()    
    return jpg_files

def jpg2bmp(jpg_filename):
    txt = jpg_filename.split('.')
    bmp_filename = txt[0] + ".bmp"
    Image.open(jpg_filename).save(bmp_filename)
    os.remove(jpg_filename)
    return bmp_filename

def newpdfname():
    nam_in = input("Would you like to name the new PDF file? (Y/N)\n")
    if nam_in in ['Y','y','Yes','yes']:
        str_file = input("Enter the filename:\n")
        newfile = str_file + '.pdf'
    else:
        from datetime import datetime
        dateTimeObj = datetime.now()
        mo = str(dateTimeObj.month).zfill(2); d = str(dateTimeObj.day).zfill(2); y = str(dateTimeObj.year)
        h = str(dateTimeObj.hour).zfill(2); mi = str(dateTimeObj.minute).zfill(2); s = str(dateTimeObj.second).zfill(2)
        newfile = 'PDF_' + mo + d + y + '_' + h + mi + s + '.pdf'
    return newfile

def images2pdf(images):
    imagelist = []
    for i in images:
        im = Image.open(i).convert('RGB')
        imagelist.append(im)
    firstpage = imagelist[0]
    rempages = imagelist[1:]
    
    newfile = newpdfname()
    firstpage.save(newfile, save_all=True, append_images=rempages)
    for i in images: os.remove(i)
    return newfile

def updatebmp(image, mode):
    im = Image.open(image).convert('RGB')
    imdata = np.asarray(im)
    
    if mode == 'dark':
        saturate_arr = np.ones_like(imdata) * 70
        imdata = cv2.subtract(imdata, saturate_arr) # cv2.subtract() performs saturation (i.e., min at 0)
        
        R,G,B = cv2.split(imdata)
        mask = (R < 150) & (G < 150) & (B < 150)
        thresh = mask.astype('uint8') * 70
        imdata[~mask] = [255, 255, 255]
        for layer in range(3): imdata[:,:,layer] = cv2.subtract(imdata[:,:,layer], thresh)
    
    saveimage = Image.fromarray(imdata)
    saveimage.save(image)
    return

def mergepdfs(pdf2merge):
    pdfWriter = PyPDF2.PdfFileWriter()
    for filename in pdf2merge:
        pdfFileObj = open(filename,'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)
    newfile = newpdfname()
    pdfOutput = open(newfile, 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()
    return

def main():
    ans_in = '0'; no_of_opts = 6
    while (type(ans_in) != int):
        ans_in = input(
        '''
        Please enter an integer: \n
        1) export BMPs from a PDF\n
        2) combine images to a PDF\n
        3) restore BMP size after image editing\n
        4) darken BMP images\n
        5) merge PDFs into a single PDF\n
        6) compress a PDF (if possible)\n
        '''
                )
        try: 
            c = int(ans_in)
        except ValueError: c = 0
        if c not in range(1, no_of_opts + 1): print("\nERROR: \nTo exit, press Ctrl+D. Otherwise continue.")
        else: ans_in = c
        
    file = importfile(ans_in)
    
    start_time = time.time()
    if ans_in in [1,6]:
        # EXPORT BMP FILES
        print("Exporting BMP files from PDF...\n")
        images = jpg_from_pdf(file)
        direc = file.split('/'); direc[len(direc)-1] = ''; direc = '/'.join(direc)
        bmpimages = []
        for i in images: 
            bmp_im = jpg2bmp(direc + i)
            bmpimages.append(bmp_im)
        print("Images exported.")
        if ans_in == 6: file = bmpimages
        
        # DARKEN BMP FILES
        if ans_in == 1:
            dark_in = input("Would you like to darken the images? (Y/N)\n")
            if dark_in in ['Y','y','Yes','yes']:
                print("Darkening BMP images...\n")
                start_time = time.time()
                for i in bmpimages: updatebmp(i,'dark')
                print("Images darkened.")
    if ans_in in [2,6]: 
        # COMBINE IMAGES
        print("Combining images...\n")
        images2pdf(file)
        print("PDF created.")
    if ans_in == 3:
        # FIX BMP SIZE
        print("Fixing BMP(s)...\n")
        for i in file: updatebmp(i,'none')
    if ans_in == 4: 
        print("Darkening BMP(s)...\n")
        for i in file: updatebmp(i,'dark')
    if ans_in == 5:
        # MERGE PDFs
        print("Merging pdfs...\n")
        mergepdfs(file)
        
    time_diff = round(time.time() - start_time, 4)
    print("Task completed. {} seconds elapsed.\n".format(time_diff))    
    if ans_in in [1,5]:
        # DELETE ORIG PDF FILE    
        del_in = input("Do you want to delete the original PDF file? (Y/N)\n")
        if del_in in ['Y','y','Yes','yes']: os.remove(file)

if __name__ == "__main__":
    main()
    user_termin = input("Task(s) completed. Press ENTER to exit the program.\n")
    quit()

