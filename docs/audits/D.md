I’ll keep this read-only and use only scratch outputs. I’m first verifying the project contracts and the exact conversion/peephole code, then I’ll inventory raw products and align them against the streamed archive.

"Read" failed
Completed with input: {
  "path": "E:\\Project\\raincast\\AGENTS.md"
}
Tool execution failed: Path does not exist

Read 
Completed with input: {
  "path": "E:\\Project\\raincast\\docs\\PROJECT.md"
}

Read 
Completed with input: {
  "path": "E:\\Project\\raincast\\docs\\RULES.md"
}

Read , lines 55 to 130
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\utils.py",
  "view_range": [
    55,
    130
  ]
}

Read , lines 35 to 70
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\hko\\evaluation.py",
  "view_range": [
    35,
    70
  ]
}

Read , lines 120 to 140
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\evaluator.py",
  "view_range": [
    120,
    140
  ]
}

Read , lines 1 to 75
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\models\\convLSTM.py",
  "view_range": [
    1,
    75
  ]
}

Read , lines 115 to 145
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\experiments\\convLSTM_balacned_mse_mae\\main.py",
  "view_range": [
    115,
    145
  ]
}

Read , lines 1 to 80
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\docs\\reportConvlstm.md",
  "view_range": [
    1,
    80
  ]
}

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\nowcasting\utils.py'; $i=0; Get-Content $p | % { $i++; if($i -ge 60 -and $i -le 130){'{0}:{1}' -f $i,$_} }

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\nowcasting\hko\evaluation.py'; $i=0; Get-Content $p | % { $i++; if($i -ge 50 -and $i -le 68){'{0}:{1}' -f $i,$_} }

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\nowcasting\evaluator.py'; $i=0; Get-Content $p | % { $i++; if(($i -ge 120 -and $i -le 135) -or ($i -ge 350 -and $i -le 365)){'{0}:{1}' -f $i,$_} }

Ran terminal command: $roots=@('E:\PrecipitationNowcasting','C:\Users\Admin.000'); foreach($r in $roots){ Write-Output "ROOT $r"; Get-ChildItem -LiteralPath $r -Directory -Force -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName }

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\experiments\convLSTM_balacned_mse_mae\main.py'; Select-String -Path $p -Pattern 'Adam|optimizer|model.parameters|batch_to_sequence|channel' -Context 1,2

Ran terminal command: & 'E:\Project\raincast\.venv\Scripts\python.exe' -c "import importlib.util; print('netCDF4',bool(importlib.util.find_spec('netCDF4'))); print('h5py',bool(importlib.util.find_spec('h5py'))); print('xarray',bool(importlib.util.find_spec('xarray'))); print('psutil',bool(importlib.util.find_spec('psutil')))"

Search for `radar_sequence|savez|resize|interpolate|zoom|cv2|map_coordinates|griddata`

Ran terminal command: $root='E:\PrecipitationNowcasting'; Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction SilentlyContinue | Where-Object {$_.FullName -notmatch '\\(\.git|node_modules|\.venv|site-packages)\\' -and $_.Extension -match '\.(nc|h5|hdf5|npy|npz)$' -and $_.Name -match '(?i)MAX|PPI|NHB'} | Group-Object {$_.DirectoryName} | Sort-Object Name | ForEach-Object {"$($_.Name) count=$($_.Count)"}

Ran terminal command: $root='E:\PrecipitationNowcasting'; Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction SilentlyContinue | Where-Object {$_.FullName -notmatch '\\(\.git|node_modules|\.venv|site-packages)\\' -and $_.Name -match '(?i)MAX|PPI' } | Select-Object -First 80 FullName,Length

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\experiments\convLSTM_balacned_mse_mae\main.py'; $i=0; Get-Content $p | % {$i++; if($i -ge 230 -and $i -le 238){'{0}:{1}' -f $i,$_}}

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\nowcasting\models\convLSTM.py'; $i=0; Get-Content $p | % {$i++; if($i -le 30){'{0}:{1}' -f $i,$_}}

Ran terminal command: & 'E:\Project\raincast\.venv\Scripts\python.exe' -c "import numpy as np; a=58.53;b=1.56; print('r x dBZ70 dBZ70m10');\nfor r in [0.5,2,5,10,30]:\n d=10*b*np.log10(r)+10*np.log10(a); x=(d+10)/70; print(r,x,d,d-10)\nfor a,b in [(58.53,1.56),(61.75,1.61)]:\n d=10*b*np.log10(10)+10*np.log10(a); print(a,b,(d+0)/70,(d+10)/70,d)"
Tool execution failed with exit code 1

Ran terminal command: Get-ChildItem 'E:\PrecipitationNowcasting\Dataset-Processed' -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 100 FullName,Length

Ran terminal command: Get-ChildItem 'E:\PrecipitationNowcasting\Dataset' -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 100 FullName,Length

Ran terminal command: $root='E:\PrecipitationNowcasting'; Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction SilentlyContinue | Where-Object {$_.FullName -notmatch '\\(\.git|node_modules|\.venv|site-packages)\\' -and $_.Extension -match '\.(nc|h5|hdf5)$'} | Group-Object {$_.Extension.ToLower()} | % {"$($_.Name) count=$($_.Count)"}

