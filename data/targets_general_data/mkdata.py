from ensembler.initproject import GatherTargetsFromUniProt
from ensembler.uniprot import get_uniprot_xml
import pandas as pd

# ============
# Get data
# ============

targetids = open('../TKs.txt').read().splitlines()

gtfup = GatherTargetsFromUniProt(
    'family:"tyr protein kinase family" AND taxonomy:9606 AND reviewed:yes',
    uniprot_domain_regex='^Protein kinase(?!; truncated)(?!; inactive)',
    run_main=False,
)

gtfup._gather_targets(write_output_files=False)

# ============
# Process data
# ============

targetids = [t.id for t in gtfup.targets]
seqs = [t.seq for t in gtfup.targets]

entry_names = [t[0:t.index('_D')] for t in targetids]

residue_spans_text = ['{0}-{1}'.format(rspan[0]+1, rspan[1]+1) for rspan in gtfup.residue_spans]

hgnc_symbols = []
uniprot_recommended_names = []
# domain_descriptions = []

for t, targetid in enumerate(targetids):
    name = entry_names[t]
    domain_idx = int(targetid[-1])

    entry = gtfup.uniprotxml.xpath('entry[name/text()="{0}"]'.format(name))[0]
    hgnc_symbol = entry.find('dbReference[@type="HGNC"]/property').get('value')
    uniprot_recommended_name = entry.find('protein/recommendedName/fullName').text
    # domain_description = entry.findall('feature[@type="domain"]')[domain_idx].get('description')

    hgnc_symbols.append(hgnc_symbol)
    uniprot_recommended_names.append(uniprot_recommended_name)

# TODO domain descriptions

# ============
# pandas
# ============

df = pd.DataFrame()

df['Ensembler target id'] = targetids
df['Target sequence'] = seqs
df['UniProt entry name'] = entry_names
df['Residue span (UniProt coords; 1-based)'] = residue_spans_text
df['HGNC HUGO symbol'] = hgnc_symbols
df['UniProt recommended name'] = uniprot_recommended_names
df['UniProt domain description'] = gtfup.domain_descriptions
df['Organism'] = ['human'] * len(df)

df.sort(columns=['Ensembler target id'], inplace=True)

df.to_csv('targets-data.csv')

table_cols = ['Ensembler target id', 'UniProt entry name', 'Residue span (UniProt coords; 1-based)', 'HGNC HUGO symbol', 'UniProt recommended name', 'UniProt domain description', 'Organism']
with open('targets-data.txt', 'w') as tablefile:
    tablefile.write(df.to_string(columns=table_cols))
