---
layout: project
title: "Defold extensions"
description: "Open-source libraries and extensions for Defold game engine"
image: /assets/portfolio/defold-extensions.jpg
order: 5
seo:
  type: WebPage
---

I've created several open-source extensions for [Defold](https://defold.com). Defold is a free game engine developed by [King](https://king.com). It uses [Lua](https://www.lua.org) for scripting.

### [whDefRouter — screen manager](https://www.megus.org/defold-router/)

Defold doesn't provide standard functions to implement complex navigation between game screens. The provided examples only show the general idea of switching screens with collection proxies, but a game usually has more than just two screens. So I developed a reusable navigation solution. I took the inspiration from UINavigationContoller in iOS and React/Redux. My library was the first of its kind, but now other solutions also exist.

### [whDefQuest — a helper library for quest games](https://github.com/Megus/whdefquest)

A modular helper library for quest games created with Defold game engine. The primary functions it gives are:

- Inventory management
- Dialogues with NPC

Everything else can be added with custom modules. The library itself doesn't use any Defold-specific API, so you can use it with any other game engine.

## [DefTensor — TensorFlow Lite for Defold](https://github.com/Megus/deftensor)

An attempt to implement a Defold Native Extension for TensorFlow Lite. It can be used to run TF models on mobile devices. It's still WIP; currently, it runs only on macOS.