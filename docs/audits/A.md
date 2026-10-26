I’ll locate the thesis source and inspect only its data/model pipeline plus the current RainCast model. I’ll run read-only inventory and CPU probes, keeping any temporary scripts outside both repositories and reporting exact failures where the thesis data or split metadata is unavailable.

Read , lines 1 to 235
Completed with input: {
  "path": "E:\\Project\\raincast\\services\\inference\\app\\model.py",
  "view_range": [
    1,
    235
  ]
}

Ran terminal command: Get-ChildItem -Force 'E:\Project' | Select-Object Mode,Name,FullName

Search for `npz_dataset|nan_to_num|nanmean|nanmax|isnan|fillna|mask|np.save|np.savez|512|...`

Read , lines 35 to 75
Completed with input: {
  "path": "E:\\Project\\raincast\\docs\\PROJECT.md",
  "view_range": [
    35,
    75
  ]
}

Search for `Nha Be|Nha_Be|convLSTM|ConvLSTM|npz_dataset|encoder_forecaster|radar|dBZ|nowc...`

Ran terminal command: Get-ChildItem -Recurse -Directory 'E:\Project' -Force | Where-Object { $_.Name -match 'thesis|nowcast|weather|radar|rain|model|data|experiment|output' -and $_.FullName -notmatch '\\(node_modules|venv|\.venv|target|build|dist|__pycache__)\\' } | Select-Object -First 200 FullName

Ran terminal command: Get-ChildItem -Path 'E:\' -Recurse -File -Force -ErrorAction SilentlyContinue -Filter 'npz_dataset.py' | Where-Object { $_.FullName -notmatch '\\(node_modules|venv|\.venv|site-packages|target|build|dist|\.git)\\' } | Select-Object -First 50 FullName

Ran terminal command: Get-ChildItem -Path 'E:\' -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object { $_.Name -in @('encoder_forecaster_89000.pth','net_params.py','convLSTM.py','evaluator.py') -and $_.FullName -notmatch '\\(node_modules|venv|\.venv|site-packages|target|build|dist|\.git)\\' } | Select-Object -First 100 FullName

Ran terminal command: Get-ChildItem -Path 'C:\Users\Admin.000' -Recurse -File -Force -ErrorAction SilentlyContinue -Filter 'npz_dataset.py' | Where-Object { $_.FullName -notmatch '\\(node_modules|venv|\.venv|site-packages|target|build|dist|\.git)\\' } | Select-Object -First 50 FullName

The thesis repository was found at `E:\PrecipitationNowcasting\ConvLSMT`. I’ll now inventory its actual files and metadata, then run isolated read-only probes against the 77000 checkpoint and one real prepared sample if the split/data files are present.

Ran terminal command: Get-ChildItem -Recurse -File -Force 'E:\PrecipitationNowcasting\ConvLSMT' | Where-Object { $_.FullName -notmatch '\\(\.git|__pycache__|\.pytest_cache|venv|\.venv|site-packages)\\' } | Select-Object FullName,Length | Sort-Object FullName

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\experiments\\net_params.py",
  "view_range": [
    1,
    180
  ]
}

Read 
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\npz_dataset.py"
}

Read 
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\models\\model.py"
}

Read , lines 120 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\evaluator.py",
  "view_range": [
    120,
    180
  ]
}

Read 
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\models\\convLSTM.py"
}

Read , lines 90 to 175
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\experiments\\convLSTM_balacned_mse_mae\\main.py",
  "view_range": [
    90,
    175
  ]
}

Read , lines 1 to 100
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\experiments\\convLSTM_balacned_mse_mae\\main.py",
  "view_range": [
    1,
    100
  ]
}

Read , lines 1 to 220
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\config.py",
  "view_range": [
    1,
    220
  ]
}

Search for `DATA|NPZ|TRAIN|VALID|TEST|FILE|PATH|input_len|target_len|stride|split_npz_fil...`

Ran terminal command: Get-ChildItem -Recurse -Directory -Force 'E:\PrecipitationNowcasting\ConvLSMT' | Where-Object { $_.FullName -notmatch '\\(\.git|__pycache__|venv|\.venv|site-packages)\\' } | Select-Object FullName | Sort-Object

Ran terminal command: Get-ChildItem -Recurse -File -Force 'E:\PrecipitationNowcasting\ConvLSMT' -Include *.npy,*.npz,*.h5,*.hdf5,*.pkl,*.pth,*.txt,*.csv,*.json | Where-Object { $_.FullName -notmatch '\\(\.git|__pycache__|venv|\.venv|site-packages)\\' } | Select-Object FullName,Length | Sort-Object FullName

Read 
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\tests\\test_npz_dataset.py"
}

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\models\\forecaster.py",
  "view_range": [
    1,
    180
  ]
}

Read 
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\outputs\\test_metrics.json"
}

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\models\\encoder.py",
  "view_range": [
    1,
    180
  ]
}

Read , lines 1 to 115
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\evaluator.py",
  "view_range": [
    1,
    115
  ]
}

Ran terminal command: Get-ChildItem -Recurse -File -Force 'E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset' | Select-Object FullName,Length | Sort-Object FullName

Read , lines 1 to 220
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\hko\\evaluation.py",
  "view_range": [
    1,
    220
  ]
}

Search for `NHB_PPI|\.nc|netCDF|npy_uncompressed|np.save|np.load|2022_|2023_|nhb_`

Ran terminal command: Get-ChildItem -Recurse -File 'E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset' -Filter *.npy | Select-Object FullName,Length; Get-ChildItem -Recurse -File 'E:\PrecipitationNowcasting\ConvLSMT' -Filter *.npz | Select-Object FullName,Length

