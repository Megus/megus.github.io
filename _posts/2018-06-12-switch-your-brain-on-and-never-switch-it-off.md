---
layout: post
title: "Switch your brain on and never switch it off!"
description: "Three stories about programmers who forgot to switch on they brain."
tags: [programming]
---

I started to learn programming when I was six, and this year I'm celebrating thirty years of my programming experience (for the last sixteen years I'm getting paid for it). I learned a lot, and I believe it's time to start to share my experience with the world. The first thing I want to share is my motto:

> — Switch your brain on and never switch it off!

I first heard this phrase from the CTO at one of my previous jobs  —  Alexander Ionov. It sounds so trivial and obvious, but it greatly affected me. I want to tell you about some cases where developers forgot to switch on their brains.

## 1. Bubble sort in the production code

It happened when we were developing a game for a social network. A network had been planning to launch a developer platform in a month, and our game was to become one of the first games there. What a godsend! However, this godsend turned into a nightmare. My teammate wrote a leaderboard generation function that queried the whole top scores table from the database and used a bubble sort. There was no code review and a little testing. The game was approved by QA team and successfully published. In the very first hours after launch the server stopped responding to requests - it was too busy doing sorting! We had to stay in the office until midnight that day and fixed the issue with simple SQL sorting.

In a couple of days SQL sorting queries also became slow, but we wrote a proper leaderboard generation module before it was too late.

I understand why my teammate did it this way: he wrote a temporary implementation (and it's perfectly fine to use bubble sort as a temporary solution), but forgot that thousands of people would use the app he wrote. Don't forget to do load testing and think how you can scale your app.

## 2. A pedometer app that crashes in an hour

A team was working on an update to a pedometer mobile app. The code quality was bad, and the team decided to refactor it. They did a great job improving the architecture, but then they made a big mistake rewriting the core logic, the step counting routine. The old routine was working perfectly fine, but the new one was very unstable, it took weeks to make it work. They finally did it, and everyone was happy, but client's QA engineers found out that app crashes during long workouts.

I joined the team to help and here's what I found: the rewritten step counting routine was querying all recorded data every step to calculate aggregate values like pace, speed, and distance. So, the data to process used more and more memory leading to an inevitable "Out of memory" crash. The original routine used a sliding window approach and could run for hours. We reverted back to the old code and adapted it to the new data model.

There's a golden rule in software development: "If something works, don't touch it!"

## 3. A chat app that can't handle a hundred messages in a conversation

Another mobile app: a messenger for sending pictures. Everything was OK until a conversation became quite long. The app crashed because it tried to keep all chat images in the memory. I'm not saying it's terrible, it's a good temporary solution for a prototype when you are more focused on the user experience. However, when you finish prototyping, you should replace your temporary solution with a proper implementation. And never forget to test your code on the real use cases!

----

I'm not saying that the developers who make these mistakes lack skills. No, usually they do a great job, but sometimes they just forget to switch their brains on. It happens to all of us, and it happened to me as well. However, every mistake is an opportunity to learn. Don't miss these opportunities!

Can you share some funny situations like that?