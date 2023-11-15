import xml.etree.ElementTree as ET
import sys
import re

tree = ET.parse(sys.argv[1])
# with open(sys.argv[1]) as f:
#     xml = f.read()
# tree = ET.fromstring(re.sub(r"(<\![^>]+>)", r"\0\n<root>\n", xml) + "</root>")
root = tree.getroot()

with open(sys.argv[2], 'w') as writer:
    writer.write(f"Species Name\tTaxid\tAssembly Accession\tExisting Annotation\tExisting Protein Sequence\tURL\n")
    # for docset in root.findall('.//DocumentSummarySet'):
    for document_summary in root.findall('.//DocumentSummary'):
        protein = False
        annotation = False
        source = 'GenBank'
        taxid = document_summary.find('Taxid').text
        accession = document_summary.find('AssemblyAccession').text
        if 'GCF' in accession:
            source = 'RefSeq'
        species_name = document_summary.find('SpeciesName').text

        properties = [elt.text for elt in document_summary.findall('PropertyList/string')]
        if any(prop in ['has_annotation', 'has_egap_annotation'] for prop in properties):
            protein = True
            annotation = True
        if document_summary.find(f"FtpPath_{source}") == None: # Pas de ftp pour les assemblages trop vieux ?
            url = None
        else:
            ftp = document_summary.find(f"FtpPath_{source}").text
            url = "https:" + ftp.strip().split(":")[1] + "/" + ftp.strip().split("/")[-1]
        status = document_summary.find('RefSeq_category').text
        if status == 'representative genome':
            line = f"{species_name}\t{taxid}\t{accession}\t{annotation}\t{protein}\t{url}\n"
            writer.write(line)
