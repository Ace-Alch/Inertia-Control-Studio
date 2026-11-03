from pathlib import Path
root=Path(__file__).resolve().parent
vendor=(root/'vendor/three.cjs').read_text()
js='const THREE=(()=>{const exports={};\n'+vendor+'\nreturn exports;})();\n'
js+='\n'.join((root/'src'/f).read_text() for f in ['swing-data.js','core.js','optimizer.js','app.js','display.js','presets.js','scene.js'])
html=(root/'src/layout.html').read_text().replace('/*STYLE*/',(root/'src/style.css').read_text()).replace('/*SCRIPTS*/',js.replace('</script','<\\/script'))
(root/'index.html').write_text(html)
print('Built',len(html),'characters')
