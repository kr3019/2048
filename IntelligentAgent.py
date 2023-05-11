"""
Created on Tue Nov  8 19:38:42 2022

@author: kanupriyaraheja
"""

import time
import math
from BaseAI import BaseAI


time_limit = .2
INFINITY = float('inf')
direc = [0, 1, 2, 3]


class IntelligentAgent(BaseAI):
    
    #function to get move
    def getMove(self, grid):
        self.prev_time = time.perf_counter()
        util_max = -INFINITY
        move = 0
        alpha = -INFINITY
        beta = INFINITY
        for d in direc:
            grid_copy = grid.clone()
            if not grid_copy.move(d):
                continue
            temp = self.expectiminimax(grid_copy,alpha,
                    beta,1.0, 1)
            if util_max >= beta:
                break
            if util_max > alpha:
                alpha = util_max
            if temp > util_max:
                move=d
                util_max = temp

        return move
    
    #expectiminimax with alpha beta pruning
    def expectiminimax(
        self,
        grid,
        alpha,
        beta,
        probability,
        depth
        ):

        if depth == 0 or self.checktime(time.perf_counter()):
            return self.heuristic(grid)
        number_of_empty_tiles = len(grid.getAvailableCells())
        min_temp = INFINITY
        for i in range(4):
            for j in range(4):
                if grid.map[i][j] == 0:
                    row = list(grid.map[i]) 
                    temp = 0
                    porbability_sum = 0
                    for (p, val) in ((0.1, 4), (0.9, 2)):
                        p_product = p * probability
                        if 0.9 * p_product < 0.1 and number_of_empty_tiles > 4:
                            continue
                        row[j] = val
                        grid.map[i] = row
                        temp += p * self.maximize(grid,alpha, beta,p_product,depth)
                        porbability_sum += p
                    row[j] = 0  
                    grid.map[i] = row  
                    if porbability_sum == 0:
                        temp = self.heuristic(grid)
                    else:
                        temp /= porbability_sum
                    if temp < min_temp:
                        min_temp = temp
                    if min_temp <= alpha:
                        break
                    if min_temp < beta:
                        beta = min_temp
        return min_temp

    # maximize step

    def maximize(
        self,
        grid,
        alpha,
        beta,
        probability,
        depth
        ):

        util_max = -INFINITY
        for d in direc:
            grid_copy = grid.clone()
            successful = grid_copy.move(d)
            if not successful:
                continue
            temp = self.expectiminimax(grid_copy,  alpha, beta,probability,depth - 1)
            if temp > util_max:
                util_max = temp
            if util_max >= beta:
                break
            if util_max > alpha:
                alpha = util_max
        return util_max

    
    #monotonocity heuristic
    def monotone_heuristic(self,grid):
        val1=0
        val2=0
        val3=0
        val4=0
        
        log2 = math.log(2)

        for i in range(4):
            
            curr_value = 0
            
            next_value = curr_value + 1
            
            grid_map = grid.map
            while next_value < 4:
                while next_value < 4 and grid_map[i][next_value]==0:
                    next_value = next_value+1
                if next_value >= 4:
                    next_value = next_value-1
                curr=0
                next=0
                if grid_map[i][curr_value]:
                    curr = math.log(grid_map[i][curr_value])/log2
                if grid_map[i][next_value]:
                    next = math.log(grid_map[i][next_value])/log2
                if curr > next:
                    val1 += next - curr
                elif next > curr:
                    val2 += curr - next
                curr_value = next_value
                next_value += 1
                
        for i in range(4):
            
            curr_value = 0
            
            next_value = curr_value + 1
            
            grid_map = grid.map
            while next_value < 4:
                while next_value < 4 and grid_map[next_value][i]==0:
                    next_value = next_value+1
                if next_value >= 4:
                    next_value = next_value-1
                curr=0
                next=0
                if grid_map[curr_value][i]:
                    curr = math.log(grid_map[curr_value][i])/log2
                if grid_map[i][next_value]:
                    next = math.log(grid_map[next_value][i])/log2
                if curr > next:
                    val3 += next - curr
                elif next > curr:
                    val4 += curr - next
                curr_value = next_value
                next_value += 1

        return max(val1, val2) + max(val3, val4)


    #corner heuristic 
    def corner_heuristic(self, grid):
        a=0
        grid_map=grid.map
        for i in range(4):
            for j in range(4):
                if (grid_map[i][j] != 0):
                    a=a+grid_map[i][j]*(i*i*j*j)
        return a
    
    #identical heuristic
    def identitcal_heuristic(self, grid):
        a=0
        grid_map=grid.map
        for i in range(3):
            for j in range(4):
                if grid.map[i][j] == grid.map[i + 1][j]:
                    a=a+grid_map[i][j]

        for i in range(4):
            for j in range(3):
                if grid_map[i][j] == grid_map[i][j + 1]:
                    a=a+grid_map[i][j]
        return a

    #heuristic aggregator fun    
    def heuristic(self, grid):
        no_of_available= len(grid.getAvailableCells())
        non_emp_heuristic = 4*4 - no_of_available
        h = self.corner_heuristic(grid) + self.identitcal_heuristic(grid) + self.smoothness_heuristic(grid) + self.monotone_heuristic(grid) - non_emp_heuristic ** 2;
        return h

    # smoothness heuristic
    def smoothness_heuristic(self, grid):
        smoothness = 0
        grid_map = grid.map
        for i in range(4):
            for j in range(4):
                if grid_map[i][j] == 0:
                    grid_map[i][j] = 2
        for i in range(4):
            for j in range(4):
                temp = INFINITY

                if i > 0:
                    temp = min(temp, abs(grid_map[i][j] - grid_map[i
                               - 1][j]))
                if j > 0:
                    temp = min(temp, abs(grid_map[i][j] - grid_map[i][j
                               - 1]))
                if i < 3:
                    temp = min(temp, abs(grid_map[i][j] - grid_map[i
                               + 1][j]))
                if j < 3:
                    temp = min(temp, abs(grid_map[i][j] - grid_map[i][j
                               + 1]))

                smoothness = smoothness - temp

        return smoothness

    def checktime(self, currrent_time):
        if currrent_time - self.prev_time <= time_limit:
            return False
        else:
            self.finish = True
            return True