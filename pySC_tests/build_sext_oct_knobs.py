from pySC import ResponseMatrix
import json
import numpy as np
import matplotlib.pyplot as plt


sexm = json.load(open('sextupole_matrix.json','r'))['sextupole_responses']
octm = json.load(open('octupole_matrix.json','r'))['octupole_responses']

sRM = ResponseMatrix(matrix=np.array(sexm))
oRM = ResponseMatrix(matrix=np.array(octm))

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.plot(sRM.singular_values/sRM.singular_values[0], 'bo')
ax.plot(oRM.singular_values/oRM.singular_values[0], 'ro')
ax.set_yscale('log')

isRM = sRM.build_pseudoinverse(method='svd_values', parameter=8, zerosum=False)
ioRM = oRM.build_pseudoinverse(method='svd_values', parameter=6, zerosum=False)
# ioRM = sRM.build_pseudoinverse(method='tikhonov', parameter=20, zerosum=False)

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.plot(isRM.matrix.T)
ax2.set_yscale('log')
print(np.max(np.abs(isRM.matrix), axis=1))

fig3 = plt.figure(3)
ax3 = fig3.add_subplot(121)
ax4 = fig3.add_subplot(122)
ax3.plot(ioRM.matrix.T)
ax4.plot(np.max(np.abs(ioRM.matrix), axis=1),'o')
ax4.plot(np.std(ioRM.matrix, axis=1), 'o')
ax3.set_yscale('log')
ax4.set_yscale('log')

print(np.max(np.abs(ioRM.matrix), axis=1))


max_str = 0.1
# oct_fields = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
sext_fields = [           4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
oct_fields = [      2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

sext_knobs = np.zeros([len(sext_fields), isRM.matrix.shape[1]])
for jj, ii in enumerate(sext_fields):
    sext_knobs[jj] = isRM.matrix[ii] / np.max(np.abs(isRM.matrix[ii])) * max_str

oct_knobs = np.zeros([len(oct_fields), ioRM.matrix.shape[1]])
for jj, ii in enumerate(oct_fields):
    oct_knobs[jj] = ioRM.matrix[ii] / np.max(np.abs(ioRM.matrix[ii])) * max_str

fig4 = plt.figure(4)
ax5 = fig4.add_subplot(121)
ax6 = fig4.add_subplot(122)
ax5.pcolormesh(sext_knobs)
ax6.pcolormesh(oct_knobs)

import csv
with open('kostas_sextupoles.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(sext_knobs)
with open('kostas_octupoles.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(oct_knobs)
plt.show()