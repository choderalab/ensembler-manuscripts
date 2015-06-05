import os
import Bio.SeqIO
import Bio.SubsMat.MatrixInfo
import Bio.pairwise2
import pandas as pd
import re
from ensembler.core import sequnwrap, xpath_match_regex_case_sensitive
from ensembler.uniprot import get_uniprot_xml
from ensembler.initproject import extract_template_pdbchains_from_uniprot_xml

templates_full_seq_fasta_filepath = 'templates_general_data/templates-full-seq.fa'
templates_full_seq = list(Bio.SeqIO.parse(templates_full_seq_fasta_filepath, 'fasta'))

templateids = []
seqs = []
uniprot_mnemonics = []
domain_ids = []
pdbids = []
chainids = []

for template in templates_full_seq:
    templateid = template.id
    seq = template.seq

    match = re.match('(.*_.*)_D([0-9]+)_(....)_(.)', templateid)
    uniprot_mnemonic, domain_id, pdbid, chainid = match.groups()
    domain_id = int(domain_id)

    templateids.append(templateid)
    seqs.append(str(seq))
    uniprot_mnemonics.append(uniprot_mnemonic)
    domain_ids.append(domain_id)
    pdbids.append(pdbid)
    chainids.append(chainid)

df = pd.DataFrame({
    'Ensembler template id': templateids,
    'Template sequence': seqs,
    'UniProt entry name': uniprot_mnemonics,
    'domain id': domain_ids,
    'PDB ID': pdbids,
    'PDB chain ID': chainids,
})

unique_uniprot_mnemonics = list(set(uniprot_mnemonics))
uniprot_seqs = {}
hgnc_symbols = {}
uniprot_recommended_names = {}
gene_names = {}
organisms = {}
domain_descriptions_by_uniprot_entry = {}
resi_spans_by_pdbchain = {}

for uniprot_mnemonic in unique_uniprot_mnemonics:
    uniprot_search = 'mnemonic:{0}'.format(uniprot_mnemonic)
    uniprot_xml = get_uniprot_xml(uniprot_search)

    entry = uniprot_xml.find('entry')
    uniprot_seqs[uniprot_mnemonic] = sequnwrap(entry.find('sequence').text).replace('X', '')

    organism_id = int(entry.find('organism/dbReference[@type="NCBI Taxonomy"]').get('id'))
    organism_common = entry.find('organism/name[@type="common"]')
    if organism_common is not None:
        organism = organism_common.text
    else:
        organism = entry.find('organism/name[@type="scientific"]').text
    organisms[uniprot_mnemonic] = organism

    gene_name_node = entry.find('gene/name[@type="primary"]')
    gene_name = gene_name_node.text if gene_name_node is not None else ''
    gene_names[uniprot_mnemonic] = gene_name

    if organism_id == 9606:
        hgnc_symbol = entry.find('dbReference[@type="HGNC"]/property').get('value')
        hgnc_symbols[uniprot_mnemonic] = hgnc_symbol
    else:
        hgnc_symbols[uniprot_mnemonic] = ''

    recommended_name = entry.find('protein/recommendedName/fullName').text
    uniprot_recommended_names[uniprot_mnemonic] = recommended_name

    uniprot_domain_regex = '^Protein kinase(?!; truncated)(?!; inactive)'
    selected_domains = entry.xpath(
        'feature[@type="domain"][match_regex(@description, "%s")]' % uniprot_domain_regex,
        extensions={(None, 'match_regex'): xpath_match_regex_case_sensitive}
    )
    domain_descriptions_by_uniprot_entry[uniprot_mnemonic] = [domain.get('description') for domain in selected_domains]

    df_rows_for_this_uniprot_entry = df[df['UniProt entry name'] == uniprot_mnemonic]
    pdbids_for_this_uniprot_entry = list(set(df_rows_for_this_uniprot_entry['PDB ID']))
    chainids_for_this_uniprot_entry = {pdbid: list(df_rows_for_this_uniprot_entry[df_rows_for_this_uniprot_entry['PDB ID'] == pdbid]['PDB chain ID']) for pdbid in pdbids_for_this_uniprot_entry}
    selected_pdbchains = extract_template_pdbchains_from_uniprot_xml(uniprot_xml, uniprot_domain_regex=uniprot_domain_regex, specified_pdbids=pdbids_for_this_uniprot_entry, specified_chainids=chainids_for_this_uniprot_entry)
    for pdbchain in selected_pdbchains:
        key = (uniprot_mnemonic, pdbchain['pdbid'], pdbchain['chainid'])
        value = '{0}-{1}'.format(pdbchain['residue_span'][0], pdbchain['residue_span'][1])
        resi_spans_by_pdbchain[key] = value

# XXX adding these manually because the PDB structures have been superseded
resi_spans_by_pdbchain['BUB1_HUMAN', '3E7E', 'A'] = '787-1085'
resi_spans_by_pdbchain['MK13_HUMAN', '4EXU', 'A'] = '25-308'
resi_spans_by_pdbchain['PAN3_YEAST', '4Q8J', 'C'] = '299-549'
resi_spans_by_pdbchain['PAN3_YEAST', '4Q8J', 'E'] = '299-549'
resi_spans_by_pdbchain['PAN3_YEAST', '4Q8J', 'F'] = '299-549'
resi_spans_by_pdbchain['PAN3_YEAST', '4Q8J', 'H'] = '299-549'
resi_spans_by_pdbchain['PAN3_YEAST', '4Q8J', 'I'] = '299-549'
resi_spans_by_pdbchain['PAN3_YEAST', '4Q8J', 'K'] = '299-549'
resi_spans_by_pdbchain['PAN3_YEAST', '4Q8J', 'L'] = '299-549'

df['Organism'] = [organisms[mnem] for mnem in uniprot_mnemonics]
df['HGNC HUGO symbol'] = [hgnc_symbols.get(mnem) for mnem in uniprot_mnemonics]
df['UniProt recommended name'] = [uniprot_recommended_names[mnem] for mnem in uniprot_mnemonics]
df['UniProt recommended gene name'] = [gene_names[mnem] for mnem in uniprot_mnemonics]
df['Template residue span (UniProt coords; 1-based)'] = [resi_spans_by_pdbchain[key] for key in zip(uniprot_mnemonics, pdbids, chainids)]

domain_descriptions = []
for mnem, domain_id in zip(uniprot_mnemonics, domain_ids):
    domain_descriptions.append(
        domain_descriptions_by_uniprot_entry[mnem][domain_id]
    )
df['UniProt domain description'] = domain_descriptions

df.sort(columns=['Ensembler template id'], inplace=True)

df.to_csv(
    path='templates_general_data/templates-data.csv',
)

with open('templates_general_data/templates-data.txt', 'w') as templates_txt_file:
    df.to_string(
        buf=templates_txt_file,
        columns=[
            'Ensembler template id',
            'UniProt entry name',
            'PDB ID',
            'PDB chain ID',
            'Template residue span (UniProt coords; 1-based)',
            'UniProt recommended name',
            'UniProt recommended gene name',
            'HGNC HUGO symbol',
            'Organism',
            'UniProt domain description',
        ]
    )
