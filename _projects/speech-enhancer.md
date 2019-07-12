---
layout: project
title: "Speech enhancer"
description: "Automatic speech recordings enhancer working in a browser"
image: /assets/portfolio/speech-enhancer.png
order: 2
seo:
  type: WebPage
---

I developed a speech recording enhancer that works in a browser. It makes speech louder and more intelligible by applying several effects:

- Noise reduction based on noise profile
- Equalization
- Dynamic range compression

There are no parameters to tweak because users shouldn’t have to do anything to have their recordings sound equally load no matter what device they use or where do they record. It’s a kind of a “magic button.”

The enhancer is implemented in JavaScript and uses WebAudio API for equalization and dynamic range compression to make processing faster.