Search for `MAX|PPI|radar_sequence|Dataset-Processed|NHB_`

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\docs\reportConvlstm.md'; Select-String -Path $p -Pattern '12,643,945|parameter|peephole' -Context 2,2

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\nowcasting\models\convLSTM.py'; $i=0; Get-Content $p | % {$i++; if($i -ge 35 -and $i -le 55){'{0}:{1}' -f $i,$_}}

The local evidence already exposes a key calibration conflict: the executable thesis converter uses `x=(dBZ+10)/70`, while project documentation says Nha Be arrays were prepared with `x=dBZ/70`. I’m treating these as two separate hypotheses, not silently choosing one.

Ran terminal command: $s='C:\Users\Admin.000\raincast-raw-audit-20261026'; New-Item -ItemType Directory -Force $s | Out-Null; if(-not (Test-Path "$s\Scripts\python.exe")){python -m venv $s}; & "$s\Scripts\python.exe" -m pip install netCDF4 --quiet

Ran terminal command: Get-Command 7z,rar,unrar -ErrorAction SilentlyContinue | Select-Object Name,Source
Tool execution failed with exit code 1

Ran terminal command: & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' -c "from netCDF4 import Dataset; p=r'E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526\NHB_PPI_20230526_000303.nc'; ds=Dataset(p); print(ds.ncattrs()); print(ds.dimensions.keys()); [(print(n,v.dimensions,v.shape,v.dtype,{a:getattr(v,a) for a in v.ncattrs()})) for n,v in ds.variables.items()]; ds.close()"

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\docs\reportConvlstm.md'; $i=0; Get-Content $p | % {$i++; if($i -ge 278 -and $i -le 288){'{0}:{1}' -f $i,$_}}

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\docs\dataset-status.md'; $i=0; Get-Content $p | % {$i++; if($i -le 25){'{0}:{1}' -f $i,$_}}

Edit 

Ran terminal command: & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' 'C:\Users\Admin.000\raincast-raw-audit-20261026\inspect_raw.py'

Edit 

Ran terminal command: & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' 'C:\Users\Admin.000\raincast-raw-audit-20261026\thresholds.py'

Ran terminal command: @'
import torch
p=r'E:\PrecipitationNowcasting\ConvLSMT\outputs\encoder_forecaster_77000.pth'
s=torch.load(p,map_location='cpu',weights_only=True)
print('checkpoint_total',sum(v.numel() for v in s.values()))
for k,v in s.items(): print(k,tuple(v.shape),v.numel())
peephole=2*(3*64*102*102+3*192*34*34+3*192*17*17)
print('peephole_total_six_cells',peephole)
print('docs_plus_peepholes',12643945+peephole)
print('docs_minus_peepholes',12643945-peephole)
'@ | & 'E:\Project\raincast\.venv\Scripts\python.exe' -

Edit 

Ran terminal command: & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' 'C:\Users\Admin.000\raincast-raw-audit-20261026\compare_scales.py'
Tool execution failed with exit code 1

Edit 

Ran terminal command: & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' 'C:\Users\Admin.000\raincast-raw-audit-20261026\compare_scales.py'

Ran terminal command: @'
import zipfile,numpy as np
p=r'E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz'
with zipfile.ZipFile(p) as z:
 with z.open('radar_sequence.npy') as f:
  print(np.lib.format.read_magic(f)); print(np.lib.format.read_array_header_1_0(f))
  # header read returns tuple
  shape,fort,dtype=np.lib.format.read_array_header_1_0(f)
'@ | & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' -
Tool execution failed with exit code 1

Ran terminal command: @'
import zipfile,numpy as np
p=r'E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz'
with zipfile.ZipFile(p) as z:
 with z.open('radar_sequence.npy') as f:
  np.lib.format.read_magic(f); shape,fort,dtype=np.lib.format.read_array_header_1_0(f); n=int(np.prod(shape[1:])*dtype.itemsize); b=f.read(n); x=np.frombuffer(b,dtype).reshape(shape[1:]); print(shape,dtype,n,x[:,:,0].min(),x[:,:,0].max(),x[:,:,1].min(),x[:,:,1].max(),np.unique(x[:,:,1])[:10])
'@ | & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' -

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\plot_case_study.py'; $i=0; Get-Content $p | % {$i++; if($i -ge 90 -and $i -le 120){'{0}:{1}' -f $i,$_}}

Read , lines 1 to 80
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\convert_npz_to_npy.py",
  "view_range": [
    1,
    80
  ]
}

Read , lines 1 to 80
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\npz_dataset.py",
  "view_range": [
    1,
    80
  ]
}

Ran terminal command: @'
import torch
p=r'E:\PrecipitationNowcasting\ConvLSMT\outputs\encoder_forecaster_77000.pth'
s=torch.load(p,map_location='cpu',weights_only=True)
print('dtype_counts', {str(next(iter([v.dtype]))):0 for v in []})
print('total',sum(v.numel() for v in s.values()))
'@ | & 'E:\Project\raincast\.venv\Scripts\python.exe' -

Ran terminal command: @'
import zipfile,numpy as np
p=r'E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz'
with zipfile.ZipFile(p) as z:
 with z.open('radar_sequence.npy') as f:
  np.lib.format.read_magic(f); shape,_,dtype=np.lib.format.read_array_header_1_0(f); n=int(np.prod(shape[1:])*dtype.itemsize); vals=set()
  for i in range(shape[0]):
   x=np.frombuffer(f.read(n),dtype)
   if len(vals)<10: vals.update(np.unique(x[:,]))
  print('shape',shape,'sample_unique_channel1_not_available')
