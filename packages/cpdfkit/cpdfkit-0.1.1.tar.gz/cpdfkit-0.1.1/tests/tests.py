import unittest
import os
import tempfile
from unittest.mock import patch
from cpdfkit import generate_pdf, find_chrome

class TestChromePDFToolkit(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for storing test output files
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_find_chrome(self):
        # Test whether Chrome can be found on the system
        chrome_path = find_chrome()
        self.assertIsNotNone(chrome_path, "Chrome or Chromium should be found on the system")

    def test_generate_pdf_from_url(self):
        # Test generating a PDF from a URL and saving to a file
        output_path = os.path.join(self.test_dir.name, "output_url.pdf")
        generate_pdf(
            url_or_path="https://example.com",
            output_path=output_path,
            format="A4",
            margin_top=10,
            margin_bottom=10,
            margin_left=10,
            margin_right=10,
            js_delay=2,
            landscape=False
        )
        self.assertTrue(os.path.exists(output_path), "PDF file should be generated from URL")

    def test_generate_pdf_from_html_string(self):
        # Test generating a PDF from an HTML string and saving to a file
        html_content = """
        <html>
        <head><title>Test PDF</title></head>
        <body><h1>Hello, PDF!</h1><p>This is a test.</p></body>
        </html>
        """
        output_path = os.path.join(self.test_dir.name, "output_html.pdf")
        generate_pdf(
            html_string=html_content,
            output_path=output_path,
            format="A4",
            margin_top=10,
            margin_bottom=10,
            margin_left=10,
            margin_right=10,
            js_delay=2,
            landscape=False
        )
        self.assertTrue(os.path.exists(output_path), "PDF file should be generated from HTML string")

    def test_generate_pdf_as_byte_stream_from_url(self):
        # Test generating a PDF from a URL and returning as a byte stream
        pdf_bytes = generate_pdf(
            url_or_path="https://codingcow.de",
            format="A4",
            margin_top=10,
            margin_bottom=10,
            margin_left=10,
            margin_right=10,
            js_delay=2,
            landscape=False
        )
        self.assertIsNotNone(pdf_bytes, "PDF byte stream should be generated from URL")
        self.assertIsInstance(pdf_bytes, bytes, "Output should be of type bytes")

    def test_generate_pdf_as_byte_stream_from_html_string(self):
        # Test generating a PDF from an HTML string and returning as a byte stream
        html_content = """
        <html>
        <head><title>Test PDF</title></head>
        <body><h1>Hello, PDF!</h1><p>This is a test.</p></body>
        </html>
        """
        pdf_bytes = generate_pdf(
            html_string=html_content,
            format="A4",
            margin_top=10,
            margin_bottom=10,
            margin_left=10,
            margin_right=10,
            js_delay=2,
            landscape=False
        )
        self.assertIsNotNone(pdf_bytes, "PDF byte stream should be generated from HTML string")
        self.assertIsInstance(pdf_bytes, bytes, "Output should be of type bytes")

    @patch('cpdfkit.find_chrome', return_value=None)
    def test_generate_pdf_no_chrome(self, mock_find_chrome):
        # Test that an error is raised if Chrome is not found
        with self.assertRaises(EnvironmentError):
            generate_pdf(
                url_or_path="https://codingcow.de",
                format="A4",
                margin_top=10,
                margin_bottom=10,
                margin_left=10,
                margin_right=10,
                js_delay=2,
                landscape=False
            )

    def test_invalid_input(self):
        # Test that an error is raised if neither url_or_path nor html_string is provided
        with self.assertRaises(ValueError):
            generate_pdf(
                format="A4",
                margin_top=10,
                margin_bottom=10,
                margin_left=10,
                margin_right=10,
                js_delay=2,
                landscape=False
            )

if __name__ == "__main__":
    unittest.main()
