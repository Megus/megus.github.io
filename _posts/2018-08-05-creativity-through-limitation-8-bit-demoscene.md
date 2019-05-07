---
layout: post
title: "Creativity through limitation: 8-bit demoscene"
image: /assets/blog-images/2018-08-05-cover.jpg
comments: true
tags: [demoscene, "creativity_through_limitations", "8bit"]
---

"Creativity through limitation" is an excellent approach to creative work. Sometimes you feel overwhelmed with possibilities and get stuck because of this. It may seem strange at first, but adding constraints and limits can boost your creativity. You can come up with your artificial limitations or use a tool that limits you. It works in any area: music, art, etc. Programming is not an exception. This article is about demoscene on 8-bit computer platforms and the most common trick everybody used to overcome limited graphics possibilities of these platforms.

<!--more-->

> [Demoscene] is a computer art subculture; its roots are in software cracking culture. Starting back in the 80s, crackers were adding small introductions to games — cracktros. Cracktros usually featured sweet music and visual effects. Crackers started competing for the best effects, and it became a whole new culture — the demoscene. A demo is like a music video, but the computer in real-time generates all visuals.

My favorite 8-bit platforms are ZX Spectrum and Commodore 64. It's so cool to watch how demomakers push the hardware to absolute limits; you want to scream "It's impossible!", However, it's possible. In the late 90s, I was a member of the demoscene team [Brainwave]; we made several demos for ZX Spectrum, PC, and GameBoy Advance.

8-bit platforms have different graphical limitations. Often you're limited to two or four colors for an 8-by-8 pixel block, or it's up to 16 colors for each pixel from a bigger palette. However, there's a trick which allows using more colors: "racing the beam." It is based on how CRT displays work. A ray draws the frame line by line, so if you synchronize to its movement and change color attributes before it draws the next line, you can get more colors. I had thought that this trick was used only on ZX Spectrum until I learned more about other platforms. Now I know that the history of "racing the beam" goes back to the late 70s and Atari 2600 game console, where it was the only way to display something more or less complex. So, let's begin with Atari 2600 demos!

---- 

## Atari 2600