'@ | & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' -

Edit 

`Check archive member streaming basics` completed

Read Terminal
Completed with input: {
  "shellId": "30",
  "delay": 0
}

Ran terminal command: & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' 'C:\Users\Admin.000\raincast-raw-audit-20261026\events.py'

Ran terminal command: @'
import torch
p=torch.nn.Parameter(torch.zeros(1)).to('cpu'); print(type(p), isinstance(p,torch.nn.Parameter))
'@ | & 'E:\Project\raincast\.venv\Scripts\python.exe' -

Ran terminal command: @'
import zipfile,numpy as np
p=r'E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz'
with zipfile.ZipFile(p) as z:
 with z.open('radar_sequence.npy') as f:
  np.lib.format.read_magic(f); shape,_,dtype=np.lib.format.read_array_header_1_0(f); n=int(np.prod(shape[1:])*dtype.itemsize); counts={0:0,1:0}; other=0; total=0
  for i in range(shape[0]):
   x=np.frombuffer(f.read(n),dtype).reshape(shape[1:])[:,:,1]
   counts[0]+=int((x==0).sum()); counts[1]+=int((x==1).sum()); other+=int(((x!=0)&(x!=1)).sum()); total+=x.size
  print('channel1_total',total,'zero',counts[0],'one',counts[1],'other',other)
'@ | & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' -

The raw NetCDF inspection is complete: the local extracted raw set is one May 26 PPI day with 144 frames, 720×720 `DBZ` plus `RAIN_RATE`, and 10-minute cadence with no duplicate timestamps. The month-wide archive has 4,462 frames but no timestamps, so an exact May-wide index-to-time mapping cannot be asserted.

Read Terminal
Completed with input: {
  "shellId": "33",
  "delay": 60
}

Ran terminal command: @'
import math
for r in [.5,2,5,10,30]:
 d=10*1.56*math.log10(r)+10*math.log10(58.53); x=(d+10)/70
 print(r,x,70*x,70*x-10)
'@ | & 'C:\Users\Admin.000\raincast-raw-audit-20261026\Scripts\python.exe' -

# RainCast / ConvLSTM Data-Calibration Audit

All repository and data files were inspected read-only. No files were modified, committed, copied into Git repositories, or deleted. Scratch scripts were placed under `C:\Users\Admin.000\raincast-raw-audit-20261026`.

## 1. Threshold Logic

### 1.1 Thesis conversion functions

The executable conversion code is in `nowcasting/utils.py`.

#### `pixel_to_dBZ`

`nowcasting/utils.py:60-71`

```python
def pixel_to_dBZ(img):
    ...
    return img * 70.0 - 10.0
```

This implements:

```text
dBZ = 70*x - 10
```

#### `dBZ_to_pixel`

`nowcasting/utils.py:73-84`

```python
def dBZ_to_pixel(dBZ_img):
    ...
    return np.clip((dBZ_img + 10.0) / 70.0, a_min=0.0, a_max=1.0)
```

This implements:

```text
x = clip((dBZ + 10) / 70, 0, 1)
```

#### `pixel_to_rainfall`

`nowcasting/utils.py:87-103`

```python
def pixel_to_rainfall(img, a=58.53, b=1.56):
    ...
    dBZ = pixel_to_dBZ(img)
    dBR = (dBZ - 10.0 * np.log10(a)) / b
    rainfall_intensity = np.power(10, dBR / 10.0)
    return rainfall_intensity
```

This uses:

```text
dBZ = 70*x - 10
R = (10^((dBZ - 10 log10(a)) / b))^(1/10)
```

Equivalent Z-R form:

```text
Z = a R^b
```

with:

```text
a = 58.53
b = 1.56
```

#### `rainfall_to_pixel`

`nowcasting/utils.py:106-123`

```python
def rainfall_to_pixel(rainfall_intensity, a=58.53, b=1.56):
    ...
    dBR = np.log10(rainfall_intensity) * 10.0
    # dBZ = 10b log(R) +10log(a)
    dBZ = dBR * b + 10.0 * np.log10(a)
    pixel_vals = (dBZ + 10.0) / 70.0
    return pixel_vals
```

The evaluator threshold is therefore based on:

```text
x = (10*b*log10(R) + 10*log10(a) + 10) / 70
```

### 1.2 How the evaluator applies thresholds

`nowcasting/hko/evaluation.py:51-60`

```python
if thresholds is None:
    thresholds = cfg.HKO.EVALUATION.THRESHOLDS
...
thresholds = rainfall_to_pixel(np.array(thresholds,
                                        dtype=np.float32)
                               .reshape((1, 1, len(thresholds), 1, 1)))
bpred = (prediction >= thresholds)
btruth = (truth >= thresholds)
```

The evaluator converts rainfall thresholds to normalized pixel thresholds before comparing predictions and targets.

The evaluation entry point constructs `HKOEvaluation` at `nowcasting/evaluator.py:120-133`:

```python
evaluater = HKOEvaluation(seq_len=OUT_SEQ_LEN, use_central=False)
model.eval()
```

The default test fallback is defined at `nowcasting/evaluator.py:355-363`:

```python
test_glob = (
    f"{cfg.NPZ.DATA_DIR}/nhb_2023_05.npy {cfg.NPZ.DATA_DIR}/nhb_2023_06.npy "
)
```

