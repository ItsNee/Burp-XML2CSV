import xml.etree.ElementTree as ET
import base64
import csv

# Function to safely decode base64 content
def safe_base64_decode(data, encoding='utf-8'):
    try:
        decoded_data = base64.b64decode(data)
        return decoded_data.decode(encoding)
    except UnicodeDecodeError:
        # If decoding fails, return the binary representation
        return decoded_data

# Parse the XML file
tree = ET.parse('burpexport.xml')
root = tree.getroot()

# Open a CSV file to write
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write the header
    csvwriter.writerow([
        'time', 'url', 'host', 'ip', 'port', 'protocol', 'method', 'path', 
        'extension', 'request', 'status', 'responselength', 'mimetype', 
        'response', 'comment'
    ])
    
    # Iterate through each item in the XML
    for item in root.findall('item'):
        time = item.find('time').text
        url = item.find('url').text
        host = item.find('host').text
        ip = item.find('host').attrib.get('ip', '')
        port = item.find('port').text
        protocol = item.find('protocol').text
        method = item.find('method').text
        path = item.find('path').text
        extension = item.find('extension').text
        request = item.find('request').text
        request_base64 = item.find('request').attrib.get('base64', 'false')
        status = item.find('status').text
        responselength = item.find('responselength').text
        mimetype = item.find('mimetype').text
        response = item.find('response').text
        response_base64 = item.find('response').attrib.get('base64', 'false')
        comment = item.find('comment').text if item.find('comment') is not None else ''

        # Decode base64 if necessary
        if request_base64 == 'true':
            request = safe_base64_decode(request)
        if response_base64 == 'true':
            response = safe_base64_decode(response)
        
        # Write the row to CSV
        csvwriter.writerow([
            time, url, host, ip, port, protocol, method, path, extension, 
            request, status, responselength, mimetype, response, comment
        ])

print('CSV file has been created successfully.')
