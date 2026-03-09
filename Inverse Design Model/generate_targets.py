import numpy as np
import xlsxwriter
np.random.seed(1)


m = 10

E = np.random.uniform(3, 990, m).reshape(-1, 1)
P = np.random.uniform(0.15, 0.45, m).reshape(-1, 1)
rho = np.random.uniform(1.5, 2.2, m).reshape(-1, 1)
soil = np.concatenate([E, P, rho], axis=1)

bg = np.zeros((m, 2))
bg_L = np.round(np.random.uniform(20, 80, m), 2)
bg_U = np.round(bg_L+np.random.uniform(10, 20, m), 2)
bg[:, 0], bg[:, 1] = bg_L, bg_U

book = xlsxwriter.Workbook('targets.xlsx')
sheet1 = book.add_worksheet('targeted_bandgaps')
sheet2 = book.add_worksheet('soil_parameters')
for i in range(m):
    for j in range(2):
        sheet1.write(i, j, bg[i, j])
    for j in range(3):
        sheet2.write(i, j, soil[i, j])
book.close()