Ran terminal command: $root='E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset'; Get-ChildItem -Recurse -File $root | Group-Object Extension | Sort-Object Name | Select-Object Name,Count,@{N='Bytes';E={($_.Group | Measure-Object Length -Sum).Sum}}; Get-ChildItem -Directory $root | Select-Object Name; Get-ChildItem -Recurse -File $root -Filter *.nc | Select-Object -First 3 FullName,Length

Ran terminal command: Get-Content 'E:\PrecipitationNowcasting\ConvLSMT\hko_data\hko7_rainy_train_days.txt'; Write-Output '--- valid ---'; Get-Content 'E:\PrecipitationNowcasting\ConvLSMT\hko_data\hko7_rainy_valid_days.txt'; Write-Output '--- test ---'; Get-Content 'E:\PrecipitationNowcasting\ConvLSMT\hko_data\hko7_rainy_test_days.txt'

Read 
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\helpers\\convert_nc_to_npy.py"
}

Read 
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\convert_npz_to_npy.py"
}

Read , lines 1 to 80
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\utils.py",
  "view_range": [
    1,
    80
  ]
}

Read 
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\README.md"
}

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\hko_data\hko7_rainy_test_days.txt'; $lines=Get-Content $p; Write-Output "test_count=$($lines.Count) first=$($lines[0]) last=$($lines[-1])"; $p='E:\PrecipitationNowcasting\ConvLSMT\hko_data\hko7_rainy_train_days.txt'; $lines=Get-Content $p; Write-Output "train_count=$($lines.Count) first=$($lines[0]) last=$($lines[-1])"; $p='E:\PrecipitationNowcasting\ConvLSMT\hko_data\hko7_rainy_valid_days.txt'; $lines=Get-Content $p; Write-Output "valid_count=$($lines.Count) first=$($lines[0]) last=$($lines[-1])"

Ran terminal command: Get-ChildItem -Recurse -File 'E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset' -Filter *.nc | Select-Object -First 5 Name; Get-ChildItem -Recurse -File 'E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset' -Filter *.nc | Select-Object -Last 5 Name

Ran terminal command: @'
import os, sys, json, math
from pathlib import Path
import numpy as np
root=Path(r'E:\PrecipitationNowcasting\ConvLSMT')
print('--- local prepared .npy stats ---')
for p in sorted(root.rglob('*.npy')):
    if any(x in p.parts for x in ['__pycache__']): continue
    a=np.load(p, mmap_mode='r', allow_pickle=False)
    finite=np.isfinite(a)
    print(p.relative_to(root), 'shape=',a.shape,'dtype=',a.dtype,'min=',float(np.nanmin(a)) if a.size else None,'max=',float(np.nanmax(a)) if a.size else None,'nan_count=',int(np.isnan(a).sum()),'finite_count=',int(finite.sum()),'normalised_0_1=',bool(np.all(a[finite]>=0)&np.all(a[finite]<=1)) if finite.any() else None)
print('--- local .npz stats ---')
for p in sorted(root.rglob('*.npz')):
    if any(x in p.parts for x in ['__pycache__']): continue
    try:
        with np.load(p, allow_pickle=False) as z:
            print(p.relative_to(root), 'keys=',z.files)
            for k in z.files:
                a=z[k]; finite=np.isfinite(a)
                print(' ',k,'shape=',a.shape,'dtype=',a.dtype,'min=',float(np.nanmin(a)) if a.size else None,'max=',float(np.nanmax(a)) if a.size else None,'nan_count=',int(np.isnan(a).sum()),'normalised_0_1=',bool(np.all(a[finite]>=0)&np.all(a[finite]<=1)) if finite.any() else None)
    except Exception as e: print(p.relative_to(root),'ERROR',type(e).__name__,str(e))
print('--- first raw netcdf metadata ---')
try:
 import xarray as xr
 p=sorted((root/'nha-be-dataset'/'20230526').glob('*.nc'))[0]
 ds=xr.open_dataset(p)
 print('file=',p.name)
 print('dims=',dict(ds.sizes))
 print('data_vars=',list(ds.data_vars))
 for k,v in ds.data_vars.items():
  a=v.values; finite=np.isfinite(a)
  print(k,'shape=',a.shape,'dtype=',a.dtype,'min=',float(np.nanmin(a)) if a.size else None,'max=',float(np.nanmax(a)) if a.size else None,'nan_count=',int(np.isnan(a).sum()),'normalised_0_1=',bool(np.all(a[finite]>=0)&np.all(a[finite]<=1)) if finite.any() else None)
 ds.close()
except Exception as e: print('NETCDF_ERROR',type(e).__name__,str(e))
'@ | & 'e:/Project/raincast/.venv/Scripts/python.exe' -

Read , lines 1 to 10
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\hko_data\\hko7_rainy_valid_days.txt",
  "view_range": [
    1,
    10
  ]
}

Read , lines 1 to 20
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\hko_data\\hko7_rainy_test_days.txt",
  "view_range": [
    1,
    20
  ]
}

Read , lines 1 to 10
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\hko_data\\hko7_rainy_train_days.txt",
  "view_range": [
    1,
    10
  ]
}

pylanceInstalledTopLevelModules
Completed with input: {
  "pythonPath": "E:\\Project\\raincast\\.venv\\Scripts\\python.exe",
  "workspaceRoot": "E:\\Project\\raincast"
}

Search for `nan_to_num|fillna|isnan|isfinite|NaN|nan|mask`

