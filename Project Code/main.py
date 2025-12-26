from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time
import matplotlib.pyplot as plt

from maze import MazeVisualizer, START_POS, GOAL_POS, ROWS, COLS
from search_algo import bfs,dfs,ucs,ids,hill_climbing,astar,get_algorithm_stats

# Global variables
visualizer = None
algorithm_name = ""

def display():
    """OpenGL display callback"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    gluLookAt(COLS/2, 35, ROWS/2 + 20, COLS/2, 0, ROWS/2, 0, 1, 0)
    
    visualizer.update_agent()
    visualizer.draw_scene()
    
    glutSwapBuffers()

def reshape(w, h):
    """Handle window reshape"""
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def init_opengl():
    """Initialize OpenGL settings"""
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [10, 25, 10, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1])
    glEnable(GL_COLOR_MATERIAL)
    glClearColor(0.25, 0.25, 0.28, 1)

def run_algorithm(algorithm_choice, move_delay=0.15):
    global visualizer, algorithm_name
    if algorithm_choice.lower() == 'bfs':
        algorithm_name = "BFS (Breadth-First Search)"
        movement_seq, discovered, path = bfs(START_POS, GOAL_POS)
    elif algorithm_choice.lower() == 'dfs':
        algorithm_name = "DFS (Depth-First Search)"
        movement_seq, discovered, path = dfs(START_POS, GOAL_POS)
    elif algorithm_choice.lower() == 'ucs':
        algorithm_name = "UCS (Uniform Cost Search)"
        movement_seq, discovered, path = ucs(START_POS, GOAL_POS)    
    elif algorithm_choice.lower() == 'astar':
        algorithm_name = "A* (A-Star Search)"
        movement_seq, discovered, path = astar(START_POS, GOAL_POS)
    elif algorithm_choice == 'ids':
        algorithm_name = "IDS (Iterative Deepening Search)"
        movement_seq, discovered, path = ids(START_POS, GOAL_POS)
    elif algorithm_choice == 'hill':
        algorithm_name = "Hill Climbing Search"
        movement_seq, discovered, path = hill_climbing(START_POS, GOAL_POS)
    
    else:
        print(f"Error: Unknown algorithm '{algorithm_choice}'")
        print("Available: 'bfs', 'dfs', 'astar','ids',''ucs,'hill climbing'")
        return False
    
    if not path:
        print("No path found! But here's what was explored:")
        path_found = False
    
    # Create visualizer
    visualizer = MazeVisualizer(move_delay)
    visualizer.set_algorithm_data(movement_seq, discovered, path)
    
    # Calculate visualization time
    viz_time = len(movement_seq) * move_delay + len(path) * move_delay
    
    # Print statistics
    stats = get_algorithm_stats(discovered, movement_seq, path, viz_time)
    print("\n" + "="*50)
    print("ALGORITHM STATISTICS")
    print("="*50)
    print(f"Algorithm: {algorithm_name}")
    print(f"Explored nodes: {stats['nodes_explored']}")
    print(f"Total movements: {stats['total_movements']}")
    print(f"Final path length: {stats['path_length']}")
    print(f"Visualization time: {viz_time:.2f} seconds")
    print("="*50)
    
    return True

def compare_algorithms():
    algorithms = [
        ('BFS', bfs),
        ('DFS', dfs),
        ('UCS', ucs),
        ('A*', astar),
        ('IDS', ids),
        ('Hill', hill_climbing),
    ]

    move_delay = 0.15
    results = {}

    for name, algorithm in algorithms:
        movement_seq, discovered, path = algorithm(START_POS, GOAL_POS)
        viz_time = (len(movement_seq) + len(path)) * move_delay

        results[name] = {
            'Discovered nodes': len(discovered),
            'Moves': len(movement_seq),
            'Finel path': len(path),
            'Viz Time (s)': viz_time
        }

    metric_width = 16
    col_width = 12

    # Header
    header = f"| {'Metric':^{metric_width}} |"
    for algo in results:
        header += f" {algo:^{col_width}} |"

    print("-" * len(header))
    print(header)
    print("-" * len(header))

    metrics = ['Discovered nodes', 'Moves', 'Finel path', 'Viz Time (s)']

    for metric in metrics:
        row = f"| {metric:^{metric_width}} |"
        for algo in results:
            value = results[algo][metric]
            if metric == 'Viz Time (s)':
                value_str = f"{value:>8.2f}"
            else:
                value_str = f"{value:>8}"
            row += f" {value_str:^{col_width}} |"
        print(row)

    print("-" * len(header))
    return results

def visualize_comparison_results(results):
    algorithms = list(results.keys())
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']

    fig = plt.figure(figsize=(20, 6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.4])
    axes = [fig.add_subplot(gs[0, i]) for i in range(3)]
    
    fig.suptitle('Algorithm Comparison Results', fontsize=16, fontweight='bold')
    discovered = [results[algo]['Discovered nodes'] for algo in algorithms]
    moves = [results[algo]['Moves'] for algo in algorithms]
    
    x = range(len(algorithms))
    width = 0.35
    
    bars1 = axes[0].bar([i - width/2 for i in x], discovered, width, 
                        label='Discovered Nodes', color='#FF6B6B', alpha=0.8)
    bars2 = axes[0].bar([i + width/2 for i in x], moves, width,
                        label='Total Moves', color='#4ECDC4', alpha=0.8)
    
    axes[0].set_title('Exploration Metrics', fontweight='bold', fontsize=12)
    axes[0].set_ylabel('Count')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(algorithms)
    axes[0].legend()
    axes[0].grid(axis='y', alpha=0.3)
    
    for bar in bars1:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)

    path_length = [results[algo]['Finel path'] for algo in algorithms]
    
    axes[1].plot(algorithms, path_length, 'o--', color='#45B7D1', 
                linewidth=2, markersize=10, markerfacecolor='#FFA07A', 
                markeredgewidth=2, markeredgecolor='#45B7D1')
    axes[1].set_title('Final Path Length', fontweight='bold', fontsize=12)
    axes[1].set_ylabel('Path Length')
    axes[1].set_ylim(bottom=0) 
    axes[1].grid(True, alpha=0.3, linestyle='--')
    
    for i, (algo, length) in enumerate(zip(algorithms, path_length)):
        axes[1].text(i, length + 2, f'{int(length)}', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    viz_time = [results[algo]['Viz Time (s)'] for algo in algorithms]
    max_time = max(viz_time)
    
    bars3 = axes[2].barh(algorithms, viz_time, color=colors, alpha=0.8)
    axes[2].set_title('Visualization Time', fontweight='bold', fontsize=12)
    axes[2].set_xlabel('Time (seconds)')
    axes[2].set_xlim(0, max_time * 1.2)  
    axes[2].grid(axis='x', alpha=0.3)
    
    for i, (bar, time) in enumerate(zip(bars3, viz_time)):
        bar_width = bar.get_width()
        if bar_width > max_time * 0.15:
            axes[2].text(bar_width * 0.95, bar.get_y() + bar.get_height()/2.,
                        f'{time:.2f}s', ha='right', va='center', fontsize=10, 
                        color='white', fontweight='bold')
        else:
            axes[2].text(bar_width + max_time * 0.02, bar.get_y() + bar.get_height()/2.,
                        f'{time:.2f}s', ha='left', va='center', fontsize=10, 
                        color='black', fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
def main():
    
    print("\n" + "="*60)
    print("FIRE ESCAPE ROUTE AGENT - AI PATHFINDING PROJECT")
    print("="*60)
    print(f"Maze Size: {ROWS}x{COLS}")
    print(f"Start Position: {START_POS}")
    print(f"Goal Position: {GOAL_POS}")
    print("="*60)
    print("\nAlgorithms:")
    print("  bfs    - Breadth-First Search")
    print("  dfs    - Depth-First Search")
    print("  astar  - A-Star Search")
    print("  ids    - Itrative Deeping Search")
    print("  ucs    - uniform Cost Search")
    print("  hill   - Hill Climbing Search")
    print("  compare - Compare all algorithms")
    
    algorithm = input("Enter the algorithm to run (bfs, dfs, ucs, astar, ids, hill, compare): ").lower()
    valid_algorithms = ['bfs', 'dfs', 'ucs', 'astar', 'ids', 'hill', 'compare']

    if algorithm not in valid_algorithms:
        print("Invalid algorithm. Exiting.")
        exit()
    
    if algorithm == 'compare':
        visualize_comparison_results(results=compare_algorithms())
        return
        
    # Run algorithm
    if not run_algorithm(algorithm,0.15):
        return


    
    # Initialize OpenGL
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 1000)
    glutCreateWindow(f"Fire Escape Route Agent - {algorithm_name}".encode())
    
    init_opengl()
    glutDisplayFunc(display)
    glutIdleFunc(glutPostRedisplay)
    glutReshapeFunc(reshape)
    
    print("\nStarting visualization...")
    print("  Phase 1: Watch agent explore the maze")
    print("  Phase 2: Watch agent Follow the optimal path to goal")
    print("\nClose window to exit.")
   
    
    glutMainLoop()
    
if __name__ == "__main__":
    main()