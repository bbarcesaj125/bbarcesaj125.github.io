# Post Parser

This is a Python script that I wrote as part of my effort to migrate my website **[Tootips](https://tootips.com)** from _Blogger_ to _Jekyll_.
When you use the Jekyll built-in Blogger importer, it imports your Blogger posts to the Jekyll's `.yaml` format by adding a _Front Matter_ like so:

```
---
layout: single
title: 'Deluge: Lightweight BitTorrent Client'
date: '2012-05-29T17:54:00.000+02:00'
author: bbarcesaj
tags:
- PPA
- Torrent
- Ubuntu
- Windows
- Cross-Platform
- EyeCandy
- Review
modified_time: '2012-06-15T20:22:47.073+02:00'
thumbnail: http://1.bp.blogspot.com/-I5MhKiXm1D8/T8Tt05rbeAI/AAAAAAAAARU/bMVq7yH3mkc/s72-c/Selection_006.png
blogger_id: tag:blogger.com,1999:blog-8900647196714997279.post-6398697937519042863
blogger_orig_url: http://www.tootips.com/2012/05/deluge-lightweight-bittorrent-client.html
---
```

While this might work for most people, there are however some use cases where you need to edit every imported post to add customizations like a header image or a meta description etc.
In these cases, you are left with two choices: either you edit every post manually to include the desired changes, which can become quite a burden, especially if you have hundreds of posts, or you could take the lazy approach and write a little program or script to automate the whole process. Personally, I chose the latter, why? Well, because I can xD

As I explained in this repository's [`README.md`](../README.md) file, the script `post-parser.py` does the following:

- It converts Blogger thumbnail links into full size image links using regular expressions (of course xD)
- It inserts those full size image links as teaser images into their respective posts
- It scraps Blogger posts' original links to extract the meta description and then inserts it as the excerpt in the imported posts
- It performs some ImageMagick trickery on these full size images to create fancy header images for every posts

Since my Jekyll installation uses the **[Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) theme**, I had to add the following lines to every post to make use of the theme's header overlay feature:

```
excerpt: "This post should [...]"
header:
  overlay_image: /assets/images/unsplash-image-1.jpg
  overlay_filter: 0.5 # same as adding an opacity of 0.5 to a black background
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
  actions:
    - label: "More Info"
      url: "https://unsplash.com"
```

After I run `post_parser.py` on my `_posts` directory, the resulting post's front matter should look something like this:

```
---
layout: single
title: 'Deluge: Lightweight BitTorrent Client'
date: '2012-05-29T17:54:00.000+02:00'
author: bbarcesaj
tags:
- PPA
- Torrent
- Ubuntu
- Windows
- Cross-Platform
- EyeCandy
- Review
modified_time: '2012-06-15T20:22:47.073+02:00'
thumbnail: http://1.bp.blogspot.com/-I5MhKiXm1D8/T8Tt05rbeAI/AAAAAAAAARU/bMVq7yH3mkc/s72-c/Selection_006.png
blogger_id: tag:blogger.com,1999:blog-8900647196714997279.post-6398697937519042863
blogger_orig_url: http://www.tootips.com/2012/05/deluge-lightweight-bittorrent-client.html
excerpt: "Deluge is a cross-platform torrent client which supports protocol encryption."
header:
  teaser: http://1.bp.blogspot.com/-I5MhKiXm1D8/T8Tt05rbeAI/AAAAAAAAARU/bMVq7yH3mkc/s1600/Selection_006.png
  overlay_image: "/images/posts/2012-05-29-deluge-lightweight-bittorrent-client-final.webP"
  overlay_filter: rgba(0, 255, 55, 0.4), rgba(9, 105, 17, 0.78)
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---
```

## Dependencies

The Python dependencies are included in the [`Pipfile`](./Pipfile). As you see in this file, the only required dependency is `BeautifulSoup4`.
Since this script uses **ImageMagick** to process the images, you will need to install that too.

## Usage

First, create a directory at the root of your Jekyll project, then put `post_parser.py` in it. In my example, I created a directory called `_scripts`. You can use any name you like.
After that, you need to install the dependencies listed above. To install the Python dependencies, you can use the following commands:

```
$ cd ./_scripts
$ pip install or pipenv install
```

Next, you need to install **ImageMagick**. To do that, you can use your distribution package manager as **ImageMagick** is included in all the major distributions' official repositories.
Finally, you can invoke the script just like you would do with any Python script. I highly recommend that you back up your `_posts` directory before using this script, so that you can easily restore your posts in case something goes wrong.
