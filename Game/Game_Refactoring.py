
import sys
import os
import datetime
import time

sys.path.append("../Core")
from algoritmos_de_busca_solucao import BFS_solution
from algoritmos_de_busca_solucao import DFS_Iter_solution
from algoritmos_de_busca_solucao import DFS_Recr_solution

from algoritmos_de_busca_solucao_informada import AStar_H1_solution
from algoritmos_de_busca_solucao_informada import AStar_H2_solution

from enum import Enum
from copy import deepcopy

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout,\
    QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtWidgets import QComboBox, QSlider, QMessageBox, QLabel
from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt



BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class BoardMode(Enum):
    EDIT_MODE     = 1
    PLAY_MODE     = 2
    UNSTABLE_MODE = 3



class Board(QWidget):
    def __init__(self, max_order):
        self.board_size                   = 400
        self.max_order                    = max_order
        self.current_order                = max_order
        self.mode                         = BoardMode.PLAY_MODE
        self.unused_values                = []
        self.max_tolerable_solution_depth = 8

        self.logic_board = self.create_logic_board(self.current_order)
        self.graphic_board = self.create_graphic_board()
        self.set_final_state()
        self.graphic_edit_board = self.create_graphic_edit_board()
        self.all_widgets = {}

# ---------------------------------------------------------------------------- #

    def create_graphic_board(self):
        buttons = []
        # Cria N×N buttuns, onde N é a ordem do tabuleiro.

        for i in range(self.max_order):
            buttons.append([])
            for j in range(self.max_order):
                valid_button = i < self.current_order and j < self.current_order

                # Cada button tem a forma de um quadrado.
                buttonSize = self.board_size/self.current_order
                button = QPushButton()
                button.setFixedSize(buttonSize, buttonSize)
                button.setVisible(valid_button)
                button.setText(\
                    str(i * self.current_order + j) if valid_button else " ")

                button.clicked.connect(\
                    lambda arg, coord=(i, j): self.piece_click(coord))
                buttons[i].append(button)


        return buttons

# ---------------------------------------------------------------------------- #

    def create_graphic_edit_board(self):
        # Cria N×N comboboxs. Cada um serve para colocar um valor numa determi-
        # nada peça.

        comboboxs = []
        for i in range(self.max_order):
            comboboxs.append([])
            for j in range(self.max_order):
                combobox = QComboBox()
                comboboxSize = self.board_size / self.current_order
                combobox.setFixedSize(comboboxSize, comboboxSize)
                combobox.setVisible(False)

                combobox.currentIndexChanged.connect(\
                    lambda arg, param=(i, j):\
                        self.select_piece_value_edit_mode(param)\
                )

                comboboxs[i].append(combobox)

        return comboboxs

# ---------------------------------------------------------------------------- #

    def create_logic_board(self, order):
        # Cria o tabuleiro. O tabuleiro é constituido por uma matrix de ordem
        # N×N.
        board = [[i *order + j for j in range(order)]\
                               for i in range(order)]

        return board

# ---------------------------------------------------------------------------- #

    def update_graphic_board(self):
        # Atualiza o jogo no modo "PLAY".
        self.update_graphic_board_text()
        self.update_graphic_board_size()

        # Atualiza o jogo no modo "EDIT".
        self.update_edit_graphic_board_text()
        self.update_edit_graphic_board_size()

        # Atualiza a visibilidade do jogo.
        self.update_board_visibility()

        # Destaca a peça que pode ser movida e as peças adjacentes.
        self.highlight_graphic_board()

        if self.logic_board == self.final_state and\
             hasattr(self, 'message'):
            self.message.setText("\\o/ Solved :D")

            for i in range(self.max_order):
                for j in range(self.max_order):
                    if self.graphic_board[i][j].isVisible():
                        self.graphic_board[i][j].\
                            setStyleSheet("background-color: yellow;")

