import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

from Sdk_jg import maker

kivy.require('2.0.0')


class SudokuApp(App):
    def build(self):
        self.puzzle, self.solu = maker('inicio')
        self.soluOn = False
        self.selected_cell = None

        # Criando o layout principal como FloatLayout
        self.main_layout = FloatLayout()

        # imagem de fundo
        img = Image(source='snup.jpg', fit_mode='fill')
        self.main_layout.add_widget(img)

        # Criando a grade de Sudoku
        self.grid = GridLayout(cols=9, rows=9, padding=10, spacing=2,
                               size_hint=(None, None), size=(600, 600),
                               pos_hint={'center_x': 0.5, 'center_y': 0.54})

        self.cells = []
        for row in range(9):
            row_cells = []
            for col in range(9):
                btn = Button(font_size=30, size_hint=(None, None), width=60, height=60,
                             background_normal='', background_color=self.destaque(row, col))
                btn.bind(on_press=self.cell_pressed)
                row_cells.append(btn)
                self.grid.add_widget(btn)
            self.cells.append(row_cells)

        # botando os botoes sobre a imagem de fundo
        self.main_layout.add_widget(self.grid)

        #cronometro
        self.timer_seconds = 0
        self.timer_label = Label(text="Tempo: 00:00", font_size=25, size_hint=(None, None), size=(200, 50),
                                 pos_hint={'top': 1, 'center_x': 0.5})
        self.main_layout.add_widget(self.timer_label)

        #verificar resposta
        control_layout = BoxLayout(size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'y': 0.095})
        self.solve_btn = Button(text="Terminar jogo", on_press=self.show_solution, background_normal='',
                                background_color=(0, 0.75, 0, 1), color=(0, 0, 0, 0.8))
        control_layout.add_widget(self.solve_btn)
        dificuldade_layout = BoxLayout(size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'y': 0.02})

        #cores dos botoes
        facil_btn = Button(
            text="Fácil",
            on_press=lambda instance: self.change_dificuldade('facil'),
            background_normal='',
            background_color=(1, 0.8, 0, 1),  # Amarelo
            color=(0, 0, 0, 0.8)  # Texto PRETO
        )

        medio_btn = Button(
            text="Médio",
            on_press=lambda instance: self.change_dificuldade('medio'),
            background_normal='',
            background_color=(1, 0.5, 0, 1),  # LARANJA
            color=(0, 0, 0, 0.8)  # Texto preto
        )

        dificil_btn = Button(
            text="Difícil",
            on_press=lambda instance: self.change_dificuldade('dificil'),
            background_normal='',
            background_color=(1.9, 0, 0, 1.5),  # VERMELHO
            color=(0, 0, 0, 0.8)  # Texto PRETO
        )

        dificuldade_layout.add_widget(facil_btn)
        dificuldade_layout.add_widget(medio_btn)
        dificuldade_layout.add_widget(dificil_btn)

        self.main_layout.add_widget(control_layout)
        self.main_layout.add_widget(dificuldade_layout)

        self.update_grid()
        return self.main_layout

    #destaca as grades em azul claro
    def destaque(self, row, col):
        if (row // 3 + col // 3) % 2 == 0:  #multiplos de 3
            return (0.8, 0.9, 1, 1)  # Azul claro para criar contraste
        return (1, 1, 1, 1)  # Branco

    def update_grid(self):
        for row in range(9):
            for col in range(9):
                btn = self.cells[row][col]
                num = self.puzzle[row][col]

                if num != '':
                    btn.text = str(num)
                    btn.color = (0, 0, 0, 1)  # Preto para números fixos
                else:
                    btn.text = ""

                btn.background_color = self.destaque(row, col)

    def cell_pressed(self, instance):
        """Destaca a célula selecionada e sua linha/coluna."""
        if self.selected_cell:
            row, col = self.get_cell_position(self.selected_cell)
            self.selected_cell.background_color = self.destaque(row, col)

        self.selected_cell = instance
        row, col = self.get_cell_position(instance)

        # Destaca linha e coluna
        for i in range(9):
            self.cells[row][i].background_color = (0.8, 0.9, 1, 1)  # Azul claro
            self.cells[i][col].background_color = (0.8, 0.9, 1, 1)

        instance.background_color = (0.5, 0.7, 1, 1)  # Azul escuro para célula selecionada

    def get_cell_position(self, cell):
        for row in range(9):
            if cell in self.cells[row]:
                return row, self.cells[row].index(cell)
        return None, None

    def update_grid(self):
        """Atualiza a grade com os números e solução"""
        for row in range(9):
            for col in range(9):
                btn = self.cells[row][col]
                num = self.puzzle[row][col]

                if type(num) == str and num != '' and self.soluOn:  # Se o numero for do tipo string
                    if btn.text == str(self.solu[row][col]):  # Mostrar a solução
                        btn.color = (0, 1.7, 0, 1)  # Verde para certo
                    else:
                        btn.color = (1, 0, 0, 1)  #vermelho para errado
                    btn.text = str(self.solu[row][col])
                elif type(num) == str and num != '':
                    btn.text = num  # Numero de entrada
                elif type(num) == int and num != '':
                    btn.text = str(num)  # Mostrar numeros estáticos
                    btn.color = (0, 0, 0, 1)  # Preto para numeros estáticos
                else:
                    btn.text = ""

    def show_solution(self, instance):
        """Exibe as soluções de Sudoku"""
        self.soluOn = True
        self.update_grid()
        self.solve_btn.disabled = True
        achou = False
        for r in range(9):
            for c in range(9):
                if self.cells[r][c] == '':
                    achou = True

        if achou == False:  # nao tem casa vazia
            Clock.unschedule(self.update_timer)

    def new_game(self, instance):
        """Inicia um novo jogo"""
        self.puzzle, self.solu = maker(self.current_dificuldade)  # Usa a dificuldade atual
        self.soluOn = False
        self.update_grid()

    #niveis por difculdade
    def change_dificuldade(self, dificuldade):
        """Altera a dificuldade e gera um novo jogo"""
        self.current_dificuldade = dificuldade
        self.new_game(None)  # Gera um novo jogo com a nova dificuldade
        self.solve_btn.disabled = False

    def cell_pressed(self, instance):
        """Ação ao pressionar um quadrado"""
        if instance.text in '' or (0, 0, 1, 1.5):
            self.selected_cell = instance
            self.open_input_popup()

    def open_input_popup(self):
        """Abre um popup para inserir um número"""
        input_popup = Popup(title="Insira um valor",
                            size_hint=(None, None), size=(400, 400))
        popup_layout = BoxLayout(orientation='vertical')

        # Campo de entrada de texto
        text_input = TextInput(font_size=40, multiline=False, size_hint_y=1)
        popup_layout.add_widget(text_input)

        # Botões numéricos
        num_layout = GridLayout(cols=3, size_hint_y=1)
        for num in range(1, 10):
            button = Button(text=str(num), on_press=lambda instance, n=num: self.fill_value(n, text_input, input_popup))
            num_layout.add_widget(button)
        clear_btn = Button(text="Limpar", on_press=lambda instance: self.clear_value(text_input, input_popup))
        num_layout.add_widget(clear_btn)

        popup_layout.add_widget(num_layout)
        input_popup.content = popup_layout
        input_popup.open()

    def fill_value(self, num, text_input, popup):
        """Preenche o número na célula selecionada"""
        if self.selected_cell:
            self.selected_cell.text = str(num)
            self.selected_cell.color = (0, 0, 1, 1.5)
            row, col = self.get_cell_position(self.selected_cell)
            self.puzzle[row][col] = str(num)  # Atualiza com o valor inserido
        text_input.text = ""  # Limpa o campo de entrada
        popup.dismiss()  # Fecha o popup

    def clear_value(self, text_input, popup):
        """Limpa a célula selecionada"""
        if self.selected_cell:
            self.selected_cell.text = ""
            row, col = self.get_cell_position(self.selected_cell)
            self.puzzle[row][col] = ' '  # Limpa a célula do puzzle
        text_input.text = ""  # Limpa o campo de entrada
        popup.dismiss()  # Fecha o popup

    def get_cell_position(self, cell):
        """Retorna a posição da célula na grade"""
        for row in range(9):
            if cell in self.cells[row]:
                return row, self.cells[row].index(cell)
        return None, None

    def update_timer(self, dt):
        self.timer_seconds += 1
        minutos = self.timer_seconds // 60
        segundos = self.timer_seconds % 60
        self.timer_label.text = f"Tempo: {minutos:02}:{segundos:02}"

    def new_game(self, instance):
        """Inicia um novo jogo e reseta o tempo"""
        self.puzzle, self.solu = maker(self.current_dificuldade)
        self.soluOn = False
        self.timer_seconds = 0  # Reseta o timer
        self.timer_label.text = "Tempo: 00:00"

        Clock.unschedule(self.update_timer)  # Para o timer antigo
        Clock.schedule_interval(self.update_timer, 1)  # Inicia um novo timer

        self.update_grid()


if __name__ == "__main__":
    app = SudokuApp()
    app.current_dificuldade = 'inicio'  # Dificuldade padrão
    app.run()
