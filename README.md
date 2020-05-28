# Checkers-Board-Search

In this exercise of Artificial intelligence course I build a function that checks for two checkers boards (on an
6×6 board) that given, if there is a chain of checkers legal moves that lead from the first board given to you to the second one. 
The board is a 2 dimensional array, in which a value of 0 indicates the place is empty, and the value of 1 indicates
there is a piece there. To simplify rules (and since there is no “other side”), a piece can disappear if it makes a move beyond the final (6th) line. So an agent making a move in line 6 will disappear.

The algorithms that implemented to solve the problems:

- **Hill climbing**
- **Simulated annealing**
- **Local beam search (k=3)**
- **Genetic algorithm**
- ** A*-heuristic search **

 T = T − T ∗ ( 1 min(𝑠𝑐𝑜𝑟𝑒)+𝑐𝑢𝑟𝑟𝑒𝑛𝑡(𝑠𝑐𝑜𝑟𝑒) )  
 
