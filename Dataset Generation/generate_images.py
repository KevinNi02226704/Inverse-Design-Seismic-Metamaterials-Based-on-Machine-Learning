import numpy as np
from PIL import Image
import xlsxwriter


def get_position():
    p1 = [np.random.choice(np.arange(5, 24), 1)[0]]  
    prob = np.array([0.1, 0.8, 0.1])
    while True:
        p1.append(np.random.choice([p1[-1]-1, p1[-1], np.minimum(p1[-1]+1, 20)], 1, p=prob)[0])
        if p1[-1] == p1[-2]-1:
            prob = np.array([0.8, 0.1, 0.1])
        elif p1[-1] == p1[-2]+1:
            prob = np.array([0.1, 0.1, 0.8])
        else:
            prob = np.array([0.1, 0.8, 0.1])
        if p1[-1] < len(p1):
            del p1[-1]
            while True:
                if p1[-1]-p1[-2] == 1:
                    del p1[-1]
                else:
                    break
            break
    return p1


def calculate_filling_fraction(p1):
    fr1 = 0
    for i in range(len(p1)):
        fr1 +=(p1[i]-i)*2-1
    fr1 = fr1/(25*25)
    return fr1


def generate_image(p1, num):
    im = np.zeros((25, 25))
    for i in range(len(p1)):
        for j in range(i, p1[i]):
            im[i, j] = 1
            im[j, i] = 1
    im = np.concatenate([np.rot90(im, -1), im], axis=1)
    im = np.concatenate([np.rot90(im, 2), im], axis=0)
    book = xlsxwriter.Workbook('images/excel/'+str(num)+'.xlsx')
    sheet1 = book.add_worksheet('images')
    sheet2 = book.add_worksheet('image_parameters')
    for i in range(50):
        for j in range(50):
            sheet1.write(i, j, im[i, j])
    for i in range(len(p1)):
        sheet2.write(0, i, p1[i])
    book.close()
    im = (1-im)*255
    im = Image.fromarray(im)
    im = im.convert('L')
    im.save('images/figure/'+str(num)+'.jpg')


end = 10
k = 0
print('start')
while True:
    p1 = get_position()
    fr1 = calculate_filling_fraction(p1)
    if fr1 < 0.3 or fr1 > 0.65:
        pass
    else:
        im = generate_image(p1, k)
        print(k)
        k += 1
    if k == end:
        break

np.sqrt(54)