Ran terminal command: Get-Command ncdump -ErrorAction SilentlyContinue | Select-Object Source; Get-Command h5dump -ErrorAction SilentlyContinue | Select-Object Source; Get-Command netcdf_info -ErrorAction SilentlyContinue | Select-Object Source

Find files matching `**/*.npz`

Find files matching `**/npy_uncompressed/**/*.npy`

Read , lines 1 to 240
Completed with input: {
  "path": "E:\\Project\\raincast\\services\\inference\\app\\model.py",
  "view_range": [
    1,
    240
  ]
}

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\npz_dataset.py",
  "view_range": [
    1,
    180
  ]
}

Read , lines 100 to 210
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\experiments\\convLSTM_balacned_mse_mae\\main.py",
  "view_range": [
    100,
    210
  ]
}

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\models\\model.py",
  "view_range": [
    1,
    180
  ]
}

Ran terminal command: $p=(Get-ChildItem 'E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526\*.nc' | Select-Object -First 1).FullName; Write-Output $p; Format-Hex -Path $p -Count 32; strings $p | Select-Object -First 40

Ran terminal command: @'
import sys, torch
sys.path.insert(0, r'E:\Project\raincast\services\inference')
from app.model import build_model
p=r'E:\PrecipitationNowcasting\ConvLSMT\outputs\encoder_forecaster_77000.pth'
print('checkpoint_exists=',__import__('os').path.exists(p))
model=build_model()
try:
 ckpt=torch.load(p,map_location='cpu',weights_only=False)
 print('checkpoint_type=',type(ckpt).__name__)
 state=ckpt.get('state_dict',ckpt) if isinstance(ckpt,dict) else ckpt
 result=model.load_state_dict(state,strict=True)
 print('load_result=',result)
except Exception as e:
 print('load_error=',type(e).__name__,str(e))
 raise SystemExit
model.eval()
for n in (512,360):
 x=torch.rand(6,1,1,n,n)
 try:
  with torch.no_grad(): y=model(x)
  print(f'forward_{n}_shape=',tuple(y.shape),'min=',float(y.min()),'max=',float(y.max()),'mean=',float(y.mean()))
 except Exception as e:
  print(f'forward_{n}_error=',type(e).__name__,str(e))
'@ | & 'e:/Project/raincast/.venv/Scripts/python.exe' -

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\Project\\raincast\\services\\inference\\app\\preprocess.py",
  "view_range": [
    1,
    180
  ]
}

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\experiments\\net_params.py",
  "view_range": [
    1,
    180
  ]
}

Read , lines 1 to 220
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\models\\convLSTM.py",
  "view_range": [
    1,
    220
  ]
}

Read , lines 90 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\evaluator.py",
  "view_range": [
    90,
    180
  ]
}

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\hko\\evaluation.py",
  "view_range": [
    1,
    180
  ]
}

Ran terminal command: @'
import sys, os, torch
root=r'E:\PrecipitationNowcasting\ConvLSMT'; sys.path.insert(0,root); os.chdir(root)
try:
 from experiments.net_params import convlstm_encoder_params, convlstm_forecaster_params
 from nowcasting.models.model import EF
 from nowcasting.models.encoder import Encoder
 from nowcasting.models.forecaster import Forecaster
 print('import_thesis_model=ok')
 m=EF(Encoder(convlstm_encoder_params[0], convlstm_encoder_params[1]), Forecaster(convlstm_forecaster_params[0], convlstm_forecaster_params[1]))
 p=os.path.join(root,'outputs','encoder_forecaster_77000.pth')
 ck=torch.load(p,map_location='cpu',weights_only=False)
 print('checkpoint_keys=',len(ck), 'first=',next(iter(ck)))
 try:
  r=m.load_state_dict(ck,strict=True); print('thesis_load=',r)
 except Exception as e: print('thesis_load_error=',type(e).__name__,str(e).splitlines()[0])
 m.eval()
 for n in (512,360):
  try:
   with torch.no_grad(): y=m(torch.rand(6,1,1,n,n))
   print('thesis_forward',n,tuple(y.shape))
  except Exception as e: print('thesis_forward_error',n,type(e).__name__,str(e))
except Exception as e:
 print('thesis_import_error=',type(e).__name__,str(e))
'@ | & 'e:/Project/raincast/.venv/Scripts/python.exe' -

Ran terminal command: @'
import sys, os, torch
root=r'E:\PrecipitationNowcasting\ConvLSMT';sys.path.insert(0,root);os.chdir(root)
from experiments.net_params import convlstm_encoder_params, convlstm_forecaster_params
from nowcasting.models.model import EF
from nowcasting.models.encoder import Encoder
from nowcasting.models.forecaster import Forecaster
m=EF(Encoder(convlstm_encoder_params[0],convlstm_encoder_params[1]),Forecaster(convlstm_forecaster_params[0],convlstm_forecaster_params[1]))
ck=torch.load(root+r'\outputs\encoder_forecaster_77000.pth',map_location='cpu',weights_only=False)
try:m.load_state_dict(ck,strict=True)
except RuntimeError as e:
 s=str(e); print(s[:5000])
m.eval()
with torch.no_grad():
 y=m(torch.rand(6,1,1,512,512))
print('thesis_512_output_shape=',tuple(y.shape),'min=',float(y.min()),'max=',float(y.max()),'mean=',float(y.mean()))
'@ | & 'e:/Project/raincast/.venv/Scripts/python.exe' -

Search for `stride=2|ConvLSTMCell|def forward|torch.stack`

