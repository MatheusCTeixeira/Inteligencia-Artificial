
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

from PyQt5.QtChart import QBarSeries, QBarSet, QChart, QChartView, QBarCategoryAxis

#--------------------------------------------------------------------------#


class Piece(QLabel):
    """ Representa uma peça no tabuleiro """
    matrix_piece = []
    map = None

    def __init__(self, text, position, map):
        super().__init__()
        super().setText(text)
        self.position = position
        self.map = map

        i, j = self.position
        while len(self.matrix_piece) <= i:
            self.matrix_piece.append([])

        while len(self.matrix_piece[i]) <= j:
            self.matrix_piece[i].append(self)

    def swap_text(self, lbl1, lbl2):
        text = lbl1.text()
        lbl1.setText(lbl2.text())
        lbl2.setText(text)

    def swap_map(self, pos1, pos2):
        i1, j1 = pos1
        i2, j2 = pos2

        val = self.map[i1][j1]
        self.map[i1][j1] = self.map[i2][j2]
        self.map[i2][j2] = val
        
    def mousePressEvent(self, mouse_event):
        """ Processa o evento de click em um peça do tabuleiro """
        i, j = self.position               

        if i > 0 and self.matrix_piece[i - 1][j].text() == "0":
            self.swap_text(self.matrix_piece[i][j],\
                           self.matrix_piece[i - 1][j])
            self.swap_map(self.position, (i - 1, j))

        elif i + 1 < len(self.matrix_piece) and self.matrix_piece[i + 1][j].text() == "0":
            self.swap_text(self.matrix_piece[i][j],\
                           self.matrix_piece[i + 1][j])                    
            self.swap_map(self.position, (i + 1, j))            

        elif j > 0 and self.matrix_piece[i][j - 1].text() == "0":
            self.swap_text(self.matrix_piece[i][j],\
                           self.matrix_piece[i][j - 1])
            self.swap_map(self.position, (i, j - 1))        

        elif j + 1 < len(self.matrix_piece[0])  and self.matrix_piece[i][j + 1].text() == "0":
            self.swap_text(self.matrix_piece[i][j],\
                           self.matrix_piece[i][j + 1])
            self.swap_map(self.position, (i, j + 1))
        
        for line in self.map:
            for x in line:
                print("%3d" %x, end='')
            print()


        print("---------------------------------------------\n")

#--------------------------------------------------------------------------#


class ControlButton(QPushButton):
    """ Representa os buttons para iterar a solução """

    def __init__(self, text, action):
        super().__init__()
        super().setText(text)

        self.action = action

    def mouseReleaseEvent(self, event):
        """ Ação de clicar no button """
        print(self.action())

        super().mouseReleaseEvent(event)

#--------------------------------------------------------------------------#


class Game:
    """ Representa a interface do jogo """

    def __init__(self, N):
        app = QApplication([])

        self.current_step = 0
        self.N = N

        vLayout = QVBoxLayout()
        vLayout.addWidget(
            QLabel("<h1><center>Quebra-Cabeça N Peças</center></h1>"))
        vLayout.addWidget(self.create_board(self.N))
        vLayout.addWidget(self.step_solution())
        vLayout.addWidget(self.solution_methods())

        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout)
        hLayout.addWidget(self.draw_result())

        widget = QWidget()
        widget.setLayout(hLayout)
        widget.setStyleSheet("background: white;")
        widget.show()

        app.exec_()

    def create_board(self, N):
        """ Cria o tabuleiro """

        self.board = [[a+b*N for a in range(N)] for b in range(N)]
        piece_size = 70

        pane = QWidget()
        pane.setStyleSheet("border: 1px solid black;")

        grid = QGridLayout()
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                piece = Piece(str(self.board[i][j]), (i, j), self.board)
                piece.setAlignment(QtCore.Qt.AlignCenter)
                piece.setFont(QFont("source code pro", 20))
                piece.setFixedSize(piece_size, piece_size)
                piece.setLineWidth(2)
                piece.setStyleSheet("border: 1px solid red;\
                                     background: yellow;   \
                                     border-radius: 4px;")
                grid.addWidget(piece, i, j)

        pane.setLayout(grid)
        return pane

    def solution_methods(self):
        """ Adiciona as opções de soluções utilizando IA """

        cbbMethods = QComboBox()
        cbbMethods.addItems(["BFS", "DFS", "A* + Manhattan", "HC"])

        pane = QWidget()

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Método de solução: "))

        hbox.addWidget(cbbMethods)

        pane.setLayout(hbox)

        return pane

    def step_solution(self):
        """ Itera entre os passos que levam a solução (semelhante a depurar a solução) """

        pane = QWidget()

        hbox = QHBoxLayout()
        hbox.addWidget(ControlButton("<<", lambda: self.current_step - 1))
        hbox.addWidget(ControlButton("||", lambda: 0))
        hbox.addWidget(ControlButton(">>", lambda: self.current_step + 1))
        pane.setLayout(hbox)

        return pane

    def draw_result(self):
        """ Exibe os resultados para comparação entre os métodos """

        names = ["BFS", "DFS", "A*", "HC"]

        serie = QBarSeries()
        for k in range(len(names)):
            sett = QBarSet(names[k])
            for i in range(1, 3 + 1):
                sett.append(i)
            serie.append(sett)

        axis = QBarCategoryAxis()
        axis.append("Duração")
        axis.append("Profundidade")
        axis.append("Largura")

        chart = QChart()
        chart.addSeries(serie)
        chart.setAxisX(axis)
        chart.setTitle("Comparação entre os métodoss")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart_view = QChartView(chart)
        chart_view.setMinimumWidth(550)
        chart_view.setMaximumWidth(600)
        chart_view.setMaximumHeight(600)

        return chart_view

#--------------------------------------------------------------------------#


game = Game(3)