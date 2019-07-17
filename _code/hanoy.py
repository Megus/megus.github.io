import time

# Recursive solution
def hanoi_recursive(disks, source, target, spare):
  if disks == 0:
    return []

  moves = hanoi_recursive(disks - 1, source, spare, target)
  moves.append((source, target))
  moves.extend(hanoi_recursive(disks - 1, spare, target, source))
  return moves

# Iterative solution without peg remapping
def hanoi_iterative(disks):
  if disks == 0:
    return []
  
  moves = []

  for m in range(1, 1 << disks):
    s = (m & (m - 1)) % 3
    t = ((m | (m - 1)) + 1) % 3
    moves.append((s, t))

  return moves

# Iterative solution with peg remapping
def hanoi_iterative_remap(disks, source, target, spare):
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

# The solution from 2000
def count_binary_zeros(n):
  zeros = 0
  for _ in range(0, 31):
    if n % 2 == 0:
      zeros = zeros + 1
    else:
      break
    n = n >> 1
  
  return zeros


def hanoi_2000(disks, source, target):
  moves = []

  f = 0
  s = source
  t = target
  n = disks

  for m in range(1, 1 << disks):
    while n > 1:
      n = n - 1
      t = 3 - s - t

    if f == 0:
      moves.append((s, t))
      f = 1
    else:
      if count_binary_zeros(m) % 2 == 0:
        s = 3 - s - t
      
      t = 3 - s - t
      moves.append((s, t))
      s = 3 - s - t
      n = count_binary_zeros(m)
      f = 0

  return moves





def demo():
  moves = hanoi_2000(4, 0, 2)
  print(moves)

  moves = hanoi_recursive(4, 0, 2, 1)
  print(moves)

  moves = hanoi_iterative_remap(4, 0, 2, 1)
  print(moves)

# Measure time of multiple calls to hanoi recursive
def measure_performance():
  time1 = time.time()
  for _ in range(20):
    hanoi_recursive(16, 0, 2, 1)

  time_recursive = time.time() - time1

  time1 = time.time()
  for _ in range(20):
    hanoi_2000(16, 0, 2)

  time_2000 = time.time() - time1

  time1 = time.time()
  for _ in range(20):
    hanoi_iterative_remap(16, 0, 2, 1)

  time_iterative_remap = time.time() - time1

  print(f'Recursive: {time_recursive}')
  print(f'Iterative 2000: {time_2000}')
  print(f'Iterative with remapping: {time_iterative_remap}')

  time_ratio = time_recursive / time_2000
  print(f'Recursive/iteratve 2000 time ratio: {time_ratio}')
  time_ratio = time_recursive / time_iterative_remap
  print(f'Recursive/iterative with remapping time ratio: {time_ratio}')



demo()
#measure_performance()
