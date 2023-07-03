import os

CAR_YEARS_CHOICES = [
    '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
    '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
    '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029',
    ]

USER_ROL = {
    'AD':'Admin', 
    'DR':'Drive',
    'CL':'Client', 
    'NN':'None', 
}


ORDER_STATUS = {
    'PD': 'Pendiente',
    'EP': 'En Proceso',
    'FN': 'Finalizado',
    'CN': 'Cancelado',
}


MAP_KEY = os.environ.get('MAP_KEY')
USER_MAIL = os.environ.get('USER_MAIL')
USER_MAIL_PASSWORD = os.environ.get('USER_MAIL_PASSWORD')
SITE_URL = os.environ.get('SITE_URL')
TRANSPORTES_FLOR = (-2.1852634,-79.8914505)