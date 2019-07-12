import time

def hanoy_recursive(disks, source, target, spare):
  if disks == 0:
    return []

  moves = hanoy_recursive(disks - 1, source, spare, target)
  moves.append((source, target))
  moves.extend(hanoy_recursive(disks - 1, spare, target, source))
  return moves

def hanoy_iterative(disks):
  if disks == 0:
    return []
  
  moves = []

  for m in range(1, 1 << disks):
    s = (m & (m - 1)) % 3
    t = ((m | (m - 1)) + 1) % 3
    moves.append((s, t))

  return moves


def hanoy_iterative_remap(disks, source, target, spare):
  if disks == 0:
    return []
  
  is_even = (disks % 2 == 0)
  pegs = [
    source,
    target if is_even else spare,
    spare if is_even else target
  ]
  moves = []

  for m in range(1, 1 << disks):
    s = (m & (m - 1)) % 3
    t = ((m | (m - 1)) + 1) % 3
    moves.append((pegs[s], pegs[t]))

  return moves

#moves = hanoy_recursive(5, 0, 2, 1)
#print(moves)

#moves = hanoy_iterative_remap(5, 0, 2, 1)
#print(moves)

# Measure time of multiple calls to hanoy recursive
time1 = time.time()
for _ in range(20):
  hanoy_recursive(16, 0, 2, 1)

time_recursive = time.time() - time1

time1 = time.time()
for _ in range(20):
  hanoy_iterative(16)

time_iterative = time.time() - time1

time1 = time.time()
for _ in range(20):
  hanoy_iterative_remap(16, 0, 2, 1)

time_iterative_remap = time.time() - time1

print(f'Recursive: {time_recursive}')
print(f'Iterative: {time_iterative}')
print(f'Iterative with remapping: {time_iterative_remap}')

time_ratio = time_recursive / time_iterative
print(f'Recursive/iterative time ratio: {time_ratio}')
time_ratio = time_recursive / time_iterative_remap
print(f'Recursive/iterative with remapping time ratio: {time_ratio}')
