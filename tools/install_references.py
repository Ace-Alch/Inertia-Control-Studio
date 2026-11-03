import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data={str(n):json.loads((root/f'tools/reference{n}.json').read_text()) for n in (2,3)}
(root/'src/swing-data.js').write_text('// Nominal force references and TVLQR feedback. These data never set plant state.\nfunction swingLibrary(){return '+json.dumps(data,separators=(',',':'))+';}\n')
