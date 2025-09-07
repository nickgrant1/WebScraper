import unittest
from crawl import *


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)
        input_url='https://blog.boot.dev/path/'
        self.assertEqual(normalize_url(input_url), expected)
        input_url='http://blog.boot.dev/path/'
        self.assertEqual(normalize_url(input_url), expected)
        input_url='http://blog.boot.dev/path'
        self.assertEqual(normalize_url(input_url), expected)
        input_url='//blog.boot.dev/path'
        self.assertEqual(normalize_url(input_url), expected)

    def test_domain_check(self):
        input_url = "https://blog.boot.dev/path"
        other_url = "//blog.boot.dev/path"
        actual = domain_check(input_url, other_url)
        self.assertTrue(actual)

    html='''<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>'''
    def test_get_h1_from_html(self):
        expected = 'Welcome to Boot.dev'
        self.assertEqual(get_h1_from_html(self.html), expected)

        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html(self):
        expected = 'Learn to code by building real projects.'
        self.assertEqual(get_first_paragraph_from_html(self.html), expected)
        html = '<p>This is the second paragraph.</p>'
        self.assertEqual(get_first_paragraph_from_html(html), 'This is the second paragraph.')
        html = '<h1>Welcome to Boot.dev</h1>'
        self.assertEqual(get_first_paragraph_from_html(html), '')

        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
    
    def test_get_urls_images_from_html_empty(self):
        html = '<h1>Welcome to Boot.dev</h1>'
        self.assertEqual(get_first_paragraph_from_html(html), '')
        html = '<p>Learn to code by building real projects.</p>'
        self.assertEqual(get_h1_from_html(html), '')

    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)
        input_body = '<html><body><a "//blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)

    def test_get_urls_from_html_errors(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a "//blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        with self.assertRaises(Exception):
            self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/path/to"><span>Boot.dev</span></a><a href="/path/to"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/path/to"]
        self.assertEqual(actual, expected+expected)

    def test_get_urls_from_html_empty(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><p>Some text</p></body></html>'
        actual = get_images_from_html(input_body, input_url)
        self.assertEqual(actual, [])

    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)
        
    def test_get_images_form_html_errors(self):   
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img alt="Logo"></body></html>'
        with self.assertRaises(Exception):
            actual = get_images_from_html(input_body, input_url)

    def test_get_images_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="https://blog.boot.dev/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected+expected)

    def test_get_images_from_html_empty(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><p>Some text</p></body></html>'
        actual = get_images_from_html(input_body, input_url)
        self.assertEqual(actual, [])

    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_links(self):
        input_url = "https://blog.boot.dev"
        actual = extract_page_data(self.html, input_url)
        expected = {
            "url": 'https://blog.boot.dev',
            'h1': 'Welcome to Boot.dev',
            'first_paragraph': 'Learn to code by building real projects.',
            'outgoing_links': [],
            'image_urls': []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_paragraph(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        input_url = "https://blog.boot.dev.nick"
        actual = extract_page_data(input_body, input_url)
        expected = {
            'url': 'https://blog.boot.dev.nick',
            'h1': '',
            'first_paragraph': 'Main paragraph.',
            'outgoing_links': [],
            'image_urls': []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_header(self):
        input_body = '''<html><body>
            <h1>Outside paragraph.</h1>
            <p>paragraph.</p>
        </body></html>'''
        input_url = "https://blog.boot.dev.nick"
        actual = extract_page_data(input_body, input_url)
        expected = {
            'url': 'https://blog.boot.dev.nick',
            'h1': 'Outside paragraph.',
            'first_paragraph': 'paragraph.',
            'outgoing_links': [],
            'image_urls': []
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()