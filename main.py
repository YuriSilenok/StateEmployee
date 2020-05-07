from PIL import Image, ImageFont, ImageDraw
import xml.etree.ElementTree as ET
import pandas as pd
import sys, os, textwrap

if __name__ == "__main__":
    PROJECTS = 'Projects'
    projectName = sys.argv[1]
    config = ET.parse( os.path.abspath(os.path.join(PROJECTS,projectName, 'config.xml'))).getroot()
    instances = config.findall('instance')
    for indInst in range(len(instances)):
        tableXML = instances[indInst].find('table')
        imgXML = instances[indInst].find('image')
        centerW = int(imgXML.attrib['centerW'])
        table = pd.read_csv(os.path.abspath(os.path.join(PROJECTS,projectName, tableXML.attrib['name'])))
        for indRow, row in table.iterrows():
            img = Image.open(os.path.abspath(os.path.join(PROJECTS,projectName, imgXML.attrib['name'])))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", 50, encoding='UTF-8')
            textesXML = tableXML.findall('text')
            for textXML in textesXML:
                text = row[textXML.attrib['column']]
                lines = textwrap.wrap(text, width=45)
                h = 50
                for indLine in range(len(lines)):
                    textW, textH = draw.textsize(lines[indLine], font)
                    x = centerW - textW / 2
                    y = int(textXML.attrib['y']) + indLine * h
                    draw.text((x, y), lines[indLine], fill='black', font=font)
            path = os.path.abspath(
                os.path.join(
                    PROJECTS,projectName, 
                    'result', 
                    row[imgXML.attrib['folder']]
                )
            )
            if not os.path.exists(path): 
                os.makedirs(path)
            img.save(os.path.join(path , row[imgXML.attrib['file']] + '.jpg'))
