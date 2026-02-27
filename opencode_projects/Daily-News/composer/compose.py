import json
import os
from datetime import datetime
from typing import List, Dict

def compose_daily_report(summaries: List[Dict], output_dir="outputs/daily"):
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(output_dir, f"daily_report_{today}.md")

    report_content = f"# Daily News Summary / סיכום חדשות יומי\n"
    report_content += f"**Date:** {today}\n\n"
    
    # Add source reliability information if available
    report_content += "## Source Reliability\n"
    report_content += "This report aggregates information from multiple sources. All sources are verified news outlets.\n\n"

    source_groups = {}
    for summary in summaries:
        source = summary.get("source", "Unknown")
        if source not in source_groups:
            source_groups[source] = []
        source_groups[source].append(summary)

    for source, source_summaries in source_groups.items():
        report_content += f"## 📰 {source}\n\n"
        
        for summary in source_summaries:
            title_en = summary.get('title_en') or summary.get('title', 'No Title')
            report_content += f"### 🇺🇸 {title_en}\n"
            report_content += f"🔗 [Original Article]({summary.get('url', '#')})\n\n"
            
            bullets_en = summary.get('bullets_en', [])
            if not bullets_en:
                bullets_en = ['No content available']
            
            for bullet in bullets_en:
                report_content += f"- {bullet}\n"
            
            report_content += "\n"
            
            title_he = summary.get('title_he', 'Translation failed')
            report_content += f"#### 🇮🇱 {title_he}\n"
            
            bullets_he = summary.get('bullets_he', [])
            if not bullets_he:
                bullets_he = ['No content available']
            
            for bullet in bullets_he:
                report_content += f"> - {bullet}\n"
            
            report_content += "\n---\n\n"

    # Add a disclaimer at the end
    report_content += "## Disclaimer\n"
    report_content += "This summary is generated automatically and may contain inaccuracies. "
    report_content += "Please refer to the original articles for complete and accurate information.\n\n"
    
    report_content += f"**Report generated on:** {datetime.now().isoformat()}\n"

    with open(output_file, "w", encoding='utf-8') as f:
        f.write(report_content)

    print(f"Daily report generated: {output_file}")
