from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_qt5 as backend



def decoration(ax):
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.5)   
    ax.tick_params(which = "major", labelsize = 11, length = 5, width = 1.5,
                    direction = 'in', grid_linestyle = "dashed", grid_linewidth = 0.5)
    ax.tick_params(which = "minor", labelsize = 10, length = 4, width = 1,
                    direction = 'in')
    ax.grid()
    ax.minorticks_on()

class MplToolbar(NavigationToolbar2QT):
    def __init__(self, canvas_, parent_):
        self.toolitems = [t for t in NavigationToolbar2QT.toolitems if
            t[0] in ('Home', None, 'Pan', 'Zoom', 'Subplots', 'Save')]
        NavigationToolbar2QT.__init__(self, canvas_, parent_)

def decorate_REF(ax1, ax2, lns):
    for axis in ['top','bottom','left','right']:
        ax2.spines[axis].set_linewidth(1.5)   
    ax2.spines['left'].set_color("#0040ff")
    ax2.spines['right'].set_color("#47d147")
    ax1.tick_params('y', colors= "#0040ff")
    ax2.tick_params('y', colors= "#47d147")
    for ax in [ax1, ax2]:
        ax.tick_params(which = "major", labelsize = 11, length = 5, width = 1.5,
                        direction = 'in', grid_linestyle = "dashed", grid_linewidth = 0.5)
        ax.tick_params(which = "minor", labelsize = 10, length = 4, width = 1,
                        direction = 'in')
        
    # plt.xticks([1, 2, 3], ['mon', 'tue', 'wed'])
    
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, fontsize = 8, edgecolor  = 'k',loc = 1, frameon = True, handlelength = 0.7)
    ax1.set_xlabel("Incidence Angle (°)",fontsize= 12, fontname = "Arial", weight = 'semibold')
    ax1.set_ylabel("Reflectivity",fontsize= 12, fontname = "Arial", weight = 'semibold')
    ax2.set_ylabel("Phase(" + r"$\pi$)",fontsize= 12, fontname = "Arial", weight = 'semibold')
    ax1.grid()
    # ax1.minorticks_on()


# case = 3 exp and simu
# case = 2 simu
# case = 1 exp only

def plotREFs(convas, x, phase, ref, exp_ref, case):
    ax1 = convas.figure.subplots()
    if(case != 1):
        if(case == 3):
            ln3 = ax1.plot(exp_ref[0], exp_ref[1], label = "Exp. Ref.", color = "#000080", linewidth = 1.5)
        ln1 = ax1.plot(x, ref, label = "Simu. Ref.", color = "#0040ff", linewidth = 1.5)  
        ax2 = ax1.twinx()
        ln2 = ax2.plot(x, phase, label = "Simu. Phase", color = "#47d147", linewidth = 1.5)
        lns = ln1 + ln2
        if(case == 3):
            lns = lns + ln3
        decorate_REF(ax1, ax2, lns)
        ax2.set_ylim(-0.05, 1.05*phase.max())
        # ax2.set_yticks([0, 0.5, 1])
        # ax2.set_yticklabels(["0", " ", r"$\pi$"])
        ax1.set_xlim(x.min(), x.max())
        refRange = ref.max() - ref.min()
        ax1.set_ylim(ref.min() - 0.05*refRange , ref.max() + 0.05* refRange)
    else:   
        ax1.plot(exp_ref[0], exp_ref[1], label = "Exp. Ref.", color = "#000080", linewidth = 1.5)
        ax1.legend(fontsize = 8, edgecolor  = 'k',loc = (0.7, 0.8), frameon = True, handlelength = 0.7)
        ax1.set_xlabel("Incidence Angle (°)",fontsize= 12, fontname = "Arial", weight = 'semibold')
        ax1.set_ylabel("Reflectivity",fontsize= 12, fontname = "Arial", weight = 'semibold')
        ax1.set_xlim(exp_ref[0].min(), exp_ref[0].max())
        decoration(ax1)
    ax1.minorticks_on()
    convas.figure.subplots_adjust(left = 0.18, bottom = 0.2, top = 0.97, right = 0.83)
    convas.draw()

# case = 3 exp and simu
# case = 2 simu
# case = 1 exp only

def plotRCs(convas, x, name_list, simu_RCs, nor_factor, exp_RCs, case):

    colors = ["#9400D3", "#32CD32", "#FF0000","#0000CD", "#FFA500", "#FF69B4"]
    ax = convas.figure.subplots()
    if(case != 1):
        simu_RCs_min = 2
        simu_RCs_max = -1
        for i, item in enumerate(simu_RCs):
            ax.plot(x, item/nor_factor[i], label = "Simu_" + name_list[i], color = colors[i%6], linewidth = 1.5)
            if((item/nor_factor[i]).max() > simu_RCs_max):
                simu_RCs_max = (item/nor_factor[i]).max()

            if((item/nor_factor[i]).min() < simu_RCs_min):
                simu_RCs_min = (item/nor_factor[i]).min()

        if(case == 3):
            for i in range(1, len(exp_RCs)):
                ax.plot(exp_RCs[0], exp_RCs[i], label = "EXP_line%d" %i, color = colors[np.absolute(6 - i)], linewidth = 1.5)
        ax.set_xlim(x.min(), x.max())    
        ax.set_ylim(0.98* simu_RCs_min, 1.03* simu_RCs_max)    
    else:
        for i in range(1, len(exp_RCs)):
            ax.plot(exp_RCs[0], exp_RCs[i], label = "EXP_line%d" %i, color = colors[np.absolute(6 - i)], linewidth = 1.5)
        ax.set_xlim(exp_RCs[0].min(), exp_RCs[0].max())
    ax.legend(fontsize = 7, edgecolor  = 'k', loc= 2, bbox_to_anchor=(1.01, 1.02), frameon = True, handlelength = 0.7)
    ax.set_xlabel("Incidence Angle (°)",fontsize= 12, fontname = "Arial", weight = 'semibold')
    ax.set_ylabel("Yield",fontsize= 12, fontname = "Arial", weight = 'semibold')
    decoration(ax)  
    convas.figure.subplots_adjust(left = 0.18, bottom = 0.2, top = 0.97, right = 0.83)
    convas.draw()
 