Search for `CONVLSTM_STAGE|ConvLSTM\(|conv1_leaky_1|deconv1_leaky_1|deconv2_leaky_1`

Search for `Wci|Wcf|Wco|state_height|torch.zeros`

Search for `class NPZRadarDataset|input_len|sequence_len|np.nanmax|np.clip|split_npz_file...`

Search for `mask = torch.ones_like|np.clip|output = model|files containing|nhb_2022_`

Search for `TODO|FIXME|HACK|pass$|NotImplemented|placeholder`

Search for `H=W|512|360|nha-be|npy_uncompressed|npz_ready|NHB_PPI`

Ran terminal command: $r='E:\PrecipitationNowcasting\ConvLSMT'; foreach($ext in '*.npy','*.npz','*.nc','*.pth','*.pkl','*.csv','*.txt'){ $n=(Get-ChildItem -Recurse -File $r -Filter $ext -ErrorAction SilentlyContinue).Count; Write-Output "$ext=$n" }; Write-Output "npy_uncompressed_exists=$(Test-Path ($r+'\nha-be-dataset\npy_uncompressed'))"; Write-Output "npz_ready_exists=$(Test-Path ($r+'\nha-be-dataset\npz_ready'))"

Ran terminal command: git -C 'E:\PrecipitationNowcasting\ConvLSMT' status --short --branch; git -C 'E:\PrecipitationNowcasting\ConvLSMT' --no-pager log -5 --oneline

Read , lines 1 to 45
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\docs\\dataset-status.md",
  "view_range": [
    1,
    45
  ]
}

Read , lines 1 to 75
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\config.py",
  "view_range": [
    1,
    75
  ]
}

Read , lines 270 to 320
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\docs\\reportConvlstm.md",
  "view_range": [
    270,
    320
  ]
}

Read , lines 1 to 45
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\evaluator.py",
  "view_range": [
    1,
    45
  ]
}

Read , lines 1 to 40
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\docs\\model.md",
  "view_range": [
    1,
    40
  ]
}

Search for `def pixel_to_dBZ|def rainfall_to_pixel|def pixel_to_rainfall|70.0|10.0`

Search for `output_padding|central|use_central|CENTRAL_REGION|clamp`

Ran terminal command: Test-Path 'E:\PrecipitationNowcasting\ConvLSMT\outputs\encoder_forecaster_89000.pth'; Get-ChildItem 'E:\PrecipitationNowcasting\ConvLSMT\outputs' -Filter '*.pth' | Select-Object Name,Length

# RainCast / ConvLSTM Data-Preparation Audit

**Audit scope:** `E:\PrecipitationNowcasting\ConvLSMT` and the RainCast inference implementation in `E:\Project\raincast`.

**Read-only constraints followed:** No files were modified, created, deleted, committed, reset, or stashed. No radar data or checkpoints were copied into either repository. The audit used only existing files and temporary in-memory commands.

---

## 1. Raw Data Inventory

### 1.1 Repository-wide inventory

Actual command output:

```text
*.npy=1
*.npz=1
*.nc=144
*.pth=1
*.pkl=16
*.csv=2
*.txt=8
npy_uncompressed_exists=False
npz_ready_exists=False
```

The only raw radar files found are:

```text
E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526\*.nc
```

There are **144 `.nc` files**, consistent with one day of measurements at 10-minute intervals.

Example filenames:

```text
NHB_PPI_20230526_000303.nc
NHB_PPI_20230526_001303.nc
NHB_PPI_20230526_002303.nc
NHB_PPI_20230526_003303.nc
...
NHB_PPI_20230526_235304.nc
```

The filename sequence supports an approximately 10-minute cadence: `00:03`, `00:13`, `00:23`, etc.

The files are NetCDF4/HDF5 files. The first bytes were:

```text
89 48 44 46 0D 0A 1A 0A
```

That is the HDF5 signature used by NetCDF4 files.

The local Python environment does not contain `xarray`, `netCDF4`, `h5py`, or another usable NetCDF reader. Therefore, the following raw-file properties are **NOT FOUND** from the available environment:

- Internal variable names.
- Radar array dimensions.
- Radar array dtype.
- Minimum and maximum reflectivity.
- NaN count.
- Whether the raw values are normalized.
- Coordinate metadata and fill-value semantics.

The conversion script `convert_nc_to_npy.py` confirms that the intended conversion loads the first NetCDF data variable and stacks one array per file. It does not normalize, resize, crop, fill NaNs, or apply a mask.

Relevant evidence:

- `convert_nc_to_npy.py:15` discovers `.nc` files.
- `convert_nc_to_npy.py:35` selects the first data variable when no variable is specified.
- `convert_nc_to_npy.py:43` extracts the underlying NumPy array.
- `convert_nc_to_npy.py:57` stacks arrays along the temporal axis.
- `convert_nc_to_npy.py:65` saves the result as `.npy`.

### 1.2 Prepared `.npy` files

Only one `.npy` file exists:

```text
E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526\20230526.npy
```

Actual inspection output:

```text
shape= (144,)
dtype= float32
min= 10.6596097946167
max= 10.6596097946167
nan_count= 0
finite_count= 144
normalised_0_1= False
```

This is not a valid radar sequence for `NPZRadarDataset`, because the loader requires an array with three or four dimensions:

```text
[T,H,W] or [T,H,W,C]
```

Evidence:

- `npz_dataset.py:63` rejects arrays whose rank is not 3 or 4.
- `npz_dataset.py:14` documents the expected array shapes.

