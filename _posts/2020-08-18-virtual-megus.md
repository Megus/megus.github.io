---
layout: post
title: "Virtual Megus: my experiment with generative music"
description: "A year ago, I began working on my biggest pet project — Virtual Megus. What is it and why I’m working on it."
image: /assets/blog-images/2020-08-18-cover.jpg
tags: [virtualmegus, music]
---

# Virtual Megus: my experiment with generative music

{% youtube ntrQNkF8z7g %}

A year ago, I began working on my current biggest pet project — [Virtual Megus](https://megus.org/virtual-megus/), a generative music system. Music is my hobby, and programming is my job. Projects which combine both of my main passions were always my favorite. I had the idea to create a program that composes music for years but never did it. Last August, I was on vacation and had plenty of time, so I finally decided to give it a try.

Brian Eno, an ambient music pioneer, used the term “Generative music” to describe any music that is ever-different and changing, created by a system. However, the idea of creating music using algorithms or systems is far from new. According to [this article](https://ccrma.stanford.edu/~blackrse/algorithm.html), it dates back to the ancient Greeks! During the Classical period, one of “Musical dice games” (“Musikalisches Würfelspiel” in German) was attributed to Mozart himself, but, according to Wikipedia, this attribution hasn’t been authenticated.

There are many generative music apps, and I tried a number of them. Some were simple and were generating abstract, ambient, and unstructured music. Others had an overwhelming amount of possibilities, but the learning curve was steep. So, like any typical programmer, I decided to invent my own system.

Eno’s definition of generative music covers many different approaches. Manipulating pieces of pre-recorded music, random noises, rule-based composition — these are just a few examples. I picked the path of algorithmic composition. Creations often resemble their creators, mine is not an exception, hence the name — Virtual Megus. I want my system to “compose” melodic electronic music with a song-like structure. It’s an ambitious task, and as a self-taught musician without any formal music education, I realized that I can’t do it without learning music theory. I found an old Soviet music harmony textbook and began studying. When I learn something new, I add it to Virtual Megus.

When I was beginning the work, I decided to make Virtual Megus available to everyone, that’s why it’s not a desktop or a mobile app, but a web application. Everything happens right in a browser, there’s no server-side code at all. As I wanted to learn WebAudio API better, I implemented everything myself from scratch without using any 3rd-party libraries like [Tone.js](https://tonejs.github.io). I also didn’t want to use any Javascript build systems, so all code is pure ES8 and is hosted directly from the repository with GitHub Pages.

What I’ve implemented so far:

- Sample-based drum machine.
- Monophonic and polyphonic synths.
- Song structure generator based on a state machine.
- Chord sequence generator for diatonic scales.
- Generators for drum patterns, bass, arpeggios, pads, and melodies.
- Visualization system.

The most challenging one for me now is the melody generator. It produces quite lovely results but still makes many harmony mistakes. I continue to improve every module, sometimes I even rewrite them from scratch when I decide to improve the system architecture or come up with new ideas.

My generative music journey is only beginning. Virtual Megus backlog already has over 40 items, and it’s growing every week! Whenever I learn something new about music theory from books, Wikipedia, or YouTube videos, I get even more ideas.

- [Listen to Virtual Megus](https://megus.org/virtual-megus/)
- [Source code on GitHub](https://github.com/Megus/virtual-megus)