### 1.3 Threshold table

For the thesis evaluator’s default Z-R relation:

```text
a = 58.53
b = 1.56
```

The evaluator’s normalized threshold is based on the executable `dBZ = 70*x - 10` convention.

| Rainfall threshold | Evaluator normalized threshold | dBZ if `dBZ = 70*x` | dBZ if `dBZ = 70*x - 10` |
|---:|---:|---:|---:|
| 0.5 mm/h | 0.3282531044111957 | 22.9777173087837 | 12.9777173087837 |
| 2 mm/h | 0.4624264739071417 | 32.36985317349992 | 22.36985317349992 |
| 5 mm/h | 0.5511102472683387 | 38.577717308783704 | 28.577717308783704 |
| 10 mm/h | 0.6181969320163115 | 43.27378524114181 | 33.27378524114181 |
| 30 mm/h | 0.7245268116395506 | 50.71687681476854 | 40.71687681476854 |

The important 10 mm/h values are:

```text
Evaluator threshold: 0.6181969320163115

If archive x = dBZ / 70:
    10 mm/h corresponds to x = 33.27378524114181 / 70
                       = 0.4753397891591687

If archive x = (dBZ + 10) / 70:
    10 mm/h corresponds to x = 0.6181969320163115
```

For the alternative Z-R relation:

```text
a = 61.75
b = 1.61
```

the 10 mm/h physical reflectivity is:

```text
dBZ = 34.006369619317034
```

Therefore:

```text
If x = dBZ / 70:
    x = 0.48580528027595765

If x = (dBZ + 10) / 70:
    x = 0.6286624231331005
```

### VERDICT

The executable evaluator uses `x=(dBZ+10)/70`, but project documentation explicitly says the Nha Be archive may use `x=dBZ/70`; both conventions must remain separate until raw/archive alignment proves which one was used.

---

## 2. Raw vs Archive Value Scale

### 2.1 Raw radar locations and products

The extracted local raw dataset is:

`E:/PrecipitationNowcasting/ConvLSMT/nha-be-dataset/20230526/`

Observed files:

```text
raw_nc_count 144
raw_first E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526\NHB_PPI_20230526_000303.nc
raw_last  E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526\NHB_PPI_20230526_235304.nc
```

The files are:

```text
Product: PPI
Format: NetCDF
Filename pattern: NHB_PPI_YYYYMMDD_HHMMSS.nc
Count locally available: 144
Month represented: May 2023, day 26 only
```

The broader raw archive folder is:

`E:/PrecipitationNowcasting/Dataset/`

It contains monthly `.rar` archives such as:

```text
2020 Produc T6.rar
2021 Produc T2.rar
2021 Produc T3.rar
...
2022 Producs T12.rar
Producs T01-2023.rar
Producs T02-2023.rar
...
Producs T05-2023.rar
Producs T6-2023.rar
```

A RAR listing utility was not available in the inspected environment, so exact file counts inside those compressed monthly archives are:

```text
NOT FOUND
```

The only extracted raw product count that can be verified directly is the 144-file May 26 PPI set.

### 2.2 Raw NetCDF structure

The first raw frame was:

```text
E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526\NHB_PPI_20230526_000303.nc
```

Global attributes:

```text
radar_name: nha-be-radar
time: 2023-05-26T00:03:03Z
product_type: PPI
scan_name: CD2_005_120 CD2
scan_type: CD2
source: Sigmet IRIS product
range_km: 120
pixel_size_km: 0.3333
known_artifacts: vertical stripe ~+100km east (hardware interference);
                 horizontal stripe ~-100km south (hardware issue);
                 ground clutter ~10km center radius;
                 cone of silence in MAX center (NaN)
nan_fraction: 0.9536631944444445
```

Variables:

| Variable | Shape | Units | Description |
|---|---:|---|---|
| `x` | `(720,)` | km | Distance east from radar |
| `y` | `(720,)` | km | Distance north from radar |
| `lat_radar` | scalar | degrees north | Radar latitude |
| `lon_radar` | scalar | degrees east | Radar longitude |
| `DBZ` | `(720,720)` | dBZ | Reflectivity |
| `RAIN_RATE` | `(720,720)` | mm/hr | Derived rain rate |

`DBZ` metadata:

```text
dtype: float32
units: dBZ
long_name: reflectivity
_FillValue: NaN
```

Measured first-frame `DBZ` statistics:

```text
min: -16.0
max: 59.5
NaN count: 494379
```

`RAIN_RATE` metadata:

```text
units: mm/hr
long_name: rain rate (Marshall-Palmer Z-R: Z = 200*R^1.6)
_FillValue: NaN
```

Measured first-frame `RAIN_RATE` statistics:

```text
min: 0.0036463323049247265
max: 190.8122100830078
NaN count: 494379
```

The raw PPI therefore contains physical dBZ values and a derived rain-rate field. It is not itself normalized `[0,1]` data.

### 2.3 Archive structure

Archive:

`E:/PrecipitationNowcasting/NhaBe-npz/nhb_2023_05.npz`

Previously verified:

```text
member: radar_sequence.npy
shape: (4462, 512, 512, 2)
dtype: float32
channel 0 min/max: 0.0 / 1.0
channel 1 min/max: 0.0 / 1.0
NaNs: 0
```

The exact archive channel-one counts were rechecked:

```text
channel1_total: 1169686528
zero:           1032812473
one:             136874055
other:          0
```