# ---------------------------------------------------------------------------- #

    def update_board_visibility(self):
        # Exibe ou oculta as peças de acordo com a ordem do tabuleiro e com o
        # modo de jogo.

        for i in range(self.max_order):
            for j in range(self.max_order):
                isInRange = i < self.current_order and j < self.current_order

                self.graphic_board[i][j]\
                    .setVisible(isInRange and self.mode == BoardMode.PLAY_MODE)

                self.graphic_edit_board[i][j]\
                    .setVisible(isInRange and self.mode == BoardMode.EDIT_MODE)

# ---------------------------------------------------------------------------- #

    def list_possible_moves(self):
        # Indica quais posições a peça que pode se deslocar pode ser movida.
        moves = []

        zero_position = None
        for i in range(self.current_order):
            position_found = False
            for j in range(self.current_order):
                if self.logic_board[i][j] == 0:
                    zero_position = (i, j)
                    position_found = True
                    break
            if position_found:
                break

        i, j = zero_position
        if i > 0:
            moves.append((i - 1, j))
        if i < self.current_order - 1:
            moves.append((i + 1, j))
        if j > 0:
            moves.append((i, j - 1))
        if j < self.current_order - 1:
            moves.append((i, j + 1))

        return moves

# ---------------------------------------------------------------------------- #

    def highlight_graphic_board(self):
        # Destaca as peças do jogo.

        for i in range(self.max_order):
            for j in range(self.max_order):

                # Destaca apenas as peças estão visiveis.
                if self.graphic_board[i][j].isVisible():

                    # A peça que pode ser movida.
                    if self.graphic_board[i][j].text() == "0":
                        self.graphic_board[i][j].\
                            setStyleSheet("background-color: darkgray;\
                                border: 1px solid red;")
                    else:
                    # As demais peças não possuem nenhum destaque.
                        self.graphic_board[i][j].\
                            setStyleSheet("background-color: None;")

        # Destaca os possiveis movimentos.
        for pos in self.list_possible_moves():
            i, j = pos
            self.graphic_board[i][j].\
                setStyleSheet("background-color: lightgray;\
                border: 1px solid red;")

# ---------------------------------------------------------------------------- #

    def update_graphic_board_text(self):
        # Atualiza o texto contido em cada button em de acordo com o que está
        # no tabuleiro lógico.

        if self.mode != BoardMode.PLAY_MODE:
            return

        for i in range(self.current_order):
            for j in range(self.current_order):
                self.graphic_board[i][j]\
                    .setText(str(self.logic_board[i][j]))

# ---------------------------------------------------------------------------- #

    def update_graphic_board_size(self):
        # Atualiza o tamanho do tabuleiro.

        if self.mode != BoardMode.PLAY_MODE:
            return

        new_size = self.board_size / self.current_order
        for i in range(self.current_order):
            for j in range(self.current_order):
                self.graphic_board[i][j]\
                    .setFixedSize(new_size, new_size)

# ---------------------------------------------------------------------------- #

    def update_edit_graphic_board_text(self):
        if self.mode != BoardMode.EDIT_MODE:
            return

        self.mode = BoardMode.UNSTABLE_MODE

        for i in range(self.current_order):
            for j in range(self.current_order):
                    self.graphic_edit_board[i][j]\
                        .setCurrentText(str(self.logic_board[i][j]))

        self.mode = BoardMode.EDIT_MODE

# ---------------------------------------------------------------------------- #

    def update_edit_graphic_board_size(self):
        if self.mode != BoardMode.EDIT_MODE:
            return

        new_size = self.board_size / self.current_order
        for i in range(self.current_order):
            for j in range(self.current_order):
                self.graphic_edit_board[i][j]\
                    .setFixedSize(new_size, new_size)

# ---------------------------------------------------------------------------- #

    def set_order(self, order):
        if order > self.max_order:
            print("Invalid order")
            return

        self.current_order = order
        self.logic_board = self.create_logic_board(order)
        self.set_final_state()

        self.update_graphic_board()

