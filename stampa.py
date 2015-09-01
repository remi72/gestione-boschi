__author__ = 'remigioscolari'

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def pagina(c, tronchi, numero_pagina, totale_pagine):
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(297, 800, 'MOUNTAIN WORKS di Carrara Roberto')
    c.setFont("Helvetica", 11)
    c.drawCentredString(297, 785, 'cell. 333 4441935 - mountainworks@hotmail.it')
    c.setFont("Helvetica", 9)
    c.drawCentredString(297, 770, 'Via Roma, 171 - 24013 Oltre il Colle (BG)'
                                  ' - C.F. e R.I. BG: CRR RRT 90H21 A794T - P.IVA: 03750440160')
    c.setFont("Helvetica", 10)
    c.drawCentredString(297, 40, 'Pagina {} di {}'.format(numero_pagina, totale_pagine))

    def colonna1(tronchi):
        c.rect(65, 732, 225, 18)
        c.line(130, 732, 130, 750)
        c.line(175, 732, 175, 750)
        c.line(235, 732, 235, 750)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(97, 737, 'N. TRONCO')
        c.drawCentredString(152, 737, 'LUNG.')
        c.drawCentredString(205, 737, 'DIAMETRO')
        c.drawCentredString(262, 737, 'MC')
        c.setFont("Helvetica", 10)

        for i, tronco in enumerate(tronchi):
            c.rect(65, 716-16*i, 225, 16)
            c.line(130, 716-16*i, 130, 716-16*i+16)
            c.line(175, 716-16*i, 175, 716-16*i+16)
            c.line(235, 716-16*i, 235, 716-16*i+16)
            c.drawCentredString(97, 720-16*i, '{}'.format(str(tronco.placchetta).zfill(5)))
            c.drawCentredString(152, 720-16*i, '{}'.format(tronco.lunghezza))
            c.drawCentredString(205, 720-16*i, '{}'.format(tronco.diametro))
            c.drawCentredString(262, 720-16*i, '{:.3f}'.format(tronco.mc))

    def colonna2(tronchi):
        c.rect(305, 732, 225, 18)
        c.line(370, 732, 370, 750)
        c.line(415, 732, 415, 750)
        c.line(475, 732, 475, 750)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(337, 737, 'N. TRONCO')
        c.drawCentredString(392, 737, 'LUNG.')
        c.drawCentredString(445, 737, 'DIAMETRO')
        c.drawCentredString(502, 737, 'MC')
        c.setFont("Helvetica", 10)

        for i, tronco in enumerate(tronchi):
            c.rect(305, 716-16*i, 225, 16)
            c.line(370, 716-16*i, 370, 716-16*i+16)
            c.line(415, 716-16*i, 415, 716-16*i+16)
            c.line(475, 716-16*i, 475, 716-16*i+16)
            c.drawCentredString(337, 720-16*i, '{}'.format(str(tronco.placchetta).zfill(5)))
            c.drawCentredString(392, 720-16*i, '{}'.format(tronco.lunghezza))
            c.drawCentredString(445, 720-16*i, '{}'.format(tronco.diametro))
            c.drawCentredString(502, 720-16*i, '{:.3f}'.format(tronco.mc))

    if len(tronchi) > 40:
        tronchi40 = tronchi[:40]
        tronchi80 = tronchi[40:]
        colonna1(tronchi40)
        colonna2(tronchi80)
    else:
        colonna1(tronchi)


def totali(c, totalemc, corteccia, totalenettomc):
        c.rect(100, 60, 400, 16)
        c.line(230, 60, 230, 76)
        c.line(360, 60, 360, 76)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(105, 65, 'TOTALE mc:')
        c.drawString(170, 65, '{}'.format(totalemc))
        c.drawCentredString(294, 65, 'CORTECCIA:  {}'.format('SI' if corteccia else 'NO'))
        c.drawString(365, 65, 'TOTALE mc -10%:')
        c.drawCentredString(473, 65, '{}'.format(totalenettomc))


def stampa(file, tronchi, totalemc, corteccia, totalenettomc):
    c = canvas.Canvas(file, pagesize=A4)
    a=float(len(tronchi))/80
    if a%1: a += 1
    totale_pagine = int(a)
    numero_pagina = 0
    tronchi80 = []
    for i, tronco in enumerate(tronchi):
        if i%80 == 0 and tronchi80:
            numero_pagina += 1
            pagina(c, tronchi80, numero_pagina, totale_pagine)
            tronchi80 = []
            c.showPage()
        tronchi80.append(tronco)
    numero_pagina += 1
    pagina(c, tronchi80, numero_pagina, totale_pagine)
    totali(c, totalemc, corteccia, totalenettomc)
    c.save()
    return True
