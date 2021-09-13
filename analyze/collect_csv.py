#!/usr/bin/env python3

import os
import io
import re
import json

sample_names = [
    'SRR6750041',
    'SRR6750042',
    'SRR6750043',
    'SRR6750044',
    'SRR6750045',
    'SRR6750046',
    'SRR6750047',
    'SRR6750048',
    'SRR6750049',
    'SRR6750050',
    'SRR6750051',
    'SRR6750052',
    'SRR6750053',
    'SRR6750054',
    'SRR6750055',
    'SRR6750056',
    'SRR6750057',
    'SRR6750058',
    'SRR6750059'
]

# sample_category = [
#     '100 cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '150K cns mm',
#     '3k nuc hs mm',
#     '300 nuc hs mm',
#     '1k frozen nuc hs mm',
#     '200 frozen nuc hs mm'
# ]

sample_category = [
    'small',
    'main',
    'main',
    'main',
    'main',
    'main',
    'main',
    'main',
    'main',
    'main',
    'main',
    'main',
    'main',
    'main',
    'main',
    'fresh',
    'fresh',
    'frozen',
    'frozen',
]
barcode_id_ex = re.compile('(?P<row>[A-H])(?P<column>[1-9](?:[0-9])?)')

def to_json(ontology):
    return json.dumps(ontology, sort_keys=True, ensure_ascii=False, indent=4)

def get_barcode_sequence(barcode):
    return ''.join(barcode['barcode'])

def get_barcode_id(barcode_id):
    m = barcode_id_ex.match(barcode_id)
    return '{row}{column:0>2}'.format(**(m.groupdict()))

def write_to_tsv(path, table):
    with io.open(path, 'wb') as file:
        for row in table:
            file.write('\t'.join([str(i) for i in row]).encode('utf8'))
            file.write('\n'.encode('utf8'))

def overall():
    def collect_batch(confidence, iteration):
        path = '../full_run_{}/{}_{}_report.json'.format(confidence, sample, iteration)
        if os.path.exists(path):
            with io.open(path, 'rb') as file:
                content = json.loads(file.read().decode('utf8'))
                row = [
                    confidence,
                    sample,
                    category,
                    iteration,
                    content['outgoing']['count'],
                    content['outgoing']['pf count'],
                    content['outgoing']['pf count'] / content['outgoing']['count']
                ]
                table.append(row)

    header = [
        'confidence',
        'sample',
        'category',
        'iteration',
        'count',
        'pf_count',
        'ratio'
    ]
    table = []
    for category, sample in zip(sample_category, sample_names):
        collect_batch(95, 'first')
        collect_batch(95, 'second')
        collect_batch(99, 'first')
        collect_batch(99, 'second')
        collect_batch(999, 'first')
        collect_batch(999, 'second')

    return [ header ] + table

def noise_and_confidence():
    def collect_batch(confidence, iteration):
        path = '../full_run_{}/{}_{}_report.json'.format(confidence, sample, iteration)
        if os.path.exists(path):
            with io.open(path, 'rb') as file:
                content = json.loads(file.read().decode('utf8'))
                for index, decoder in enumerate(content['cellular']):
                    row = [
                        confidence,
                        sample,
                        category,
                        iteration,
                        index + 1,
                        decoder['average classified confidence'],
                        decoder['average pf classified confidence'],
                        decoder['low conditional confidence count'], # noise
                        decoder['low confidence count'], # low confidence
                    ]
                    table.append(row)

    header = [
        'confidence',
        'sample',
        'category',
        'iteration',
        'decoder',
        'mean_confidence',
        'mean_pf_confidence',
        'noise',
        'low_confidence',
    ]
    table = []

    for category, sample in zip(sample_category, sample_names):
        collect_batch(95, 'first')
        collect_batch(95, 'second')
        collect_batch(99, 'first')
        collect_batch(99, 'second')
        collect_batch(999, 'first')
        collect_batch(999, 'second')

    # table.sort(key=lambda i: i[2])
    # table.sort(key=lambda i: i[3])
    # table.sort(key=lambda i: i[1])
    # table.sort(key=lambda i: i[0])

    return [ header ] + table

def barcode_noise_and_confidence():
    def collect_batch(confidence, iteration):
        path = '../full_run_{}/{}_{}_report.json'.format(confidence, sample, iteration)
        if os.path.exists(path):
            with io.open(path, 'rb') as file:
                content = json.loads(file.read().decode('utf8'))
                for index, decoder in enumerate(content['cellular']):
                    for barcode in decoder['classified']:
                        row = [
                            confidence,
                            sample,
                            category,
                            iteration,
                            index + 1,
                            get_barcode_sequence(barcode),
                            decoder['average classified confidence'],
                            decoder['average pf classified confidence'],
                            barcode['low conditional confidence count'], # noise
                            barcode['low confidence count'], # low confidence
                        ]
                        table.append(row)

    header = [
        'confidence',
        'sample',
        'category',
        'iteration',
        'decoder',
        'barcode',
        'mean_confidence',
        'mean_pf_confidence',
        'noise',
        'low_confidence',
    ]
    table = []

    for category, sample in zip(sample_category, sample_names):
        collect_batch(95, 'first')
        collect_batch(95, 'second')
        collect_batch(99, 'first')
        collect_batch(99, 'second')
        collect_batch(999, 'first')
        collect_batch(999, 'second')

    # table.sort(key=lambda i: i[4])
    # table.sort(key=lambda i: i[3])
    # table.sort(key=lambda i: i[2])
    # table.sort(key=lambda i: i[1])
    # table.sort(key=lambda i: i[0])

    return [ header ] + table

def priors():
    def collect_batch(confidence, iteration):
        path = '../full_run_{}/{}_{}_adjusted.json'.format(confidence, sample, iteration)
        if os.path.exists(path):
            with io.open(path, 'rb') as file:
                content = json.loads(file.read().decode('utf8'))
                for index, decoder in enumerate(content['cellular']):
                    for barcode_id, barcode in decoder['codec'].items():
                        row = [
                            confidence,
                            sample,
                            category,
                            iteration,
                            index + 1,
                            get_barcode_id(barcode_id),
                            get_barcode_sequence(barcode),
                            barcode['concentration']
                        ]
                        table.append(row)
    header = [
        'confidence',
        'sample',
        'category',
        'iteration',
        'decoder',
        'well',
        'barcode',
        'prior'
    ]
    table = []

    for category, sample in zip(sample_category, sample_names):
        collect_batch(95, 'first')
        collect_batch(95, 'second')
        collect_batch(99, 'first')
        collect_batch(99, 'second')
        collect_batch(999, 'first')
        collect_batch(999, 'second')

    # table.sort(key=lambda i: i[4])
    # table.sort(key=lambda i: i[3])
    # table.sort(key=lambda i: i[2])
    # table.sort(key=lambda i: i[1])
    # table.sort(key=lambda i: i[0])

    return [ header ] + table

write_to_tsv('overall.tsv', overall())
write_to_tsv('priors.tsv', priors())
write_to_tsv('noise_and_confidence.tsv', noise_and_confidence())
write_to_tsv('barcode_noise_and_confidence.tsv', barcode_noise_and_confidence())

# overall()
# priors()
# noise_and_confidence()
