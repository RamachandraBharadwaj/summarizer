# Web pentest report summarizer

Many cybersecurity web pentest reports have the same problem : too mant hyperlinks, verbose technical terms, unreadable and non-user friendly format of text and information. No proper mitigation is alo provided and no explanation regarding what CVE ID or CWE is. There is also no significant explanation regarding how CVSS SCORE of each vulnerability could help us in solving problems related to the web application in question, for which the report has been generated. So to address this issue, We can use RAG -like system to format reports dynamically along with required mitigation for each vulnerability based on their CVE ID.

using mitre.org for vulnerability intelligence, to provide context to summarizer and report generating LLMs, we can leverage beautiful soup to extract required data and to give context efficient summary for each vulnerability.

