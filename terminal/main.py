from PIL import Image, ImageFont, ImageDraw
import xml.etree.ElementTree as ET
import pandas as pd
import sys, os, textwrap

if __name__ == "__main__":
    PROJECTS = 'Projects'
    projectName = sys.argv[1]
    config = ET.parse(
        os.path.abspath(
            os.path.join(
                PROJECTS,
                projectName,
                'config.xml'))).getroot()
    instances = config.findall('instance')
    for indInst in range(len(instances)):
        tableXML = instances[indInst].find('table')
        imgXML = instances[indInst].find('image')
        centerW = int(imgXML.attrib['centerW'])
        table = pd.read_csv(
            os.path.abspath(
                os.path.join(
                    PROJECTS,
                    projectName, 
                    tableXML.attrib['name']))).fillna('')
        for indRow, row in table.iterrows():
            img = Image.open(
                os.path.abspath(
                    os.path.join(
                        PROJECTS,projectName, 
                        imgXML.attrib['name'])))
            draw = ImageDraw.Draw(img)
            textesXML = tableXML.findall('text')
            for textXML in textesXML:
                text = row[textXML.attrib['column']]
                if text != "":
                    lines = textwrap.wrap(
                        text, 
                        int(textXML.attrib.get('width', 45))
                    )
                    spacing = int(textXML.attrib.get('spacing',50))
                    for indLine in range(len(lines)):
                        textSize = int(tableXML.attrib.get('textSize',50))
                        textSize = int(textXML.attrib.get('size', textSize))
                        font = ImageFont.truetype(
                            font="arial.ttf", 
                            size=textSize, 
                            encoding='UTF-8')
                        textW, textH = draw.textsize(lines[indLine], font)
                        x = int(textXML.attrib.get('x', centerW - textW / 2))
                        y = int(textXML.attrib['y']) + indLine * spacing
                        color = textXML.attrib.get('color','black')
                        draw.text(
                            (x,y), 
                            lines[indLine], 
                            fill=color, 
                            font=font)
            folder = row[imgXML.attrib['folder']].replace('""','"').replace(' "'," «").replace('" ',"» ").replace('"',"»")
            path = os.path.abspath(
                os.path.join(
                    PROJECTS,
                    projectName, 
                    'result', 
                    folder
                )
            )
            if not os.path.exists(path): 
                os.makedirs(path)
            name = os.path.join(path , row[imgXML.attrib['file']] + '.jpg')
            print(name)
            img.save(name)
