from report_generator import create_pdf_report, create_markdown_report

def test_report_files_are_created(tmp_path):
    pdf = tmp_path / "sample.pdf"
    md = tmp_path / "sample.md"
    create_pdf_report("Demo Market", "# Executive Summary\nThis is a test report.", pdf)
    create_markdown_report("Demo Market", "Sample content", md)
    assert pdf.exists() and pdf.stat().st_size > 500
    assert md.exists() and "Demo Market" in md.read_text(encoding="utf-8")
    assert pdf.read_bytes().startswith(b"%PDF")
