import io, os, tempfile, math, json
from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename

from pdf2docx import Converter
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib import utils

bp = Blueprint('main', __name__)

ALLOWED_PDF = {'pdf'}
ALLOWED_IMG = {'jpg','jpeg','png','webp','bmp'}

def allowed(filename, exts):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in exts

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/convert/pdf-to-docx', methods=['POST'])
def pdf_to_docx():
    f = request.files.get('pdf_file')
    if not f or not allowed(f.filename, ALLOWED_PDF):
        flash('Please upload a valid PDF file.')
        return redirect(url_for('main.index'))
    filename = secure_filename(f.filename)
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    f.save(tmp_pdf.name)

    out_stream = io.BytesIO()
    tmp_docx_path = tempfile.mktemp(suffix='.docx')
    try:
        cv = Converter(tmp_pdf.name)
        # start=0, end=None ==> all pages
        cv.convert(tmp_docx_path, start=0, end=None)
        cv.close()
        with open(tmp_docx_path, 'rb') as rf:
            out_stream.write(rf.read())
        out_stream.seek(0)
    finally:
        for p in (tmp_pdf.name, tmp_docx_path):
            try: os.unlink(p)
            except Exception: pass

    suggested = (filename.rsplit('.',1)[0] or "converted") + '.docx'
    return send_file(out_stream, as_attachment=True, download_name=suggested,
                     mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@bp.route('/convert/images-to-pdf', methods=['POST'])
def images_to_pdf():
    files = request.files.getlist('image_files')
    if not files:
        flash('Please upload at least one image.')
        return redirect(url_for('main.index'))

    # Filter & normalize
    imgs = []
    for f in files:
        if allowed(f.filename, ALLOWED_IMG):
            imgs.append((secure_filename(f.filename), f))

    if not imgs:
        flash('No valid images selected.')
        return redirect(url_for('main.index'))

    # Ordering from UI (optional)
    order = request.form.get('images_order')
    if order:
        try:
            idxs = [int(i) for i in order.split(',') if i.strip().isdigit()]
            if len(idxs) == len(imgs):
                imgs = [imgs[i] for i in idxs]
        except Exception:
            pass

    # Options
    layout = request.form.get('layout', 'single')  # 'single' or 'grid'
    cols = int(request.form.get('cols', 2) or 2)
    rows = int(request.form.get('rows', 2) or 2)
    orientation = request.form.get('orientation', 'portrait')
    pagesize = request.form.get('pagesize', 'A4')
    margin = float(request.form.get('margin', 24) or 24)
    fit_mode = request.form.get('fit', 'contain')  # contain | cover
    out_name = request.form.get('outname','album.pdf') or 'album.pdf'

    # Choose page size
    if pagesize.upper() == 'LETTER':
        ps = letter
    else:
        ps = A4
    if orientation == 'landscape':
        ps = landscape(ps)
    page_w, page_h = ps
    content_w, content_h = page_w - 2*margin, page_h - 2*margin

    # Build PDF
    pdf_stream = io.BytesIO()
    c = canvas.Canvas(pdf_stream, pagesize=ps)
    c.setAuthor("FlixConvert")
    c.setTitle("Images to PDF")
    c.setCreator("FlixConvert (Python/Flask)")

    def fit_box(iw, ih, bw, bh, mode='contain'):
        ir = iw/ih
        br = bw/bh
        if mode == 'cover':
            if ir < br:
                w = bw
                h = bw/ir
            else:
                h = bh
                w = bh*ir
        else: # contain
            if ir > br:
                w = bw
                h = bw/ir
            else:
                h = bh
                w = bh*ir
        x = (bw - w)/2
        y = (bh - h)/2
        return w, h, x, y

    if layout == 'grid':
        # grid tiling
        cols = max(1, min(8, cols))
        rows = max(1, min(10, rows))
        cell_w = content_w / cols
        cell_h = content_h / rows
        x0, y0 = margin, margin
        i = 0
        for name, storage in imgs:
            storage.stream.seek(0)
            img = Image.open(storage.stream).convert('RGB')
            cw, ch = cell_w, cell_h
            w, h, ox, oy = fit_box(img.width, img.height, cw, ch, fit_mode)
            col = i % cols
            row = (i // cols) % rows
            if i > 0 and col == 0 and row == 0:
                c.showPage()
                c.setAuthor("FlixConvert")
            # compute cell origin from bottom-left
            x = x0 + col * cell_w + ox
            y = y0 + (rows - 1 - row) * cell_h + oy
            c.drawImage(ImageReader(img), x, y, width=w, height=h, preserveAspectRatio=False, mask='auto')
            i += 1
            if (i % (cols*rows)) == 0 and i < len(imgs):
                c.showPage()
                c.setAuthor("FlixConvert")
        if (i % (cols*rows)) != 0:
            pass  # last page already drawn
    else:
        # one image per page
        for name, storage in imgs:
            storage.stream.seek(0)
            img = Image.open(storage.stream).convert('RGB')
            w, h, ox, oy = fit_box(img.width, img.height, content_w, content_h, fit_mode)
            x = margin + ox
            y = margin + oy
            c.drawImage(ImageReader(img), x, y, width=w, height=h, preserveAspectRatio=False, mask='auto')
            c.showPage()

    c.save()
    pdf_stream.seek(0)
    if not out_name.lower().endswith('.pdf'):
        out_name += '.pdf'
    return send_file(pdf_stream, as_attachment=True, download_name=out_name, mimetype='application/pdf')