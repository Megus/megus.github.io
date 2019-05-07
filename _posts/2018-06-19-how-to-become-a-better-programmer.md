---
layout: post
title: "How to become a better programmer"
comments: true
tags: [programming]
---

To become a better programmer, you need to keep doing two things: practice and learn. Yes, it's that simple and obvious. Finding what to learn may be difficult, and it's great when there's someone who can give good advice. I didn't get much advice myself through my developer career, so I try to be a better leader and guide members of my teams. Here are several common recommendations I give to every junior developer.

<!--more-->

## Learn the basics of functional programming

I had a short Lisp course at the university, but I didn't understand how can I use what I learned. For a long time, I ignored functional programming. It was something obscure to me. Don't repeat my mistake! Even if you won't ever need to write in functional languages like Haskell, Scala, Erlang or Clojure, it's crucial to understand functional programming concepts and apply them in your work. Two essential concepts are:

- [Pure functions]
- [Data immutability]

Pure functions are like math functions: they always evaluate the same result given the same arguments, and they don't cause any side effects. Make as much of your functions pure as possible! Pure functions are easier to debug and maintain, and you can cover them with unit tests easily.

Immutable data structures are great because of reasons similar to pure functions: when your code uses immutable data, you get less unpleasant side effects, it saves your debug time. Instead of modifying data directly, you create a copy with necessary changes. This way if the original data is used elsewhere then your changes don't have a chance to break anything. Some languages, e.g., Swift, have native support for immutable data structures, in other languages like Javascript you can use frameworks to create immutable objects.

## Learn different programming languages

There are hundreds of languages, and you don't need to learn all of them. I like learning (or at least reading about) new languages to find useful concepts and ideas. Even if you don't use some language, you can still learn something valuable that you can apply to your work.

Of all the languages I want to highlight one of my favorite ones — [C](#). It was the second high-level language I learned (the first one was Basic), and I'm still confident that it was a very important time investment. I wouldn't recommend it as the first language for anyone, but you should try and learn C to understand how things work on a lower level. When you grasp the idea of pointers, you may feel enlightenment. I did, even that I had good experience with Assembler already.

## Understand data structures

It's important to know how different data structures (dictionaries, lists, sets, trees, etc.) work inside. Most languages or their standard libraries provide these structures out-of-the-box, and you rarely need to implement them yourself. However, this knowledge may become important when you optimize your code for performance or memory usage. To improve the understanding, try to implement common data structures in C. It's an excellent exercise.

## Learn about software architecture

You shouldn't underestimate the importance of a good software architecture! If your project is bigger than a simple calculator, you'd better design an architecture properly.

Define interfaces/protocols, make smaller classes, use class inheritance wisely, break down your code into layers (entities, repositories, use cases, user interface, etc.), write testable code... Software architecture is a vast topic, there are many different approaches and no single correct answer, but my recommendations would be:

- Learn [SOLID principles].
- Read about [“Clean Architecture” by Robert Martin (Uncle Bob)].

---- 

It's not an exhaustive list of recommendations, and it only covers hard skills. To become a better developer, you should also develop various soft skills. And here are some bits of advice to wrap up this article:

- Be curious, never stop learning!
- Be modest, accept the fact that there are developers better than you and learn from them.
- Don't be afraid to ask questions
- Become a good team player

[Pure functions]: https://en.wikipedia.org/wiki/Pure_function
[Data immutability]: https://en.wikipedia.org/wiki/Immutable_object
[SOLID principles]: https://en.wikipedia.org/wiki/SOLID
[“Clean Architecture” by Robert Martin (Uncle Bob)]: https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html
