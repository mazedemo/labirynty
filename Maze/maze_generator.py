import random

def eller(maze_graphics, maze):

    def get_set(set_list, x_it, y_it):
        for set_it in set_list:
            if (x_it, y_it) in set_it:
                return set_it

    # W tej zmiennej przechowujemy informację o tym, ile zbiorów zostało utworzonych do tej pory.
    set_counter = 0
    sets = []


    # W tej pętli tworzymy osobny obszar (zbiór) dla każdej komórki pierwszego rzędu (Ilustracja 2.)
    for x in range(1, maze.x_size + 1):
        new_set = set()
        sets.append(new_set)
        sets[-1].add((x, 1))
        set_counter = set_counter + 1
        maze.set_cell(x, 1, set_counter)

    # W tym algorytmie chodzimy po wierszach, jeden po drugim, w przeciwieństwie do drugiego algorytmu, który działa
    # na pojedynczych komórkach i ich sąsiadach.
    for y in range(1, maze.y_size+1):

        # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
        maze_graphics.redraw(maze)

        # W tej pętli łączymy losowo zbiory znajdujące się w danym wierszu, robimy to poprzez usuwanie ścian między
        # między wylosowanymi komórkami, które są w różnych zbiorach (Ilustracja 3.)
        for x in range(1, maze.x_size):

            # W tym miejscu możemy wpływać na to jak często będziemy łączyć komórki
            if random.random() < 0.5 or y == maze.y_size:
                sets_ready = 0

                # Tutaj sprawdzamy czy w komórka w aktualnej kolumnie ma obcego sąsiada
                for set_t in sets:

                    if (x, y) in set_t:
                        if (x+1, y) in set_t:
                            break
                        set_a = set_t
                        sets_ready = sets_ready + 1
                    elif (x+1, y) in set_t:
                        set_b = set_t
                        sets_ready = sets_ready + 1

                    if sets_ready == 2:
                        break

                # Jeśli znajdziemy rzeczywiście jest mamy sąsiada z innego zbioru to wykonujemy poniższy blok kodu
                if sets_ready == 2:

                    # Usuwamy znalezione zbiory ze zbioru naszych zbiorów
                    sets.remove(set_a)
                    sets.remove(set_b)

                    # Łączymy znalezione zbiory
                    set_a = set_a.union(set_b)

                    # Dodajemy je jako jeden wspólny zbiór
                    sets.append(set_a)

                    # W tym miescu oznaczamy komórki które zostały wchłonięte do innego zbioru
                    for val in set_a:
                        maze.set_cell(val[0], val[1], maze.get_cell(x, y))

                    # Usuwamy naszą ścianę, po czym przechodzimy do kolejnej kolumny w pętli
                    maze.set_wall(x, y, x + 1, y, ' ')

        # Jeśli aktualny wiersz był naszym ostatnim, to algorytm kończy się
        if y == maze.y_size:
            return


        # Teraz musimy usunąć ściany do następnego wiersza, każdy zbiór powinien miec przynajmniej jedno takie
        # połączenie, gdyby tak nie było, to dany zbiór zostałby na stałe wyizolowany, przez co nasz algorytm
        # nie byłby idealny

        processed_sets = set()

        # Wybieramy losową kolejność kolumn w których będziemy rozważać usunięcie poziomej ściany do kolejnego wiersza
        x_range = list(range(1, maze.x_size+1))
        random.shuffle(x_range)

        # W tej pętli przechodzimy po kolumnach w losowej kolejności
        for x in x_range:
            # Tutaj mamy kolejny element losowy który możemy zmieniać. Jeśli dany zbiór nie ma jeszcze przejścia w dół,
            # to dodajemy je, jeśli natomiast posiada przynajmniej jedno takie przejście, to losowo określamy czy damy
            # mu kolejne (Ilustracja 4.)
            if (maze.get_cell(x, y) not in processed_sets) or random.random() < 0.5:
                processed_sets.add(maze.get_cell(x, y))
                maze.set_wall(x, y, x, y+1, ' ')
                maze.set_cell(x, y + 1, maze.get_cell(x, y))
                set_a = get_set(sets, x, y)
                sets.remove(set_a)
                set_a.add((x, y+1))
                sets.append(set_a)
            # Jeśli w danej kolumnie nie tworzymy przejścia, to musimy utworzyć nowy zbiór, w którym znajdzie się
            # tylko jedna komórka z następnego wiersza (Ilustracja 5.)
            else:
                new_set = set()
                sets.append(new_set)
                sets[-1].add((x, y+1))
                set_counter = set_counter + 1
                maze.set_cell(x, y+1, set_counter)