- CPU: [MOS 6507] @ 1.19MHz
- RAM: 128 bytes (it's not a mistake. BYTES)
- Graphics: 256x192, up to 320x240, 128 colors
- Sound: [custom TIA chip]
- Release date: 1977

[Atari 2600] (also known as VCS) is the most famous second generation video game console. "Racing the beam" was the "advanced trick" on other 8-bit platforms, but for VCS game developers it was a common pain. The palette of TIA chip (it handled both video and audio) is pretty rich, but to get more than two colors in a single line, you need to race the beam while it's drawing this line.

128 bytes of RAM is not enough for anyone, every byte counts! Sound capabilities are limited as hell too: two channels with volume control and 32 possible pitches. Pitches are out of tune, so it's difficult to make it sound nice.

Atari 2600 demos are not as entertaining as, for example, C64 ones, but watch them keeping in mind all the crazy platform limitations. It's no surprise that demo coders like VCS — it's a real challenge to make any classic demo effect on it!

<iframe allowfullscreen src="https://www.youtube.com/embed/j90nIyq6_vM"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=62955">Bang! by Xayax</a></p>

<iframe allowfullscreen src="https://www.youtube.com/embed/1nTRMTnTeLQ"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=68505">Chiphead by KK/Altair^DMA</a></p>

---- 

## Atari XL/XE

- CPU: [MOS 6502] @ 1.79MHz
- RAM: 64KB
- Graphics: up to 320x192, 256 colors
- Sound: [custom POKEY chip]
- Release date: 1983

[Atari 8-bit computers] are a big step forward compared to VCS. New chips [ANTIC] and [GTIA] gave them multiple graphics modes and greater possibilities. ANTIC allows mixing different modes on a screen with a display list — a little program that defines how to draw each line. In graphics modes, you could set a color for each pixel, but only from a subset of all possible colors. In 320x192 mode, you have only 2 colors, in 80x192 modes — up to 16. If you want to display more colors simultaneously, you need to update palette each scanline — the same "racing the beam" trick.

Sounds produced by POKEY are also a giant leap from VCS's TIA. Four oscillators with several 1-bit waveforms and decent pitch accuracy (you could also pair two channels to improve it).

<iframe allowfullscreen src="https://www.youtube.com/embed/9EAG_811b4o"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=64930">Near by Agenda</a></p>

<iframe allowfullscreen src="https://www.youtube.com/embed/HVuEd742Yyg"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=9044">Numen by Taqart</a></p>

---- 

## Amstrad CPC 6128

- CPU: [Zilog Z80] @ 4MHz
- RAM: 128KB
- Graphics: 160x200, 320x200 or 640x200, 27 colors
- Sound: [General Instrument AY-3-8912]
- Release date: 1985

On [CPC] you can also set a color for each pixel, similar to Atari XL/XE. In 160x200 mode you can use 16 colors from 27 color palette, in 320x200 — 4 colors (similar to CGA on PC), in 640x200 — 2 colors. There's no display list like in Atari XL/XE, but there is a very handy h-sync interrupt which simplifies implementing "racing the beam" trick.

AY sound chip has three pulse wave oscillators, a noise generator that can be mixed with any pulse oscillator, and a simple amplitude envelope generator. However, musicians came up with a way to get more complex waveforms by using the fact that envelope generator can generate looped sawtooth and triangle envelopes and loop frequency can go to the audio range.

<iframe allowfullscreen src="https://www.youtube.com/embed/dDVAzMjA7bM"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=61177">Still Rising by Vanity</a></p>

<iframe allowfullscreen src="https://www.youtube.com/embed/6wBwbRYL-F4"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=75725">phX by Condense</a></p>

---- 

## ZX Spectrum 128

- CPU: [Zilog Z80] @ 3.5MHz
- RAM: 128KB
- Graphics: 256x192, 16 colors
- Sound: [General Instrument AY-3-8912] or Yamaha YM2149F
- Release date: 1985

[Speccy] was my first computer. ZX Basic and Z80 assembly were my first programming languages. Spectrum was the most popular 8-bit computer in Russia because Soviet engineers "hacked" its custom ULA chip and made numerous clones.

You can use only two colors ("ink" and "paper") in an 8-by-8 pixel block on Spectrum. The video memory splits into a bitmap part, and color attributes part. By using "multicolor" (that's how we call "racing the beam" on Speccy), you can get two colors in an 8-by-1 pixel block. Unlike other platforms, there are no h-sync interrupts or a way to know which line is currently being drawn, so you need to count every instruction cycle in your code to make perfect multicolor. Moreover, you'd better not waste precious CPU time by waiting; the best coders used all available CPU cycles to do some calculations for their effects.

Even with multicolor you're still limited to the 16 colors palette. Here comes another trick: if you flip two colors each frame, you get a flickery illusion of a "mixed" color. You get about 36 colors this way. The cover image for this article was drawn using this technique. Developers often used the same trick on other platforms.

<iframe allowfullscreen src="https://www.youtube.com/embed/zQ1C4FpsR2o"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=6110">Stellar Contour by Brainwave</a></p>

<iframe allowfullscreen src="https://www.youtube.com/embed/b-kkzl2foaQ"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=68035">Across the Edge by deMarche</a></p>

---- 

## Commodore 64

- CPU: [MOS 6510] @ 1MHz
- RAM: 64KB
- Graphics: 160x200 or 320x200, 16 colors
- Sound: [MOS 6581/8580 SID]
- Release date: 1982

[C64] is the king of 8-bit platforms. It is the highest-selling 8-bit computer ever, and the community is still very active. Graphics-wise C64 is comparable to other platforms, but it has some nice features:

- Hardware sprites.
- Hardware scrolling.
- Raster interrupts (remember multicolor on Speccy? On C64 you don't need to count every CPU cycle to synchronize, there's an interrupt for that)
- Combining high-res (fewer colors) and low-res (more colors) graphics on a screen.

In 320x200 mode Commodore is similar to Spectrum — only 2 colors in 8x8 block, but in 160x200 video mode, it can have 4 colors in 4x8 blocks. On top of that, it can display eight sprites. Just like on Spectrum, to achieve more colors and better graphics, C64 coders used "racing the beam" (synchronizing code with CRT display ray) trick, but as [VIC-II] video chip has raster interrupts, it was easier to implement.

The CPU of C64 is pretty slow, but the creative and smart usage of VIC-II allows demomakers to achieve results that are comparable or even better than on faster machines like ZX Spectrum or Amstrad CPC.

The most outstanding feature of C64 for me is its sound chip — SID. It was designed by a musician for musicians, and it's fantastic! Three oscillator channels with multiple waveforms, ring modulation, oscillator sync, analog multimode filter and ADSR envelopes. No other platform came close to this power!

<iframe allowfullscreen src="https://www.youtube.com/embed/52mQzN439W4"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=75743">We Come In Peace by Fairlight, Censor Design, Offence</a></p>

<iframe allowfullscreen src="https://www.youtube.com/embed/W-Crwct7U0c"></iframe>
<p class="footnote"><a href="http://www.pouet.net/prod.php?which=1216">Second Reality (C64 version) by Smash Designs</a></p>

[Demoscene]: https://en.wikipedia.org/wiki/Demoscene
[Brainwave]: http://www.pouet.net/groups.php?which=715
[MOS 6507]: https://en.wikipedia.org/wiki/MOS_Technology_6507
[custom TIA chip]: https://en.wikipedia.org/wiki/Television_Interface_Adaptor
[Atari 2600]: https://en.wikipedia.org/wiki/Atari_2600
[MOS 6502]: https://en.wikipedia.org/wiki/MOS_Technology_6502
[custom POKEY chip]: https://en.wikipedia.org/wiki/POKEY
[Atari 8-bit computers]: https://en.wikipedia.org/wiki/Atari_8-bit_family
[ANTIC]: https://en.wikipedia.org/wiki/ANTIC
[GTIA]: https://en.wikipedia.org/wiki/CTIA_and_GTIA
[Zilog Z80]: https://en.wikipedia.org/wiki/Zilog_Z80
[General Instrument AY-3-8912]: https://en.wikipedia.org/wiki/General_Instrument_AY-3-8910
[CPC]: https://en.wikipedia.org/wiki/Amstrad_CPC
[Speccy]: https://en.wikipedia.org/wiki/ZX_Spectrum
[MOS 6510]: https://en.wikipedia.org/wiki/MOS_Technology_6510
[MOS 6581/8580 SID]: https://en.wikipedia.org/wiki/MOS_Technology_SID
[C64]: https://en.wikipedia.org/wiki/Commodore_64
[VIC-II]: https://en.wikipedia.org/wiki/MOS_Technology_VIC-II