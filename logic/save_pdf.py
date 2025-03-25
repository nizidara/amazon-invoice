import base64
import os

from properties import invoice_dir

# pdfの保存
def save_pdf(driver, order_date, order_id):
    try:
        # PDFとして保存
        pdf_path = os.path.join(invoice_dir, f'{order_date}_{order_id}.pdf')

        pdf = driver.execute_cdp_cmd('Page.printToPDF', {
            'printBackground': True,
            'landscape': False,
            'paperWidth': 8.27,  # A4の幅（インチ）
            'paperHeight': 11.69,  # A4の高さ（インチ）
            'marginTop': 0,
            'marginBottom': 0,
            'marginLeft': 0,
            'marginRight': 0,
        })

        # Base64エンコードされたPDFデータをデコード
        pdf_bytes = base64.b64decode(pdf['data'])
        
        with open(pdf_path, 'wb') as file:
            file.write(pdf_bytes)

        return os.path.exists(pdf_path)
    
    except Exception as e:
        print(f"Error saving PDF: {e}")
        return False