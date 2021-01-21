import random

def recursive_backtracker(maze_graphics, maze):

    # W tej liście przechowujemy komórki labiryntu które już odwiedziliśmy, komórki z tej listy są potem przetwarzane
    # w pętli poniżej
    visited_stack = []

    # Ten algorytm startuje w losowym miejscu pustego jeszcze labiryntu, dlatego musimy wylosować
    # naszą pozycję
    init_x = random.randint(1, maze.x_size)
    init_y = random.randint(1, maze.y_size)

    # Jako że wybraliśmy już naszą pozycję początkową, to możemy ją oznaczyć jako odwiedzoną
    visited_stack.append([init_x, init_y])

    # W komórkach labiryntu możemy przechowywać różne informacje, które mogą nam pomóc w trakcie jego tworzenia,
    # w tym wypadku pomaga nam to natychmiast określić czy dana komórka była już odwiedzona ('V', z ang. visited).
    # Dodatkowo jest to informacja dla biblioteki do wyświetlania, w jakim stanie jest nasz labirynt.
    maze.set_cell(init_x, init_y, 'V')

    # Algorytm ściąga ze wspomnianej wcześniej listy odwiedzone komórki jedna po drugiej. W tym samym kroku, może też
    # dodać do niej kolejne komórki. Kiedy wszystko zostanie przetworzone, lista będzie pusta, a pętla skończy się.
    while visited_stack:
        # Pobieramy z listy ostatnio dodaną komórkę, nazwijmy ją aktualną
        current_cell = visited_stack.pop()

        # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
        maze.set_cell(current_cell[0], current_cell[1], 'C')

        # Bierzemy wszystkich sąsiadów (maks. 4) aktualnej komórki, którzy nie byli jeszcze odwiedzeni
        neighbours = maze.get_cell_not_visited_neighbours(current_cell[0], current_cell[1])

        # Jeśli nie ma takich sąsiadów, to algorytm nie ma gdzie się udać, dlatego sprawdzamy poprzenie komórki
        # z listy, aż nie uda nam się pójść dalej
        if not neighbours:
            # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
            maze_graphics.redraw(maze)

            # Oznaczamy aktualną komórkę jako odwiedzoną i przetworzoną (nie znajduje się już na liście)
            maze.set_cell(current_cell[0], current_cell[1], 'V')

            # Przechodzimy to kolejnej iteracji pętli
            continue

        # Jeśli aktualna komórka ma nieodwiedzonych sąsiadów, to dodajemy ją z powrotem do naszej listy, abyśmy byli
        # w stanie wrócić do niej rekurencyjnie
        visited_stack.append(current_cell)

        # Losowo wybieramy jednego z sąsiadów aktualnej komórki
        chosen_neighbour = random.choice(neighbours)

        # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
        maze.set_wall(current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], 'C')

        # Oznaczamy wybranego sąsiada jako odwiedzonego i dodajemy go do naszej listy
        maze.set_cell(chosen_neighbour[0], chosen_neighbour[1], 'V')
        visited_stack.append(chosen_neighbour)

        # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
        maze_graphics.redraw(maze)

        # Początkowo labirynt ma wszystkie ściany wypełnione, wraz z kolejnym krokami algorytmu kolejne ściany są
        # usuwane. W tym momencie następuje usunięcie ściany między aktualną komórką, a jej wybranym wcześniej sąsiadem
        maze.set_wall(current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], ' ')

        # Oznanczamy aktualną komórkę jako oznaczoną
        maze.set_cell(current_cell[0], current_cell[1], 'V')
