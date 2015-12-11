#! /usr/bin/python
import html2text
import subprocess
import os

fns = """
_posts/2011-05-25-lunch-pa-restaurang-platinis.html
_posts/2011-05-25-nu-har-aven-jag-blivit-med-en-blog.html
_posts/2011-05-25-restaurang-rosen-och-sjuttitalet.html
_posts/2011-05-27-dhl-och-hemmakontor.html
_posts/2011-05-30-dhl-fortsattningen.html
_posts/2011-06-05-restaurang-trattoria-la-casa.html
_posts/2011-06-09-reverse-engineering-part-1-introduction.html
_posts/2011-06-09-reverse-engineering-part-2-schematics.html
_posts/2011-07-12-pong-asian-tapas-kista.html
_posts/2011-07-12-restaurang-88-kista.html
_posts/2011-11-15-sd-sniffer.html
_posts/2011-11-27-sd-sniffer-part-2.html
_posts/2011-12-03-tdr-scope.html
_posts/2012-11-12-persistent-device-naming-on-fedora-17.html
_posts/2012-11-14-the-gnome-3-disaster.html
_posts/2013-04-15-nfc-vad-ar-det.html
_posts/2013-08-03-coaxial-cables.html
_posts/2013-10-24-creating-android-menu-icons-with_6403.html
_posts/2013-10-24-weader-simple-atomrss-feed-reader-for.html
_posts/2013-11-15-lifehacking.html
_posts/2013-11-18-halloween-milling.html
_posts/2014-03-05-getting-html-source-from-android-webview.html
_posts/2014-10-25-kass-marknadsforing.html
_posts/2015-08-09-scratching-itch-rdesktop.html
_posts/2015-11-14-running-wxpython-30-on-linux-mint-172.md
""".strip().split()

def fix_permalink(fn):
    prefix = 'blogger_orig_url:'

    a = []
    for l in open(fn):
        if l.startswith(prefix):
            l = 'permalink:' + l[len(prefix):]
            l = l.replace('http://blog.weinigel.se', '')
        a.append(l)

    open(fn, 'w').writelines(a)

def convert_to_markdown(fn):
    if not fn.endswith('.html'):
        return

    oldfn = fn + '~'
    newfn = fn[:-5] + '.md'

    print fn, oldfn

    try:
        data = open(fn).read()
        os.rename(fn, oldfn)
    except IOError:
        data = open(oldfn).read()

    i = 0
    i = data.index('---\n', i) + 4
    i = data.index('---\n', i) + 4
    front_matter = data[:i]
    html = data[i:]

    markdown = html2text.html2text(html)
    markdown = markdown.replace('&nbsp_place_holder;', ' ')

    print markdown
    print '-' * 72

    open(newfn, 'w').write(front_matter + markdown)

def main():
    for fn in fns:
        # fix_permalink(fn)
        convert_to_markdown(fn)

main()

