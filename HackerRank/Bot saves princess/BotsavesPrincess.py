#!/usr/bin/python
def displayPathtoPrincess(n, grid):
    pos = [(n-1)/2 , (n-1)/2] #center of grid
    pr = list(tuple(((x,y) for x in range (0,n) for y in range(0,n) if grid[x][y] == 'p'))[0])
    st = []
    while pos != pr:
        if pos[1] == pr[1] and pos[0] < pr[0]: #same row
            st.append('RIGHT')
            pos[0] += 1
        if pos[1] < pr[1]:
            st.append('DOWN')
            pos[1] += 1
        if pos[1] == pr[1] and pos[0] > pr[0]: #same row
            st.append('LEFT')
            pos[0] -= 1
        if pos[1] > pr[1]:
            st.append('UP')
            pos[1] -= 1
    print('\n'.join(st))

#convert input into a list of lists:
m = int(input())
grid = []
for i in range(0, m):
    grid.append(list(input()))

displayPathtoPrincess(m, grid)
