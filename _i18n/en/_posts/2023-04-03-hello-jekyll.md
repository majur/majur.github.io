---
title: Hello Jekyll
author: juraj
date: 2023-04-03 10:33:00 +0800
categories: [Dev]
tags: [100DaysToOffload, jekyll]
math: true
mermaid: true
pin: false
image:
  path: /assets/img/jekyll-logo.png
  lqip:
  alt: Jekyll logo
---

I have a new website. Until recently it was running on my Rails project [Blog on Rails](https://github.com/majur/blog-on-rails). However, it's not progressing as fast as I need it to, so I decided to migrate my site to [Jekyll](https://jekyllrb.com). I've known about this static page generator written in Ruby for a long time, but only tried it out a few weeks ago. And I immediately fell in love with it. I have similar feelings about it as I had when I first started with Ruby on Rails. I type a few commands into the terminal, and suddenly I'm running a new website in my browser.
## How does it work? 
The way it works is that I have a template (specifically [this one](https://github.com/cotes2020/jekyll-theme-chirpy)) that provides where on the page to display what, and how it should look. I then write the content itself in markdown which is a language designed for writing formatted text. It looks something like this:

```markdown
# Heading

Plain text

[Link text](link)

**Bold font**

![Image](path-to-picture.png)
```
{: file='_posts/my-markdown-subor.md'}

Once I have the page content finished, a single command will generate the entire page as a folder containing the .html files:

```terminal
bundle exec jekyll s
```

I can then upload this to any hosting. I chose the better option for me, and set up a repository on Github that always deploys the current output from Jekyll from the current `main` branch to my Github Pages. I then pointed my domain to the Github servers. And it's all for free. 

The main advantage of Jekyll (and other static page generators as well) is that the output is a static site composed purely of .html, .css and image files. But at the same time, when I change something in the template, like the text in the footer, I change it in one file, but Jekyll changes it in all the .html files that contain the footer. So I have a very fast and secure site (without a database) that I can manage in a simple way. 

---
P.S.: I've been using Markdown for annotations in [Obsidian](https://obsidian.md) for a couple of years now. I highly recommend this deluxe software.

[#100DaysToOffload](https://100daystooffload.com) 2/100
