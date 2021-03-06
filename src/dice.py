# Dice rolling
import numpy as np

def dice(dice_size):
    num = np.random.randint(1, int(dice_size))
    return num

def simple_dice(dice_size, dice_num):
    if (dice_size.isnumeric() and dice_num.isnumeric()):
        dice_size = int(dice_size)
        dice_num = int(dice_num)
        dice_val = np.array([], dtype=np.int64)
        for i in range(dice_num):
            dice_val = np.append(dice_val, dice(dice_size))
        msg = 'π²: ' + str(np.sum(dice_val)) + ' = ' + str(dice_val)
    else:
        msg = 'π²: γͺγγ·γ§γ³γδΈζ­£γ§γγ'
    return msg