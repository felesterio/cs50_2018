from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""

    # in each cell, tuple(cost, Operation.DELETED/INSERTED/SUBSTITUTED), in [0][0] store (0, NONE)

    # set up 2D list, i is row, j is column
    cost = []
    for num in range(len(a) + 1):
        cost.append([])

    cost[0].append((0, None))

    # FIRST ROW
    for j in range(1, len(b) + 1):
        cost[0].append((j, Operation.INSERTED))

    # FIRST COLUMN
    for i in range(1, len(a) + 1):
        cost[i].append((i, Operation.DELETED))

    # recursion function, fill in entry
    # fill in by rows
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):

            three_choices = []
            # insertion cost[i][j-1] + 1
            insert_cost = cost[i][j - 1][0] + 1
            three_choices.append(insert_cost)

            # deletion cost[i-1][j] +1
            delete_cost = cost[i - 1][j][0] + 1
            three_choices.append(delete_cost)

            # substitution cost[i-1][j-1] + 2 or 0
            if a[i - 1] == b[j - 1]:
                x = 0
            else:
                x = 1
            sub_cost = cost[i - 1][j - 1][0] + x
            three_choices.append(sub_cost)

            final_cost = min(three_choices)
            index = three_choices.index(final_cost)

            if index == 0:
                move = Operation.INSERTED
            elif index == 1:
                move = Operation.DELETED
            elif index == 2:
                move = Operation.SUBSTITUTED

            cost[i].append((final_cost, move))

    return cost