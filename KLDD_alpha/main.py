from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT)
import numpy as np
# for testing
import matplotlib.pyplot as plt
import copy
# self define function or class
from layout.layout import Ui_MainWindow

from layout.groupComboBox import CheckComboBox
from alert.alert import input_alert
from plots.plot import plotREFs, plotRCs, MplToolbar
from backEnd.backEnd_calc import calc_ref_phase, calc_RCs, process, cal_layer_distance
from backEnd.material_infor import crystal_infor
from layout.adjust_data import Adjust_Exp_Data
import csv

class MyQtApp(Ui_MainWindow):

    # initialize variables
    input_compelete = False
    adjust_exp_REF = [1, 0.00, 0.00]
    adjust_exp_RC = [1, 0.00, 0.00]

    aphase = 0

    exp_REF = np.array([0])
    exp_REF_origin = np.array([0])
    simu_phase = np.array([0])
    simu_REF = np.array([0])
    ref_range = np.array([0])

    exp_RC = np.array([0])
    exp_RC_origin = np.array([0])
    simu_RC_origin = np.array([0])
    simu_RC = []
    rc_range = np.array([0])
    atom_name_list = []
    rc_legend = []
    normal_factor = []
    material_info_file = ""
    
    #initialize test parameters
    def initialize_test_parameters(self):
        self.Bragg_h.setText("0")
        self.Bragg_k.setText("0")
        self.Bragg_l.setText("6")

        self.photon_energy.setText("3500")

        self.range_start.setText("-0.15")
        self.range_end.setText("0.15") 
        self.step_size.setText("0.001") 

        self.polar_angle.setText("36") 
        self.take_off_angle.setText("90") 

        self.DWF.setText("2.7")  
        self.sigma.setText("0.1") 

        self.IMFP_lineEdit.setText("20") 


    def __ini__(self):
        super(MyQtApp, self).__ini__()

    def updateFeatures(self):
        # adding two canvas for the simulaiton
        self.RC_canvas, self.RC_widget = self.addToolBar_figure(self.frame_4, ui.verticalLayout_2)
        self.REF_canvas, self.REF_widget = self.addToolBar_figure(self.frame_3, ui.verticalLayout)
        # adding three combobox for grouping output RCs
        self.group_CB = []
        self.group_lineEdit = [self.input_atom_1,
                               self.input_atom_2,
                               self.input_atom_3]
        for i in range(1,4):
            CB = CheckComboBox(placeholderText= "Mat_Info Empty")
            CB.setMaximumSize(QtCore.QSize(165, 26))
            self.gridLayout_3.addWidget(CB, i, 1, 1, 1)
            self.group_CB.append(CB)

    def addToolBar_figure(self, parent, parent_layout):
    	# adding tool bar
        figure = FigureCanvas(Figure(figsize=(5, 3), dpi = 100))
        TB_widget = QtWidgets.QWidget(parent)
        TB_widget.setMinimumSize(QtCore.QSize(350, 40))
        toolBar_RC = MplToolbar(figure, TB_widget)
        # adding canvas
        parent_layout.addWidget(TB_widget)
        FG_widget = QtWidgets.QWidget(parent)
        FG_widget.setMinimumSize(QtCore.QSize(350, 200))
        layout = QtWidgets.QVBoxLayout(FG_widget)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.addWidget(figure)
        parent_layout.addWidget(FG_widget)
        return figure, FG_widget

    def apply_input_const(self):
        self.lineEdit_input = [self.Bragg_h, self.Bragg_k, self.Bragg_l,
        self.photon_energy, self.range_start, self.range_end,
        self.step_size, self.polar_angle, self.take_off_angle,
        self.DWF, self.sigma, self.IMFP_lineEdit]
        ref_plane = QtGui.QIntValidator(-1 ,100)
        float_num = QtGui.QDoubleValidator()
      
        for i, item in enumerate(self.lineEdit_input):
            if(i <= 2):
                item.setValidator(ref_plane)
            else:
                item.setValidator(float_num)

    def check_valid_input(self):
        self.input_compelete = True
        for item in self.lineEdit_input:
            self.input_compelete = self.input_compelete and (item.text() != '')        
        # check the completeness of data for REF
        try:
            self.material_infor
        except:
            self.input_compelete = False
        if self.input_compelete:
            self.Brag_reflection = []
            self.angles = []
            self.GB = []
            for i, item in enumerate(self.lineEdit_input):
                if(i < 3):
                    self.Brag_reflection.append(int(item.text()))
                elif(i == 3):
                    self.hv = float(item.text())
                elif(i == 7 or i == 8):
                    self.angles.append(float(item.text()))
                elif(i == 9 or i == 10):
                    self.GB.append(float(item.text()))
            # make sure start_value < end_value    
            if(float(self.range_start.text()) < float(self.range_end.text()) ):
                start_value = float(self.range_start.text()) 
                end_value = float(self.range_end.text())  
            else: 
                start_value = float(self.range_end.text()) 
                end_value = float(self.range_start.text())
            self.range = [start_value, float(self.step_size.text()),end_value]
            self.IMFP = float(self.IMFP_lineEdit.text()) 
            # print(self.Brag_reflection, self.hv, self.range, self.angles, self.GB, self.IMFP)

    def load_material_info(self):
        # function code
        self.material_info_file = QtWidgets.QFileDialog.getOpenFileName(self.widget_5, 'Open File')   
        self.material_info_file =  self.material_info_file[0]    
        if(self.material_info_file != ''):
            try:
                self.show_load.setText(str(self.material_info_file))
                self.atom_name_list, self.ASF_atoms, lattice, coordinates = crystal_infor(str(self.material_info_file))
                self.material_infor = [lattice, 0, 0, coordinates]
                self.update_group_CB()
            except:
                self.alert = input_alert()
                self.alert.new_content(["FAIL to LOAD Mater_info", "CHECK THE FILE FORMAT"], "#993333")
                self.alert.show()


        # testing code
        # self.material_info_file = "/Users/shihchiehlin/Desktop/KLDD/INFO.txt"
        # self.show_load.setText(self.material_info_file)
        # self.atom_name_list, self.ASF_atoms, lattice, coordinates = crystal_infor(self.material_info_file)
        # self.update_group_CB()
        # self.material_infor = [lattice, 0, 0, coordinates]

    def menu_online(self):
        self.menuSave = QtWidgets.QAction('&SAVE', MainWindow) 
        self.menuSave.setShortcut("Ctrl+S")
        self.menuSave.setStatusTip('SAVE File')
        self.menuSave.triggered.connect(self.file_save) 
        self.menubar.addAction(self.menuSave)

        self.menuLoad = QtWidgets.QAction('&LOAD', MainWindow) 
        self.menuLoad.setShortcut("Ctrl+L")
        self.menuLoad.setStatusTip('LOAD File')
        self.menuLoad.triggered.connect(self.file_load) 
        self.menubar.addAction(self.menuLoad)

        self.menuExit = QtWidgets.QAction('&EXIT', MainWindow) 
        self.menuExit.setShortcut("Ctrl+Q")
        self.menuExit.setStatusTip('EXIT Program')
        self.menuExit.triggered.connect(QtWidgets.qApp.quit) 
        self.menubar.addAction(self.menuExit)
        self.menubar.setNativeMenuBar(False)


    def file_save(self):
        save_file_name = QtWidgets.QFileDialog.getSaveFileName(self.menubar, 'Save File')
        if(save_file_name[0] != ""):
            file = open(save_file_name[0] + ".kldd",'w')
            if(self.material_info_file != ""):
                file.write(self.material_info_file)
            file.write("\n")
            for item in self.lineEdit_input:
                if(item.text() != ''):
                    file.write(item.text())
                file.write("\n")
            file.write("%.2f\n"%self.aphase)
            file.write("%d" %self.unit_cell_spinBox.value())
            file.close()

    def file_load(self):
        load_file_name = QtWidgets.QFileDialog.getOpenFileName(self.menubar, 'Open File')
        if(load_file_name[0] != ""):
            input_file = open(load_file_name[0],'r')
            load_parameters = list(csv.reader(input_file))
            try:
                self.material_info_file = load_parameters[0][0]
                self.show_load.setText(str(self.material_info_file))
                self.atom_name_list, self.ASF_atoms, lattice, coordinates = crystal_infor(str(self.material_info_file))
                self.material_infor = [lattice, 0, 0, coordinates]
                self.update_group_CB()
            except:
                pass

            for i in range(1, len(load_parameters) - 1):
                try:
                    self.lineEdit_input[i - 1].setText(load_parameters[i][0])
                except:
                    pass
            try:
                self.aphase = float(load_parameters[13][0])
            except:
                pass
            try:
                self.unit_cell_spinBox.setValue(float(load_parameters[14][0])) 
            except:
                pass

    def button_online(self):
        # load material information
        self.browse_file.pressed.connect(self.load_material_info)     
        # reflectivity related
        self.push_simu_REF.pressed.connect(self.check_valid_input)
        self.push_simu_REF.pressed.connect(self.calc_REF)
        self.bt_load_ref.pressed.connect(self.load_exp_REF)
        self.bt_load_ref.pressed.connect(self.show_data_adjust)
        self.save_REF_txt.pressed.connect(self.save_REF)
        
        # self.bt_load_ref.pressed.connect(self.update_exp_REF)
        # rocking curves related
        self.push_simu_RC.pressed.connect(self.check_valid_input)
        self.push_simu_RC.pressed.connect(self.show_data_adjust)
        self.push_simu_RC.pressed.connect(self.calc_RC)

        self.bt_load_rc.pressed.connect(self.load_exp_RC)
        self.bt_load_rc.pressed.connect(self.show_data_adjust)
        
        # self.save_RC_txt.pressed.connect(self.file_save)
        self.save_RC_txt.pressed.connect(self.save_RCs)

    def cal_error_message(self):
        self.alert = input_alert()
        error_content_list = []
        hkl_all_zero = True

        for item in self.Brag_reflection:
            if(item != 0):
                hkl_all_zero = False

        h = self.Brag_reflection[0]
        k = self.Brag_reflection[1]
        l = self.Brag_reflection[2]

        try:
            miniMum_energy = 12400/(2* cal_layer_distance(h, k, l, self.material_infor[0]))
        except:
            pass

        if(hkl_all_zero):
            error_content_list.append("(h, k, l) = (0, 0, 0) IS")
            error_content_list.append(" NOT A VALID INPUT")
        elif(self.hv < miniMum_energy):
            error_content_list.append("The MINIMUM VALID PHOTON")
            error_content_list.append("ENERGY FOR (%d, %d, %d) is %.2f eV" %(h, k, l, miniMum_energy))
            self.alert.resize(350, 120)
        else:
            error_content_list.append("CACULATION ERROR")
            error_content_list.append("PLEASE CHECK INPUT")
        self.alert.new_content(error_content_list, "#993333")
        self.alert.show()

    def calc_REF(self):
        self.REF_canvas.figure.clf()
        if self.input_compelete:
            try:
                self.ref_range, self.simu_phase, self.simu_REF = calc_ref_phase(self.Brag_reflection,
                     self.hv, self.range, self.GB, self.material_infor, self.ASF_atoms)
                self.update_REF_canvas()  
            except:
                self.cal_error_message()   
        else:
            self.alert = input_alert()
            self.alert.show()

    def load_exp_REF(self):
        self.exp_REF_name = QtWidgets.QFileDialog.getOpenFileName(self.widget_7, 'Open File')
        if(self.exp_REF_name[0] != ''):
            self.exp_REF_origin = np.loadtxt(self.exp_REF_name[0], unpack = True)
            self.update_REF_canvas()
            
    def update_REF_canvas(self):
        self.REF_canvas.figure.clf()
        self.case = 0
        if(len(self.exp_REF_origin) != 1):
            self.exp_REF = process(self.exp_REF_origin, self.adjust_exp_REF)
            self.case += 1

        if(len(self.simu_phase) != 1):
            self.case += 2
  
        if(self.case != 0):
            plotREFs(self.REF_canvas, self.ref_range, self.simu_phase, self.simu_REF, self.exp_REF, self.case)

    def show_data_adjust(self):
        try:
            if(self.adjust_dialog.isVisible() == False):
                self.adjust_dialog.show()
        except: 
            self.adjust_dialog = Adjust_Exp_Data()
            # self.adjust_dialog.setGeometry(1018, 100, 249, 192)

        self.adjust_dialog_parameters = [self.adjust_dialog.box_smooth,
                                self.adjust_dialog.bg_slope,
                                self.adjust_dialog.shift_x]
                                
        for i, item in enumerate(self.adjust_dialog_parameters):
            item.setValue(self.adjust_exp_REF[i])
            item.valueChanged.connect(self.update_data_adjust)

        self.adjust_dialog.aphase.setValue(self.aphase)
        self.adjust_dialog.aphase.valueChanged.connect(self.update_aphase)
        self.adjust_dialog.aphase.valueChanged.connect(self.calc_RC)

    # def update_adjust_dialog(self):
    #     if(str(self.adjust_dialog.comboBox.currentText()) == "Ref. Exp."):
    #         for i, item in enumerate(self.adjust_dialog_parameters):
    #             item.setValue(self.adjust_exp_REF[i])
    #     else:
    #         for i, item in enumerate(self.adjust_dialog_parameters):
    #             item.setValue(self.adjust_exp_RC[i])

    def update_data_adjust(self):
        if(str(self.adjust_dialog.comboBox.currentText()) == "Ref. Exp."):
            for i, item in enumerate(self.adjust_dialog_parameters):
                self.adjust_exp_REF[i] = item.value()
            if(len(self.exp_REF_origin) != 1):
                self.update_REF_canvas()
        else:
            for i, item in enumerate(self.adjust_dialog_parameters):
                self.adjust_exp_RC[i] = item.value()
            if(len(self.exp_RC_origin) != 1):
                self.update_RC_canvas()

    def update_aphase(self):
        self.aphase = self.adjust_dialog.aphase.value()
     
    def save_REF(self):
        if(self.simu_phase.size != 1):
            save_ref_name = QtWidgets.QFileDialog.getSaveFileName(self.widget_19, 'Open File')
            if(save_ref_name[0] == ""):
                return
            np.savetxt(save_ref_name[0] + ".txt", np.vstack((self.ref_range, self.simu_phase, self.simu_REF)).T, delimiter= '\t', header = "x_axis\tPhase\tReflectivity\t")
            self.alert = input_alert()
            self.alert.new_content(["Reflectivity Data Saved"], "#000033")
            self.alert.show()
        else:
            self.alert = input_alert()
            self.alert.new_content(["SIMULATION NOT DONE YET", "PLEASE CHECK"], "#000033")
            self.alert.show()
    
    def calc_RC(self):
        if self.input_compelete:
            self.simu_RC_origin = []
            self.normal_factor_origin = []
            No_uc = self.unit_cell_spinBox.value()
            try:
                for atom in self.atom_name_list: 
                    self.rc_range, rc, rc_normal_factor =  calc_RCs(atom, self.aphase, self.IMFP, self.angles, No_uc, self.Brag_reflection, self.hv, self.range, self.GB, self.material_infor, self.ASF_atoms)
                    self.simu_RC_origin.append(rc)
                    self.normal_factor_origin.append(rc_normal_factor)
                self.update_RC_canvas()
            except: 
                self.cal_error_message()
        else:
            self.alert = input_alert()
            self.alert.show()

    def load_exp_RC(self):
        self.exp_RC_name = QtWidgets.QFileDialog.getOpenFileName(self.widget_8, 'Open File')
        if(self.exp_RC_name[0] != ''):
            self.exp_RC_origin = np.loadtxt(self.exp_RC_name[0], unpack = True)
            self.update_RC_canvas()
            
    def update_RC_canvas(self):
        self.RC_canvas.figure.clf()
        self.case = 0

        if(len(self.exp_RC_origin) != 1):
            self.exp_RC = process(self.exp_RC_origin, self.adjust_exp_RC)
            self.case += 1

        if(len(self.simu_RC_origin)!= 1):
            self.simu_RC = []
            self.rc_legend = []
            self.normal_factor = []
            self.no_self_define_RC = True
            for i in range(3):
                if(len(self.group_CB[i].checkedIndices()) != 0):
                    new_RC, new_nor_factor = self.self_define_RC(i)
                    new_legend = self.self_define_RC_legend(i)
                    self.simu_RC.append(new_RC)
                    self.normal_factor.append(new_nor_factor)
                    self.rc_legend.append(new_legend)
                    self.no_self_define_RC = False

            if(self.no_self_define_RC):
                self.simu_RC = copy.deepcopy(self.simu_RC_origin)
                self.rc_legend = copy.deepcopy(self.atom_name_list)
                self.normal_factor = copy.deepcopy(self.normal_factor_origin)
            self.case += 2

        if(self.case != 0):
            plotRCs(self.RC_canvas, self.rc_range, self.rc_legend, self.simu_RC, self.normal_factor, self.exp_RC, self.case)

    def self_define_RC_legend(self, ith):
        if(self.group_lineEdit[ith].text() != ''):
            return str(self.group_lineEdit[ith].text())
        else:
            rc_list = self.group_CB[ith].checkedIndices()
            produce_name = ""
            for i in rc_list:
                produce_name += self.atom_name_list[i] + "+"
            return produce_name[:-1]

    def self_define_RC(self, ith):
        rc_list = self.group_CB[ith].checkedIndices()
        self_define_RC = np.zeros(len(self.simu_RC_origin[rc_list[0]]))
        self_define_normal_fatcor = 0
        for i in rc_list:
            self_define_RC += self.simu_RC_origin[i]
            self_define_normal_fatcor += self.normal_factor_origin[i]
        return self_define_RC, self_define_normal_fatcor


    def update_group_CB(self):
        for item in self.group_CB:
            model = item.model()
            item.setPlaceholderText("NO SELECTION")
            for i, atom in enumerate(self.atom_name_list):
                item.addItem(atom)
                model.item(i).setCheckable(True)

    def save_RCs(self):
        if(len(self.simu_RC)!= 0):
            save_RC_name = QtWidgets.QFileDialog.getSaveFileName(self.widget_19, 'Open File')
            if(save_RC_name[0] == ""):
                return
            Header = "x_axis\t"
            self.rcs_saved_data = np.copy(self.rc_range)

            for i, item in enumerate(self.simu_RC):
                self.rcs_saved_data = np.vstack((self.rcs_saved_data, item))
                Header = Header + "raw_" + self.rc_legend[i] + "\t"

            for i, item in enumerate(self.simu_RC):
                self.rcs_saved_data = np.vstack((self.rcs_saved_data, (item/self.normal_factor[i])))
                Header = Header + "nor_" + self.rc_legend[i] + "\t"

            np.savetxt(save_RC_name[0]+ ".txt", self.rcs_saved_data.T, delimiter= '\t', header = Header)
            self.alert = input_alert()
            self.alert.new_content(["Rocking Curves Data Saved"], "#000033")
            self.alert.show()
        else:
            self.alert = input_alert()
            self.alert.new_content(["SIMULATION NOT DONE YET", "PLEASE CHECK"], "#000033")
            self.alert.show()   

if __name__ == "__main__":
    import sys    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyQtApp()
    ui.setupUi(MainWindow)
    # ui.initialize_test_parameters()
    ui.menu_online()
    ui.updateFeatures()
    ui.apply_input_const()
    ui.button_online()
    MainWindow.show()
    sys.exit(app.exec_())