import numpy as np
from numpy import log as ln
import math
import matplotlib.pyplot as plt

#import pylab
N = 5 ##число нейтронов
x = [0] * N ##начальнаяя координата
y = [0] * N
z = [0] * N
c = 0
n_pass = 0
L = 80 ##толщина пластины
cells = 1000 ##счетчик прошедших нейтронов
delta_r = L / cells
n = [0] * cells ##число ячеек и нейтроннов попавших в ячейку
q = [0] * N

i = 0
k = 0
j = 0

sigma = 5e-02

Vx = [2000] * N
Vy = [2000] * N
Vz = [2000] * N
V = [2000] * N ## модуль скорости
## скорости ЦМ
Vcx = [0] * N
Vcy = [0] * N
Vcz = [0] * N
## скорости рассеяных нейтронов 
Vx_s = [0] * N
Vy_s = [0] * N
Vz_s = [0] * N
r = [0] * N
##t = [0] * N
kT = 0.025 
m = 1
Vnucl = ((kT/m)**0.5)*(-2*ln(np.random.random())) 
# while i < N  :
    
#     #lymbda = - ln(1 - np.random.random()) / sigma

#     #x = lymbda
    
for s in range(4):
    # print(s)
    # x = lymbda * costeta
    # y = lymbda * math.sin(math.acos(costeta)) * math.sin(fi)
    # z = lymbda * math.sin(math.acos(costeta)) * math.cos(fi)
    while k < N:
        lymbda = - ln(np.random.random()) / sigma
        costeta = 2 * np.random.random() - 1
        fi = 2 * math.pi * np.random.random()
        ##costeta = 2 * np.random.random() - 1
        # print(costeta)
        # print(math.acos(costeta))
        # print(math.sin(math.acos(costeta))
        ##Скорости в L до рассеяния
        Vx[k] = Vx[k] * costeta
        Vy[k] = Vy[k] * math.sin(math.acos(costeta)) * math.sin(fi) ## sinteta=sin(acos(costeta))
        Vz[k] = Vz[k] * math.sin(math.acos(costeta)) * math.cos(fi)
        
        
        ##углы для ядра
        costeta_nucl = 2 * np.random.random() - 1
        fi_nucl = 2 * math.pi * np.random.random()
        
        ##скорость ядра
        Vnuclx = Vnucl * costeta_nucl
        Vnucly = Vnucl * math.sin(math.acos(costeta_nucl)) * math.sin(fi_nucl)
        Vnuclz = Vnucl * math.sin(math.acos(costeta_nucl)) * math.cos(fi_nucl)
        
        ##скорость Ци
        Vcx[:] = [(i + (Vx[k] + Vnuclx)) / 2 for i in Vcx] 
        Vcy[:] = [(i + (Vy[k] + Vnucly)) / 2 for i in Vcy]
        Vcz[:] = [(i + (Vz[k] + Vnuclz)) / 2 for i in Vcz]
        
        ## уголы рассеяния нейтрона в ЦМ
        cospsi = 2 * np.random.random() - 1 ## угол рассеяния в ЦМ
        psi = 2 * math.pi * np.random.random()
        
        ##скорость рассеяного нейтрона в ЦМ
        
        Vx_s = [(i + (Vx[k] - Vnuclx)) / 2 * cospsi for i in Vcx] 
        Vy_s = [(i + (Vy[k] - Vnucly)) / 2 * math.sin(math.acos(cospsi)) * math.sin(psi) for i in Vcy]
        Vz_s = [(i + (Vz[k] - Vnuclz)) / 2 * math.sin(math.acos(cospsi)) * math.cos(psi) for i in Vcz]
      
        ##скорость рассеяного нейтрона в L
        Vx[k] = Vx_s[k] + Vcx[k]
        Vy[k] = Vy_s[k] + Vcy[k]
        Vz[k] = Vz_s[k] + Vcz[k]
        ## Vx[k] = (Vx[k] * (1 + cospsi) + Vnucl * (1 - cospsi))/2
        
        V[k] = (Vx[k]**2 + Vy[k]**2 + Vz[k]**2)**0.5
        
        x[k] += (Vx[k] / V[k]) * lymbda
        y[k] += (Vy[k] / V[k]) * lymbda
        z[k] += (Vz[k] / V[k]) * lymbda
        r[k] = (x[k]**2 + y[k]**2 + z[k]**2)**0.5
        q[k] = math.floor(r[k] / delta_r)       
        # while j == k:
        #     t[j] = t[j] + lymbda / V[k]
        #     j += 1
        #t[k] =  r[k] / V[k]
        print(r[k]/V[k])

        import plotly.io as io
        import plotly.graph_objs as go
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=[x[0]], y=[y[0]],z=[z[0]], mode='markers',  name='f(x)=x<sup>2</sup>'))

        frames=[]
        for i in range(1, len(x)):
            frames.append(go.Frame(data=[go.Scatter3d(x=x[:i+1], y=y[:i+1], z=z[:i+1])]))

        fig.frames = frames   

        fig.update_layout(legend_orientation="h",
                          legend=dict(x=0, xanchor="center"),
                          updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None])])],
                          margin=dict(l=0, r=0, t=0, b=0))
        fig.update_traces(hoverinfo="all", hovertemplate="Аргумент: %{x}<br>Функция: %{y}")
        io.renderers.default='browser'
        fig.show()
        k += 1 
# while c < len(q):
#     if q[c] < cells:
#         n[q[c]] = n[q[c]] + 1
#         c += 1
#     else :
#         c += 1
#         n_pass += 1

    
     
        ##print("x2 =", x)
    #     if x < 0:
    #        # print('??????????????????????')
    #         break
    # if x > L:
    #     n += 1
    # i += 1

#print(Vnuclx)
#print(Vcx)
#print(Vx_s)
# print('r = ',r)
# print('delta_r = ', delta_r)
# print('q = ', q)
# print('n = ', n)
# print('прошедших нейтронов:', n_pass)
# # print(V)
# print(x)
# print(y)
# print(z)

# ##3D
# fig = plt.figure(1, [12.8, 9.6])
# ax = fig.add_axes(rect = (0, 0.00, 1, 1), projection='3d')
# ax.scatter(x, y, z)

# plt.show()
