---
layout: post
title: "Making of PICOCHAK"
description: "“Behind the scenes” of the PICO-8 demo I created for CAFe'2019 demoparty."
image: /assets/blog-images/2020-05-04-cover.jpg
tags: ["Programming", "Demoscene", "PICO-8", "Lua"]
---

Last October, I made the first demoscene production after an almost two-decades-long break — a demo for PICO-8 fantasy console “PICOCHAK: Attack of Donuts.”

{% youtube gUooT-v4LIU %}

- [PICOCHAK at pouët.net](https://www.pouet.net/prod.php?which=83557 "PICOCHAK at pouët.net")
- [Topic at Lexaloffle BBS](https://www.lexaloffle.com/bbs/?tid=35774 "Topic at Lexaloffle BBS")
- [Source code at GitHub](https://github.com/Megus/picochak "Source code at GitHub")

The moment I had learned that [CAFe demoparty](https://cafeparty.org.ru/2019/) is going to be back in 2019, I decided to take part in it. In 1999, CAFe became the first party I had visited. I wasn’t creating PICOCHAK alone; other members of the PICOCHAK team are:

- [Oleg Nikitin (n1k-o/Stardust)](https://soundcloud.com/n1k-o/) — music
- [Alexey Golubtsov (Diver/Stardust)](https://zxart.ee/rus/avtory/d/diver/qid:121913/) — graphics
- Damir Nasyrov (Adam Bazaroff) — Tatar culture expert

It was easy to come up with a concept. As CAFe is held in Kazan, the capital of Tatarstan, Oleg suggested using Tatar food references. I added that I like space-themed demos. By mixing these, we got our “Tatar food in space” idea. Chak-chak is a Tatar national sweet, so we made it a protagonist in the story, hence the name — PICOCHAK. Our demo took second place in the console demo competition.

PICOCHAK in numbers:

- Duration: 4 minutes, 24 seconds
- 12 effects
- 446 8x8 sprites (2 64х64 textures, 38 8х8 font sprites, 104x64 demo logo, 8 24x24 planet sprites, 72x64 “gas station” sprite, 8 16x16 “ship” sprites).
- 5 3D models (569 vertices and 1120 triangles in total).
- 80 music patterns.

PICO-8 has many limitations, just like real retro hardware (I have an [article about PICO-8](https://megus.org/2019/06/18/creativity-through-limitation-pico-8.html) in my “Creativity through limitations” series). With this demo, I wanted to push PICO-8 limits, because that’s what [retro demoscene](https://megus.org/2018/08/05/creativity-through-limitation-8-bit-demoscene.html) is about, in my opinion. I believe that I succeeded. I haven’t had so much fun while coding since the [4K intro “Malady”](https://megus.org/projects/malady.html) I made for ZX Spectrum back in 1999. Never-ending battle with platform constraints, inventing coding tricks, finding smart ways to improve the code — these were a breath of fresh air, which helped me to deal with the burnout I got at my daily job.

## Working on effects

I didn’t have the goal of inventing something new and unique. For my “demoscene comeback,” I wanted to re-create some classic demoscene effects because I missed the opportunity to do them on real retro-hardware back in time. I had already had a simple 3D engine on PICO-8, but for PICOCHAK I added some new features:

- Concave (non-convex) objects support
- Flat shading
- Textures (without perspective correction)

I also re-created three classic effects: roto-zoomer, twister, and bump mapping. All other effects use sprites. As mentioned above, the demo has 446 8x8 sprites, while PICO-8 has a memory for 256 sprites only. To fit this much sprites, I used [the PX9 compression algorithm by Zep](https://www.lexaloffle.com/bbs/?tid=34058).

<div class="image-row">
<img style="width: 33%; height: 33%;" src="/assets/blog-images/2020-05-04-rotozoomer.gif" />
<img style="width: 33%; height: 33%;" src="/assets/blog-images/2020-05-04-twister.gif" />
<img style="width: 33%; height: 33%;" src="/assets/blog-images/2020-05-04-bump-mapping.gif" />
</div>

I’m not going to write about the implementation of effects, because it’s pretty easy to find all the necessary information on the Internet. This article is about the unique PICO-8 challenges I faced when creating PICOCHAK.

## Scenario system — connecting all effects together

To transform a bunch of effects to a demo, it needs some control system which provides synchronization with music and switches effects. I called it a “scenario system.” In PICOCHAK, it went through three iterations. Every time I had rewritten the code from scratch, I got fewer tokens and better readable code. The common idea for all three iterations was that every effect is a function, which performs some initialization procedures and then returns `update` and `draw` functions for the effect.

If you’re unfamiliar with PICO-8:  `update` function updates the state, and `draw` function performs the actual drawing on the screen. Both functions are called 30 or 60 times per second. While you can put state updates and drawing code in any of these functions, it’s better to separate them. If your `draw` function takes more than 1/60 or 1/30 seconds to complete, you get FPS drop, but the perceived speed of objects on the screen doesn’t change, because PICO-8 will always call the `update` function 30 or 60 times per seconds.

### 1st attempt: state machine

Initially, I decided to “describe” each effect as a [state machine](https://en.wikipedia.org/wiki/Finite-state_machine), and `update` functions in effects had series of `if` expressions: one `if` for each state. It worked fine, but it was hard to read and took many tokens. I could’ve stayed with this system, but I needed tokens for other effects.

### 2nd attempt: better state machine

I was still thinking that state machines are the best for programming scenarios, so I made the better version, which took fewer tokens. The code became shorter, but still hard to read. The more effects I added, the less satisfied I was with it. I started to get lost in pieces of logic scattered here and there. I needed a better solution.

### 3rd attempt: coroutines

Coroutines for the rescue! Every effect had got a coroutine with the control code, which became linear, you can read it like an actual scenario. Now, every effect function returns 4 values:

- Scenario coroutine
- `update` function with common animations
- `draw` function
- Background color (-1 if clearing screen before `draw` call is not needed)

To simplify synchronization, I created four helper functions: `loop_frames`, `wait_frames`, `loop_sync` and `wait_sync`. Here’s a usage example:

```lua
while loop_frames(64) do
  donuty -= 2
end

move_donuts, show_mega = true, true
wait_frames(120)
while loop_frames(210) do
  offy -= 1
end
wait_sync()
```

What this code does:

- Decrease `donuty` variable by 2 every frame (repeat for 64 frames)
- Set some flags
- Do nothing for 120 frames (common animations in an `update` function are still running)
- Decrease `offy` variable by 1 every frame (repeat for 210 frames)
- Wait for the next music synchronization point

Just as I said: the control code is linear and very easy to read. You don’t see any `yield`s because they’re all inside those helper functions.

The overall demo scenario is a Lua table with effect functions and music synchronization points. The music synchronization point is the number of music patterns played since the beginning of the demo. Each effect may have multiple synchronization points. Here’s a part of PICOCHAK scenario:

```lua
fx_intro, 1,
fx_foodstars, 4, 6, 8,
fx_donuts, 9, 13, 15, 17, 19,
fx_donut_attack, 25, 27,
fx_sky_transition,
function() return fx_preparations(104, 0, 0) end, 29,
fx_kaleidoscope, 31,
```

## Music control system

Music was another challenge for us. PICO-8 doesn’t have much space for music, so it was clear: if we want to have a four-minute-long soundtrack, we need to use some tricks. Here’s what I came up with:

**Pattern loops.** I change loop parameters dynamically because 64 pattern slots are not enough, the “unrolled” soundtrack would have taken over 80 pattern slots.

**Overwriting patterns.** At some point after the intro, I overwrite the first 12 SFX with data stored in sprite memory. This trick gave n1k-o a bit more freedom and added variety to the music.

**Audio effects.** It’s an undocumented feature of PICO-8. There are 4 per-channel audio effects: reverb, filter, distortion, and “half-speed.” Turning effects on and off during loops made repetitions less annoying.

I created a little “music control system,” which used a list of “audio commands.” Each command consists of 2 numbers: time and the command itself. Like in the scenario system, time is measured in the number of patterns played since the beginning of the demo. Here are some examples of commands:

```lua
23, 0x0404,   -- FX: filter and distortion for channel 3
24, 0x131c.8, -- Set loop for patterns 0x13-0x1c
27, 0x0.01,   -- FX: reverb on channel 1
31, 0x0.09,   -- FX: reverb on channels 1 and 4
47, 0x0.8,    -- Overwrite patterns
```

n1k-o, our composer, writes a lot of music for ZX Spectrum with Vortex Tracker. To let him use one of his favorite tools, I created a converter from Vortex Tracker to PICO-8 format. ZX sound chip and PICO-8 sound system are different, so it was impossible to make a perfect converter. However, we developed some conventions which allowed him to do most of the work in Vortex Tracker and use PICO-8 music editor only for the final touches. The [VT2-to-PICO-8 converter code is available on GitHub](https://github.com/Megus/vt2-to-pico-8).

## Optimizing code size

There are three limitations on the code size on PICO-8:

- 8192 tokens
- 15KB of compressed code size
- 65535 characters

The limits are listed in the order of their importance. If you’re creating something big on PICO-8, the first limit you’re going to hit is, most likely, the token limit. If you have too many tokens, you can’t even load a cart. The compressed code size limit is more forgiving — you can load and run a cart, but you won’t be able to export it to p8.png format.

When I started optimizing the code, I also began taking notes on how many tokens I saved after each optimization. According to my records, I managed to cut over 3000 tokens! That means that not optimized code would have taken over 11k tokens!

The most token-heavy module of the demo is the 3D engine. The first function I optimized was the matrix multiplication function. It was unrolled entirely to make it faster. However, it’s used only three times each frame and doesn’t impact performance significantly, so I rewrote it using loops. The next one was a triangle rasterizer. Initially, I used a speedy implementation by ElectricGryphon, but it is very long, so I wrote my own function. It is not perfect, but it’s much shorter and only a tiny bit slower. Another significant optimization was rewriting a sorting function (I use it for concave objects). Instead of some 3rd party implementation of a merge sort, I wrote an in-place radix sort. Not only is it shorter, but it is also faster.

<div class="image-row">
<img style="width: 33%; height: 33%;" src="/assets/blog-images/2020-05-04-three-objects.gif" />
<img style="width: 33%; height: 33%;" src="/assets/blog-images/2020-05-04-donut.gif" />
<img style="width: 33%; height: 33%;" src="/assets/blog-images/2020-05-04-picochak.gif" />
</div>

All 3D models in PICOCHAK are programmatically generated, and these generators took about a thousand tokens. It was OK in the beginning, but when I started to add more effects, it became clear that it’s too much. I decided to put all model data (vertices and triangles) to sprite/map memory, and I failed: there wasn’t enough space. In the end, I chose a hybrid approach: storing vertices in the map memory and building triangles programmatically.

All these are the algorithmic optimizations, but there are also some conventional techniques which you can apply to any PICO-8 code:

### Multiple assignments on the same line

```lua
-- Instead of this:
local a = 1
local b = 2

-- Write this:
local a, b = 1, 2
```

It makes your code difficult to read, but it saves you one token for each variable. Be careful, such assignments are “atomic,” so the code like this won’t work:

```lua
local obj, v = arr[1], obj.field
```

By the way, multiple assignments are perfect for swapping variable values without using a temporary variable:

```lua
x, y = y, x
```

### Move repeating code to functions

This is a pretty obvious recommendation, but it can save you a lot of tokens. I made functions even for basic calculations like this:

```lua
function ssin(t, scale, tscale)
  return sin(t / (tscale or 1)) * scale
end
```

It is important to remember that each function call costs you some CPU time. In the twister effect, I had to find a balance between using functions and unrolling them to achieve 60 FPS.

### Use language features

PICO-8 has some additions to Lua syntax which save tokens:

```lua
a = a + 1 -- 5 tokens
a += 1 -- 3 tokens
```

You can use `all()` to iterate through arrays. It takes fewer tokens, but it’s a bit slower. Another trick is to use `%` instead of `band(x, mask)` for masking if you work with positive integers.

### Put all strings to a single variable

There’s quite a lot of text in PICOCHAK. Initially, every string took 3 tokens: the string itself and a pair of coordinates. To save tokens, I used the fact that a string of any length is just one token for PICO-8. The demo is linear, and each line is used only once, so I could merge all texts and coordinates into a single very long string variable. I shaved off over a hundred tokens with this trick!

### Optimizing compressed code size

When I was close to the completion, I finally ran into the compressed code size limit. However, it was elementary to fix:

- Convert code indentation to tabs
- Remove almost all comments
- Give some variables shorter names

----

The process of creating PICOCHAK was challenging but enjoyable. I enjoyed every minute of it, including the routine moments of code size optimization. I’m definitely making another demo for PICO-8 in the future!