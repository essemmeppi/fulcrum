"""Render the municipal evidence explorer without automation classifications.

Run from any directory: python path/to/render_page.py
The JSON portfolio remains the source of truth; no new process edges are inferred.
"""
import base64
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

def render():
    portfolio = json.loads((HERE / 'deta-portfolio.json').read_text())
    inventory = list(csv.DictReader((HERE / 'deta-whole-hall-inventory.csv').open()))
    for workflow in portfolio['workflows']:
        for claim in workflow['claims']:
            claim.pop('automation', None)
    data = {'portfolio': portfolio, 'inventory': inventory}
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    icon = base64.b64encode((REPO/'docs/favicon/favicon-32x32.png').read_bytes()).decode()
    template = (HERE/'page-template.html').read_text()
    result = template.replace('__CDIT_DATA__', payload).replace('__FAVICON__', icon)
    assert '__CDIT_DATA__' not in result
    assert all(s not in result for s in ('agent_can_execute', 'agent_prepares_human_decides', 'human_only', 'automation_class'))
    output = REPO/'docs/ro-tm-deta.html'
    output.write_text(result)
    print(f'Rendered {output.name}: {len(result):,} characters, {len(portfolio["workflows"])} workflows')
    return output

if __name__ == '__main__':
    render()