The 144-element vector contains the same value in every element: `10.6596097946167`. Based on its shape, constant value, and non-normalized range, it is most likely metadata or a coordinate-like vector rather than radar reflectivity. It cannot be confirmed exactly from the available metadata.

**Exact meaning: NOT FOUND.**

The intended `.npz` and uncompressed `.npy` training directories are absent:

```text
nha-be-dataset\npz_ready exists: False
nha-be-dataset\npy_uncompressed exists: False
```

### 1.3 Existing `.npz` file

The only `.npz` file is:

```text
E:\PrecipitationNowcasting\ConvLSMT\hko_data\mask_dat.npz
```

Actual output:

```text
keys= ['outlier_mask', 'exclude_mask', 'out_boundary_mask']

outlier_mask      shape=(480, 480), dtype=uint8, min=0, max=1, nan_count=0
exclude_mask      shape=(480, 480), dtype=uint8, min=0, max=1, nan_count=0
out_boundary_mask shape=(480, 480), dtype=uint8, min=0, max=1, nan_count=0
```

This is an HKO-7 mask archive, not a RainCast radar event archive.

### 1.4 Split lists

The repository contains HKO-style split files:

- `hko7_rainy_train_days.txt`
- `hko7_rainy_valid_days.txt`
- `hko7_rainy_test_days.txt`

Counts from the actual files:

```text
test_count=131
train_count=812
valid_count=50
```

These dates are mostly from 2009–2015 and do not directly identify the local Nha Be 2023 `.nc` files.

### VERDICT:

The repository contains 144 raw NetCDF4 radar files and one unrelated-looking 144-element `.npy` vector, but the actual prepared radar sequences required for training and evaluation are **NOT FOUND**. Raw NetCDF array statistics require a NetCDF reader that is not currently available.

---

## 2. Sample Construction

### 2.1 Input and target window lengths

The dataset loader is `npz_dataset.py`.

Defaults:

```python
input_len=6
target_len=6
stride=1
```

Evidence:

- `npz_dataset.py:25` sets `input_len=6`.
- `npz_dataset.py:26` sets `target_len=6`.
- `npz_dataset.py:27` sets `stride=1`.
- `npz_dataset.py:52` defines the total sequence length as `input_len + target_len`.
- `npz_dataset.py:72` computes sliding-window count.
- `npz_dataset.py:102` extracts each 12-frame window.
- `npz_dataset.py:113` returns the first six frames as inputs.
- `npz_dataset.py:114` returns the final six frames as targets.

Therefore, the intended sample is:

```text
6 input frames + 6 target frames = 12 consecutive frames
```

The training configuration also sets:

- Input length: 6.
- Target length: 6.
- Default `NPZ_STRIDE`: 1.

Evidence: `nowcasting/config.py:49-51`.

### 2.2 Time interval between frames

The repository documentation states that the Nha Be dataset uses 10-minute intervals:

- `docs/dataset-status.md:14`
- `docs/model.md:6`
- `docs/model.md:33`

The raw filenames also support a 10-minute cadence:

```text
000303
001303
002303
003303
```

Interpreted as approximately:

```text
00:03
00:13
00:23
00:33
```

The loader itself does not inspect timestamps or resample frames. It simply uses array order. Therefore:

- Intended temporal interval: 10 minutes.
- Code-enforced temporal interval: none.
- Actual interval in the missing prepared arrays: **NOT FOUND**.

### 2.3 Train/validation/test split

The generic loader split is file-based, not window-randomized.

Evidence:

- `npz_dataset.py:143-151` sorts files.
- `npz_dataset.py:151` assigns the final ratio-based subset to validation.
- The training script separates test files by filename pattern containing `nhb_2022_`.

Evidence:

- `experiments/convLSTM_balacned_mse_mae/main.py:66`.

The default validation ratio is `0.2`:

- `nowcasting/config.py:53`.

The evaluator supports an explicit test glob:

- `nowcasting/evaluator.py:12-21`.

The documentation separately states that May and June 2023 were intended as an independent test period:

- `docs/model.md:6`.
- `docs/model.md:33`.

However, the actual May/June 2023 prepared files are absent, so the implemented split cannot be verified against those claims.

### 2.4 Spatial size

The project documentation states that the prepared Nha Be arrays are `512 x 512`:

- `docs/dataset-status.md:10`.
- `docs/model.md:6`.
- `docs/reportConvlstm.md:86`.

The model configuration uses fixed ConvLSTM state sizes:

```text
Stage 1: 102 x 102
Stage 2: 34 x 34
Stage 3: 17 x 17
```

Evidence: `experiments/net_params.py:16-18`.

The corresponding encoder convolution strides are:

```text
5, 3, 2
```

Evidence: `experiments/net_params.py:90-100`.

For a `512 x 512` input, these produce:

```text
512 -> 102 -> 34 -> 17
```

The available evidence supports a fixed 512-pixel model input. However, no preprocessing code was found that proves how an original `360 x 360` grid was converted to `512 x 512`.

The only documentation statement is:

> “512 x 512 pixels (cropped/interpolated over the Nha Be radar region).”

Evidence: `docs/dataset-status.md:10`.

The actual crop, interpolation, padding, or resampling code is **NOT FOUND**.

### VERDICT:

The intended sample is six consecutive input frames followed by six target frames, normally at 10-minute intervals, with stride 1. The prepared data is documented as `512 x 512`, but the actual conversion from a possible `360 x 360` source grid is **NOT FOUND**.

---

## 3. NaN / Invalid Pixels

### 3.1 Dataset loader behavior

