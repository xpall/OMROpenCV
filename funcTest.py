def alignGrading(grading):
    alignedGrades = [
        [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], 
        [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], 
        [0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 
        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
        ]
    rowNumber = 0
    itemNumber = 0
    for item in grading:
        if itemNumber < 20:
            alignedGrades[rowNumber][0] = item
            itemNumber += 1
            rowNumber += 1
        elif itemNumber < 40:
            alignedGrades[rowNumber - 20][1] = item
            itemNumber += 1
            rowNumber += 1
        else:
            alignedGrades[rowNumber - 30][2] = item
            rowNumber += 1
    return alignedGrades

grading = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
print(alignGrading(grading))