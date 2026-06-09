# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

hidden = [
    'psutil', 'webview', 'clr_loader', 'pyc_loader',
    'config', 'config.paths', 'config.asset_system', 'config.runtime',
    'utils', 'utils.bootstrap', 'utils.autopatch', 'utils.legacy_patch', 'utils.debug',
    'launcher.desktop_main',
    'services.bootstrap', 'services.sidecar_api', 'services.engine_proxy',
    'services.profile_manager', 'services.node_bridge',
    'core.engine', 'core.models', 'core.win32_input',
]

a = Analysis(
    ['gxclicker.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('ui-web', 'ui-web'),
        ('profiles', 'profiles'),
        ('config', 'config'),
        ('utils', 'utils'),
        ('services', 'services'),
        ('core', 'core'),
        ('launcher', 'launcher'),
    ],
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt6', 'pytest'],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Game XClicker Elite',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/brand/favicon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Game XClicker Elite',
)
