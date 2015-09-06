from distutils.core import setup
import py2exe

packages= [
    'reportlab',
    'reportlab.lib',
    'reportlab.pdfbase',
    'reportlab.pdfgen',
    'reportlab.platypus',
]

setup(name = 'Gestione Tronchi',
      version = '0.9',
      author = 'Remigio Scolari',
      windows = [
          {
              'script': 'main.py',
              'icon_resources': [(1, 'icon.ico')]
          }
      ],
      options = {'py2exe':{'packages':packages}},
)
