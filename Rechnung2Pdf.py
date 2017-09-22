import os, yaml, pprint, datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

output_dir = base_dir + "/Rechnungen/"
template_dir = base_dir + "/template/"
meta_dir = base_dir + "/Meta/"

def RechnungErstellen(meta):
    now = datetime.datetime.now()
    
    with open(meta_dir+"Rechnung.yaml") as f:
        yaml_meta = yaml.load(f)
    
    for row in meta:
        yaml_meta[row] = meta[row]
        
    strtime = now.strftime("%Y-%m-%d")
    i = 1
    while os.path.exists("%s%s-%s.pdf" % (output_dir,strtime,i)):
        i += 1
        
    invoice = "%s-%s" % (strtime,i)
    yaml_meta['invoice-nr'] = invoice
    yaml_dir = output_dir+"Yaml/"+invoice+".yaml"
        
    with open(yaml_dir, "w+") as f:
        yaml.dump(yaml_meta, f, explicit_start=True, explicit_end=True)
        
    os.system("pandoc -o "+output_dir+invoice+".pdf --template="+template_dir+"Rechnung.tex --latex-engine=xelatex "+yaml_dir)

testmeta = {
    'lang': 'english',
    'to': [
        'Merlin Buczek',
        'Grazer Damm 166',
        '12159 Berlin'
    ]
}
RechnungErstellen(testmeta)
