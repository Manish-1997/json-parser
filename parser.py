import json
import csv

# Add the attributes and its count to dict
def add_attributeDict(label,attribute,value,attributeDict):
    if (label,attribute,value) in attributeDict:
        attributeDict[(label,attribute,value)] += 1
    else:
        attributeDict[(label,attribute,value)] = 1

# Extract required data from json and returns dict of its count  
def extract():
    try:
        with open('builds.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: JSON file not found")
        return ({},{})

    annotations = data['maker_response']['sensor_fusion_v2']['data']['annotations']

    labelDict = {}
    attributeDict = {}

    for item in annotations:
        if item['label'] in labelDict:
            labelDict[item['label']] += 1
        else:
            labelDict[item['label']] = 1

    for item in annotations:
        for attribute,value in item['attributes'].items():
            if type(value['value']) is list:
                for each_value in value['value']:
                    add_attributeDict(item['label'],attribute,each_value,attributeDict)
            else:
                add_attributeDict(item['label'],attribute,value['value'],attributeDict)

    return (labelDict,attributeDict)

# Builds both the csv file with attributes and its count
def build_csv(labelDict,attributeDict):
    with open('label.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['LABEL', 'COUNT'])
        for label, count in labelDict.items():
            writer.writerow([label, count])

    with open('attribute.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['LABEL', 'ATTRIBUTE_NAME', 'ATTRIBUTE_VALUE', 'ATTRIBUTE_COUNT'])
        for attribute, count in attributeDict.items():
            writer.writerow([attribute[0], attribute[1], attribute[2], count])

def main():
    labelDict,attributeDict = extract()
    build_csv(labelDict,attributeDict)
    print("CSV files have been created successfully")

if __name__ == "__main__":
    main()


