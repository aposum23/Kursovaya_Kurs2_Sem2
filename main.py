import json
import PySimpleGUI as sg


versh_arr = []


def obhod(graf, find, versh=0):
    global versh_arr
    if versh == len(graf):
        return
    cur_versh = versh
    for num, elem in enumerate(graf[versh]):
        if elem != 0 and num > cur_versh:
            if elem == find:
                if not str(num + 1) in versh_arr:
                    print(f'versh: {num + 1}')
                    versh_arr.append(str(num + 1))
                return
            else:
                versh = obhod(graf, find, num)
    return cur_versh


def make_window(type):
    sg.theme('DarkAmber')
    layout_open = [[sg.Button('Открыть файл'), sg.Button('Создать файл')],
                   [sg.Text('Выберите json файл:'),
                    sg.InputText(),
                    sg.FileBrowse('Выбрать файл')],
                   [sg.Text('Введите значение которое надо найти')],
                   [sg.InputText()],
                   [sg.Button('Найти')],
                   [sg.Button('Закрыть')]]
    layout_create = [[sg.Button('Открыть файл'), sg.Button('Создать файл')],
                     [sg.Text('Введите матрицу смежности вашего графа:')],
                     [sg.InputText()],
                     [sg.Text('Введите имя файла:')],
                     [sg.InputText()],
                     [sg.Button('Создать')],
                     [sg.Button('Закрыть')]]
    if type == 'open':
        window = sg.Window('Обход графа в глубину', layout_open)
    elif type == 'create':
        window = sg.Window('Обход графа в глубину', layout_create)

    return window


if __name__ == '__main__':
    window = make_window('open')
    graf = None
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Закрыть':
            break

        if event == 'Найти':
            try:
                file = values[0]
                with open(file, 'r') as file:
                    graf = json.load(file)
                find = values[1]
                versh = obhod(graf['graf'], int(find))
                sg.popup(f'Были найдены вершины с следующими номерами: {versh_arr}')
                versh_arr = []
            except Exception as e:
                print(e)
                sg.popup(f'Ошибка: {e}')

        if event == 'Создать файл':
            window.close()
            window = make_window('create')

        if event == 'Открыть файл':
            window.close()
            window = make_window('open')

        if event == 'Создать':
            val = json.loads(values[0])
            file = {'graf': val}
            with open(values[1] + '.json', 'w') as outfile:
                json.dump(file, outfile)
            sg.popup('Файл создан успешно!')
    window.close()
