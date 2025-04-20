from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
import os
import datetime
import uuid
import re

app = Flask(__name__)
CORS(app)
pending_data = {}

UPLOAD_FOLDER = './uploads'
HTML_FOLDER = './html_reports'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HTML_FOLDER'] = HTML_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HTML_FOLDER, exist_ok=True)

def extract_cwe_ids_from_appendix(soup):
    """
    Extract CWE IDs from the Appendix section of the ZAP report.
    This function looks for each <li> item in the Appendix's <ol> list and fetches the CWE ID from the table.
    """
    appendix_section = soup.find('section', {'id': 'appendix'})
    cwe_ids = []

    if appendix_section:
        ol_list = appendix_section.find('ol')
        if ol_list:
            for li in ol_list.find_all('li'):
                # Look for 'CWE ID' row in the table inside each <li>
                table = li.find('table', {'class': 'alert-types-table'})
                if table:
                    cwe_row = table.find('th', string="CWE ID")  # Find the row with "CWE ID"
                    if cwe_row:
                        cwe_td = cwe_row.find_next('td')  # Find the associated <td> for CWE ID
                        if cwe_td:
                            cwe_link = cwe_td.find('a')  # Extract the hyperlink
                            if cwe_link:
                                cwe_id = cwe_link.text.strip()  # Get the text of the CWE ID
                                cwe_ids.append(cwe_id)
    return cwe_ids


