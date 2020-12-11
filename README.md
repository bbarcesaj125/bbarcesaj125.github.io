# [Tootips](https://tootips.com)

![Repository Size](https://img.shields.io/github/repo-size/bbarcesaj125/bbarcesaj125.github.io) ![Lines of Codes](https://img.shields.io/tokei/lines/github/bbarcesaj125/bbarcesaj125.github.io) ![Last Commit](https://img.shields.io/github/last-commit/bbarcesaj125/bbarcesaj125.github.io)

This repository hosts the source code of **[tootips.com](https://www.tootips.com)**. Tootips is a blog centered around the world of Linux and open source applications in general. It was started back in 2012, and was recently migrated from _Blogger_ to _Jekyll_.
This installation uses a forked version of the notorious **[Minimal Mistakes'](https://github.com/bbarcesaj125/minimal-mistakes) Jekyll theme**.

During the migration process, I used the builtin Jekyll Blogger importer to import my old posts from the Blogger platform to Jekyll.
I also wrote a python script `post_parse.py` to batch process the imported Blogger posts so that they will be compatible with the new theme. You can find this script in the `_scripts` directory.

The script does the following:

- It converts Blogger thumbnail links into full size image links using regular expressions (of course xD)
- It inserts those full size image links as teaser images into their respective posts
- It scraps Blogger posts' original links to extract the meta description and then inserts it as the excerpt in the imported posts
- It performs some ImageMagick trickery on these full size images to create fancy header images for every posts

The **ImageMagick** part of the script takes a post image like this:

[![Post image sample][2]][1]

[1]: https://tootips.com/2015/02/tox-distributed-and-secure-p2p-instant.html
[2]: https://1.bp.blogspot.com/-J9cLdzE7YGo/VPC-7D0t_sI/AAAAAAAACM8/C3KVt1_luhU/s1600/Tox-IM-Tootips.png "post image"

It then combines it with this background image:

[![Background image][4]][3]

[3]: https://tootips.com/2015/02/tox-distributed-and-secure-p2p-instant.html
[4]: /assets/images/background-pattern.webP?raw=true "background image"

The final result is a nice looking large image which can be used as a header image:

[![Header image][6]][5]

[5]: https://tootips.com/2015/02/tox-distributed-and-secure-p2p-instant.html
[6]: /assets/images/post-header-image-example.webP?raw=true "header image"
