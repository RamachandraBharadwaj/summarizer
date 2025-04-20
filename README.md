# Web pentest report summarizer

Many cybersecurity web pentest reports have the same problem : too mant hyperlinks, verbose technical terms, unreadable and non-user friendly format of text and information. No proper mitigation is alo provided and no explanation regarding what CVE ID or CWE is. There is also no significant explanation regarding how CVSS SCORE of each vulnerability could help us in solving problems related to the web application in question, for which the report has been generated. So to address this issue, We can use RAG -like system to format reports dynamically along with required mitigation for each vulnerability based on their CVE ID.

using mitre.org for vulnerability intelligence, to provide context to summarizer and report generating LLMs, we can leverage beautiful soup to extract required data and to give context efficient summary for each vulnerability.

here are the front end snapshots (made in react) :
![Screenshot 2025-04-20 173656](https://github.com/user-attachments/assets/b98ecb4f-e8bb-41eb-bf13-81e0fa11f066)

![Screenshot 2025-04-20 173711](https://github.com/user-attachments/assets/ef6b7888-7f68-45a4-8f98-8a8aa1af01e4)

![Screenshot 2025-04-20 173959](https://github.com/user-attachments/assets/f54e408f-5615-465a-bbe0-7d2b60167276)

Old format :
![Screenshot 2025-04-20 174634](https://github.com/user-attachments/assets/a43837fb-7e3c-4a75-b24c-c742797636b7)

newer intuitive format :
![Screenshot 2025-04-20 181746](https://github.com/user-attachments/assets/34d918c9-47ea-44cc-b583-9cf059db4ecf)

![Screenshot 2024-11-11 145638](https://github.com/user-attachments/assets/81abe817-617e-456f-9237-dd83435e7231)

future plans (if proceeded) would include a chatbot integration (with agentic worflow and context)
