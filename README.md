# InvoiceGenerator

**Advanced Python Invoice Generator with QR Payment and PDF Output**

---

## Overview
This project is a professional invoice generator written in Python. It reads client data from a CSV file, generates advance invoices in PDF format, and includes a QR code for instant payments. It is ideal for freelancers, small businesses, and startups.

---

## Features
- Generate professional PDF invoices with a clean design.
- Supports multiple services, hours, rates, and automatic total calculation.
- Calculates advance payment and balance due.
- Circular logo and social media icons for branding.
- Generates QR codes for instant payments.
- CSV-driven for bulk invoice generation.
- Easy to customize for your branding and workflow.

---

## Folder Structure

```

InvoiceGenerator/
├── invoice_generator.py       # Main Python script
├── clients.csv                # CSV file containing client data
├── invoice_number.txt         # Tracks invoice numbers
├── templates/
│   ├── logo.png               # Company logo
│   ├── logo_circle.png        # Circular logo
│   ├── icon_facebook.png
│   ├── icon_instagram.webp
│   ├── icon_linkedin.png
│   ├── icon_website.png
│   ├── Jane Roe_qr.png        # QR codes generated per client
│   └── John Doe_qr.png

````

---

## Setup Instructions

1. **Install Python** (if not installed): [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Install dependencies**:  
```bash
pip install fpdf pandas pillow qrcode
````

3. **Prepare your CSV file** (`clients.csv`) with columns:

```
Name, Company, Email, Address, Services, Hours, Rate
```

* `Services`, `Hours`, and `Rate` should be comma-separated if multiple services exist.

4. **Add your logos and social icons** in the `templates/` folder.

---

## How to Run

From your project folder, run:

```bash
python invoice_generator.py
```

* PDFs will be generated in the `invoices/` folder (created automatically).
* Invoice numbers increment automatically and are saved in `invoice_number.txt`.

---

## Notes

* Customize the header colors, fonts, and logos directly in the script.
* Ensure the QR code URL in the script points to your actual payment system.

---

## License

This project is free to use and modify.

---

## Contact

**Momand** – [[codewithmomand.com](https://www.codewithmomand.com)](https://momand0987650-sketch.github.io/codewithmomand/)
Email: momand0987650@gmail.com
