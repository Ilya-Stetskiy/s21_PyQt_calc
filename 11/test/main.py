import ctypes
import os
import subprocess
import datetime
from array import *
from ctypes import *
import sys
from PyQt5.QtCore import QEvent, Qt
import matplotlib.pyplot as plt
import math
from PyQt5 import uic, QtWidgets  # Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *


# from rb import Ui_Dialog_rb
class Window_vklad(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window_vklad, self).__init__(parent)
        uic.loadUi("vklad.ui", self)
        self.pushButton.clicked.connect(lambda: self.calc())
        self.But_add.clicked.connect(lambda: self.add(""))
        self.But_minus.clicked.connect(lambda: self.add("-"))
        self.But_clear_hist.clicked.connect(lambda: self.clear())
        self.show()

    def clear(self):
        self.text_history.clear()
        self.text_history.repaint()

    def add(self, char):
        time = self.date_change.date().toPyDate() - self.dateStart.date().toPyDate()
        text = str(time.days) + " " + char + str(self.text_sum_2.toPlainText())
        self.text_history.appendPlainText(text)

    def month(self, time_new, days):
        if time_new.month in [4, 6, 9, 11]:
            time_new = time_new + datetime.timedelta(days=30)
        elif time_new.month == 2 and time_new.day not in [28, 29]:
            time_new = time_new + (datetime.date(time_new.year, 3, 1) - datetime.date(time_new.year, 2, 1))
        elif (time_new.month == 1 and time_new.day > (
                datetime.date(time_new.year, 3, 1) - datetime.date(time_new.year, 2, 1)).days):
            time_new = datetime.date(time_new.year, 3, 1) - datetime.timedelta(days=1)

        elif time_new.month == 2 and time_new.day in [28, 29]:
            time_new = datetime.date(time_new.year, 3, days)
        else:
            time_new = time_new + datetime.timedelta(days=31)
        return time_new

    def calc(self):

        cap = array('i')
        capital = (c_int * len(cap))(*cap)
        summ = self.text_sum.toPlainText()
        time_start = self.dateStart.date().toPyDate()
        time_fin = datetime.date(
            time_start.year + self.spinBox_year.value() + (time_start.month + self.spinBox_month.value() - 1) // 12,
            (time_start.month + self.spinBox_month.value() - 1) % 12 + 1,
            time_start.day + datetime.timedelta(days=self.spinBox_days.value()).days)

        time = time_fin - time_start
        # time = self.dateFin.date().toPyDate() - self.dateStart().date().toPyDate()
        percent = self.text_percent.toPlainText()
        if time.days <= 0:
            self.text_res_perep.setText("Ошибка даты")
        else:
            history = str(self.text_history.toPlainText())
            flag_capital = 0
            if self.checkBox.isChecked():
                flag_capital = 1

            time_new = self.dateStart.date().toPyDate()

            if int(self.comboBox.currentIndex()) == 0:
                size_of_capital = c_int * 1
                capital = size_of_capital(time.days)
            elif int(self.comboBox.currentIndex()) == 1:  # years
                time_new = datetime.date(time_new.year + 1, time_new.month, time_new.day)
                while time_new <= time_fin:
                    d_days = time_new - time_start
                    cap.append(d_days.days)

                    time_new = datetime.date(time_new.year + 1, time_new.month, time_new.day)
                capital = (c_int * len(cap))(*cap)

            elif int(self.comboBox.currentIndex()) == 2:  # month
                day = time_new.day
                time_new = self.month(time_new, day)

                while time_new <= time_fin:
                    d_days = time_new - time_start
                    cap.append(d_days.days)
                    time_new = self.month(time_new, day)
                capital = (c_int * len(cap))(*cap)
            else:  # days
                oneday = datetime.timedelta(days=1)
                time_new = time_new + oneday
                while time_new <= time_fin:
                    d_days = time_new - time_start
                    cap.append(d_days.days)

                    time_new = time_new + oneday
                capital = (c_int * len(cap))(*cap)
            nal = array('i')
            n_y = array('i')
            if time_start.month != 12:
                time_next_year = datetime.date(time_start.year, 12, 31)
            else:
                time_next_year = datetime.date(time_start.year + 1, 12, 1)

            nal.append((time_next_year - time_start).days)
            time_new_year = datetime.date(time_start.year + 1, 1, 1)
            n_y.append((time_new_year - datetime.date(time_start.year, 1, 1)).days)

            while time_next_year <= time_fin:
                time_next_year = datetime.date(time_next_year.year + 1, 12, 31)
                time_new_year = datetime.date(time_new_year.year + 1, 1, 1)
                n_y.append((time_new_year - datetime.date(time_new_year.year - 1, 1, 1)).days)
                nal.append((time_next_year - time_start).days)
            nalog = (c_int * len(nal))(*nal)
            new_year = (c_int * len(n_y))(*n_y)
            execute.vklad_not.restype = ctypes.c_double
            res_percent = execute.vklad_not(bytes(summ, encoding='ASCII'), c_int(time.days),
                                            bytes(percent, encoding='ASCII'), bytes(history, encoding='ASCII'), capital,
                                            nalog, c_int(len(nal)),
                                            bytes(self.text_percent_2.toPlainText(), encoding='ASCII'), new_year,
                                            c_int(1), c_int(flag_capital))
            res_sum = execute.vklad_not(bytes(summ, encoding='ASCII'), c_int(time.days),
                                        bytes(percent, encoding='ASCII'), bytes(history, encoding='ASCII'), capital,
                                        nalog, c_int(len(nal)),
                                        bytes(self.text_percent_2.toPlainText(), encoding='ASCII'), new_year,
                                        c_int(2), c_int(flag_capital))
            res_nalog = execute.vklad_not(bytes(summ, encoding='ASCII'), c_int(time.days),
                                          bytes(percent, encoding='ASCII'), bytes(history, encoding='ASCII'), capital,
                                          nalog, c_int(len(nal)),
                                          bytes(self.text_percent_2.toPlainText(), encoding='ASCII'), new_year,
                                          c_int(3), c_int(flag_capital))

            self.text_res_perep.setText("{:.2f}".format(res_percent))
            self.text_res_sum.setText("{:.2f}".format(res_sum))
            self.text_res_nalog.setText("{:.2f}".format(res_nalog))
            self.text_res_perep.repaint()


