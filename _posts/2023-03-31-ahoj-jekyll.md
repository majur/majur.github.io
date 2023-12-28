---
title: Ahoj Jekyll
author: juraj
date: 2023-03-31 10:33:00 +0800
categories: [Dev]
tags: [100DaysToOffload-sk, jekyll]
math: true
mermaid: true
pin: false
image:
  path: /assets/img/jekyll-logo.png
  lqip:
  alt: Jekyll logo
---

Mám nový web. Donedávna bežal na mojom Rails projekte [Blog on Rails](https://github.com/majur/blog-on-rails-legacy). S ním sa mi ale nedarí napredovať tak rýchlo ako by som potreboval, a preto som sa rozhodol svoj web zmigrovať na [Jekyll](https://jekyllrb.com). O tomto generátore statických stránok písanom v Ruby som vedel už dlho, ale až pred pár týždnami som si ho vyskúšal. A hneď som si ho zamiloval. Mám z neho podobné pocity aké som mal na mojom začiatku s Ruby on Rails. Zadám pár príkazov do terminálu, a zrazu mi beží nový web v prehliadači.
## Ako to funguje? 
Funguje to tak že mám šablónu (konkrétne [túto](https://github.com/cotes2020/jekyll-theme-chirpy)), ktorá zabezpečuje kde na stránke sa má čo zobraziť, a ako to má vyzerať. Samotný obsah potom píšem v markdowne čo je jazyk určený na písanie formátovaného textu. Vyzerá cca takto:

```markdown
# Nadpis

Bežný text

[Text linku](link)

**Tučné písmo**

![Obrázok](cesta-k-obrazku.png)
```
{: file='_posts/moj-markdown-subor.md'}

Keď mám obsah stránky dopísaný, tak jediným príkazom vygenerujem celú stránku ako zložku obsahujúcu .html súbory:

```terminal
bundle exec jekyll s
```

To môžem potom nahrať na hocijaký hosting. Ja som zvolil pre mna lepšiu možnost a na Githube som si nastavil repozitár, ktorý mi z aktuálnej vetvy `main` vždy nasadí na Github Pages aktuálny výstup z Jekyllu. Následne som na servery Githubu nasmeroval svoju doménu. A to všetko zadarmo. 

Hlavná výhoda Jekyllu (ale aj ostatných generátorov statických stránok) je tá, že výstupom je statický web zložený čisto zo súborov .html, .css a obrázkou. Zároveň ale keď zmením niečo v šablóne, napríklad text vo footeri, tak ja to mením v jednom súbore, ale Jekyll mi to zmení vo všetkých .html súboroch, v ktorých sa nachádza footer. Takže mám veľmi rýchly a bezpečný web (bez databázy), ktorý viem jednoduchým spôsobom spravovať. 

---
P.S.: Markdown používam na poznámky v programe [Obsidian](https://obsidian.md) už pár rokov. Veľmi odporúčam tento luxusný software. 

[#100DaysToOffload](https://100daystooffload.com) 2/100
