---
layout: post
title: "Coding problems: why do I like them? Solving Tower of Hanoi puzzle"
description: ""
image: /assets/blog-images/2019-07-17-cover.jpg
tags: [programming]
css: /assets/css/hanoi.css
---

If you’ve ever tried to get a job in a big company or participated in a programming contest, you know what coding problems (or coding challenges) are. A typical example would be to “implement a queue using two stacks.” Many people hate them as a part of interviews because coding problems don’t demonstrate your ability to write good code. 

Most coding problems are irrelevant to the daily job of a developer, and there’s no practical application for them. They’re just brain teasers or exercises. However, that is why I like them, and I would recommend programmers to solve them at least sometimes. Everybody knows that you need to do exercises to stay fit. The brain is a “muscle” too in the sense that you need to exercise to get the most of it. I think that coding exercises help developer’s brain to “stay fit.”

As developers, we spend much time fixing bugs and doing routine work. We rarely have tricky problems, but problem-solving is a crucial skill for a developer. Coding problems may help you to improve it. Also, as I already said, coding problems don’t have practical application usually, but you can pick something useful from them still.

In this article, I want to tell you about the first coding challenge I had at university, and how I solved it back then and now. 

<!--more-->

## Tower of Hanoi

<div class="centered"><img src="/assets/blog-images/2019-07-17-hanoi.gif"></div>

Tower of Hanoi is an old puzzle, and solving it is a well-known coding problem. You have three pegs with disks of different sizes on one of them; the objective is to move all disks to another peg, obeying simple rules:

1. You can move only one disk at a time.
2. You can’t put a larger disk on a smaller one

I knew about the Tower of Hanoi since childhood, but as a developer, I met it after my first year at university. My summer practice task was to visualize Tower of Hanoi solution process. The recursive solution is trivial:

1. Move `n−1` disks from the source peg to the spare peg
2. Move the biggest disk from the source peg to the target peg
3. Move `n−1` disks from the spare peg to the target peg
4. The base case is to move 0 disks — do nothing.

```python
def hanoi_recursive(disks, source, target, spare):
  if disks == 0:
    return []

  moves = hanoi_recursive(disks - 1, source, spare, target)
  moves.append((source, target))
  moves.extend(hanoi_recursive(disks - 1, spare, target, source))
  return moves
```

Time complexity is O(2<sup>n</sup>), auxiliary space required is O(n), where `n` is a number of disks. If you're not familiar with space complexity estimation or recursive algorithms, it may look like it’s O(1). However, every function call allocates some memory on the stack, and this code makes up to `n` consecutive recursive calls.

I finished my summer practice task in one day and felt bored — too easy! I was young and full of enthusiasm, and I wondered: is there another way to solve this puzzle? Can I do it iteratively? Today you could go to [Wikipedia](https://en.wikipedia.org/wiki/Tower_of_Hanoi) and find several iterative solutions, but it was 2000 and Wikipedia opened only next year. StackOverflow couldn’t help either, because it opened eight years later. However, even if both had existed those days, I would have tried devising the solution myself anyway. After a couple of days and a pile of paper, I found the solution. Unfortunately, I forgot it. The only thing I remembered was that I used the binary representation of the move number. So, I solved it again for this article; however, I can’t be sure it’s the same as nineteen years ago.

Here’s the final solution code in Python:

```python
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
```

This code is about 450% faster than the recursive one, but the time complexity is still O(2<sup>n</sup>) — you can’t improve it because you need to do 2<sup>n</sup>−1 moves to solve the puzzle. It works faster because there’s no function calling overhead and there are fewer memory allocations, so auxiliary space is O(1).

As you can see, I use some binary “magic” in my solution. How did I devise these formulas? I made a spreadsheet with solutions for the different number of disks and started to analyze them. This time I used Google Sheets, nineteen years ago I used paper. I use zero-based pegs numbers; we’re moving all disks from peg 0 to peg 2.

{% csvtable site.data.hanoi_1 %}

The first thing I noticed is that the peg pairs repeat every 3 moves, which led me to a thought that formula should have `x % 3` somewhere. However, even that the final formulas have it, it’s not because of repeating pairs. The second observation was that the first moves are always the same for any number of disks, except for “swapping” target and spare peg number for even and odd numbers. It led to “peg remapping” in my final solution.

As I said above, the only thing I remembered about my old solution was that I used the binary representations of the move numbers. So, I started to analyze them. The only thing I could find was that the number of binary zeroes at the right determines the disk to move, not the peg. Then I tried to do some random things and suddenly found something that worked: `m AND (m − 1)`. If you divide this number by 3, the remainder defines the source peg for the move! I admit that it was a pure guess, but that’s how you discover new things sometimes: experiment and try different things until you find a solution. After that I, experimented a bit more and came up with `m OR (m - 1)`. When you increment it and then divide by 3, the remainder is the target peg for the move. Problem solved!

{% csvtable site.data.hanoi_2 hanoi2 %}

```python
def hanoi_iterative(disks):
  if disks == 0:
    return []
  
  moves = []

  for m in range(1, 1 << disks):
    s = (m & (m - 1)) % 3
    t = ((m | (m - 1)) + 1) % 3
    moves.append((s, t))

  return moves
```

The only thing left for the universal solution was “peg remapping” because these formulas assume:

- the source peg is always 0;
- the target peg is 1 for an even number of disks and 2 for an odd number of disks.

That’s it. I think it was a good exercise in problem-solving and code optimization. 450% speed boost was impressive. Surely, you never need to solve the Tower of Hanoi in your daily job. However, there are tons of real tasks which have trivial slow solutions, but require deep thought and experimenting to find the optimal ones. I like such tasks; they make me feel proud of my job.

---- 

PS: While searching for something on an old HDD, I found my original solution from university time! It was in Pascal, but I rewrote it in Python for convenience. Even that it’s far less optimal than the one described in the article, it still performs a bit better than the recursive one.

```python
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
```