Thus every sampled/streamed channel-one value is exactly `0.0` or `1.0`.

### 2.4 Distribution comparison

Non-zero raw `DBZ` quantiles across the 144 local PPI frames:

```text
[0.5, 1.0, 4.5, 9.5, 19.0, 30.0, 37.0, 49.0, 75.0]
```

The maximum raw dBZ is `75.0` across the local files, although the first frame’s maximum was `59.5`.

Raw values transformed as `dBZ/70`:

```text
[0.0071428571827709675,
 0.014285714365541935,
 0.06428571790456772,
 0.13571429252624512,
 0.27142858505249023,
 0.4285714328289032,
 0.5285714268684387,
 0.699999988079071,
 1.0714285373687744]
```

Raw values transformed as `clip((dBZ+10)/70, 0, 1)`:

```text
[0.15000000596046448,
 0.15714286267757416,
 0.20714285969734192,
 0.2785714268684387,
 0.41428571939468384,
 0.5714285969734192,
 0.6714285612106323,
 0.8428571224212646,
 1.0]
```

Sampled archive channel-zero non-zero quantiles:

```text
[6.063600039851735e-07,
 0.006733467206358909,
 0.046200260519981384,
 0.08822669088840485,
 0.15421666204929352,
 0.2801925241947174,
 0.4773478448390962,
 0.7861872315406799,
 1.0]
```

These are not a valid pixelwise comparison because:

1. The raw files are only May 26.
2. The archive covers May but has no timestamps.
3. The raw grid is 720×720.
4. The archive grid is 512×512.
5. The local raw set does not contain 4,462 frames.
6. No local preprocessing implementation was found that specifies the spatial conversion.

The distributions are therefore only broadly compatible with normalized reflectivity. They do not prove either transform.

### VERDICT

The raw files contain physical dBZ and rain-rate products; the archive contains normalized float data. Distribution-only comparison is inconclusive between `dBZ/70` and `(dBZ+10)/70`. Pixelwise conversion cannot be verified without a matching timestamp and spatial preprocessing implementation.

---

## 3. Channels and Spatial Preprocessing

### 3.1 Code evidence

The training code retains channel zero:

`experiments/convLSTM_balacned_mse_mae/main.py:141-146`

```python
def batch_to_sequence(batch):
    inputs, targets = batch
    inputs = inputs.to(cfg.GLOBAL.DEVICE, non_blocking=True).permute(1, 0, 2, 3, 4)
    targets = targets.to(cfg.GLOBAL.DEVICE, non_blocking=True).permute(1, 0, 2, 3, 4)
    # CUSTOM LOGIC FOR BASELINE: Method 1 — keep only channel 0 (reflectivity)
    inputs = inputs[:, :, 0:1, :, :]
    targets = targets[:, :, 0:1, :, :]
```

The case-study loader does the same:

`plot_case_study.py:93-110`

```python
seq = np.moveaxis(seq, -1, 1)
# CUSTOM LOGIC FOR BASELINE: channel 0 only
seq = seq[:, 0:1, :, :]
if np.nanmax(seq) > 1.0:
    seq = seq / max_dbz
seq = np.clip(seq, 0.0, 1.0)
```

The project documentation calls channel zero horizontal reflectivity:

`docs/reportConvlstm.md:...`

The exact line number for the descriptive channel statement was not reproduced in the final command output, but the code behavior is directly verified above.

### 3.2 Search for preprocessing code

Search terms:

```text
radar_sequence
savez
resize
interpolate
zoom
cv2
map_coordinates
griddata
```

Search scope:

- `E:/PrecipitationNowcasting/Dataset-Processed/`
- `E:/PrecipitationNowcasting/Dataset/`
- `E:/PrecipitationNowcasting/Thesis_LeDucDong/`
- broader `E:/PrecipitationNowcasting` source files

Result:

```text
No preprocessing source files matching those terms were found.
```

`Dataset-Processed` contains only:

```text
E:\PrecipitationNowcasting\Dataset-Processed\2020.lnk
```

The only local conversion script found is `convert_npz_to_npy.py`. It only extracts the existing `radar_sequence.npy` member from `.npz`; it does not convert raw NetCDF, resize images, or create channels:

`convert_npz_to_npy.py:15-40`

```python
with zipfile.ZipFile(npz_path) as archive:
    names = archive.namelist()
    ...
    with archive.open(member_name, "r") as source, open(tmp_path, "wb") as target:
        while True:
            chunk = source.read(CHUNK_SIZE)
            if not chunk:
                break
            target.write(chunk)
```

### 3.3 Channel interpretation

Verified:

- Channel zero is the channel used by the thesis model.
- The code labels channel zero as reflectivity.
- Archive channel one is strictly binary `0/1`.
- Channel one is not passed to the ConvLSTM model.

Reasonable but unproven interpretation:

```text
Channel 1 may be a validity/availability mask.
```

Evidence supporting that interpretation:

- It is exactly binary.
- The raw NetCDF contains extensive NaN regions.
- A binary valid-data mask would be consistent with those regions.

However, no local preprocessing code creates `radar_sequence`, so the exact meaning of channel one is:

```text
NOT FOUND
```

It could also be another binary product or flag.

### 3.4 Spatial conversion

Verified:

```text
Raw PPI grid: 720×720
Archive/model grid: 512×512
```

The project documentation says the archive is:

```text
512×512 pixels (cropped/interpolated over the Nha Be radar region)
```

but no implementation of the crop, resize, interpolation, or reprojection was found.

Exact 720→512 or 360→512 conversion:

```text
NOT FOUND
```

### VERDICT

Channel zero is verified as the model’s reflectivity input. Channel one is verified as binary but its semantic identity is NOT FOUND. The spatial conversion from raw 720×720 PPI to archive 512×512 is NOT FOUND.

---

## 4. Time Alignment

### 4.1 Raw timestamps

Raw filenames encode timestamps such as:

```text
NHB_PPI_20230526_000303.nc
NHB_PPI_20230526_235304.nc
```

The first file’s internal NetCDF time attribute is:

```text
2023-05-26T00:03:03Z
```

The final file’s filename timestamp is:

```text
2023-05-26 23:53:04
```

Observed raw file count:

```text
144
```

Observed filename timestamp spacing:

```text
minimum:  9.95 minutes
median:  10.00 minutes
maximum: 10.05 minutes
duplicates: 0
```

The small deviations are seconds-level timestamp jitter around a 10-minute cadence.

The command reported many individual intervals with values such as:

```text
9.95
9.966666666666667
9.983333333333333
10.0
10.016666666666667
10.033333333333333
10.05
```

There were no large missing-frame gaps in the extracted May 26 sequence; all differences were within approximately ±3 seconds of 10 minutes.

### 4.2 Archive count comparison

Archive frame count:

```text
4462
```

Expected number of 10-minute frame slots in a 31-day May:

```text
31 * 24 * 6 = 4464
```

Difference:

```text
4464 - 4462 = 2 frames
```

The archive does not contain timestamps or metadata. The two missing frame positions cannot be identified.

### 4.3 Index-to-file hypothesis

Requested hypothesis:

```text
archive index i = i-th raw file in sorted time order
```

This cannot be tested for the month because:

- Archive: 4,462 frames.
- Available raw May 2023 files: 144 frames.
- The raw files cover only May 26.
- The archive has no timestamp metadata.
- No local preprocessing mapping exists.

Pixelwise comparison at archive indices spread across the month, including `3641-3656`, is therefore:

```text
NOT FOUND
```

There is no defensible way to associate those archive indices with May 26 raw files.

### 4.4 Timestamps for archive starts 3641–3656

Requested timestamp range:

```text
archive starts 3641 through 3656
```

Result:

```text
NOT FOUND
```

The archive has no timestamps, and the count mismatch prevents a verified index mapping.

The raw timezone is explicitly UTC in the first NetCDF global attribute:

```text
2023-05-26T00:03:03Z
```

A local-time conversion would normally require the owner’s intended timezone contract. The project context suggests Vietnam time, UTC+07:00, but archive timestamps themselves cannot be produced from that assumption.

### VERDICT

Raw May 26 timestamps are verified at approximately 10-minute spacing, but archive index-to-time mapping and the timestamps for starts 3641–3656 are NOT FOUND.

---

## 5. Peepholes and Parameter Counts

### 5.1 Peephole creation

The current thesis implementation is `nowcasting/models/convLSTM.py`.

The parameters are created at lines 17–19:

```python
self.Wci = nn.Parameter(
    torch.zeros(1, num_filter, self._state_height, self._state_width)
).to(cfg.GLOBAL.DEVICE)

self.Wcf = nn.Parameter(
    torch.zeros(1, num_filter, self._state_height, self._state_width)
).to(cfg.GLOBAL.DEVICE)

self.Wco = nn.Parameter(
    torch.zeros(1, num_filter, self._state_height, self._state_width)
).to(cfg.GLOBAL.DEVICE)
```

Therefore:

- Initial values: zeros.
- Type: `nn.Parameter`.
- Device transfer: `.to(cfg.GLOBAL.DEVICE)`.
- They are model parameters, not buffers.

The recurrent computation uses them at `convLSTM.py:46-52`:

```python
i, f, tmp_c, o = torch.chunk(conv_x, 4, dim=1)

i = torch.sigmoid(i+self.Wci*c)
f = torch.sigmoid(f+self.Wcf*c)
c = f*c + i*torch.tanh(tmp_c)
o = torch.sigmoid(o+self.Wco*c)
h = o*torch.tanh(c)
```

Gate order in this source is:

```text
i, f, candidate, o
```

### 5.2 Optimizer inclusion

The training script creates the optimizer as:

`experiments/convLSTM_balacned_mse_mae/main.py:233-237`

```python
criterion = Weighted_mse_mae().to(cfg.GLOBAL.DEVICE)
encoder_forecaster = build_convlstm_model()

optimizer = torch.optim.Adam(encoder_forecaster.parameters(), lr=LR)
scheduler = lr_scheduler.StepLR(optimizer, step_size=LR_step_size, gamma=gamma)
```

Because `Wci`, `Wcf`, and `Wco` are `nn.Parameter` attributes, they are included in `encoder_forecaster.parameters()` in this implementation.

They should therefore:

- Receive gradients.
- Be updated by Adam.
- Appear in `state_dict()`.
- Be saved by a normal `torch.save(model.state_dict(), ...)`.

A direct PyTorch check also confirmed:

```text
type(nn.Parameter(torch.zeros(1)).to("cpu")):
torch.nn.parameter.Parameter
```

### 5.3 Checkpoint parameter count

