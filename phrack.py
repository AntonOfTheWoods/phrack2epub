#!/usr/bin/python
import requests
import argparse
from ebooklib import epub


def phrack_to_mobi(first, last):
    for i in range(first, last + 1):
        has_more = True
        j = 0
        print "Issue {0}".format(i)
        book = epub.EpubBook()
        book_name = 'Phrack{0:03d}'.format(i)
        book.set_identifier(book_name)
        book.set_title('Phrack Issue {0:03d}'.format(i))
        book.set_language('en')
        chapters = ()
        while has_more:
            j += 1
            print "Issue {0}, article {1}".format(i, j)
            resp = requests.get(
                'http://phrack.org/archives/issues/{0}/{1}.txt'.format(i, j))
            if resp.status_code == requests.codes.ok:
                # create chapter
                chapter_name = 'phile_{0:02d}.xhtml'.format(j)
                chapter_title = 'Phile{0:02d}'.format(j)
                c1 = epub.EpubHtml(title=chapter_title, file_name=chapter_name)
                c1.content = u'<h1>{0}</h1><pre>{1}</pre>'.format(chapter_title,
                                                                  resp.text)
                book.add_item(c1)
                chapters += (c1, )

            else:
                has_more = False

        # define Table Of Contents
        book.toc += (
            epub.Link(chapter_name, chapter_title, chapter_title),
            (epub.Section('Philes'), chapters)
        )
        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # define CSS style
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(uid="style_nav",
                                file_name="style/nav.css",
                                media_type="text/css",
                                content=style)
        # add CSS file
        book.add_item(nav_css)

        # basic spine
        book.spine = list((('nav', ) + chapters))

        # write to the file
        epub.write_epub('{0}.epub'.format(book_name), book, {})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert phrack issues to mobi.')
    parser.add_argument('--first', type=int, default=1,
                        help='First issue to process (default: 1)')
    parser.add_argument('--last', type=int, default=69,
                        help='First issue to process (default: 69)')
    args = parser.parse_args()
    phrack_to_mobi(args.first, args.last)
