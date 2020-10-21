import numpy as np
from matplotlib import pyplot as plt

extend_width = 4.6

half_extend_width = extend_width / 2

# Test case
half_pi = np.pi / 2
quarter_pi = np.pi / 4

o_contour_x = np.array([-half_extend_width, half_extend_width, half_extend_width, -half_extend_width, -half_extend_width], dtype=np.float)
o_contour_y = np.array([-half_extend_width, -half_extend_width, half_extend_width, half_extend_width, -half_extend_width], dtype=np.float)

# x larger than y
x1 = 9
y1 = 7

x2 = -x1
y2 = -y1

x3 = x1
y3 = -y1

x4 = -x1
y4 = y1

# y larger than x
x5 = 5
y5 = 8

x6 = -x5
y6 = -y5

x7 = x5
y7 = -y5

x8 = -x5
y8 = y5

# x equal to y

x9 = 15
y9 = 15

x10 = -x9
y10 = -y9

x11 = x9
y11 = -y9

x12 = -x9
y12 = y9

# x or y equal to 0

x13 = 0
y13 = 3

x14 = y13
y14 = x13

x15 = -y13
y15 = x13

x16 = x13
y16 = -y13

def get_possible_contour(bcx, bcy):
    if np.abs(bcx) > np.abs(bcy):
        k = bcy / bcx

        if bcx > 0:
            ex = bcx - half_extend_width

            shift_x = half_extend_width
        else:
            ex = bcx + half_extend_width
            shift_x = -half_extend_width

        ey = ex * k
        shift_y = half_extend_width
        res_x = 0
        res_y = half_extend_width - (bcy - ey)

    else:
        k = bcx / bcy

        if bcy > 0:
            ey = bcy - half_extend_width
            shift_y = half_extend_width
        else:
            ey = bcy + half_extend_width
            shift_y = -half_extend_width
        ex = ey * k
        shift_x = half_extend_width
        res_x = half_extend_width - (bcx - ex)
        res_y = 0

    contour_x = o_contour_x + bcx + shift_x - res_x
    contour_y = o_contour_y + bcy + shift_y - res_y

    out_x = ex + shift_x - res_x
    out_y = ey + shift_y - res_y

    center_x = np.sum(contour_x[0:4]) / 4
    center_y = np.sum(contour_y[0:4]) / 4
    o_line_x = [0, out_x]
    o_line_y = [0, out_y]
    check_x = [out_x, center_x]
    check_y = [out_y, center_y]

    return contour_x, contour_y, o_line_x, o_line_y, check_x, check_y, ex, ey
'''
k1 = y1 / x1

ex1 = x1 - half_extend_width

ey1 = ex1 * k1

shift_x = half_extend_width
shift_y = half_extend_width
res_y = half_extend_width - (y1 - ey1)

contour_x = o_contour_x + x1 + half_extend_width
contour_y = o_contour_y + y1 + half_extend_width - res_y

out_x = ex1 + shift_x
out_y = ey1 + shift_y - res_y

center_x = np.sum(contour_x[0:4]) / 4
center_y = np.sum(contour_y[0:4]) / 4
o_line_x = [0, out_x]
o_line_y = [0, out_y]
check_x = [out_x, center_x]
check_y = [out_y, center_y]

'''
def test_case():
    text_x = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16]
    text_y = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16]

    c_x = []
    c_y = []
    o_x = []
    o_y = []
    k_x = []
    k_y = []
    e_x = []
    e_y = []
    for i in range(len(text_x)):
        t1, t2, t3, t4, t5, t6, t7, t8 = get_possible_contour(text_x[i], text_y[i])
        c_x.append(t1)
        c_y.append(t2)
        o_x.append(t3)
        o_y.append(t4)
        k_x.append(t5)
        k_y.append(t6)
        e_x.append(t7)
        e_y.append(t8)


    # contour_x, contour_y, o_line_x, o_line_y, check_x, check_y, ex1, ey1 = get_possible_contour(x6, y6)
    plt.figure(figsize=(12, 12))
    plt.axis([-20, 20, -20, 20])
    for i in range(len(c_x)):
        plt.plot(c_x[i], c_y[i])
        plt.plot(o_x[i], o_y[i])
        # plt.plot(k_x[i], k_y[i])
        # print('x: ', out_x, ',y: ', out_y, 'res: ', res_y)
        plt.plot(text_x[i], text_y[i], 'r*')
        # plt.plot(e_x[i], e_y[i], 'g*')
    plt.show()

test_case()

'''
tx = -1.89
ty = 1.93
plt.figure(figsize=(12, 12))
plt.axis([-20, 20, -20, 20])
t1, t2, t3, t4, t5, t6, t7, t8 = get_possible_contour(tx, ty)
plt.plot(t1, t2)
plt.plot(t3, t4)
# plt.plot(k_x[i], k_y[i])
# print('x: ', out_x, ',y: ', out_y, 'res: ', res_y)
plt.plot(tx, ty, 'r*')
# plt.plot(e_x[i], e_y[i], 'g*')
plt.show()
'''