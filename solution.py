assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)
diagonal1 = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
diagonal2 = ['I1','H2','G3','F4','E5','D6','C7','B8','A9']

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unitlist:
        found_twin = False
        temp_pairs = {}
        for box in unit:
            twins = []
            if(len(values[box]) == 2):
                temp_pairs[box] = values[box]
            #now for each dictionary values check which two values are same and record it...
        for i in temp_pairs.keys():
            count = 0
            temp = temp_pairs[i]
            for j in temp_pairs.keys():
                temp1 = temp_pairs[j];
                if(temp1 == temp and count == 0):
                    count = count + 1
                    continue
                if(temp1 == temp and count == 1):
                    #a twin is found...There can be only one twin pairs in a unit so break out of the loop..
                    twins = [i, j]
                    found_twin = True
                    break
            if(found_twin):
                break
    # Eliminate the naked twins as possibilities for their peers
        #now eliminating the possible values for the other boxes in the unit...

        if(found_twin):
            twin_values = [values[twins[0]][0], values[twins[0]][1]]
            #find the shared peers for the twins...
            shared_peers = []
            for i in peers[twins[0]]:
                for j in peers[twins[1]]:
                    if(i == j):
                        shared_peers.append(i)
            for item in shared_peers:
                if(twin_values[0] in values[item]):
                    #eliminate these values..
                    my_string = values[item]
                    #values[item] = my_string.replace(twin_values[0], '')
                    values = assign_value(values,item,my_string.replace(twin_values[0],''))
                if(twin_values[1] in values[item]):
                    my_string = values[item]
                    #values[item] = my_string.replace(twin_values[1], '')
                    values = assign_value(values, item, my_string.replace(twin_values[1], ''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    my_dict = {}
    i = 0
    all_values = '123456789'
    for item in boxes:
        if (grid[i] == '.'):
            my_dict[item] = all_values
        elif (grid[i] in all_values):
            my_dict[item] = grid[i]
        i = i + 1
    return my_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF' : print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.
    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    fill_box_list = []
    for item in boxes:
        if (len(values[item]) == 1):
            fill_box_list.append(item)
    for item in boxes:
        if (item in fill_box_list):

            # here is a box with a single value..
            for i in peers[item]:
                if (values[item] in values[i]):
                    # remove that from the string..
                    my_string = values[i]
                    #values[i] = my_string.replace(values[item], '')
                    values = assign_value(values,i,my_string.replace(values[item], ''))
            #for eliminating values pertaining to the diagonals...
            if(item in diagonal1):
                for i in diagonal1:
                    if(i != item and values[item] in values[i]):
                        #remove that digit from the string of the box present in diagonal1
                        my_string = values[i]
                        #values[i] = my_string.replace(values[item],'')
                        values = assign_value(values, i, my_string.replace(values[item], ''))
            if(item in diagonal2):
                for i in diagonal2:
                    if(i != item and values[item] in values[i]):
                        #remove that digit from the string of the box present in diagonal1
                        my_string = values[i]
                        #values[i] = my_string.replace(values[item],'')
                        values = assign_value(values, i, my_string.replace(values[item], ''))

    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
        """
    for unit in unitlist:
        for digit in cols:
            count = 0
            check_box = 'NA'
            found = False
            for box in unit:
                if (digit in values[box]):
                    count = count + 1
                    check_box = box
                    found = True
                if (count > 1):
                    found = False
                    break
            if (found == True):
                #values[check_box] = digit
                values = assign_value(values,check_box,digit)
    #Now for handling the diagonal sudoku..
    for digit in cols:
        count = 0
        check_box = 'NA'
        found = False
        for box in diagonal1:
            if (digit in values[box]):
                count = count + 1
                check_box = box
                found = True
            if (count > 1):
                found = False
                break
        if (found == True):
            #values[check_box] = digit
            values = assign_value(values, check_box, digit)
    for digit in cols:
        count = 0
        check_box = 'NA'
        found = False
        for box in diagonal2:
            if (digit in values[box]):
                count = count + 1
                check_box = box
                found = True
            if (count > 1):
                found = False
                break
        if (found == True):
            #values[check_box] = digit
            values = assign_value(values, check_box, digit)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        #use the naked twins strategy
        values = naked_twins(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        #new_sudoku[s] = value
        new_sudoku = assign_value(new_sudoku,s,value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)



if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
