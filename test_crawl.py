import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data


class TestCrawl(unittest.TestCase):

    def test_normalize_url1(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url2(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url3(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url4(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html1(self):
        input_html = '''
        <html>
            <body>
                <h1>Welcome to Boot.dev.</h1>
                <main>
                    <p>Learn to code by building real projects.</p>
                    <p>This is a second paragraph.</p>
                </main>
            </body>
        </html>
        '''
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev."
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2(self):
        input_body = "<html><body><h2>Test Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_both_h(self):
        input_body = "<html><body><h1>Test Title1</h1><h2>Bad title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title1"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_none(self):
        input_body = "<html><body><p>no title</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_mainbody(self):
        input_body = '''<html>
            <body>
                <p>
                    Wrong paragraph
                </p>
                <main>
                    <p>
                        Right paragraph
                    </p>
                </main>
            </body>
        </html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Right paragraph"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = '''<html>
            <body>
                <p>
                    Right paragraph
                </p>

                <p>
                    Wrong paragraph
                </p>
            </body>
        </html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Right paragraph"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_none(self):
        input_body = '''<html>
            <body>
                <h1>No paragraphs</h1>
                <main></main>
            </body>
        </html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href=/test><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/test"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_mixed(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <a href=/test><span>Boot.dev</span></a>
            <a href="https://crawler-test.com"><span>Boot.dev</span></a>
        </body></html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/test","https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <img src="https://crawler-test.com/logo.png" alt="Logo">
        </body></html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple_mixed(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <img src="https://crawler-test.com/logo.png" alt="Logo">
            <img src="/logo.png" alt="Logo">
        </body></html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png","https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_title_only(self):
        input_url = "test.com"
        input_body = """<html><body>
            <h2>Test Title</h2>
            </body></html>
        """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "test.com",
            "heading": "Test Title",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)
if __name__ == "__main__":
    unittest.main()
