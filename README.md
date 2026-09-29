# Stockroom – warehouse stock manager

Python (FastAPI) backend + cloud database + installable web app that runs on phones, tablets and laptops.
Everyone works on the same live data, so it syncs across devices automatically.

## What you get

| Requirement | How it's covered |
|---|---|
| Admin and user modules | Admin: products, warehouses, users, delete transactions. Data-entry user: inbound/outbound, reports, bulk upload of transactions. A user can be locked to one warehouse. |
| 3,000+ SKUs | Indexed database; 3,200 SKUs import in about half a second. |
| Inbound / outbound forms | SKU#, product name, brand, UOM, barcode, qty, reference, remarks. Typing or scanning a SKU/barcode fills the rest from the product database. Every line can be added or removed. |
| Product database editable | Products page: add, edit, delete (products with history are deactivated, not lost). |
| Bulk upload | Products (admin) and inbound/outbound (all users), Excel or CSV, with downloadable templates and a row-by-row error report. |
| Multi-warehouse | Every transaction belongs to a warehouse; stock, dashboard and reports can be filtered per warehouse. |
| Dashboard | Units on hand, active SKUs, today/month in and out, low-stock count, 14-day chart, stock by warehouse, top outbound, recent transactions. Refreshes every 30 s. |
| Reports + filters + export | On-hand, inbound/outbound lines, in-vs-out by SKU, low stock. Filter by warehouse, brand, search, dates, type, reference. Export to Excel or CSV. |
| Real-time barcode scanning | Phone camera (continuous scanning with beep) and USB/Bluetooth scanners (they type into the scan box and press Enter). |
| Cloud sync | One server + PostgreSQL. Open the same URL on any device. |

Stock-out is blocked when it would take the balance below zero (set `ALLOW_NEGATIVE_STOCK=1` to allow).

## Run on your computer (2 minutes)

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
Open http://localhost:8000 and sign in with `admin` / `admin123` (change it under "Change password").
Without `DATABASE_URL` it uses a local SQLite file, which is for testing only.

Create test files with `python make_sample_files.py`, then use **Bulk upload**: products first, transactions second.

## Put it online (so phones and laptops share data)

**Option A – free, no programming (recommended):** GitHub (stores the code) + Neon (free permanent database) + Render (free web hosting). Step-by-step guide was given in the chat. Do NOT use Render's own free database: it is deleted after 30 days.

**Option B – any host with Docker** (Railway, Fly.io, a VPS): build the `Dockerfile` and set these environment variables:

| Variable | Value |
|---|---|
| `DATABASE_URL` | PostgreSQL URL, e.g. from Neon, Supabase or Render |
| `SECRET_KEY` | long random string (`python -c "import secrets;print(secrets.token_hex(32))"`) |
| `ADMIN_PASSWORD` | password for the first admin account |

The host must serve **https**. Phone cameras only work on https pages.

## Use it as a phone app
Open the URL in Chrome (Android) or Safari (iPhone) > menu > **Add to Home Screen**. It opens full-screen like an app.
To publish in the Play Store later, wrap the URL with Bubblewrap (TWA) or Capacitor. No code changes needed.

## Bulk file formats
**Products:** `SKU#, Product Name, Brand, UOM, Barcode, Min Stock`. New SKUs are added, existing ones updated; blank cells keep current values.
**Transactions:** `Type (IN/OUT), Warehouse (code), Date, Reference, SKU# (or barcode), Qty, Remarks`. Rows sharing type + warehouse + date + reference become one document. If any row is invalid, nothing is saved and you get a list of the problem rows.

## Project layout
```
app/main.py            app start, creates first admin + MAIN warehouse
app/models.py          tables (users, warehouses, products, stock_docs, stock_lines)
app/routers/           accounts (login/users/warehouses), products, stock (in/out + bulk), reports (+dashboard)
app/services.py        stock balance logic, Excel/CSV import and export
app/static/            the web app (core.js, pages1.js, pages2.js, style.css, PWA files)
```
Interactive API docs: `/docs`.

## Good next steps
- Warehouse-to-warehouse transfers (currently: out of one, in to the other)
- Offline queue for weak Wi-Fi zones (the app shell is cached, entries need a connection)
- Batch/expiry, bin locations, purchase-order and delivery-order printing
- Database backups: enable automatic backups on your PostgreSQL host
