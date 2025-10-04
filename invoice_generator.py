from fpdf import FPDF
import pandas as pd
from datetime import date, timedelta
import os
from PIL import Image, ImageDraw
import qrcode

print("Starting advanced professional invoice generation...")

# =============================
# Paths & Setup
# =============================
base_path = r"C:\Users\fahim\Desktop\InvoiceGenerator"
csv_file = os.path.join(base_path, "clients.csv")
templates_folder = os.path.join(base_path, "templates")
logo_file = os.path.join(templates_folder, "logo.png")
output_folder = os.path.join(base_path, "invoices")
os.makedirs(output_folder, exist_ok=True)

invoice_number_file = os.path.join(base_path, "invoice_number.txt")
if os.path.exists(invoice_number_file):
    with open(invoice_number_file, "r") as f:
        invoice_number = int(f.read().strip())
else:
    invoice_number = 1001

# Social icons
social_icons = {
    "website": os.path.join(templates_folder, "icon_website.png"),
    "linkedin": os.path.join(templates_folder, "icon_linkedin.png"),
    "instagram": os.path.join(templates_folder, "icon_instagram.png"),
    "facebook": os.path.join(templates_folder, "icon_facebook.png")
}

# =============================
# Circular logo
# =============================
circle_logo_path = os.path.join(templates_folder, "logo_circle.png")
if os.path.exists(logo_file):
    img = Image.open(logo_file).convert("RGBA")
    w, h = img.size
    size = min(w, h)
    img = img.crop(((w - size)//2, (h - size)//2, (w + size)//2, (h + size)//2))
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    img.putalpha(mask)
    background = Image.new("RGBA", img.size, (255, 255, 255, 255))
    background.paste(img, (0, 0), img)
    background.save(circle_logo_path)

# =============================
# Read CSV
# =============================
df = pd.read_csv(csv_file)

for index, row in df.iterrows():
    client_name = row['Name']
    company = row['Company']
    email = row['Email']
    billing_address = row.get('Address', '')
    
    services = str(row['Services']).split(',')
    hours_list = str(row['Hours']).split(',')
    rate_list = str(row['Rate']).split(',')
    total_list = [int(h)*int(r) for h, r in zip(hours_list, rate_list)]
    subtotal = sum(total_list)
    advance_percent = 50  # % of advance payment
    advance_payment = subtotal * advance_percent // 100
    balance_due = subtotal - advance_payment

    # =============================
    # PDF Setup
    # =============================
    pdf = FPDF('P','mm','A4')
    pdf.add_page()
    
    # Colors
    header_color = (52,152,219)
    table_header_color = (41,128,185)
    table_row_color1 = (236,240,241)
    table_row_color2 = (255,255,255)
    text_color = (0,0,0)

    # =============================
    # Header with Logo
    # =============================
    pdf.set_fill_color(*header_color)
    pdf.rect(0,0,210,50,'F')
    if os.path.exists(circle_logo_path):
        pdf.image(circle_logo_path,x=10,y=10,w=35,h=35)
    pdf.set_y(20)
    pdf.set_font("Arial",'B',24)
    pdf.set_text_color(255,255,255)
    pdf.cell(0,15,"ADVANCE INVOICE",ln=True,align='C')
    pdf.set_font("Arial",'I',10)
    pdf.set_y(45)
    pdf.cell(0,5,"www.codewithmomand.com",ln=True,align='C')

    # =============================
    # Invoice Details
    # =============================
    pdf.set_y(55)
    pdf.set_font("Arial",'',12)
    pdf.set_text_color(0,0,0)
    pdf.cell(0,8,f"Date: {date.today()}",ln=True)
    pdf.cell(0,8,f"Due Date: {date.today()+timedelta(days=7)}",ln=True)
    pdf.cell(0,8,f"Invoice #: {invoice_number}",ln=True)
    pdf.cell(0,8,f"Advance Payment: {advance_percent}%",ln=True)
    pdf.ln(2)

    # =============================
    # Client Info
    # =============================
    pdf.set_font("Arial",'B',12)
    pdf.cell(0,8,"Bill To:",ln=True)
    pdf.set_font("Arial",'',12)
    pdf.cell(0,8,f"{client_name} ({company})",ln=True)
    if billing_address:
        pdf.cell(0,8,f"Billing Address: {billing_address}",ln=True)
    pdf.cell(0,8,f"Email: {email}",ln=True)
    pdf.ln(5)

    # =============================
    # Line Items Table
    # =============================
    pdf.set_fill_color(*table_header_color)
    pdf.set_text_color(255,255,255)
    pdf.set_font("Arial",'B',12)
    pdf.cell(80,10,"Service",border=1,fill=True)
    pdf.cell(30,10,"Hours",border=1,fill=True,align='C')
    pdf.cell(40,10,"Rate ($)",border=1,fill=True,align='C')
    pdf.cell(40,10,"Total ($)",border=1,fill=True,align='C')
    pdf.ln()

    pdf.set_font("Arial",'',12)
    for i,(s,h,r,t) in enumerate(zip(services,hours_list,rate_list,total_list)):
        row_color = table_row_color1 if i%2==0 else table_row_color2
        pdf.set_fill_color(*row_color)
        pdf.set_text_color(*text_color)
        pdf.cell(80,10,s.strip(),border=1,fill=True)
        pdf.cell(30,10,str(h),border=1,fill=True,align='C')
        pdf.cell(40,10,str(r),border=1,fill=True,align='C')
        pdf.cell(40,10,str(t),border=1,fill=True,align='C')
        pdf.ln()

    # =============================
    # Totals
    # =============================
    pdf.ln(2)
    pdf.cell(150,10,"Subtotal ($)",border=0,align='R')
    pdf.cell(40,10,str(subtotal),border=1,align='C')
    pdf.ln(7)
    pdf.cell(150,10,f"Advance Payment ({advance_percent}%)",border=0,align='R')
    pdf.cell(40,10,str(advance_payment),border=1,align='C')
    pdf.ln(7)
    pdf.cell(150,10,"Balance Due ($)",border=0,align='R')
    pdf.cell(40,10,str(balance_due),border=1,align='C')
    pdf.ln(7)

    # =============================
    # Payment instructions & QR
    # =============================
    pdf.set_font("Arial",'I',10)
    pdf.set_text_color(50,50,50)
    pdf.multi_cell(0,6,"Payment due in 7 days. Please scan the QR code to pay the advance. Thank you!")

    qr_path = os.path.join(templates_folder,f"{client_name}_qr.png")
    qr = qrcode.QRCode(box_size=4,border=1)
    qr.add_data(f"https://www.payments.com/pay?amount={advance_payment}")
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black",back_color="white")
    img_qr.save(qr_path)
    pdf.image(qr_path,x=10,y=pdf.get_y(),w=30,h=30)
    pdf.set_xy(45,pdf.get_y()+10)
    pdf.cell(0,10,"Scan to pay instantly",ln=True)

    # =============================
    # Footer with social links
    # =============================
    pdf.set_y(-25)
    x_start = 60
    for key,path in social_icons.items():
        if os.path.exists(path):
            pdf.image(path,x=x_start,y=pdf.get_y()-5,w=8,h=8)
            x_start += 12
    pdf.set_x(10)
    pdf.set_font("Arial",'I',10)
    pdf.set_text_color(100,100,100)
    pdf.cell(0,10,"www.codewithmomand.com | Thank you for your business!",align='C')

    # =============================
    # Save PDF
    # =============================
    filename = os.path.join(output_folder,f"invoice_{client_name.replace(' ','_')}.pdf")
    pdf.output(filename)
    print(f"✅ Invoice generated: {filename}")

    invoice_number += 1

# Update invoice number
with open(invoice_number_file,"w") as f:
    f.write(str(invoice_number))

print("🎉 All advance invoices generated successfully!")
