from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import os

wb = load_workbook('DataFrame.xlsx')
ws = wb['database']

def download_img(url,file_name):
    res = requests.get(url)
    img = open(file_name, 'wb')
    img.write(res.content)
    img.close()

def insert_img(file_name,cell):
    img = Image(file_name)
    img.width,img.height=72,72
    ws.add_image(img, cell)

def remove_img(img_name):
    try:
        os.remove(img_name)
    except:
        print('file not found: ', img_name)
# check if file exists or not
    #if os.path.exists(img_name) is False:
        # file did not exists
        #return True

for i in range(2,len(images_url)+2):
    name = ws['B'+str(i)].value.split('/')[3].split('.')[0]
    print('name:',name)
    url = ws['B'+str(i)].value
    print('url:', url)
    download_img(url,name)
    ws['B'+str(i)]=""
    ws.row_dimensions[i].height=80
    insert_img(name,'B'+str(i))

""" worksheet = wb.getWorksheets().get(0)
cells = worksheet.getCells()
cells.setColumnWidth(1, 40)
cells.setColumnWidth(2, 80)
cells.setColumnWidth(1, 80)
cells.setColumnWidth(1, 80) """
#os.remove(file) for filename in os.listdir('/') if file.startswith('D_NQ_NP')
wb.save('output.xlsx') 

wb = load_workbook('DataFrame.xlsx')
ws = wb['database']


for i in range(2,len(images_url)+2):
    name = ws['B'+str(i)].value.split('/')[3].split('.')[0]
    remove_img(name)