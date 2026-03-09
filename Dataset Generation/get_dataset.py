import numpy as np
import openpyxl, xlsxwriter, csv

def load_features(name):
    book = openpyxl.load_workbook(name)
    sheet1 = book['images']
    sheet2 = book['soil_parameters']
    m, n1, n2 = sheet1.max_row, sheet1.max_column, sheet2.max_column
    im = np.zeros((m, n1))
    sp = np.zeros((m, n2))
    for i in range(m):
        for j in range(n1):
            im[i, j] = sheet1.cell(row=i+1, column=j+1).value
        for j in range(n2):
            sp[i, j] = sheet2.cell(row=i+1, column=j+1).value
    return im, sp

def load_bandgaps(name):
    with open(name, 'r', encoding='UTF-8') as f:
        data = csv.reader(f)
        rows = [row for row in data]
        rows = rows[8:]
        for j in range(len(rows)):
            rows[j] = float(rows[j][1])
        curve = np.zeros((6, 31))
        for i in range(6):
            curve[i, :] = rows[i*31:(i+1)*31]
    bg = np.zeros(2)
    bg[0] = np.max(curve[2, :])
    bg[1] = np.min(curve[3, :])
    return bg

def get_all_data(list_number, n_excel):
    im_all = np.zeros((len(list_number)*n_excel, 50*50))
    sp_all = np.zeros((len(list_number)*n_excel, 3))
    bg_all = np.zeros((len(list_number)*n_excel, 2))
    for i in range(len(list_number)):
        print(i)
        im, sp = load_features('integrated_images/'+str(list_number[i])+'.xlsx')
        bg = np.zeros((sp.shape[0], 2))
        for j in range(bg.shape[0]):
            bg_t = load_bandgaps('dispersion_curves/'+str(list_number[i]*n_excel+j+1)+'.csv')
            bg[j] = bg_t
        im_all[i*n_excel:(i+1)*n_excel] = im
        sp_all[i*n_excel:(i+1)*n_excel] = sp
        bg_all[i*n_excel:(i+1)*n_excel] = bg
    return im_all, sp_all, bg_all

def save_data(im, sp, bg, filename):
    book = xlsxwriter.Workbook(filename)
    sheet1 = book.add_worksheet('images')
    sheet2 = book.add_worksheet('soil_parameters')
    sheet3 = book.add_worksheet('bandgaps')
    m, n1, n2, n3 = im.shape[0], im.shape[1], sp.shape[1], bg.shape[1]
    for i in range(m):
        for j in range(n1):
            sheet1.write(i, j, im[i, j])
        for j in range(n2):
            sheet2.write(i, j, sp[i, j])
        for j in range(n3):
            sheet3.write(i, j, bg[i, j])
    book.close()

list_number = [0]
n_excel = 2
im, sp, bg = get_all_data(list_number, n_excel)
save_data(im, sp, bg, 'dataset_for_topology.xlsx')