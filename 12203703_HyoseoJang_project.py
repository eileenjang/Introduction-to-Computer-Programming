from cs1robots import *

load_world("project_easy_example.wld")
hubo = Robot(beepers = 0)
hubo.set_trace("blue")
cnt = 0
hubo.set_pause(0.01)

def turn_right():
    for i in range(3):
        hubo.turn_left()
        
    # U, L, D, R
dy = [1, 0, -1, 0]
dx = [0, -1, 0, 1]

# 돌아갈 수 있는 방향 기록
moves = list()
# 미래에 갈 수 있는 위치, 방향 기록
stack = list()
dirs = list()
# 미래에 갈 수 있는 선택지가 한 개 이상 있는 지점 기록
cross = list()
# 현재까지 방문했던 위치 기록
visit = list()


# node 위치에서 갈 수 있는 path 탐색 후 개수 반환
def check_path(node):
    global moves, visit, dirs, stack, cross
    global cur_face, cur_node
    
    cc = 0
    # 왼쪽으로 갈 수 있는지 확인
    if hubo.left_is_clear():
        new_face = (cur_face + 1) % 4
        nx = node[0] + dx[new_face]
        ny = node[1] + dy[new_face]

        new_node = (nx, ny)
        # 새로 탐색한 path가 이미 방문했거나, 이미 찾은 곳이라면 pass!
        if new_node not in visit and new_node not in stack:
            stack.append(new_node)
            dirs.append(new_face)
            cc = cc + 1
    # 오른쪽으로 갈 수 있는지 확인
    if hubo.right_is_clear():
        new_face = (cur_face - 1) % 4
        nx = node[0] + dx[new_face]
        ny = node[1] + dy[new_face]

        new_node = (nx, ny)
        if new_node not in visit and new_node not in stack:
            stack.append(new_node)
            dirs.append(new_face)   
            cc = cc + 1
    # 앞으로 갈 수 있는지 확인
    if hubo.front_is_clear():
        new_face = cur_face
        nx = node[0] + dx[new_face]
        ny = node[1] + dy[new_face]

        new_node = (nx, ny)
        if new_node not in visit and new_node not in stack:
            stack.append(new_node)
            dirs.append(new_face)
            cc = cc + 1
            
    return cc

# 현재 방향, 현재 위치
cur_face = 3
cur_node = (1, 1)
# 시작점을 방문했다고 표시
visit.append(cur_node)
path_cnt = check_path(cur_node)

# 모두 순회하고 시작점으로 다시 돌아올 수 있도록 +1
cross.append([cur_node, path_cnt + 1])
go_back = False

while cnt < 1000 and hubo._beeper_bag < 5:

    #### START OF YOUR OWN PROGRAM ###

    # In each iteration of this while loop, do something.
    # You may use various conditional statements including:
    # front_is_clear(), right_is_clear(), left_is_clear()
    # You can freely define new funtions.
    # Do not edit cs1robots.py but edit this file only.
    
    # 더 이상 갈 수 있는 path가 없는 경우 예외처리
    if len(cross) == 0:
        print ("no cross")
        break;
    
    # 길이 막혔을 때 돌아가다가, 갈림길을 만나면
    # 가능한 방향으로 이동하기 위해 뒤를 돈다
    if go_back and cur_node == cross[-1][0]:
        go_back = False

        new_face = (cur_face - 2) % 4
        while cur_face != new_face:
            hubo.turn_left()
            cur_face = (cur_face + 1) % 4
        
    # 길이 막혀 돌아가는 중
    if go_back:
        # 가장 최신으로 돌아가는 방향 확인
        face = moves.pop()
        # 현재 방향과 같으면 움직임
        if cur_face == face:
            hubo.move()
        # 방향이 다른 경우 같아질 때까지 회전 후 움직임
        else:
            while cur_face != face:
                hubo.turn_left()
                cur_face = (cur_face + 1) % 4    
            hubo.move()
            
        # 현재 위치 기록
        nx = cur_node[0] + dx[cur_face]
        ny = cur_node[1] + dy[cur_face]
        cur_node = (nx, ny)  

    # 앞으로 향하는 중
    else:
        # 더 이상 갈 수 있는 path가 없는 경우 예외처리
        if len(stack) == 0:
            print ("nowhere to go")
            break

        # 다음 이동해야 하는 위치와 방향 확인
        node = stack.pop()
        face = dirs.pop()
              
        # 현재 방향과 같으면 움직임    
        if cur_face == face:
            hubo.move()
        # 방향이 다른 경우 같아질 때까지 회전 후 움직임
        else:
            while cur_face != face:
                hubo.turn_left()
                cur_face = (cur_face + 1) % 4    
            hubo.move()
        
        # 가장 최신의 미래에 갈 수 있는 선택지에서 현재 위치 삭제
        if cur_node == cross[-1][0]:
            cross[-1][1] = cross[-1][1] - 1
            if cross[-1][1] == 0:
                cross.pop()
        
        # 현재 위치 방문했다고 기록, 돌아오기 위한 방향 기록
        cur_node = node
        visit.append(cur_node)
        moves.append((cur_face - 2) % 4)

        path_cnt = check_path(cur_node)
        # 현재 위치에서 갈 수 있는 방향이 없으면 돌아가기로 함
        if path_cnt == 0:
            go_back = True
        # 갈 수 있는 선택지가 한 개라도 있는 지점 기록
        else:
            cross.append([cur_node, path_cnt])

    #### END OF YOUR OWN PROGRAM ###

    if hubo.on_beeper():
        hubo.pick_beeper()
    cnt = cnt + 1


#### DO NOT EDIT BELOW ####
if hubo._beeper_bag >= 5:
    print("%i beepers picked. Succeeded! Got 70 points!" % hubo._beeper_bag)
else:
    print("Time over. %i beepers picked. Got %i points." % (hubo._beeper_bag, 14*hubo._beeper_bag))