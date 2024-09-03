from poke_engine import monte_carlo_tree_search

from example_state import state


result = monte_carlo_tree_search(state, duration_ms=1000)
print(f"Total Iterations: {result.iteration_count}")
print([(i.move_choice, i.total_score, i.visits) for i in result.s1])
print([(i.move_choice, i.total_score, i.visits) for i in result.s2])