The loader performs only conditional scaling and clipping:

```python
if self.normalize and np.nanmax(sequence) > 1.0:
    sequence = sequence / self.max_dbz

if self.clip:
    sequence = np.clip(sequence, 0.0, 1.0)
```

Evidence:

- `npz_dataset.py:108`.
- `npz_dataset.py:111`.

There is no call to:

```text
np.nan_to_num
fillna
masked_invalid
```

inside the dataset loader.

`np.clip` does not remove NaNs. If the source sequence contains NaNs, NaNs remain NaNs after clipping.

### 3.2 Training mask behavior

The training path creates an all-ones mask:

```python
mask = torch.ones_like(targets, dtype=torch.float32, device=cfg.GLOBAL.DEVICE)
```

Evidence:

- `experiments/convLSTM_balacned_mse_mae/main.py:148`.
- The same behavior appears in `nowcasting/evaluator.py:114`.

This means the current Nha Be baseline path does not construct a spatial validity mask from the input data.

### 3.3 Other NaN handling

The evaluator replaces NaN metric values with zero when serializing some results:

- `nowcasting/evaluator.py:160-172`.

This handles metric output serialization. It does not prove that invalid radar pixels were removed from source frames.

There are unrelated uses of `np.nan_to_num` in legacy training-statistics code:

- `nowcasting/train_and_test.py:144-159`.

No source-frame sanitization was found in the active `.npy` dataset loader.

### 3.4 Actual prepared-sample NaN counts

The only local `.npy` file contains:

```text
shape=(144,)
nan_count=0
```

But this file is not a valid radar sequence. It cannot establish the NaN status of the missing training samples.

For the actual prepared train/validation/test radar arrays:

```text
NOT FOUND
```

### VERDICT:

The active dataset loader does not fill NaNs, replace invalid pixels, or build a validity mask. The only inspected `.npy` vector has zero NaNs but is not a valid radar sequence. Whether NaNs were removed during upstream preprocessing is **NOT FOUND**.

---

## 4. Model Forward at 360 vs 512

Two model implementations exist and must be distinguished.

### 4.1 RainCast model with checkpoint 77000

The RainCast model is `services/inference/app/model.py`.

The local checkpoint is:

```text
E:\PrecipitationNowcasting\ConvLSMT\outputs\encoder_forecaster_77000.pth
```

Actual checkpoint verification:

```text
checkpoint_exists= True
checkpoint_type= OrderedDict
load_result= <All keys matched successfully>
```

The RainCast model loaded the checkpoint successfully.

Random-input forward results using:

```text
[T=6, B=1, C=1, H, W]
```

Actual output:

```text
forward_512_shape= (6, 1, 1, 512, 512)
min= -1.2736271619796753
max= 0.11339859664440155
mean= -0.9688045382499695

forward_360_shape= (6, 1, 1, 360, 360)
min= -1.2719060182571411
max= 0.11275968700647354
mean= -0.9656412601470957
```

Therefore, the active RainCast model accepts both 512 and 360 spatial inputs.

The current RainCast `ConvLSTMCell` creates hidden and cell states dynamically from the input frame:

- `services/inference/app/model.py:103-105`.
- It does not use thesis-style `b_h_w` peephole tensors.

The RainCast encoder has two stride-2 reductions:

- `services/inference/app/model.py:124`.
- `services/inference/app/model.py:127`.

The forecaster has two stride-2 transpose-convolution expansions:

- `services/inference/app/model.py:166`.
- `services/inference/app/model.py:177`.

For the tested even sizes:

```text
512 -> 256 -> 128 -> 256 -> 512
360 -> 180 -> 90  -> 180 -> 360
```

The RainCast model output is not inherently bounded to `[0,1]`. The current inference path must clamp or otherwise handle raw outputs before metric conversion.

### 4.2 Original thesis model and `b_h_w`

The original thesis model is configured in `experiments/net_params.py` and implemented in `nowcasting/models/convLSTM.py`.

The thesis `ConvLSTM` constructor stores:

```python
self._batch_size, self._state_height, self._state_width = b_h_w
```

Evidence: `nowcasting/models/convLSTM.py:13`.

It allocates learned peephole tensors using the configured spatial dimensions:

- `nowcasting/models/convLSTM.py:17-19`.
- `Wci`, `Wcf`, and `Wco` are shaped according to `state_height` and `state_width`.

It also initializes hidden and cell states with those fixed dimensions:

- `nowcasting/models/convLSTM.py:28-30`.

The peephole terms are used in the input, forget, and output gates:

- `nowcasting/models/convLSTM.py:48-51`.

The thesis configuration fixes:

```text
Stage 1: 102 x 102
Stage 2: 34 x 34
Stage 3: 17 x 17
```

Evidence: `experiments/net_params.py:16-18`.

### 4.3 Original thesis model forward results

The original thesis model was instantiated directly.

For `512 x 512` random input:

```text
thesis_forward 512 (6, 1, 1, 512, 512)
```

For `360 x 360` random input:

```text
thesis_forward_error 360 RuntimeError
Sizes of tensors must match except in dimension 1.
Expected size 72 but got size 102 for tensor number 1 in the list.
```

This confirms that the original thesis model is tied to the fixed 512-to-102-to-34-to-17 geometry.

### 4.4 Checkpoint provenance issue

The checkpoint loads into the active RainCast model:

```text
<All keys matched successfully>
```

It does **not** load strictly into the original thesis model. Actual error:

