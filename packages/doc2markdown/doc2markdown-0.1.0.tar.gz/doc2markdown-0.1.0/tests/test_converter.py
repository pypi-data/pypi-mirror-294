import unittest
import os
import tempfile
from unittest.mock import patch, mock_open, Mock
from doc2markdown.converter import (
    extract_pdf_to_markdown,
    extract_pptx_to_markdown,
    extract_docx_to_markdown,
    clean_markdown,
    process_file_to_markdown,
    process_folder,
)

class TestConverter(unittest.TestCase):
    @patch('doc2markdown.converter.PdfReader')
    def test_extract_pdf_to_markdown(self, mock_pdf_reader):
        mock_pdf = Mock()
        mock_pdf.pages = [
            Mock(extract_text=lambda: 'Page 1 content'),
            Mock(extract_text=lambda: 'Page 2 content'),
        ]
        mock_pdf_reader.return_value = mock_pdf

        result = extract_pdf_to_markdown('test.pdf')
        expected = "# test.pdf\n\n## Page 1\n\nPage 1 content\n\n## Page 2\n\nPage 2 content\n\n"
        self.assertEqual(result, expected)
        mock_pdf_reader.assert_called_once_with('test.pdf')

    @patch('doc2markdown.converter.Presentation', autospec=True)
    def test_extract_pptx_to_markdown(self, MockPresentation):
        mock_prs = MockPresentation.return_value
        mock_slide1 = Mock()
        mock_slide1.shapes = [Mock(text='Slide 1 content')]
        mock_slide2 = Mock()
        mock_slide2.shapes = [Mock(text='Slide 2 content')]
        mock_prs.slides = [mock_slide1, mock_slide2]

        result = extract_pptx_to_markdown('test.pptx')
        expected = "# test.pptx\n\n## Slide 1\n\nSlide 1 content\n\n## Slide 2\n\nSlide 2 content\n\n"
        self.assertEqual(result, expected)
        MockPresentation.assert_called_once_with('test.pptx')

    @patch('doc2markdown.converter.Document')
    def test_extract_docx_to_markdown(self, mock_document):
        # Set up your mock document
        mock_doc = Mock()
        mock_document.return_value = mock_doc

        # Create a mock paragraph with a style that has a name
        mock_para = Mock()
        mock_para.style.name = "Heading 1"  # Or any other appropriate heading style
        mock_para.text = "Test Heading"

        # Set up the document to return this paragraph
        mock_doc.paragraphs = [mock_para]

        # Call the function and assert the result
        result = extract_docx_to_markdown('test.docx')
        # Add your assertions here

    def test_clean_markdown(self):
        dirty_markdown = "  This is  a   test  \n\n\n  with   extra   spaces  \n\n  and newlines  "
        expected = "This is a test\n\nwith extra spaces\n\nand newlines"
        self.assertEqual(clean_markdown(dirty_markdown), expected)

    @patch('doc2markdown.converter.extract_pdf_to_markdown')
    @patch('doc2markdown.converter.extract_pptx_to_markdown')
    @patch('doc2markdown.converter.extract_docx_to_markdown')
    def test_process_file_to_markdown(self, mock_docx, mock_pptx, mock_pdf):
        mock_pdf.return_value = "PDF content"
        mock_pptx.return_value = "PPTX content"
        mock_docx.return_value = "DOCX content"

        with tempfile.TemporaryDirectory() as temp_dir:
            # Test PDF
            process_file_to_markdown('test.pdf', temp_dir)
            with open(os.path.join(temp_dir, 'test.md'), 'r') as f:
                self.assertEqual(f.read(), "PDF content")

            # Test PPTX
            process_file_to_markdown('test.pptx', temp_dir)
            with open(os.path.join(temp_dir, 'test.md'), 'r') as f:
                self.assertEqual(f.read(), "PPTX content")

            # Test DOCX
            process_file_to_markdown('test.docx', temp_dir)
            with open(os.path.join(temp_dir, 'test.md'), 'r') as f:
                self.assertEqual(f.read(), "DOCX content")

            # Test unsupported file
            with self.assertLogs(level='WARNING') as cm:
                process_file_to_markdown('test.txt', temp_dir)
            self.assertIn("Skipping unsupported file: test.txt", cm.output[0])

    @patch('doc2markdown.converter.process_file_to_markdown')
    def test_process_folder(self, mock_process_file):
        with tempfile.TemporaryDirectory() as temp_input_dir, \
             tempfile.TemporaryDirectory() as temp_output_dir:
            
            # Create test files
            open(os.path.join(temp_input_dir, 'test1.pdf'), 'w').close()
            open(os.path.join(temp_input_dir, 'test2.pptx'), 'w').close()
            os.mkdir(os.path.join(temp_input_dir, 'subdir'))
            open(os.path.join(temp_input_dir, 'subdir', 'test3.docx'), 'w').close()

            process_folder(temp_input_dir, temp_output_dir)

            mock_process_file.assert_any_call(os.path.join(temp_input_dir, 'test1.pdf'), temp_output_dir)
            mock_process_file.assert_any_call(os.path.join(temp_input_dir, 'test2.pptx'), temp_output_dir)
            mock_process_file.assert_any_call(os.path.join(temp_input_dir, 'subdir', 'test3.docx'), temp_output_dir)
            self.assertEqual(mock_process_file.call_count, 3)

    @patch('doc2markdown.converter.extract_pptx_to_markdown')
    @patch('builtins.open', new_callable=mock_open, read_data="dummy data")
    def test_process_file_to_markdown(self, mock_file, mock_extract):
        mock_extract.return_value = "Mocked markdown content"
        
        with self.assertLogs(level='WARNING') as cm:
            result = process_file_to_markdown('test.pptx', 'output_dir')
        
        self.assertIn("Markdown file created", cm.output[0])
        mock_extract.assert_called_once_with('test.pptx')
        mock_file.assert_called_with('output_dir/test.md', 'w', encoding='utf-8')

if __name__ == '__main__':
    unittest.main()
