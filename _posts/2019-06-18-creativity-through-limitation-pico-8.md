---
layout: post
title: "Creativity through limitation: PICO-8 — Fantasy Console"
description: "When was the last time you coded something just for fun? PICO-8 brings fun back to programming!"
image: /assets/blog-images/2019-06-18-cover.jpg
tags: [demoscene, "creativity_through_limitations", "8bit"]
---

It is the second article in “Creativity through limitation” series. Check out the first one: [8-bit demoscene](/2018/08/05/creativity-through-limitation-8-bit-demoscene.html). In this article, I’m going to tell you about the fantasy console PICO-8 and recreate two classic demoscene effects with it.

When was the last time you coded something just for fun? If you’re like me, then it hasn’t happened for years. However, about a year ago, I learned about PICO-8, bought it, and I have to say that these were probably the most worthy $15 I spent on myself last year!

<!--more-->

## What is PICO-8?

> PICO-8 is a fantasy console for making, sharing and playing tiny games and other computer programs. When you turn it on, the machine greets you with a command line and simple built-in tools for creating your own cartridges and exploring the PICO-8 cartverse. — [PICO-8 official page](https://www.lexaloffle.com/pico-8.php)

Do you remember the era of 8-bit video game consoles and computers? PICO-8 returns you to those times. It is an “emulator” of a non-existing video game console with Lua “CPU” developed by [Lexaloffle](https://www.lexaloffle.com). It has a set of wisely designed constraints (speed, color palette, screen resolution, sound, and memory) which may look ridiculous, but it stimulates your creative muscle. Also, to let you start creating right away, PICO-8 gives you simple but convenient built-in tools: code, graphics, and sound/music editors.

![PICO-8 Built-in tools](/assets/blog-images/2019-06-18-pico-8-tools.png)

PICO-8 has a fantastic community. Many people create games, demos, and tutorials. Teachers use it at schools to teach children programming. Professional game developers use it for experiments. One thing unites them all — it’s fun!

There’s also a pretty unique creative genre on PICO-8 — Tweetcart. Tweetcart is a program that fits in a Tweet (up to 280 characters) and produces some impressive visual effect. The idea is very similar to demoscene intro.

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Tree with Moon // 278 chars -- <a href="https://twitter.com/hashtag/pico8?src=hash&amp;ref_src=twsrc%5Etfw">#pico8</a> src in reply<a href="https://twitter.com/hashtag/tweetcart?src=hash&amp;ref_src=twsrc%5Etfw">#tweetcart</a> <a href="https://twitter.com/hashtag/tweetjam?src=hash&amp;ref_src=twsrc%5Etfw">#tweetjam</a> <a href="https://t.co/3ZgbsSXaG0">pic.twitter.com/3ZgbsSXaG0</a></p>&mdash; zep.p8 (@lexaloffle) <a href="https://twitter.com/lexaloffle/status/1052502760329961473?ref_src=twsrc%5Etfw">October 17, 2018</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Gardner&#39;s sky texture. Source in next message and also in Computer graphics principles and practice (2nd edition) / Chapter 20.8.2 Clouds and atmosphere<br><br>BTW It took me about an hour to realize I had some extra spaces in the code!<a href="https://twitter.com/hashtag/pico8?src=hash&amp;ref_src=twsrc%5Etfw">#pico8</a> <a href="https://twitter.com/hashtag/tweetcart?src=hash&amp;ref_src=twsrc%5Etfw">#tweetcart</a> <a href="https://twitter.com/hashtag/tweetjam?src=hash&amp;ref_src=twsrc%5Etfw">#tweetjam</a> <a href="https://twitter.com/hashtag/screenshotsunday?src=hash&amp;ref_src=twsrc%5Etfw">#screenshotsunday</a> <a href="https://t.co/qx7XsjumOB">pic.twitter.com/qx7XsjumOB</a></p>&mdash; Michał Rostocki (@von_rostock) <a href="https://twitter.com/von_rostock/status/1114960242171949058?ref_src=twsrc%5Etfw">April 7, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

You can find more on [Twitter by #tweetcart](https://twitter.com/hashtag/tweetcart?src=hash) or at [Museum of Tweetcart History](https://museum-of-tweetcart-history.neocities.org).

----

## Creating classic demoscene effects on PICO-8

If you don’t know what demoscene is, read [the first article in this series](/2018/08/05/creativity-through-limitation-8-bit-demoscene.html). Many classic effects are recurring in different demos, and I’m going to re-create two of them on PICO-8: Vertical raster bars and Rotozoomer. PICO-8 uses the Lua programming language. If you‘re not familiar with it, it shouldn‘t be a problem, because Lua syntax is simple and straightforward.

<iframe class="frame" src="/demos/raster-rotozoomer/raster_rotozoomer.html"></iframe>
<p class="footnote">PICO-8 can run in a browser. Try it!</p>

### Vertical raster bars

Let’s start with Vertical raster bars (also known as Kefrens bars, even though the first implementation was done not by Kefrens demo group). They look impressive on old computers because you could think — wow, they draw so many vertical lines! In reality, this effect doesn’t require drawing vertical lines at all. The classic implementation utilized Amiga’s ability to run some code for every scanline and change video memory address. You create a buffer for just one line and draw it repeatedly, adding a small “bar” every time in a different position.

You can use the same approach on PICO-8. There are no horizontal blank interrupts, but you don’t need it; instead, you use `memcpy` function. Let’s create a template first.

```lua
-- PICO-8 init function, create a coroutine here
function _init()
  cfx = cocreate(fx)
end

-- The effect can run in 60 FPS, use _update60() instead of _update()
function _update60()
end

-- PICO-8 frame draw function
function _draw()
  -- Draw the frame
  coresume(cfx)
  -- Uncomment the following lines to see CPU load
  --cursor(0, 0)
  --color(15)
  --print(stat(1))
end

function fx()
  -- FX code will be here
end
```

I like to use coroutines for both drawing and updating state variables because they allow me to write code linearly and encapsulate all variables in a function. The downside of this approach is the slowdown if your drawing code occasionally takes more than one frame to complete. When you use `_update()` + `_draw()` approach, you only get frame rate drop, because PICO-8 always executes `_update()/_update60()` at the constant rate (30/60 times per second), but may call `_draw()` at the lower rate (30/15 times per second).

So, here’s the code with comments:

```lua
-- Raster bars
function fx()
  -- Raster bars variables: phase counters
  local ph1, ph2, ph3 = 0, 0, 0
  local pht1, pht2, pht3, x

  while true do
    -- Clear the line buffer. I use the last line of the screen
    -- for it to use PSET function to draw.
    memset(0x7fc0, 0, 0x40)
    -- Set temporary variables
    pht1, pht2, pht3 = ph1, ph2, ph3

    -- Loop over all 128 screen lines
    for i = 0, 127 do
      -- Vertical raster bars
      -- 1. Calculate the position for the next bar piece
      x = flr(63 + sin(pht1) * 19 + sin(pht2) * 9 + sin(pht3) * 7)
      -- 2. Draw the bar by plotting points around the calculated X position
      pset(x - 1, 127, 0)
      pset(x, 127, 5)
      pset(x + 1, 127, 13)
      pset(x + 2, 127, 13)
      pset(x + 3, 127, 5)
      -- 3. Update temporary phase variables for the next line
      pht1 += 0.01
      pht2 += 0.02
      pht3 += 0.04

      -- Copy the line buffer
      memcpy(0x6000 + i * 64, 0x7fc0, 0x40)
    end

    -- Update phase counters
    ph1 += 0.002
    ph2 += 0.004
    ph3 += 0.03

    -- We're done, wait for the next frame
    yield()
  end
end
```

Now let’s add a roto-zoomer. I tried implementing a full-screen roto-zoomer on PICO-8 in 60 FPS and ran out of CPU time. However, if you combine a roto-zoomer with raster-bars, you don’t need to do it full-screen — You can draw in empty space only! It’s easy to track empty space with raster bars: the bar gets only wider every line, it can’t get narrower, so you can keep simply track the lowest and the highest X coordinates.

Roto-zoomer usually is a rotating and zooming picture, but I don’t want to deal with images in this example and will create a rotating and zooming checkerboard. Here’s the code:

```lua
-- Raster bars + roto-zoomer
function fx()
  local ph1, ph2, ph3 = 0, 0, 0
  local pht1, pht2, pht3, x
  -- Roto-zoomer variables: rotation angle; zoom, X and Y phases
  local zph, zzoom, zpx, zpy = 0, 1, 0, 0
  -- Temporary variables
  local xr, lx, hx, ztx, zty, zdx, zdy, zsx, zsy

  while true do
    memset(0x7fc0, 0, 0x40)
    pht1, pht2, pht3 = ph1, ph2, ph3
    -- Set roto-zoomer temporary variables
    lx = 64
    hx = 0
    -- zdx, zdy — rotated and scaled step vector
    zdx = cos(zph) * (1 + sin(zzoom) * 0.5)
    zdy = sin(zph) * (1 + sin(zzoom) * 0.5)
    -- zsx, zsy — position on the checkerboard
    zsx = sin(zpx) * 20
    zsy = sin(zpy) * 20

    for i = 0, 127 do
      -- Vertical raster bars
      x = flr(63 + sin(pht1) * 19 + sin(pht2) * 9 + sin(pht3) * 7)
      pset(x - 1, 127, 0)
      pset(x, 127, 5)
      pset(x + 1, 127, 13)
      pset(x + 2, 127, 13)
      pset(x + 3, 127, 5)
      pht1 += 0.01
      pht2 += 0.02
      pht3 += 0.04

      -- Roto-zoomer
      -- 1. Update left and right boundaries
      xr = flr(x / 2)
      if (xr < lx) lx = xr
      if (xr + 2 > hx) hx = xr + 2
      -- 2. Coordinates at the beginning of the line
      ztx = zsx + i / 2 * zdy
      zty = zsy + i / 2 * zdx
      -- 3. Draw left part
      for c = 0, lx - 1 do
        poke(0x7fc0 + c, (band(bxor(zty, ztx), 8) == 8) and 0xaa or 0)
        ztx += zdx
        zty -= zdy
      end
      -- 4. Update coordinates to skip drawn raster bar
      ztx += zdx * (hx - lx + 1)
      zty -= zdy * (hx - lx + 1)
      -- 5. Draw right part
      for c = hx + 1, 63 do
        poke(0x7fc0 + c, (band(bxor(zty, ztx), 8) == 8) and 0xaa or 0)
        ztx += zdx
        zty -= zdy
      end
      -- 6. Clean some artifacts
      if pget(x + 4, 127) == 10 then pset(x + 4, 127, 0) end
      if pget(x + 5, 127) == 10 then pset(x + 5, 127, 0) end

      -- Copy line
      memcpy(0x6000 + i * 64, 0x7fc0, 0x40)
    end

    -- Update raster bars variables
    ph1 += 0.002
    ph2 += 0.004
    ph3 += 0.03

    -- Update roto-zoomer variables
    zph += 0.001
    zpx += 0.002
    zpy += 0.003
    zzoom += 0.001

    yield()
  end
end
```

![](/assets/blog-images/2019-06-18-rotozoomer.png)
<p class="footnote">Explanation of the main variables.</p>

Instead of using texture look-up, I use bitwise operations to create checkerboard. `band(ztx, 8)` gives a series of 0’s and 8’s every 8 pixels, `bxor(zty, ztx)` creates a checkerboard. To speed up the code and make both effects run in 60 FPS, I reduce the horizontal resolution and plot 2 points with a single `poke` (write a byte to memory) function instead of `pset`.

That’s it! You can find the full code and some other effect I create in [my PICO-8 repository on GitHub](https://github.com/Megus/pico-8-experiments).

---- 

As I recall, it’s the first time I’ve tried to explain a demo effect, and I’m afraid that it may not be clear enough. I tried to add as many comments as possible, but if you’ve got any questions, let me know, I’m ready to improve and add more details. Thanks for your attention!
