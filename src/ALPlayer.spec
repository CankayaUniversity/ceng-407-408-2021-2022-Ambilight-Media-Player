# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['ALPlayer.py'],
             pathex=['C:\\Program Files\\Python37\\Lib\\site-packages\\cv2'],
             binaries=[],
             datas=[],
             hiddenimports=['sklearn.neighbors._typedefs', 'sklearn.neighbors._partition_nodes', 'sklearn.utils._cython_blas', 'sklearn.utils._weight_vector', 'sklearn.neighbors._quad_tree', 'sklearn.tree._utils'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='ALPlayer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