```text
Missing key(s) in state_dict:
"encoder.rnn1.Wci", "encoder.rnn1.Wcf", "encoder.rnn1.Wco",
"encoder.rnn2.Wci", ...
"forecaster.rnn1.Wci", "forecaster.rnn1.Wcf", "forecaster.rnn1.Wco"
```

This means the local `77000` checkpoint does not contain the original thesis peephole parameters expected by the original fixed-state ConvLSTM implementation. It is compatible with the simplified RainCast model, not the original thesis class as currently checked out.

### VERDICT:

The active RainCast model with checkpoint `77000` successfully accepts both 512 and 360 inputs. The original thesis ConvLSTM model accepts 512 but fails at 360 because its recurrent states and peephole parameters are fixed to 102/34/17 spatial sizes. The local checkpoint is compatible with RainCast’s simplified model, not the original thesis ConvLSTM class.

---

## 5. Real-Sample Forward

The required real prepared test sample is absent.

Expected source:

```text
nha-be-dataset\npy_uncompressed\*.npy
```

Actual result:

```text
npy_uncompressed_exists=False
```

The only local `.npy` file has shape `(144,)` and cannot produce a valid six-frame input or target sequence.

The raw `.nc` files were not converted for this audit because:

1. The task requires using a real prepared test-split sample.
2. No prepared test split is present.
3. The available environment lacks a NetCDF reader.
4. Creating a converted dataset would create an additional artifact and would not establish the project’s intended preprocessing behavior.

Therefore the following requested statistics are **NOT FOUND** for a real prepared sample:

- Raw input minimum.
- Raw input maximum.
- Raw input mean.
- Raw model-output minimum.
- Raw model-output maximum.
- Raw model-output mean.
- Confirmation that real output scale matches normalized `[0,1]` data.

The random-input forward demonstrated that raw model outputs can fall outside `[0,1]`. The thesis evaluator explicitly clamps outputs:

- `nowcasting/evaluator.py:145`.

### VERDICT:

A real prepared test sample is **NOT FOUND**, so a real-sample forward pass and its input/output statistics cannot be reported honestly.

---

## 6. Event Candidates

The requested candidate ranking requires target arrays from the test split.

Required information per sample:

- Sample identifier.
- First input-frame date/time.
- Target heavy-rain pixel count.
- Invalid-pixel fraction.

The prepared test arrays are absent:

```text
nha-be-dataset\npy_uncompressed exists: False
```

The available `.npy` file is not a radar sequence and has no sample-level date/time metadata.

The raw filenames contain date/time information, for example:

```text
NHB_PPI_20230526_000303.nc
```

However, no valid prepared 12-frame window can be constructed and validated from the local repository using the available tools.

The requested formula is:

```text
dBZ = 70*x - 10
R = (10^(dBZ/10) / 61.75)^(1/1.61)
heavy rain = R >= 10 mm/h
```

No candidate counts can be computed without target arrays.

### VERDICT:

The top-20 event-candidate table is **NOT FOUND** because the prepared test split and valid target arrays are absent.

---

## 7. Sanity Metrics

### 7.1 Requested model and persistence comparison

The requested comparison requires:

- Five real test samples.
- Six target frames per sample.
- The `77000` checkpoint.
- Persistence predictions using the last input frame.
- Heavy-rain threshold `R >= 10 mm/h`.
- Per-lead CSI, POD, FAR, and BIAS.

No valid test sample is available, so none of these per-sample metrics can be computed.

Result:

```text
Top-five 77000 metrics: NOT FOUND
Top-five persistence metrics: NOT FOUND
```

### 7.2 Grid handling

The thesis evaluator uses the full grid:

```python
HKOEvaluation(seq_len=OUT_SEQ_LEN, use_central=False)
```

Evidence: `nowcasting/evaluator.py:132`.

Therefore, the intended thesis comparison uses the complete `512 x 512` grid, not the configured optional central region.

The central-region setting is:

```text
(120, 120, 360, 360)
```

Evidence: `nowcasting/config.py:34`, but it is not used by the active evaluator because `use_central=False`.

The evaluator clamps predictions before metric calculation:

- `nowcasting/evaluator.py:145`.

### 7.3 Thesis stored metrics

The stored metrics in `outputs/test_metrics.json` contain approximately:

```text
Aggregate CSI: 0.2213826150
POD:            0.5968401708
FAR:            0.7461986466
BIAS:           2.3516035776

CSI by lead:
0.3701190682
0.2758648837
0.2195569382
0.1814667323
0.1521621491
0.1291259177
```

These are stored values. They were not recomputed from the local 77000 checkpoint during this audit because the test data is absent.

The requested comparison against the thesis `89000` values is therefore:

```text
77000 aggregate metrics: NOT FOUND
77000 per-lead metrics:  NOT FOUND
Difference from 89000:   NOT FOUND
```

### 7.4 Calibration inconsistency

The requested audit formula uses:

```text
Z-R: 61.75 and 1.61
```

The thesis utility code uses a different HKO-style calibration:

```python
a=58.53
b=1.56
```

Evidence:

- `nowcasting/utils.py:87`.
- `nowcasting/utils.py:106`.

The thesis evaluator converts thresholds through this HKO-style function rather than the requested Singapore formula.

Therefore, even if the prepared test data were restored, the audit must distinguish:

1. Metrics reproduced using the project’s existing evaluator.
2. Metrics computed using the requested `61.75 / 1.61` formula.

They are not guaranteed to be identical.

### VERDICT:

Per-sample and aggregate `77000` metrics are **NOT FOUND** because the prepared test data is absent. The stored `89000`-style metrics are available, but no honest checkpoint-to-checkpoint difference can be calculated.