# ---------------------------------------------------------------------------- #

    def piece_click(self, coord):
        if self.mode != BoardMode.PLAY_MODE:
            return

        i, j = coord
        current_value = self.logic_board[i][j]

        # Up.
        if i - 1 >= 0 and self.logic_board[i - 1][j] == 0:
            self.logic_board[i][j] = self.logic_board[i - 1][j]
            self.logic_board[i - 1][j] = current_value

        # Down.
        elif i + 1 < self.current_order and self.logic_board[i + 1][j] == 0:
            self.logic_board[i][j] = self.logic_board[i + 1][j]
            self.logic_board[i + 1][j] = current_value

        # Left.
        elif j - 1 >= 0 and self.logic_board[i][j - 1] == 0:
            self.logic_board[i][j] = self.logic_board[i][j - 1]
            self.logic_board[i][j - 1] = current_value

        # Right.
        elif j + 1 < self.current_order and self.logic_board[i][j + 1] == 0:
            self.logic_board[i][j] = self.logic_board[i][j + 1]
            self.logic_board[i][j + 1] = current_value

        self.update_graphic_board()

# ---------------------------------------------------------------------------- #

    def widget_board(self):
        # Desenha o tabuleiro usando o PyQT.
        grid_board = QGridLayout()
        grid_board.setSpacing(0)

        for i in range(self.current_order):
            for j in range(self.current_order):
                grid_board.addWidget(self.graphic_board[i][j], i, j)
                grid_board.addWidget(self.graphic_edit_board[i][j], i, j)

        board_widget = QWidget()
        board_widget.setLayout(grid_board)

        return board_widget

# ---------------------------------------------------------------------------- #

    def enable_edit_mode(self, value):
        self.mode = BoardMode.UNSTABLE_MODE

        valid_values = [v for v in range(self.current_order ** 2)]
        for i in range(self.current_order):
            for j in range(self.current_order):
                self.graphic_edit_board[i][j].clear()

                self.graphic_edit_board[i][j]\
                    .addItems([str(vl) for vl in valid_values])

                self.graphic_edit_board[i][j]\
                    .setCurrentText(str(self.logic_board[i][j]))

        self.mode = BoardMode.EDIT_MODE if value else BoardMode.PLAY_MODE
        self.update_graphic_board()

        mode = str(self.mode).split('.')[1]
        self.message.setText("Board is in {0} mode".format(mode))

# ---------------------------------------------------------------------------- #

    def select_piece_value_edit_mode(self, coord):
        if self.mode == BoardMode.UNSTABLE_MODE:
            return

        i, j = coord
        value = self.graphic_edit_board[i][j].currentText()

        self.mode = BoardMode.UNSTABLE_MODE

        (i_to_subs, j_to_subs), not_used_value = \
            self.find_unsigned_value_and_point(value, coord)

        self.graphic_edit_board[i_to_subs][j_to_subs]\
            .setCurrentText(str(not_used_value))

        self.logic_board[i_to_subs][j_to_subs] = not_used_value
        self.logic_board[i][j] = int(value)

        self.mode = BoardMode.EDIT_MODE

# ---------------------------------------------------------------------------- #

    def find_unsigned_value_and_point(self, value, coord):
        i, j = coord
        i_to_subs, j_to_subs = -1, -1

        valid_values = [x for x in range(self.current_order ** 2)]
        for _i in range(self.current_order):
            for _j in range(self.current_order):
                cm_value = int(self.graphic_edit_board[_i][_j].currentText())
                if cm_value in valid_values:
                    valid_values.remove(cm_value)

                if cm_value == int(value) and not (_i == i and _j == j):
                    i_to_subs, j_to_subs = _i, _j

        #assert
        if len(valid_values) != 1:
            print("Error: inconsistency at "  +\
                  self.__class__.__name__ + "." +\
                  self.find_unsigned_value_and_point.__name__)

            exit(1)

        return ((i_to_subs, j_to_subs), valid_values[0])

# ---------------------------------------------------------------------------- #

    def graphic_board_mode(self):
        play_mode_btn = QPushButton("PLAY MODE")
        play_mode_btn.clicked.connect(\
            lambda pq, value = False: self.enable_edit_mode(value))

        edit_mode_btn = QPushButton("EDIT MODE")
        edit_mode_btn.clicked.connect(\
            lambda pq, value = True: self.enable_edit_mode(value))

        h_layout = QHBoxLayout()
        h_layout.addWidget(play_mode_btn)
        h_layout.addWidget(edit_mode_btn)

        component = QWidget()
        component.setLayout(h_layout)

        return component