def extract_data_from_html(file_path):
    """
    Extracts vulnerability data from an HTML ZAP report.
    This function now includes the correct CWE ID extraction from the Appendix section.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    vulnerabilities = {"high": [], "medium": [], "low": []}
    table = soup.find('table', {'class': 'alert-type-counts-table'})
    rows = table.find_all('tr') if table else []

    # Extract CWE IDs from the appendix section
    cwe_ids = extract_cwe_ids_from_appendix(soup)

    # Extract vulnerabilities from the main table
    for i, row in enumerate(rows[1:]):
        cols = row.find_all('td')
        if len(cols) >= 2:
            vulnerability_name = row.find('th').text.strip()
            risk_level = cols[0].text.strip().lower()
            count_span = cols[1].find('span')
            count = count_span.text.strip() if count_span else '0'
            percentage_span = cols[1].find_all('span', class_='additional-info-percentages')
            count_percentage = percentage_span[0].text.strip() if percentage_span else '0%'

            # Map the correct CWE ID for each vulnerability based on its order in the report
            cwe_id = cwe_ids[i] if i < len(cwe_ids) else "Unknown"
            
            if 'high' in risk_level:
                vulnerabilities['high'].append([vulnerability_name, count, count_percentage, '', '', cwe_id])
            elif 'medium' in risk_level:
                vulnerabilities['medium'].append([vulnerability_name, count, count_percentage, '', '', cwe_id])
            elif 'low' in risk_level:
                vulnerabilities['low'].append([vulnerability_name, count, count_percentage, '', '', cwe_id])

    # Extract website and company name
    site_section = soup.find('ul', {'class': 'sites-list'})
    website = site_section.find('span').text.strip() if site_section else 'Unknown'
    company_name = soup.find('header').find('h1').text.strip() if soup.find('header') and soup.find('header').find('h1') else "Unknown"
    
    return vulnerabilities, website, company_name

def generate_vulnerability_html(vulnerabilities, level):
    """
    Generate HTML output for vulnerabilities at a given risk level.
    """
    if not vulnerabilities:
        return '<div class="no-vulnerabilities">No vulnerabilities found</div>'

    html_output = ""
    for i, vuln in enumerate(vulnerabilities, start=1):
        unique_id = f"{level}_{i}"
        cwe_id = vuln[5] if len(vuln) > 5 else "Unknown"  # CWE ID is the 6th element in the vulnerability list

        # Process description
        raw_description = vuln[3]
        processed_description = raw_description.encode('utf-8', 'replace').decode('utf-8')

        # Add newlines after colons
        processed_description = re.sub(r':(?!\n)', ':\n', processed_description)

        # Remove lines starting with "Code" and containing file paths
        processed_description = re.sub(r'Code\s+\S+\.java', '', processed_description)

        # Clean up excessive newlines and non-UTF-8 characters
        processed_description = re.sub(r'\n{2,}', '\n', processed_description)
        processed_description = re.sub(r'[^\x00-\x7F]+', '', processed_description)

        # Split the description into lines and format as paragraphs
        description_points = processed_description.splitlines()
        formatted_description = "\n".join(f"<p>{point.strip()}</p>" for point in description_points if point.strip())

        # Process mitigation (if any)
        raw_mitigation = vuln[4]
        mitigation_points = raw_mitigation.splitlines()
        formatted_mitigation = "\n".join(f"<p>{point.strip()}</p>" for point in mitigation_points if point.strip())

        # Generate the HTML output
        html_output += f"""
        <div class="vulnerability" style="margin-bottom: 20px;">
            <h3 style="margin-bottom: 10px;">{vuln[0]}</h3>
            <p><strong>Count:</strong> {vuln[1]}</p>
            <p><strong>Count %:</strong> {vuln[2]}</p>
            <p><strong>CWE ID:</strong> <a href="https://cwe.mitre.org/data/definitions/{cwe_id}.html" target="_blank">{cwe_id}</a></p>
            <div class="button-container" style="margin-top: 10px;">
                <button onclick="toggleSection('description{unique_id}', 'mitigation{unique_id}')">Description</button>
                <button onclick="toggleSection('mitigation{unique_id}', 'description{unique_id}')">Mitigation</button>
                <button onclick="askQuestion('{unique_id}')" class="ask-question-btn">Ask Question</button>
            </div>
            <button class="collapse-btn" onclick="collapseAll('description{unique_id}', 'mitigation{unique_id}')">Collapse</button>
            <div id="description{unique_id}" class="collapsible" style="margin-top: 10px;">
                {formatted_description}
            </div>
            <div id="mitigation{unique_id}" class="collapsible" style="margin-top: 10px;">
                {formatted_mitigation}
            </div>
        </div>
        """
    return html_output

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Concise Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    h1, h2 {{ color: #333; }}
    .info {{ margin-bottom: 20px; }}
    .info p {{ margin: 5px 0; }}
    .vulnerability {{ position: relative; margin-bottom: 20px; border: 1px solid #ccc; padding: 15px; border-radius: 5px; background-color: #f8f8f8; }}
    .vulnerability h3 {{ margin: 0 0 5px; color: #333; }}
    .vulnerability p {{ margin: 0; color: #555; }}
    .button-container {{ display: flex; gap: 10px; margin-top: 10px; }}
    button {{ padding: 5px 10px; cursor: pointer; background-color: #007bff; color: white; border: none; border-radius: 5px; }}
    button:hover {{ background-color: #0056b3; }}
    .collapsible {{ display: none; padding: 10px; border-top: 1px solid #ddd; margin-top: 10px; background-color: #f1f1f1; color: #333; }}
    .no-vulnerabilities {{ color: #777; font-style: italic; margin: 10px 0; }}
    .collapse-btn {{ position: absolute; top: 15px; right: 15px; background-color: #dc3545; }}
    .collapse-btn:hover {{ background-color: #c82333; }}
    .ask-question-btn {{background-color: #28a745; /* Green color for Ask Question button */}} 
    .ask-question-btn:hover {{background-color: #218838; /* Darker green on hover */}}

  </style>
</head>
<body>
  <h1>Web PenTest Report Analysis</h1>
  <h2>Concise Report</h2>
  <div class="info">
    <p><strong>Company Name:</strong> {company_name}</p>
    <p><strong>Website Link:</strong> <a href="{website_link}">{website_link}</a></p>
    <p><strong>Date:</strong> {date}</p>
    <p><strong>Time:</strong> {time}</p>
  </div>
  <h2>High Risk Vulnerabilities</h2>
  {high_risk_vulnerabilities}
  <h2>Medium Risk Vulnerabilities</h2>
  {medium_risk_vulnerabilities}
  <h2>Low Risk Vulnerabilities</h2>
  {low_risk_vulnerabilities}

    <script>
    function toggleSection(showId, hideId) {{
      const showElement = document.getElementById(showId);
      const hideElement = document.getElementById(hideId);
      
      if (showElement.style.display === 'block') {{
        showElement.style.display = 'none';
      }} else {{
        showElement.style.display = 'block';
        hideElement.style.display = 'none';
      }}
    }}

    function collapseAll(...ids) {{
      ids.forEach(id => {{
        document.getElementById(id).style.display = 'none';
      }});
    }}
  </script>

</body>
</html>
"""