---

# RECOMMENDED INPUT CONTRACT FOR RAINCAST

Based only on the verified code and successful checkpoint test, the safest current contract is:

## Required event contents

A RainCast event should contain two arrays:

```text
input
target
```

The local RainCast service contract expects:

```text
input:  shape (6, H, W)
target: shape (6, H, W)
dtype:   float32
```

The project documentation currently describes the intended production/demo shape as:

```text
(6, 360, 360)
```

However, the thesis ConvLSTM checkpoint and original thesis architecture require:

```text
(6, 512, 512)
```

for compatibility with the fixed `102 x 102`, `34 x 34`, and `17 x 17` recurrent states.

## Recommended spatial contract

For the local `encoder_forecaster_77000.pth` checkpoint and original thesis-compatible behavior:

```text
input:  float32, shape (6, 512, 512)
target: float32, shape (6, 512, 512)
```

The active RainCast copied model can technically process both 360 and 512 inputs, but this does not prove that the checkpoint was trained on 360-sized data. The available documentation strongly indicates that the checkpoint was trained and evaluated at 512.

## Normalization

The verified project convention is:

```text
x = (clip(dBZ, -10, 60) + 10) / 70
```

and:

```text
dBZ = 70*x - 10
```

Relevant RainCast implementation: `preprocess.py`.

The prepared arrays should therefore be `float32` values intended to represent normalized reflectivity.

The thesis loader additionally divides by `70.0` when it detects a maximum value greater than `1.0`:

- `npz_dataset.py:108-109`.

For a stable RainCast contract, inputs should already be normalized rather than relying on this heuristic.

## Temporal contract

Use:

```text
6 consecutive input frames
6 consecutive target frames
10-minute interval between frames
```

The total source sequence is therefore 12 frames covering approximately two hours.

## NaN and invalid-pixel handling

The current thesis loader does not fill NaNs or construct an invalid-pixel mask.

Therefore, the safest contract is:

```text
No NaNs or infinities are allowed in input or target arrays.
```

The available code does not establish an approved fill value or mask format. Do not substitute zero, `-10 dBZ`, or another value without confirming the intended scientific convention.

If invalid pixels exist, the contract must be extended with an explicit validity mask and the evaluator must apply it consistently. That behavior is currently **NOT FOUND**.

## Padding, resizing, and cropping

The evidence supports 512 x 512 prepared arrays, but the exact transformation from any original 360 x 360 radar grid is **NOT FOUND**.

Do not assume any of the following without recovering the preprocessing implementation or dataset artifact:

- Zero padding.
- Constant padding.
- Reflective padding.
- Bilinear resizing.
- Nearest-neighbor resizing.
- Center cropping.
- Geographic reprojection.

For compatibility with the fixed thesis model, the prepared input must be 512 x 512. The conversion method must be recovered before claiming scientific equivalence with the original radar grid.

---

# Remaining Unknowns and Required Follow-Up

1. **Raw NetCDF variable and dimensions**
   - Install or use an existing NetCDF4/HDF5 inspection tool outside the repositories.
   - Inspect variable names, dimensions, dtype, fill values, min/max, and NaNs.
   - Do not modify repository dependencies merely for this audit.

2. **Exact meaning of `20230526.npy`**
   - The file is a constant 144-element vector with value `10.6596097946167`.
   - It is not a valid radar sequence.
   - Its originating producer or variable name is **NOT FOUND**.

3. **Prepared `.npz` source**
   - `nha-be-dataset/npz_ready` is absent.
   - The conversion script expects archives containing `radar_sequence.npy`.
   - The original archives may exist in external storage referenced by `docs/guide.md`, but that storage was not accessed.

4. **Exact 360-to-512 preprocessing**
   - Documentation says “cropped/interpolated”.
   - The implementation performing this operation is **NOT FOUND**.

5. **Invalid-pixel preprocessing**
   - No active source-frame NaN filling or mask generation was found.
   - Whether preprocessing removed invalid pixels upstream is **NOT FOUND**.

6. **Checkpoint provenance**
   - `encoder_forecaster_77000.pth` loads into the RainCast simplified model.
   - It does not strictly load into the original thesis peephole ConvLSTM class.
   - `encoder_forecaster_89000.pth` is absent:

```text
False
```

7. **Metric calibration**
   - The requested audit formula uses `61.75` and `1.61`.
   - The thesis evaluator uses `58.53` and `1.56`.
   - The difference must be resolved before comparing new metrics with stored thesis values.

8. **Working-tree state**
   - The thesis repository was already dirty before this audit:

```text
## main...origin/main
 M docs/model.md
?? .vscode/
?? docs/reportConvlstm.md
```

No changes were made by this audit.

---

# Final Conclusion

The strongest evidence-backed conclusion is:

- The original thesis model was designed for `512 x 512` inputs.
- It uses fixed recurrent state sizes of `102 x 102`, `34 x 34`, and `17 x 17`.
- It fails with `360 x 360` inputs.
- The active RainCast simplified model accepts both 360 and 512 inputs because its recurrent states are allocated dynamically.
- The local `77000` checkpoint loads into the RainCast simplified model but not into the original thesis peephole ConvLSTM class.
- The intended prepared data is six input frames and six target frames, stored as normalized float32 arrays.
- The actual prepared data is missing locally.
- The exact raw NetCDF-to-512 preprocessing and invalid-pixel handling are not recoverable from the current repository contents.
- Real-sample forecasts, event ranking, and 77000 metric comparisons cannot be computed without restoring the prepared test data.

