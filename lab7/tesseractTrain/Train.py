import os
import subprocess
os.chdir('../')
srcdir = 'tesseractTrain/data'
destdir = 'tesseractTrain/trainfiles'

# Generating the tuples of filenames
files = os.listdir(srcdir)
jpgs = [x for x in files if x.endswith('.jpg')]
boxes = [x for x in files if x.endswith('.box')]
trainfiles = list(zip(jpgs, boxes))

# generating TR files and unicode charecter extraction
unicharset = f"unicharset_extractor --output_unicharset {destdir}/unicharset "

errorfiles = []


for image, box in trainfiles:
    if os.path.isfile(f"{destdir}/{image[:-4]}.tr"):
        continue
    try:
        print(image)
        os.system(f"tesseract {srcdir}/{image} {destdir}/{image[:-4]} nobatch box.train")
    except:
        errorfiles.append((image, box))
arg =" ".join([f"tesseractTrain/data/{f}" for f in os.listdir('tesseractTrain/data') if f.endswith(('box'))])
subprocess.run(unicharset + arg)




# Creating font properties file
with open(f"{destdir}/font_properties", 'w') as f:
    f.write("ocrb 0 0 0 1 0")

# # Getting all .tr files and training
output = 'tesseractTrain/trainoutput'
trfiles = [f for f in os.listdir(destdir) if f.endswith('.tr')]

mftraining = f"mftraining -F tesseractTrain/trainfiles/font_properties -U tesseractTrain/trainfiles/unicharset -O {output}/eng.rus.unicharset -D {output}"
cntraining = f"cntraining -D {output}"
for file in trfiles:
    mftraining += f" tesseractTrain/trainfiles/{file}"
    cntraining += f" tesseractTrain/trainfiles/{file}"
subprocess.run(mftraining)
subprocess.run(cntraining)

# # Renaming training files and merging them
os.chdir('tesseractTrain/trainoutput')
os.rename('inttemp', 'eng.rus.inttemp')
os.rename('normproto', 'eng.rus.normproto')
os.rename('pffmtable', 'eng.rus.pffmtable')
os.rename('shapetable', 'eng.rus.shapetable')
os.chdir('../..')
os.system(f"combine_tessdata -o "+
          f"tesseractTrain/trainoutput/eng.rus.unicharset tesseractTrain/trainoutput/eng.rus.inttemp tesseractTrain/trainoutput/eng.rus.normproto "+
          f"tesseractTrain/trainoutput/eng.rus.pffmtable tesseractTrain/trainoutput/eng.rus.shapetable")

# Writing log file
if len(errorfiles) == 0:
    errorfiles.append(('no', 'Error'))
with open('logs.txt', 'w') as f:
    f.write('\n'.join('%s %s' % x for x in errorfiles))