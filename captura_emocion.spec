# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['captura_emocion.py'],
    pathex=[],
    binaries=[],
    datas=[('estilos', 'estilos'), ('modelo_emociones', 'modelo_emociones'), ('personajes_img', 'personajes_img'), ('inswapper_128.onnx', '.'), ('personajes.py', '.'), ('face_swap_insight.py', '.'), ('estilo_nst.py', '.'), ('detectar_emocion.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='captura_emocion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='captura_emocion',
)
