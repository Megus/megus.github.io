---
layout: project
title: Guitarability
description: "Performance evaluation module for a guitar training application"
image: /assets/portfolio/guitarability.png
order: 1
---

![Guitarability UI](/assets/portfolio/guitarability-animation.gif)


Guitarability was a guitar training application for the iPad. It contained over a thousand exercises on different aspects of guitar playing (rhythm, picking, strumming, legato, scales, bends, and other). Guitarability was a “dream project” for me because I’m a self-taught guitar player and I’m interested in digital signal processing, but I hadn’t had a chance to apply my knowledge of DSP in a commercial project. I managed this project and developed one of the core modules — a performance evaluation module.

The module has two parts: timing analyzer and polyphonic pitch detector. The most challenging one was the pitch detector. The application had to recognize not only single notes but chords too. Polyphonic Pitch Detection is a difficult task; there’s no “one and only true way” to do it; there are no commercial-grade open-source implementations.

Another challenge was that my module had to work in real time on the iPad. I managed to get 600% performance boost compared to the first implementation, which couldn’t even work in real time. This performance improvement allowed to add smooth animations and video recording. I achieved the performance boost mostly by math optimizations. The module is written in Objective-C and uses Accelerate framework.
