import xml.etree.ElementTree as ET
from Bio import Entrez, Medline

# Set email address (required by NCBI)
Entrez.email = '19pw28@psgtech.ac.in'

# Define the PMID
pmid = '21331621'

# Fetch the record using the efetch utility
handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')

# Parse the XML data using the BioPython ElementT ree module
root = ET.fromstring(handle.read())

# Extract the PMCID from the XML tree
pmcid = root.find(".//PubmedData/ArticleIdList/ArticleId[@IdType='pmc']")
if pmcid is not None:
    pmcid = pmcid.text
else:
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
    record = Medline.read(handle)
    print(record['AID'][0].replace(" [doi]", ""))

print(pmcid)