Measured from:

`outputs/encoder_forecaster_77000.pth`

```text
checkpoint_total = 12643945
```

The checkpoint contains 28 tensors and no peephole tensors.

This exactly matches the documented total:

```text
docs/reportConvlstm.md:
Total model parameter count: 12,643,945
```

### 5.4 Peephole arithmetic

The architecture has six ConvLSTM cells:

- Encoder stage 1: 64 filters, state `102×102`
- Forecaster stage 1: 64 filters, state `102×102`
- Encoder stage 2: 192 filters, state `34×34`
- Forecaster stage 2: 192 filters, state `34×34`
- Encoder stage 3: 192 filters, state `17×17`
- Forecaster stage 3: 192 filters, state `17×17`

Each cell has three peephole tensors, so the total would be:

```text
2 * [
    3 * 64  * 102 * 102
  + 3 * 192 * 34  * 34
  + 3 * 192 * 17  * 17
]
```

Measured result:

```text
peephole_total_six_cells = 5,659,776
```

If those peepholes were present in addition to the 12,643,945 checkpoint parameters:

```text
12,643,945 + 5,659,776 = 18,303,721
```

But the checkpoint contains exactly:

```text
12,643,945
```

and no peepholes.

### 5.5 Were peepholes constant zeros during training?

The current source initializes peepholes to zero, but because they are optimizer parameters, the current source does **not** make them permanently constant.

The checkpoint contains no peepholes at all.

Therefore:

```text
Whether the 77000 training run used this exact peephole implementation: NOT FOUND
```

The evidence disproves the claim that the saved 77000 checkpoint contains trained peepholes. It does not prove whether:

1. Training used a no-peephole implementation.
2. Peepholes were removed before saving.
3. A different model source produced the checkpoint.
4. An export script omitted them.

The documentation is internally inconsistent: it describes peephole connections but gives a total parameter count exactly equal to the no-peephole checkpoint.

### VERDICT

The current thesis code creates trainable zero-initialized peephole parameters and passes them to Adam, but checkpoint 77000 contains none. The 12,643,945 count exactly matches the checkpoint without peepholes; the provenance of that discrepancy is NOT FOUND.

---

## 6. Event Candidates

### 6.1 Method

The archive was streamed one frame at a time. No full 9.36 GB uncompressed array was loaded into RAM.

For each 12-frame window:

- Frames 0–5 were treated as input.
- Frames 6–11 were treated as target.
- Window stride: 1.
- Candidate windows were selected with a minimum separation of 24 frames.
- Heavy-pixel counts were computed under two decoding interpretations.

#### Interpretation A: archive values are `x = dBZ/70`

For the thesis evaluator’s 10 mm/h physical threshold:

```text
dBZ = 33.27378524114181
x_threshold = 0.4753397891591687
```

#### Interpretation B: archive values are `x = (dBZ+10)/70`

The evaluator threshold is used directly:

```text
x_threshold = 0.6181969320163115
```

Archive timestamps are unavailable, so every timestamp is reported as:

```text
NOT FOUND
```

The archive also has no per-frame metadata allowing independent verification that all 12 frames in each candidate window are 10±2 minutes apart. Therefore spacing verification is:

```text
NOT FOUND
```

### 6.2 Top 15 windows: Interpretation A — `x=dBZ/70`

The heavy fraction is:

```text
heavy pixels / (6 * 512 * 512)
```

| Rank | Start index | Heavy target pixels | Heavy fraction | Timestamp | 12-frame spacing |
|---:|---:|---:|---:|---|---|
| 1 | 3648 | 264,769 | 0.1683355967203776 | NOT FOUND | NOT FOUND |
| 2 | 2915 | 230,313 | 0.14642906188964844 | NOT FOUND | NOT FOUND |
| 3 | 3726 | 151,089 | 0.09605979995727539 | NOT FOUND | NOT FOUND |
| 4 | 3795 | 142,244 | 0.09043629964192708 | NOT FOUND | NOT FOUND |
| 5 | 3912 | 101,249 | 0.06437238057454427 | NOT FOUND | NOT FOUND |
| 6 | 3771 | 97,012 | 0.061678568522135414 | NOT FOUND | NOT FOUND |
| 7 | 2359 | 95,895 | 0.06096839904785156 | NOT FOUND | NOT FOUND |
| 8 | 3945 | 95,296 | 0.060587565104166664 | NOT FOUND | NOT FOUND |
| 9 | 3361 | 95,004 | 0.06040191650390625 | NOT FOUND | NOT FOUND |
| 10 | 1213 | 86,726 | 0.05513890584309896 | NOT FOUND | NOT FOUND |
| 11 | 1074 | 79,257 | 0.05039024353027344 | NOT FOUND | NOT FOUND |
| 12 | 4352 | 77,671 | 0.04938189188639323 | NOT FOUND | NOT FOUND |
| 13 | 4058 | 76,797 | 0.04882621765136719 | NOT FOUND | NOT FOUND |
| 14 | 1048 | 73,322 | 0.04661687215169271 | NOT FOUND | NOT FOUND |
| 15 | 3672 | 71,653 | 0.04555575052897135 | NOT FOUND | NOT FOUND |

### 6.3 Top 15 windows: Interpretation B — `x=(dBZ+10)/70`

