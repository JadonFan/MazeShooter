import random

def generate_map():
	maze_width, maze_height = 20, 20 
	maze_vertical = [(x, y, x+1, y) for x in range(maze_width-1) for y in range(maze_height)]
	maze_horizontal = [(x, y, x, y+1) for x in range(maze_width) for y in range(maze_height-1)]
	maze_layout = maze_vertical + maze_horizontal
	kruskal_sets = [set([(x,y)]) for x in range(maze_width) for y in range(maze_height)]

	maze_copy = list(maze_layout)
	random.shuffle(maze_copy)

	for step in maze_layout:
		set1 = None
		set2 = None

		for indiv_set in kruskal_sets:
			if (maze_layout[0], maze_layout[1]) in indiv_set:
				set1 = indiv_set
			if (maze_layout[2], maze_layout[3]) in indiv_set:
					set2 = indiv_set

		if set1 is not set2:
			kruskal_sets.remove(set1)
			kruskal_sets.remove(set2)
			kruskal_sets.append(set1.union(set_b))
			layout.remove(step)
	return maze_layout

print(generate_map())