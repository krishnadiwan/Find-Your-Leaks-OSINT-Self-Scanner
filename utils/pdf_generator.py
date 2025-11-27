from fpdf import FPDF
from datetime import datetime
import qrcode
import tempfile

def safe_text(text):
    """Convert text to Latin-1 compatible for FPDF. Replace unsupported characters with '?'"""
    if not isinstance(text, str):
        text = str(text)
    return ''.join(c if ord(c) < 256 else '?' for c in text)

def add_qr_code(pdf, link):
    """Generate a QR code and add it to the PDF"""
    if not link:
        return
    qr = qrcode.QRCode(box_size=3, border=1)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img.save(tmp.name)
        tmp_path = tmp.name

    # Insert into PDF
    pdf.image(tmp_path, x=170, y=pdf.get_y(), w=25)
    pdf.ln(25)

class ReportPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(220, 20, 60)  # Crimson Red
        self.cell(0, 10, "Find Your Leaks - OSINT Self-Scanner", ln=True, align="C")
        self.ln(5)

    def section_title(self, title, bg_color=(230, 230, 230)):
        self.set_fill_color(*bg_color)
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, safe_text(title), ln=True, fill=True)
        self.ln(2)

    def section_content(self, content):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 7, safe_text(content))
        self.ln(2)

    def colored_bar(self, score):
        bar_width = 150
        bar_height = 7
        x_start = (210 - bar_width) / 2  # center on A4
        self.set_xy(x_start, self.get_y())
        if score <= 3:
            self.set_fill_color(0, 200, 0)  # Green
        elif score <= 7:
            self.set_fill_color(255, 215, 0)  # Yellow
        else:
            self.set_fill_color(255, 0, 0)  # Red
        self.cell(bar_width * score / 10, bar_height, "", 0, 0, '', True)
        self.ln(bar_height + 2)

def generate_report(email, username, breach_count, found_sites, score, level=None,
                    metadata_tags=None, phone_info=None, output_file=None, report_link=None):

    pdf = ReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    if not output_file:
        output_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    # Cover info
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(5)

    # QR Code
    if report_link:
        add_qr_code(pdf, report_link)

    # Phone Info
    if phone_info:
        pdf.section_title("PhoneInfoga Scan", bg_color=(240, 240, 250))
        for k, v in phone_info.items():
            pdf.section_content(f"{k}: {v}")
        pdf.section_content("Prevention: Avoid public exposure; enable 2FA.")

    # Email Breach
    pdf.section_title("Email Breach Check", bg_color=(245, 245, 240))
    pdf.section_content(f"Email: {email if email else 'N/A'}")
    pdf.section_content(f"Breaches Found: {breach_count}")
    pdf.section_content("Prevention: Change breached passwords; enable MFA; avoid reuse.")

    # Username OSINT (table)
    pdf.section_title("Username OSINT Lookup", bg_color=(240, 240, 250))
    if found_sites:
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(60, 7, "Platform", border=1, fill=True)
        pdf.cell(130, 7, "URL", border=1, fill=True)
        pdf.ln()
        pdf.set_font("Arial", "", 12)
        for site, url in found_sites.items():
            pdf.cell(60, 7, safe_text(site), border=1)
            pdf.set_text_color(0, 0, 255)
            pdf.set_font("Arial", "U", 12)
            pdf.cell(130, 7, url, border=1, ln=True, link=url)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 12)
    else:
        pdf.section_content("No public profiles found.")
    pdf.section_content("Prevention: Avoid username reuse; keep accounts private.")

    # Metadata
    pdf.section_title("Metadata Analysis", bg_color=(245, 245, 240))
    if metadata_tags and isinstance(metadata_tags, dict):
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(60, 7, "Tag", border=1, fill=True)
        pdf.cell(130, 7, "Value", border=1, fill=True)
        pdf.ln()
        pdf.set_font("Arial", "", 12)
        for k, v in metadata_tags.items():
            pdf.cell(60, 7, safe_text(k), border=1)
            pdf.cell(130, 7, safe_text(str(v)), border=1, ln=True)
    else:
        pdf.section_content("No EXIF metadata found or file unsupported.")
    pdf.section_content("Prevention: Remove EXIF metadata before sharing images.")

    # Risk Score
    pdf.section_title("Privacy Risk Score", bg_color=(240, 240, 250))
    pdf.section_content(f"Score: {score}/10")
    if level:
        pdf.section_content(f"Risk Level: {level}")
    pdf.colored_bar(score)
    pdf.section_content("Overall Recommendations: Follow preventive measures above.")

    pdf.output(output_file)
    return output_file
