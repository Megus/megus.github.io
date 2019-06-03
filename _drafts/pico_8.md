---
layout: post
title: "PICO-8"
comments: true
---

# Creativity through limitation: PICO-8 — Fantasy Console

(Insert a collage of PICO-8 screenshots)

This is the second article in “Creativity through limitation” series. Check out the first one: [8-bit demoscene](https://www.megus.org/2018/08/05/creativity-through-limitation-8-bit-demoscene.html). In this article we’re going to recreate two classic demoscene effects with a fantasy console PICO-8.

When was the last time you coded something just for fun? If you’re like me, then it haven’t happened for years. However, about a year ago I learned about PICO-8, bought it, and I have to say that these were probably the most worthy $15 I spent on myself last year!

## What is PICO-8?


> PICO-8 is a fantasy console for making, sharing and playing tiny games and other computer programs. When you turn it on, the machine greets you with a command line and simple built-in tools for creating your own cartridges and exploring the PICO-8 cartverse.

[PICO-8 official page](%20https://www.lexaloffle.com/pico-8.php)

Do you remember the era of 8-bit video game consoles and computers? PICO-8 returns you to those times. It is an “emulator” of a non-existing video game console with Lua “CPU” developed by [Lexaloffle](https://www.lexaloffle.com). It has a set of wisely designed constraints (speed, color palette, screen resolution, sound and memory) which may look ridiculous, but it stimulates your creative muscle. And to let you start creating right away PICO-8 gives you simple but convenient built-in tools: code, graphics and sound/music editor.

(Insert a picture with built-in tools)

PICO-8 has a fantastic community. Lots of people create games, demos and tutorials. Teachers use it in schools to teach children programming. Professional game developers use it for experiments. One thing unites them all — it’s fun!

There’s also a pretty unique creative genre on PICO-8 — Tweetcart. Tweetcart is a program that fits in a Tweet (up to 280 characters) and produces some nice visual effect. The idea is very similar to demoscene intro.

(Insert some tweetcart examples)

You can find more on [Twitter by #tweetcart](https://twitter.com/hashtag/tweetcart?src=hash) or at [Museum of Tweetcart History](https://museum-of-tweetcart-history.neocities.org).

## Creating a classic demoscene effect on PICO-8

If you don’t know what a demoscene is, read [the first article in this series](https://www.megus.org/2018/08/05/creativity-through-limitation-8-bit-demoscene.html). There are many classic effects recurring in different demos, and I’m going to re-create two of them on PICO-8: Vertical raster bars and Rotozoomer.

### Vertical raster bars

(insert gif with PICO-8 raster bars)

Let’s start with Vertical raster bars (also known as Kefrens bars, even though the first implementation was done not by Kefrens demo group). They look impressive on old computers, because you could think — wow, they draw so many vertical lines! In reality, this effect doesn’t require drawing vertical lines at all. The classic implementation utilized Amiga’s abilities to run some code for every scanline and change video memory address. You create a buffer for just one line and draw it repeatedly, adding a small “bar” every time in a different position.

Let’s use the same approach on PICO-8. There are no horizontal blank interrupts, but we don’t need it. We’ll use `memcpy` function. Let’s create a template.

```lua
-- PICO-8 init function, we create a coroutine here
function _init()
	cfx = cocreate(fx)
end

-- We want our effect to run in 60 FPS, so we use _update60() instead of _update()
function _update60()
end

-- PICO-8 frame draw function
function _draw()
	memset(0x6000, 0, 0x2000)
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

I like to use coroutines for both drawing and updating state variables, because they allow me to write code in a linear way and encapsulate all variables in a function. The downside of this approach is the slowdown, if your drawing code occasionally takes more than one frame to complete. When you use `_update()` + `_draw()` approach, you only get frame rate drop, because PICO-8 always executes `_update()/_update60()` at the constant rate (30/60 times per second), but may call `_draw()` at the lower rate (30/15 times per second).



```lua
function fx()
	local ph1, ph2, ph3 = 0, 0, 0
	local pht1, pht2, pht3, x, xr

	while true do
		memset(0x4300, 0, 0x40)

		pht1, pht2, pht3 = ph1, ph2, ph3
		for i = 0, 127 do
			-- Vertical raster bars
			x = flr(63 + sin(pht1) * 19 + sin(pht2) * 9 + sin(pht3) * 7)
			xr = flr(x / 2)

			if x % 2 == 0 then
				poke(0x4300 + xr, 0xd5)
				poke(0x4301 + xr, 0x5d)
			else
				poke(0x4300 + xr, band(peek(0x4300 + xr), 0xf) + 0x50)
				poke(0x4301 + xr, 0xdd)
				poke(0x4302 + xr, band(peek(0x4300 + xr), 0xf0) + 0x05)
			end

			memcpy(0x6000 + i * 64, 0x4300, 0x40)
			pht1 += 0.01
			pht2 += 0.02
			pht3 += 0.04
		end

		ph1 += 0.002
		ph2 += 0.004
		ph3 += 0.03
		yield()
	end
end
```





```lua
function fx()
	local ph1, ph2, ph3 = 0, 0, 0
	local zph, zzoom, zpx, zpy = 0, 1, 0, 0
	local pht1, pht2, pht3, x, xr, lx, hx, ztx, zty, zdx, zdy, zsx, zsy

	while true do
		memset(0x4300, 0, 0x40)

		pht1, pht2, pht3 = ph1, ph2, ph3
		lx = 64
		hx = 0
		zdx = cos(zph) * (1 + sin(zzoom) * 0.5)
		zdy = sin(zph) * (1 + sin(zzoom) * 0.5)
		zsx = sin(zpx) * 20
		zsy = sin(zpy) * 20
		for i = 0, 127 do
			-- Vertical raster bars
			x = flr(63 + sin(pht1) * 19 + sin(pht2) * 9 + sin(pht3) * 7)
			xr = flr(x / 2)
			if (xr < lx) lx = xr
			if (xr + 2 > hx) hx = xr + 2

			if x % 2 == 0 then
				poke(0x4300 + xr, 0xd5)
				poke(0x4301 + xr, 0x5d)
			else
				poke(0x4300 + xr, band(peek(0x4300 + xr), 0xf) + 0x50)
				poke(0x4301 + xr, 0xdd)
				poke(0x4302 + xr, band(peek(0x4300 + xr), 0xf0) + 0x05)
			end

			-- Roto-zoomer
			ztx = zsx + i / 2 * zdy
			zty = zsy + i / 2 * zdx
			for c = 0, lx - 1 do
				poke(0x4300 + c, (band(bxor(zty, ztx), 8) == 8) and 0xaa or 0)
				ztx += zdx
				zty -= zdy
			end

			ztx += zdx * (hx - lx + 1)
			zty -= zdy * (hx - lx + 1)

			for c = hx + 1, 63 do
				poke(0x4300 + c, (band(bxor(zty, ztx), 8) == 8) and 0xaa or 0)
				ztx += zdx
				zty -= zdy
			end

			memcpy(0x6000 + i * 64, 0x4300, 0x40)
			pht1 += 0.01
			pht2 += 0.02
			pht3 += 0.04
		end

		ph1 += 0.002
		ph2 += 0.004
		ph3 += 0.03
		zph += 0.001
		zpx += 0.002
		zpy += 0.003
		zzoom += 0.001
		yield()
	end
end
```

Github repository with my PICO-8 works

## Some fantastic creations