| Rank | Start index | Heavy target pixels | Heavy fraction | Timestamp | 12-frame spacing |
|---:|---:|---:|---:|---|---|
| 1 | 3647 | 112,979 | 0.07183011372884114 | NOT FOUND | NOT FOUND |
| 2 | 2905 | 66,107 | 0.04202969868977865 | NOT FOUND | NOT FOUND |
| 3 | 3361 | 53,261 | 0.03386243184407552 | NOT FOUND | NOT FOUND |
| 4 | 3716 | 51,121 | 0.0325018564860026 | NOT FOUND | NOT FOUND |
| 5 | 4351 | 43,488 | 0.02764892578125 | NOT FOUND | NOT FOUND |
| 6 | 2342 | 41,321 | 0.02627118428548177 | NOT FOUND | NOT FOUND |
| 7 | 3794 | 39,596 | 0.025174458821614582 | NOT FOUND | NOT FOUND |
| 8 | 4059 | 36,513 | 0.023214340209960938 | NOT FOUND | NOT FOUND |
| 9 | 1183 | 36,400 | 0.023142496744791668 | NOT FOUND | NOT FOUND |
| 10 | 3929 | 36,375 | 0.023126602172851562 | NOT FOUND | NOT FOUND |
| 11 | 2494 | 36,045 | 0.022916793823242188 | NOT FOUND | NOT FOUND |
| 12 | 3770 | 35,386 | 0.022497812906901043 | NOT FOUND | NOT FOUND |
| 13 | 3623 | 33,931 | 0.02157274881998698 | NOT FOUND | NOT FOUND |
| 14 | 3746 | 33,824 | 0.021504720052083332 | NOT FOUND | NOT FOUND |
| 15 | 2270 | 32,285 | 0.02052625020345052 | NOT FOUND | NOT FOUND |

The two interpretations produce materially different event rankings and heavy-pixel counts. For example:

```text
Top window under x=dBZ/70:
    start 3648
    heavy count 264,769
    fraction 0.1683355967203776

Top window under x=(dBZ+10)/70:
    start 3647
    heavy count 112,979
    fraction 0.07183011372884114
```

These should not be treated as equivalent event definitions.

### VERDICT

The archive supports two materially different heavy-rain rankings depending on normalization. Exact event timestamps and verified 10-minute spacing are NOT FOUND because the archive contains no timing metadata and cannot be aligned to the incomplete raw inventory.

---

# RECOMMENDED CONTRACT

## Value scale

The current evidence requires an explicit contract rather than an implicit assumption.

### Safest contract for compatibility with the current thesis evaluator

```text
event array:
    shape [12, 512, 512, 2]
    dtype float32

channel 0:
    reflectivity input
    normalized as x = (dBZ + 10) / 70
    clipped to [0,1]

channel 1:
    binary ancillary channel, currently observed as only 0.0 or 1.0
    exact semantic meaning NOT FOUND
```

However, this contract conflicts with the documentation stating that Nha Be arrays may use:

```text
x = dBZ / 70
```

Therefore a production contract should include an explicit metadata field such as:

```text
normalization = "dbz_plus_10_over_70"
```

or:

```text
normalization = "dbz_over_70"
```

It should not infer the convention from the numeric range alone.

## Threshold constant

If using the current thesis evaluator and `a=58.53`, `b=1.56`:

```text
10 mm/h normalized threshold:
    0.6181969320163115
```

That threshold is correct only when:

```text
x = (dBZ + 10) / 70
```

If the archive uses:

```text
x = dBZ / 70
```

then the equivalent threshold is:

```text
0.4753397891591687
```

## Channel

The model must consume:

```text
channel 0 only
```

This is directly verified in:

- `experiments/convLSTM_balacned_mse_mae/main.py:145-147`
- `plot_case_study.py:106-110`

Channel one should not be used as reflectivity. It is binary in the archive, but its exact meaning remains unknown.

## Grid

The model expects:

```text
512×512
```

The exact raw-to-512 crop, interpolation, or reprojection is:

```text
NOT FOUND
```

An event file should therefore already contain 512×512 frames. No padding or resize rule can be recommended as verified behavior.

## Event timing

The event file should include an explicit start time:

```text
startTime: ISO-8601 UTC timestamp
```

The archive itself does not contain this information. It cannot be reconstructed reliably from archive index alone.

A complete event contract should include:

```text
startTime
frameIntervalMinutes = 10
timezone = UTC
```

and ideally per-frame timestamps if source files may contain gaps.

# STILL UNKNOWN

1. Whether the monthly archive uses `dBZ/70` or `(dBZ+10)/70`.
2. Exact semantic meaning of archive channel one.
3. The preprocessing code that created `radar_sequence.npy`.
4. The exact raw-to-512 spatial transformation.
5. Which raw product or elevation was used to create each archive channel.
6. Exact month-wide raw file counts inside the `.rar` archives.
7. Archive index-to-timestamp mapping.
8. UTC/local timestamps for archive indices 3641–3656.
9. Whether the 77000 checkpoint was trained from the current peephole source.
10. Why the current source declares peepholes while the checkpoint contains none.
11. Whether peepholes were omitted during model construction, omitted during export, or came from a separate no-peephole implementation.
12. Whether the archive’s 4,462 frames correspond to a month with two missing observations or a different selection rule.
13. Whether channel one is a valid-data mask, quality flag, or another radar product.
14. Whether the raw PPI `DBZ` field and archive channel zero can be numerically aligned after locating the missing preprocessing pipeline.