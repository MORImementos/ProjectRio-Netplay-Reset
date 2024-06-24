from memorylib import Dolphin

dolphin = Dolphin()
team_1_array = 0x803C6726 # set based on HUD file, batting lineup etc
team_1_filled = 0x803C676E # set all to 1
chem_with_capt = 0x803c674a # optional
team_1_positions = 0x803c6738
ok_selectable = 0x80750c7f
# example of reading / writing to all 18 roster spots

new_team_1 = [0, 2, 3, 4, 5, 6, 7, 8, 9]
team_1_pos = [8, 3, 2, 1, 5, 4, 6, 0, 7]
fill = [1] * 9
print(fill)
while True:
    if dolphin.hook():
        t1 = dolphin.read_bytes(team_1_array, 9)
        print(f"T1: {list(t1)}")
        for i in range(9):
            addr = team_1_array + i
            byte_val = dolphin.read_int8(addr)
            if byte_val == -1:
                dolphin.write_int8(addr, new_team_1[i])

        # team 1 positions
        dolphin.write_bytes(team_1_positions, bytes(team_1_pos))
        pos = dolphin.read_bytes(team_1_positions, 9)

        # team 1 filled ind
        dolphin.write_bytes(team_1_filled, bytes(fill))
        dolphin.write_int8(ok_selectable, 1)
        t1 = dolphin.read_bytes(team_1_array, 9)
        print(f"T1 Roster: {list(t1)}")
        break

    else:
        break