class Window_credit(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window_credit, self).__init__(parent)
        uic.loadUi("credit.ui", self)
        self.pushButton.clicked.connect(self.calc)
        self.show()

    def calc(self):
        summ = self.text_sum.toPlainText()
        years = self.text_years.toPlainText()
        month = self.text_month.toPlainText()
        percent = self.text_percent.toPlainText()
        if int(self.comboBox.currentIndex()) == 1:
            execute.credit_a.restype = ctypes.c_double
            res_month = execute.credit_a(bytes(summ, encoding='ASCII'), bytes(years, encoding='ASCII'),
                                         bytes(month, encoding='ASCII'), bytes(percent, encoding='ASCII'))

            res_sum = float(res_month) * (12 * float(years) + float(month))
            res_perep = res_sum - float(summ)
            self.text_res_sum.setText("{:.2f}".format(res_sum))
            self.text_res_perep.setText("{:.2f}".format(res_perep))
            self.text_res_month.setText("{:.2f}".format(res_month))
        else:
            execute.credit_d.restype = ctypes.c_double
            res_sum = execute.credit_d(bytes(summ, encoding='ASCII'), bytes(years, encoding='ASCII'),
                                       bytes(month, encoding='ASCII'), bytes(percent, encoding='ASCII'))
            res_perep = res_sum - float(summ)
            self.text_res_sum.setText("{:.2f}".format(res_sum))
            self.text_res_sum.repaint()
            self.text_res_perep.setText("{:.2f}".format(res_perep))
            self.text_res_perep.repaint()
            self.text_res_month.setText("в файле")
            self.text_res_month.repaint()

            os.system("result.txt")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("CALC.ui", self)
        self.But_1.clicked.connect(lambda: self.insert("1"))
        self.But_2.clicked.connect(lambda: self.insert("2"))
        self.But_3.clicked.connect(lambda: self.insert("3"))
        self.But_4.clicked.connect(lambda: self.insert("4"))
        self.But_5.clicked.connect(lambda: self.insert("5"))
        self.But_6.clicked.connect(lambda: self.insert("6"))
        self.But_7.clicked.connect(lambda: self.insert("7"))
        self.But_8.clicked.connect(lambda: self.insert("8"))
        self.But_9.clicked.connect(lambda: self.insert("9"))
        self.But_0.clicked.connect(lambda: self.insert("0"))
        self.But_acos.clicked.connect(lambda: self.insert("acos()"))
        self.But_asin.clicked.connect(lambda: self.insert("asin()"))
        self.But_atan.clicked.connect(lambda: self.insert("atan()"))
        self.But_cos.clicked.connect(lambda: self.insert("cos()"))
        self.But_div.clicked.connect(lambda: self.insert("/"))
        self.But_dot.clicked.connect(lambda: self.insert("."))
        self.But_ln.clicked.connect(lambda: self.insert("ln()"))
        self.But_log.clicked.connect(lambda: self.insert("log()"))
        self.But_minus.clicked.connect(lambda: self.insert("-"))
        self.But_mod.clicked.connect(lambda: self.insert("mod"))
        self.But_multi.clicked.connect(lambda: self.insert("*"))
        self.But_plus.clicked.connect(lambda: self.insert("+"))
        self.But_pow.clicked.connect(lambda: self.insert("^"))
        self.But_sin.clicked.connect(lambda: self.insert("sin()"))
        self.But_sqrt.clicked.connect(lambda: self.insert("sqrt()"))
        self.But_tan.clicked.connect(lambda: self.insert("tan()"))
        self.But_close.clicked.connect(lambda: self.insert(")"))
        self.But_open.clicked.connect(lambda: self.insert("("))
        self.But_x.clicked.connect(lambda: self.insert("x"))

        self.But_credit.clicked.connect(self.credit)
        self.But_vklad.clicked.connect(self.vklad)

        self.But_equals.clicked.connect(lambda: self.equals())
        self.text.setFocus()

        self.text.installEventFilter(self)
        # cursor=self.text.setTextCursor
        # self.text.keyPressEvent()
        self.show()

    def eventFilter(self, obj, event):
        if obj is self.text and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Equal, Qt.Key_Enter, Qt.Key_Return):
                self.equals()
                return True
        return super(Window, self).eventFilter(obj, event)

    def credit(self):

        Win_credit = Window_credit(self)
        Win_credit.exec_()

    def vklad(self):
        Win_vklad = Window_vklad(self)
        Win_vklad.exec_()

    def insert(self, _str):
        self.text.insertPlainText(_str)
        if (len(_str) > 2 and _str != "mod"):
            self.text.moveCursor(QTextCursor.Left)

        self.text.repaint()
        self.text.setFocus()

    def equals(self):
        try:
            self.text.moveCursor(QTextCursor.End)
            if self.text.toPlainText()[-1:] != "=":
                self.text.insertPlainText("=")
            task = self.text.toPlainText()
            execute.not_main.restype = ctypes.c_double
            if int(self.comboBox.currentIndex()) == 0 and "x" in task:
                if self.text_x_min.toPlainText() == "":
                    x_min = -math.pi
                else:
                    x_min = float(self.text_x_min.toPlainText())
                if self.text_x_max.toPlainText() == "":
                    x_max = math.pi
                else:
                    x_max = float(self.text_x_max.toPlainText())

                x = [(x / 9999) * (x_max - x_min) + x_min for x in range(10000)]
                y = []
                y_last = 0
                for i in range(len(x)):
                    task_temp = task.replace("x", str("{:.5f}".format(x[i])))
                    try:
                        result = execute.not_main(bytes(task_temp, encoding='ASCII'))
                        if abs(result - y_last) > 10 ** 3:
                            y.append(float('nan'))
                        else:
                            y.append(result)
                        y_last = result
                    except Exception:
                        y.append(float('nan'))
                plt.plot(x, y)

                if self.text_y_max.toPlainText() != "":
                    plt.axis(ymax=float(self.text_y_max.toPlainText()))
                if self.text_y_min.toPlainText() != "":
                    plt.axis(ymin=float(self.text_y_min.toPlainText()))
                plt.title("Graph")
                plt.xlabel("Values of x")
                plt.ylabel("Values of y")
                plt.axhline(0, color="black", linewidth=0.5)
                plt.axvline(0, color="black", linewidth=0.5)
                plt.show()
            else:
                task = task.replace("x", str(self.text_x.toPlainText()))
                self.text3.setPlainText(task)
                result = execute.not_main(bytes(task, encoding='ASCII'))
                self.text.clear()
                if str(result)=="nan" :self.text2.setPlainText("Error")
                else: self.text2.setPlainText("{:.8g}".format(result))
                if self.checkBox.isChecked():
                    self.text.setPlainText(self.text2.toPlainText())
            self.text.repaint()
            self.text.setFocus()
            self.text.moveCursor(QTextCursor.End)
        except Exception:
            self.text3.setPlainText(self.text.toPlainText())
            self.text2.setPlainText("Ошибка ввода. Исправьте выражение")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.equals()
        if event.key() == Qt.Key_Equal:
            self.equals()


if __name__ == '__main__':
    pwd = os.getcwd()
    #subprocess.run(["gcc", "-m64", "-shared", "-o", "main.dll", "calc.c", "a.c"], check=True)
    #execute = ctypes.cdll.LoadLibrary(f"{pwd}\\main.dll")
    #subprocess.run(["gcc","-dynamiclib","a.c","calc.c","-lm", "-o", "main.dylib",], check=True,)
    execute = ctypes.cdll.LoadLibrary(f"{pwd}/main.dylib")
    # execute = ctypes.cdll.LoadLibrary(f"{pwd}\\main.dll")
    # execute.say_fuck()
    # print(execute.what_the_func(bytes("cos", encoding='ASCII')))
    app = QApplication(sys.argv)
    Win = Window()
    app.exec_()
