---
title: "Technologies I Am Investing in 2024"
date: 2024-02-01T14:33:01+03:00
tags:
  ["neovim", "laravel", "echo", "tailwind", "github", "kubernetes", "go", "lua"]
topics: ["Technology", "Development"]
---

As it turns out, I am bad at blogging, who knew? (I knew, since like literally one of the first piece of code I wrote everytime I learn a new language/stack is a blog and I have a blog since 2oo3 but I am still hopeful like an idiot everytime I put up a new blog, I will write lots of posts.)

But I think this is a good concept, like [yearly themes](https://www.relay.fm/cortex/150), setting some tech stacks as key points and some as goals is a good way for me personally to look back and see a good timeline.

### I love APIs but client apps suck.

I think first app I break apart from a single full stack monolith to a server side api + client side app was Poltio's social network application in 2015 or 2016.

Back then the idea of having a client app where you can just keep as couple of static files (html, js and css) and host it on a very easy to scale storage buckets like AWS S3 was amazing. Like all good things, we put too much stuff in our client bundles and made everything more complex and worse.

With how things going in client side worlds (eg: nextjs or remix), full stack applications coming back hard and they SHOULD. Like sending a HTML genrated dynamically on the server with minimal css and js required for that route is the best way for web applications.

So after watching nextjs and remix.run re-discover basic http and web concepts 20+ years later for the last couple of years, I am completely giving up and removing react, vue and their hormonal fullstack counterparts from my stack.

We (at Poltio) still have 2 nextjs applications running which I am in the process of replacing with a Laravel + Livewire application and our widgets still powered by Remix.run which will be harder to replace but not impossible.

So no more next/remix for me, thanks for all the fish.

### Small Services

I love devops, kubernetes and writing isolated services. But I don't like to overcomplicate things to the point where the small teams that I work with have more trouble understanding what the heck is going on. But since I use kubernetes like everywhere thesedays, creating and deploying a new service internally or externally is not a big deal.

For those kind of services my language of choice is Go. I was planning on focusing more on Rust in 2023 but it didn't pan out like I hoped. I really love the desicions Go is making and I have more fun writing Go. Since the memory advantages that Rust has over Go doesn't impact any code I wrote, I get to stick with what I enjoy <3

### Lua <3

I freaking LOVE lua. I started with it with neovim config but currently if I have 2 alternatives for an app, one uses lua for config/scriptting and other uses anything else (yaml/toml/etc), I choose the lua one. I love lua.

[Hammerspoon](https://www.hammerspoon.org/)
[Wezterm](https://wezfurlong.org/wezterm/index.html)
[Neovim](https://neovim.io/)

### LLMs and Transformers are NFTs in 2024

I love machine learning and ai, always have. But like the current bubble we are in where everybody talking about AI and using AI and worshipping AI is not a good place for AI. It gives crypto/nft vibes by people who have no idea about the actual technology but trying to ride the wave.

I am wishing the trend dies down a bit so people who are working on building and training the llm models can go back to building useful stuff.
