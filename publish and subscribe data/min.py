# Sample times for each player (in seconds)
time_A = [10, 12, 11]  # Times for Player A in three runs
time_B = [11, 10, 12]  # Times for Player B in three runs
time_C = [12, 11, 10]  # Times for Player C in three runs

# Calculate total times for each player
total_time_A = sum(time_A)
total_time_B = sum(time_B)
total_time_C = sum(time_C)

# Determine the player with the minimum total time
min_total_time = min(total_time_A, total_time_B, total_time_C)

# Output the result
if min_total_time == total_time_A:
    print("Player A has the minimum time.")
elif min_total_time == total_time_B:
    print("Player B has the minimum time.")
else:
    print("Player C has the minimum time.")