def create_html(data, output_html_path, website, company_name):
    print(data)
    date = datetime.date.today().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%H:%M:%S")

    high_risk_html = generate_vulnerability_html(data.get('high', []), "high")
    medium_risk_html = generate_vulnerability_html(data.get('medium', []), "medium")
    low_risk_html = generate_vulnerability_html(data.get('low', []), "low")

    html_content = html_template.format(
        company_name=company_name,
        website_link=website,
        date=date,
        time=time,
        high_risk_vulnerabilities=high_risk_html,
        medium_risk_vulnerabilities=medium_risk_html,
        low_risk_vulnerabilities=low_risk_html
    )

    with open(output_html_path, 'w') as file:
        file.write(html_content)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    extracted_data, website, company_name = extract_data_from_html(file_path)

    report_id = str(uuid.uuid4())
    pending_data[report_id] = {
        'extracted_data': extracted_data,
        'website': website,
        'company_name': company_name,
        'html_filename': f"{os.path.splitext(file.filename)[0]}.html"
    }

    return jsonify({"message": "File uploaded and processing is pending", "report_id": report_id})

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    report_id = data.get("report_id")
    print(data)

    if not report_id or report_id not in pending_data:
        return jsonify({"error": "Invalid or missing report ID"}), 400

    descriptions = data.get('descriptions', [])
    mitigations = data.get('mitigations', [])

    for desc in descriptions:
        vuln_name = desc['vulnerability']
        description = desc['description']
        for level in ['high', 'medium', 'low']:
            for vuln_data in pending_data[report_id]['extracted_data'][level]:
                if vuln_data[0] == vuln_name:
                    vuln_data[3] = description
                    break

    for mitig in mitigations:
        vuln_name = mitig['vulnerability']
        mitigation_summary = mitig['Mitigation_Summary']
        for level in ['high', 'medium', 'low']:
            for vuln_data in pending_data[report_id]['extracted_data'][level]:
                if vuln_data[0] == vuln_name:
                    vuln_data[4] = mitigation_summary
                    break

    output_html_path = os.path.join(app.config['HTML_FOLDER'], pending_data[report_id]['html_filename'])

    create_html(
            pending_data[report_id]['extracted_data'],
            output_html_path,
            pending_data[report_id]['website'],
            pending_data[report_id]['company_name']
        )

    html_url = f"{request.host_url}html_reports/{pending_data[report_id]['html_filename']}"
    download_url = f"{request.host_url}download/{pending_data[report_id]['html_filename']}"

    return jsonify({
        "message": "HTML generated successfully",
        "html_url": html_url,
        "download_url": download_url
    })

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['HTML_FOLDER'], filename, as_attachment=True)


# Route to serve the uploaded HTML file
@app.route('/uploads/<filename>', methods=['GET'])
def download_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to get the latest uploaded HTML file
@app.route('/latest_file', methods=['GET'])
def get_latest_uploaded_file():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    if not files:
        return jsonify({"error": "No files found"}), 404
    
    # Get the full paths of the files
    file_paths = [app.config['UPLOAD_FOLDER'] + '/' + file for file in files]
    
    # Sort files by modification time, the latest file will be the last one
    latest_file = max(file_paths, key=os.path.getmtime)
    
    latest_file_name = os.path.basename(latest_file)
    
    # Now, retrieve the report_id for this latest file
    report_id = None
    for key, value in pending_data.items():
        if value['html_filename'] == f"{os.path.splitext(latest_file_name)[0]}.html":
            report_id = key
            break

    # Return the download link for the latest file along with the report_id
    download_html_url = f"{request.host_url}uploads/{latest_file_name}"
    print(download_html_url)

    return jsonify({
        "message": "Latest file retrieved successfully",
        "latest_html_file_path": download_html_url,
        "report_id": report_id  # Include the report_id in the response
    })

@app.route('/html_reports/<filename>', methods=['GET'])
def view_html_report(filename):
    return send_from_directory(app.config['HTML_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)