# ---------------------------------------------------------------------------- #

    def get_logic_board(self):
        return self.logic_board

# ---------------------------------------------------------------------------- #

    def set_logic_board(self, board):
        len_of_board = len(board)
        if len_of_board > self.max_order:
            print("len is too big")
            exit(-1)

        self.current_order = len_of_board
        self.logic_board = board
        self.update_graphic_board()

# ---------------------------------------------------------------------------- #

    def graphic_order(self):
        cross = lambda i: str(i) + "x" + str(i)
        combobox = QComboBox()
        combobox.addItems([cross(x) for x in range(3, self.max_order + 1)])
        combobox.setCurrentIndex(self.current_order - 3)
        combobox.currentIndexChanged\
                .connect(\
                    lambda arg, cbb = combobox:self.process_graphic_order(cbb))

        return combobox

# ---------------------------------------------------------------------------- #

    def process_graphic_order(self, cbb):
        new_order = int(cbb.currentText()[0])
        self.set_order(new_order)
        self.message.setText("New order: [{0}x{0}]".format(new_order))

# ---------------------------------------------------------------------------- #

    def set_final_state(self):
        self.final_state = deepcopy(self.logic_board)


# ---------------------------------------------------------------------------- #

    def get_final_state(self):
        return self.final_state

# ---------------------------------------------------------------------------- #

    def graphic_final_state(self):
        button = QPushButton()
        button.setText("&Set &Final &State")

        button.clicked.connect(\
            lambda arg: self.set_final_state())

        button.clicked.connect(\
            lambda arg, msg="Final State Changed": self.message.setText(msg))

        return button

# ---------------------------------------------------------------------------- #

    def graphic_select_solution_method(self):
        combobox = QComboBox()
        combobox.addItems([
            "What Search Algorithm do you want?",
            "BFS",
            "DFS + Iterative Approach",
            "DFS + Recursive Approach",
            "A ★ + Pieces out of Place",
            "A ★ + Manhattan Distance"])
        combobox.currentTextChanged\
                .connect(lambda arg, method = combobox: self.find_solution(method))

        return combobox

# ---------------------------------------------------------------------------- #

    def find_solution(self, method):
        if self.mode == BoardMode.UNSTABLE_MODE:
            return

        self.mode = BoardMode.UNSTABLE_MODE

        method_selected = method.currentText()

        self.solution = None
        self.step = 0

        self.message.setText("Search solution...")

        start_time = datetime.datetime.now()

        if method_selected == "BFS":
            self.solution = BFS_solution(self.logic_board, self.final_state)

        elif method_selected == "DFS + Iterative Approach":
            self.solution = \
                DFS_Iter_solution(\
                    self.logic_board,\
                    self.final_state,\
                    self.max_tolerable_solution_depth)

        elif method_selected == "DFS + Recursive Approach":
            self.solution = \
                DFS_Recr_solution(\
                    self.logic_board,\
                    self.final_state,\
                    self.max_tolerable_solution_depth)

        elif method_selected == "A ★ + Pieces out of Place":
            self.solution =\
                AStar_H1_solution(\
                    self.logic_board,\
                    self.final_state)

        elif method_selected == "A ★ + Manhattan Distance":
            self.solution =\
                AStar_H2_solution(\
                    self.logic_board,\
                    self.final_state)

        else:
            print("Any method was selected.")

        # Calcula o tempo necessário para encontrar a resposta.
        elapsed_time = datetime.datetime.now() - start_time

        method.setCurrentIndex(0)

        message_solution  = "Method: %s:\n"%(method_selected)

        message_solution += "Solution: %s\n"%(\
            "Found" if len(self.solution.states) > 0 else "Unfound")

        message_solution += "Nodes: %d | Duration: %02d:%02d.%.03d\n"%\
                    (self.solution.num_nodes, int(elapsed_time.seconds/60),\
                    elapsed_time.seconds, elapsed_time.microseconds)

        self.message.setText(message_solution )
        self.mode = BoardMode.PLAY_MODE

