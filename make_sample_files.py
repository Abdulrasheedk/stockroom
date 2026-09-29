"""Creates sample upload files for testing:  python make_sample_files.py
   sample_products.xlsx (3,000 SKUs) and sample_transactions.xlsx (inbound + outbound)."""
import random
from openpyxl import Workbook

random.seed(1)
brands = ["Almarai", "Nadec", "Savola", "Nestle", "Unilever", "P&G", "Danone", "Lipton", "Pepsi", "Coca-Cola"]
uoms = ["PCS", "BOX", "KG", "CTN"]
wb = Workbook(); ws = wb.active
ws.append(["SKU#", "Product Name", "Brand", "UOM", "Barcode", "Min Stock"])
for i in range(1, 3001):
    ws.append([f"SKU-{i:05d}", f"Sample product {i}", random.choice(brands), random.choice(uoms), 6290000000000 + i, random.choice([0, 5, 10, 20])])
wb.save("sample_products.xlsx")

wb = Workbook(); ws = wb.active
ws.append(["Type", "Warehouse", "Date", "Reference", "SKU#", "Qty", "Remarks"])
for i in range(1, 501):
    ws.append(["IN", "MAIN", "2026-09-01", "PO-1001", f"SKU-{i:05d}", random.randint(50, 200), "Opening delivery"])
for i in range(1, 101):
    ws.append(["OUT", "MAIN", "2026-09-10", "DO-2001", f"SKU-{i:05d}", random.randint(1, 30), "Customer order"])
wb.save("sample_transactions.xlsx")
print("Created sample_products.xlsx and sample_transactions.xlsx")