# ---------------------------------------------------------------------------- #

    def graphic_select_depth(self):
        label = QLabel()
        label.setFixedWidth(25)
        label.setText(str(self.max_tolerable_solution_depth).zfill(2))

        slider = QSlider()
        slider.setRange(1, 30)
        slider.setValue(self.max_tolerable_solution_depth)
        slider.setOrientation(Qt.Horizontal)
        slider.valueChanged\
              .connect(lambda arg, comp = slider, clbl = label: self.selected_depth(comp, clbl))

        h_layout = QHBoxLayout()
        h_layout.addWidget(slider)
        h_layout.addWidget(label)

        widget = QWidget()
        widget.setLayout(h_layout)

        return widget

# ---------------------------------------------------------------------------- #

    def selected_depth(self, comp, lbl):
        self.max_tolerable_solution_depth = comp.value()
        lbl.setText(str(self.max_tolerable_solution_depth).zfill(2))

# ---------------------------------------------------------------------------- #

    def graphic_solution_iteraction(self):
        back_step = QPushButton()
        back_step.setIcon(QIcon(BASE_DIR + "/resources/left.png"))
        back_step.clicked.connect(lambda arg: self.back_step_solution())

        begin_step = QPushButton()
        begin_step.setIcon(QIcon(BASE_DIR + "/resources/play.png"))
        begin_step.clicked.connect(lambda arg: self.begin_step_solution())

        foward_step = QPushButton()
        foward_step.setIcon(QIcon(BASE_DIR + "/resources/right.png"))
        foward_step.clicked.connect(lambda arg: self.foward_step_solution())

        h_layout = QHBoxLayout()
        h_layout.addWidget(back_step)
        h_layout.addWidget(begin_step)
        h_layout.addWidget(foward_step)

        widget = QWidget()
        widget.setLayout(h_layout)
        return widget

# ---------------------------------------------------------------------------- #

    def back_step_solution(self):
        self.step = max(self.step - 1, 0)
        self.message.setText("Step Back [{0}/{1}]"\
            .format(self.step + 1, len(self.solution.states)))

        if self.solution != None:
            self.set_logic_board(self.solution.states[self.step])


# ---------------------------------------------------------------------------- #

    def begin_step_solution(self):
        self.step = 0
        self.message.setText("Step Begin [{0}/{1}]"\
            .format(self.step + 1, len(self.solution.states)))

        if self.solution != None:
            self.set_logic_board(self.solution.states[self.step])

# ---------------------------------------------------------------------------- #

    def foward_step_solution(self):
        self.step = min(self.step + 1, len(self.solution.states) - 1)
        self.message.setText("Step Foward [{0}/{1}]"\
            .format(self.step + 1, len(self.solution.states)))

        if self.solution != None:
            self.set_logic_board(self.solution.states[self.step])

# ---------------------------------------------------------------------------- #


    def graphic_status(self):
        label = QLabel("Status:")
        label.setAlignment(Qt.AlignLeft)

        self.message = QLabel()
        self.message.setAlignment(Qt.AlignRight)


        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(self.message)

        window = QWidget()
        window.setLayout(h_layout)

        return window

class Main:
    def __init__(self):

        app = QApplication([])

        board = Board(9)

        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(board.widget_board())
        vBoxLayout.addWidget(board.graphic_final_state())
        vBoxLayout.addWidget(board.graphic_board_mode())
        vBoxLayout.addWidget(board.graphic_order())
        vBoxLayout.addWidget(board.graphic_select_depth())
        vBoxLayout.addWidget(board.graphic_select_solution_method())
        vBoxLayout.addWidget(board.graphic_solution_iteraction())
        vBoxLayout.addWidget(board.graphic_status())

        window = QWidget()
        window.setWindowTitle("N Pieces Sliding Puzzle: AI")
        window.setLayout(vBoxLayout)
        window.show()

        app.exec_()

Main()
