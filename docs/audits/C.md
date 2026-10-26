Read skill `raincast-dev`

Ask User
Completed with input: {
  "question": "What is the exact absolute Windows path to the downloaded `nhb_2023_05.npz` archive?",
  "choices": [
    "It is in E:\\PrecipitationNowcasting\\data",
    "It is in E:\\Project\\raincast\\data",
    "I will provide a different absolute path"
  ]
}

I will inspect the supplied location read-only, identify the exact archive file, and first measure available RAM before loading anything.

Ran terminal command: $p='E:\PrecipitationNowcasting\NhaBe-npz'; Write-Output 'RAM:'; Get-CimInstance Win32_OperatingSystem | Select-Object @{Name='FreePhysicalMemoryKiB';Expression={$_.FreePhysicalMemory}},@{Name='TotalVisibleMemorySizeKiB';Expression={$_.TotalVisibleMemorySize}} | Format-List; Write-Output 'FILES:'; Get-ChildItem -LiteralPath $p -Force -File | Select-Object FullName,Length,LastWriteTimeUtc

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\Project\\raincast\\docs\\PROJECT.md",
  "view_range": [
    1,
    180
  ]
}

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\Project\\raincast\\docs\\RULES.md",
  "view_range": [
    1,
    180
  ]
}

The supplied folder contains the requested `nhb_2023_05.npz`; free physical RAM is `2,229,432 KiB` (~2.13 GiB) out of `16,097,532 KiB`. I will now inspect the archive metadata and the exact thesis membership/loader code before running window and model calculations.

Read , lines 1 to 220
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\config.py",
  "view_range": [
    1,
    220
  ]
}

Read , lines 1 to 210
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\experiments\\convLSTM_balacned_mse_mae\\main.py",
  "view_range": [
    1,
    210
  ]
}

Read , lines 1 to 210
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\evaluator.py",
  "view_range": [
    1,
    210
  ]
}

"Read" failed
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\npz_dataset.py",
  "view_range": [
    1,
    180
  ]
}
Tool execution failed: Path does not exist

Read , lines 1 to 180
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\convert_npz_to_npy.py",
  "view_range": [
    1,
    180
  ]
}

Read , lines 1 to 220
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\docs\\guide.md",
  "view_range": [
    1,
    220
  ]
}

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\npz_dataset.py'; if(Test-Path $f){$n=0;Get-Content $f|%{$n++;'{0}: {1}'-f $n,$_}} else {Get-ChildItem 'E:\PrecipitationNowcasting\ConvLSMT' -Recurse -File -Filter '*npz*dataset*'|Select-Object FullName}

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\experiments\convLSTM_balacned_mse_mae\main.py'; Select-String -Path $f -Pattern 'build_npz_loaders|TEST_GLOB|split_npz_files|list_npz_files|checkpoint|save' -Context 2,5

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\nowcasting\evaluator.py'; Select-String -Path $f -Pattern 'test_glob|NPZ_TEST_GLOB|list_npz_files|clamp|mask|threshold' -Context 2,4

Ran terminal command: & 'E:\Project\raincast\.venv\Scripts\python.exe' -c "import zipfile,struct,ast,os; p=r'E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz'; z=zipfile.ZipFile(p); print('members=',z.namelist()); print('archive_bytes=',os.path.getsize(p)); [print(n, z.getinfo(n).file_size) for n in z.namelist()];\nfor n in z.namelist():\n b=z.open(n).read(512); print('header',n, b[:200])"
Tool execution failed with exit code 1

Ran terminal command: $scratch='C:\Users\Admin.000\raincast-archive-audit-20261013'; New-Item -ItemType Directory -Force $scratch | Out-Null; @'
import zipfile, os
p=r'E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz'
z=zipfile.ZipFile(p)
print('members=', z.namelist())
print('archive_bytes=', os.path.getsize(p))
for n in z.namelist():
    info=z.getinfo(n)
    b=z.open(n).read(512)
    print('member', n, 'compressed=', info.compress_size, 'uncompressed=', info.file_size)
    print('header_bytes=', repr(b[:256]))
'@ | Set-Content -Encoding UTF8 (Join-Path $scratch 'inspect_archive.py'); & 'E:\Project\raincast\.venv\Scripts\python.exe' (Join-Path $scratch 'inspect_archive.py')

The archive contains one member, `radar_sequence.npy`, with shape `(4462, 512, 512, 2)`, `float32`, and an uncompressed array size of `9,357,492,352` bytes. It cannot be loaded wholly with the available ~2.13 GiB free RAM, so I will stream one frame at a time and retain only rolling 12-frame windows plus the top candidates in scratch.

Ran terminal command: $scratch='C:\Users\Admin.000\raincast-archive-audit-20261013'; @'
import os, zipfile, numpy as np, heapq, json, time
p=r'E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz'
out=os.path.join(os.path.dirname(__file__),'scan_results.npz')
shape=(4462,512,512,2); dtype=np.dtype('<f4'); frame_bytes=np.prod(shape[1:])*dtype.itemsize
# retain top candidates under each Z-R relation; ranking is total heavy target pixels
zrs=[('61.75/1.61',61.75,1.61),('58.53/1.56',58.53,1.56)]
heaps={k:[] for k,_,_ in zrs}; samples={}; channel_stats=[]; nan_per=[]; zero_per=[]; first=[]
start=time.time()
with zipfile.ZipFile(p) as z:
    with z.open('radar_sequence.npy') as f:
        header=f.read(128)
        if not header.startswith(b'\x93NUMPY'): raise RuntimeError(header)
        # data begins at byte 128 for this v1 header
        rolling=[]
        for i in range(shape[0]):
            b=f.read(frame_bytes)
            if len(b)!=frame_bytes: raise EOFError((i,len(b),frame_bytes))
            a=np.frombuffer(b,dtype=dtype).reshape(shape[1:])
            if i<3: first.append({'i':i,'ch0_min':float(np.nanmin(a[...,0])),'ch0_max':float(np.nanmax(a[...,0])),'ch1_min':float(np.nanmin(a[...,1])),'ch1_max':float(np.nanmax(a[...,1])),'ch0_mean':float(np.nanmean(a[...,0])),'ch1_mean':float(np.nanmean(a[...,1]))})
            if i==0: channel_stats=[{'min':float('inf'),'max':float('-inf'),'nan':0,'gt1':0,'lt0':0,'zero':0,'n':0} for _ in range(2)]
            for c in range(2):
                x=a[...,c]; s=channel_stats[c]; s['min']=min(s['min'],float(np.nanmin(x))); s['max']=max(s['max'],float(np.nanmax(x))); s['nan']+=int(np.isnan(x).sum()); s['gt1']+=int((x>1).sum()); s['lt0']+=int((x<0).sum()); s['zero']+=int((x==0).sum()); s['n']+=x.size
            rolling.append(a.copy())
            if len(rolling)>12: rolling.pop(0)
            if len(rolling)==12:
                seq=np.stack(rolling,axis=0) # 12,H,W,2
                x=seq[:6,...,0]
                target=seq[6:,...,0]
                invalid=int(np.isnan(target).sum())
                for label,A,B in zrs:
                    dbz=70*x-10
                    # Explicitly use x as normalized channel 0.
                    rain=(10**(dbz/10.0)/A)**(1.0/B)
                    heavy=np.greater_equal(rain,10.0) & np.isfinite(rain)
                    count=int(heavy.sum())
                    item=(count,i-11,invalid/(6*512*512))
                    h=heaps[label]
                    if len(h)<10: heapq.heappush(h,item)
                    elif item>h[0]: heapq.heapreplace(h,item)
                    if count>=0: samples[(label,i-11)]=seq.copy() if any(item==q for q in h) else samples.get((label,i-11))
print('elapsed_seconds=',round(time.time()-start,2))
print('first_frames=',json.dumps(first))
print('channel_stats=',json.dumps(channel_stats))
print('frame_count=',shape[0], 'frame_bytes=',frame_bytes, 'array_bytes=',int(np.prod(shape)*dtype.itemsize))
for label in heaps:
    print('TOP',label)
    for rank,item in enumerate(sorted(heaps[label],reverse=True),1): print(rank, item)
# second pass save union of top starts, avoiding huge retained dict
starts=sorted(set(v[1] for h in heaps.values() for v in h)); print('selected_starts=',starts)
with zipfile.ZipFile(p) as z:
  with z.open('radar_sequence.npy') as f:
    f.read(128); frames={}
    for i in range(shape[0]):
      b=f.read(frame_bytes)
      if i in set(s+j for s in starts for j in range(12)): frames[i]=np.frombuffer(b,dtype=dtype).reshape(shape[1:]).copy()
np.savez_compressed(out, **{f'start_{s}':np.stack([frames[s+j] for j in range(12)]) for s in starts})
print('saved=',out,'bytes=',os.path.getsize(out))
'@ | Set-Content -Encoding UTF8 (Join-Path $scratch 'scan_archive.py'); & 'E:\Project\raincast\.venv\Scripts\python.exe' (Join-Path $scratch 'scan_archive.py')

The archive scan is still running in the scratch process. It is streaming the 9.36 GB uncompressed array rather than loading it into memory, as required by the available RAM constraint.

`Stream archive statistics and rank heavy-rain windows` completed

Read Terminal
Completed with input: {
  "shellId": "66",
  "delay": 0
}

The streaming scan completed. The archive has no NaNs and both channels are float32 values in `[0,1]`; channel 0 is the thesis loader’s reflectivity channel because the training/evaluation code explicitly keeps channel 0. The top heavy-rain windows cluster around indices 3651–3656. I will now run the real RainCast checkpoint on the top three distinct windows and calculate both requested Z–R metric sets without changing source code.

Read , lines 1 to 235
Completed with input: {
  "path": "E:\\Project\\raincast\\services\\inference\\app\\model.py",
  "view_range": [
    1,
    235
  ]
}

Read , lines 120 to 190
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\nowcasting\\evaluator.py",
  "view_range": [
    120,
    190
  ]
}

Read , lines 100 to 170
Completed with input: {
  "path": "E:\\PrecipitationNowcasting\\ConvLSMT\\docs\\guide.md",
  "view_range": [
    100,
    170
  ]
}

Ran terminal command: $repo='E:\PrecipitationNowcasting\ConvLSMT'; git -C $repo status --short --branch; Write-Output 'local nc files:'; Get-ChildItem 'E:\PrecipitationNowcasting\ConvLSMT' -Recurse -File -Filter '*.nc' -ErrorAction SilentlyContinue | Select-Object FullName; Write-Output 'local monthly npy/npz:'; Get-ChildItem 'E:\PrecipitationNowcasting\ConvLSMT' -Recurse -File -Include 'nhb_*.npy','nhb_*.npz' -ErrorAction SilentlyContinue | Select-Object FullName

Ran terminal command: $scratch='C:\Users\Admin.000\raincast-archive-audit-20261013'; @'
import os, sys, json, time, numpy as np, torch
sys.path.insert(0,r'E:\Project\raincast\services\inference\app')
from model import build_model
archive=np.load(os.path.join(os.path.dirname(__file__),'scan_results.npz'))
starts=[3653,3654,3652]
checkpoint=r'E:\PrecipitationNowcasting\ConvLSMT\outputs\encoder_forecaster_77000.pth'
model=build_model().cpu()
state=torch.load(checkpoint,map_location='cpu',weights_only=False)
print('load_result=',model.load_state_dict(state,strict=True))
model.eval()

def threshold(x,A,B):
    dbz=70.0*x-10.0
    return (10.0**(dbz/10.0)/A)**(1.0/B)>=10.0

def scores(pred,truth,A,B):
    out=[]
    for t in range(6):
        p=threshold(pred[t],A,B); y=threshold(truth[t],A,B)
        h=int(np.logical_and(p,y).sum()); m=int(np.logical_and(~p,y).sum()); f=int(np.logical_and(p,~y).sum())
        def div(a,b): return None if b==0 else a/b
        out.append({'H':h,'M':m,'F':f,'CSI':div(h,h+m+f),'POD':div(h,h+m),'FAR':div(f,h+f),'BIAS':div(h+f,h+m)})
    return out
for s in starts:
    seq=archive[f'start_{s}'][:,:,0].astype(np.float32)
    x=torch.from_numpy(seq[:6,None,:, :])[:,None,:,:,:] # T,B,C,H,W
    with torch.no_grad(): raw=model(x).squeeze(1).squeeze(1).numpy()
    pred=np.clip(raw,0,1); truth=seq[6:]
    persistence=np.repeat(seq[5:6],6,axis=0)
    print('SAMPLE_START',s,'input_min',float(np.nanmin(seq[:6])),'input_max',float(np.nanmax(seq[:6])),'raw_min',float(raw.min()),'raw_max',float(raw.max()),'raw_mean',float(raw.mean()))
    print('ZR_61.75_1.61=',json.dumps(scores(pred,truth,61.75,1.61),separators=(',',':')))
    print('ZR_58.53_1.56=',json.dumps(scores(pred,truth,58.53,1.56),separators=(',',':')))
    print('PERSIST_61.75_1.61=',json.dumps(scores(np.clip(persistence,0,1),truth,61.75,1.61),separators=(',',':')))
    print('PERSIST_58.53_1.56=',json.dumps(scores(np.clip(persistence,0,1),truth,58.53,1.56),separators=(',',':')))
'@ | Set-Content -Encoding UTF8 (Join-Path $scratch 'real_forward.py'); & 'E:\Project\raincast\.venv\Scripts\python.exe' (Join-Path $scratch 'real_forward.py')
Tool execution failed with exit code 1

Ran terminal command: $f='C:\Users\Admin.000\raincast-archive-audit-20261013\real_forward.py'; (Get-Content $f -Raw).Replace("seq=archive[f'start_{s}'][:,:,0].astype(np.float32)","seq=archive[f'start_{s}'][... ,0].astype(np.float32)") | Set-Content -Encoding UTF8 $f; & 'E:\Project\raincast\.venv\Scripts\python.exe' $f

Ran terminal command: $scratch='C:\Users\Admin.000\raincast-archive-audit-20261013'; @'
import zipfile, numpy as np, time, json, os
p=r'E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz'; shape=(4462,512,512,2); fb=512*512*2*4
zs=[('61.75/1.61',61.75,1.61),('58.53/1.56',58.53,1.56)]
zero_frame=np.zeros((2,shape[0]),dtype=np.int64); sample_zero=[]; totals={z:[0,0] for z,_,_ in zs}; nwin=0; roll=[]; t=time.time()
with zipfile.ZipFile(p) as z:
 with z.open('radar_sequence.npy') as f:
  f.read(128)
  for i in range(shape[0]):
   b=f.read(fb); a=np.frombuffer(b,dtype='<f4').reshape(512,512,2)
   for c in range(2): zero_frame[c,i]=int((a[...,c]==0).sum())
   roll.append(a[...,0].copy())
   if len(roll)>12: roll.pop(0)
   if len(roll)==12 and ((i-11)%6==0):
    nwin+=1; y=np.stack(roll[6:])
    for name,A,B in zs:
     r=(10**((70*y-10)/10)/A)**(1/B); cnt=int((r>=10).sum()); totals[name][0]+=int(cnt==0); totals[name][1]+=cnt
    
print('elapsed_seconds=',round(time.time()-t,2)); print('stride=6 windows=',nwin)
for name in totals: print('zero_fraction',name,totals[name][0], '/',nwin, '=',totals[name][0]/nwin, 'mean_heavy_count=',totals[name][1]/nwin)
for c in range(2): print('channel',c,'zero_count_per_frame_min=',int(zero_frame[c].min()),'max=',int(zero_frame[c].max()),'mean=',float(zero_frame[c].mean()),'first3=',zero_frame[c,:3].tolist(),'last3=',zero_frame[c,-3:].tolist())
'@ | Set-Content -Encoding UTF8 (Join-Path $scratch 'scan_zero_windows.py'); & 'E:\Project\raincast\.venv\Scripts\python.exe' (Join-Path $scratch 'scan_zero_windows.py')

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\experiments\convLSTM_balacned_mse_mae\main.py'; $n=0;Get-Content $f|%{$n++;if($n -ge 40 -and $n -le 85){'{0}: {1}'-f $n,$_}}

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\nowcasting\config.py'; $n=0;Get-Content $f|%{$n++;if($n -ge 35 -and $n -le 72){'{0}: {1}'-f $n,$_}}

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\npz_dataset.py'; $n=0;Get-Content $f|%{$n++;if($n -ge 14 -and $n -le 115){'{0}: {1}'-f $n,$_}}

Ran terminal command: $p='E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526'; $files=Get-ChildItem -LiteralPath $p -File -Filter '*.nc'; 'nc_count='+$files.Count; $files|Select-Object -First 1 -ExpandProperty Name; $files|Select-Object -Last 1 -ExpandProperty Name

The code evidence shows two possible split modes: explicit environment glob overrides, or a default chronological-by-sorted-file fallback with the latest 20% validation split. The documentation’s May–June 2023 test statement is therefore conditional on those environment variables having been set during training; the checkpoint itself does not record them.

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\nowcasting\evaluator.py'; $n=0;Get-Content $f|%{$n++;if($n -ge 40 -and $n -le 115){'{0}: {1}'-f $n,$_}}

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\docs\guide.md'; $n=0;Get-Content $f|%{$n++;if($n -ge 90 -and $n -le 155){'{0}: {1}'-f $n,$_}}

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\convert_npz_to_npy.py'; $n=0;Get-Content $f|%{$n++;if($n -le 55){'{0}: {1}'-f $n,$_}}

Ran terminal command: $f='E:\PrecipitationNowcasting\ConvLSMT\nowcasting\evaluator.py'; Select-String -Path $f -Pattern 'def main|test_glob|NPZ_TEST_GLOB|add_argument' -Context 1,3

Read Terminal
Completed with input: {
  "shellId": "70",
  "delay": 600
}

# RainCast Archive Audit: `nhb_2023_05.npz`

## Scope and method

The supplied folder was:

```text
E:\PrecipitationNowcasting\NhaBe-npz
```

The requested archive was found at:

```text
E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz
```

No files in the thesis repository, RainCast repository, or data folder were modified. Scripts and extracted result files were written only under:

```text
C:\Users\Admin.000\raincast-archive-audit-20261013
```

The archive contains approximately 9.36 GB of uncompressed array data, while the measured free RAM was approximately 2.13 GiB. Therefore, the archive was processed frame-by-frame from the ZIP member rather than loaded fully into memory.

---

## 1. Archive inspection

### 1.1 Available memory

Real command output:

```text
FreePhysicalMemoryKiB     : 2229432
TotalVisibleMemorySizeKiB : 16097532
```

This is approximately:

- Free RAM: `2.13 GiB`
- Total visible RAM: `15.35 GiB`

### 1.2 Archive keys and array structure

Real archive inspection output:

```text
members= ['radar_sequence.npy']
archive_bytes= 589351790
member radar_sequence.npy compressed= 589351616 uncompressed= 9357492352
header_bytes= b"\x93NUMPY\x01\x00v\x00{'descr': '<f4', 'fortran_order': False, 'shape': (4462, 512, 512, 2), } ... "
```

The archive contains exactly one key/member:

| Key/member | Shape | Dtype |
|---|---:|---|
| `radar_sequence.npy` | `(4462, 512, 512, 2)` | little-endian `float32` |

The archive therefore contains:

- `4,462` frames
- `512 × 512` spatial pixels
- `2` channels per frame

The training loader’s documented input format is `[T,H,W,C]`, and the loader later moves channels to `[T,C,H,W]` in `npz_dataset.py`, lines 102–106.

### 1.3 Disk size versus array size

| Quantity | Bytes | Approximate size |
|---|---:|---:|
| `.npz` file on disk | `589,351,790` | `561.99 MiB` |
| ZIP member including NPY header | `9,357,492,352` | `8.72 GiB` |
| Array payload in memory | `9,357,492,224` | `8.72 GiB` |

The 128-byte difference between the member and array payload is the NPY header.

The archive is compressed by approximately 15.9:1 relative to the raw array payload.

### 1.4 Numeric statistics

The full archive was streamed frame-by-frame. Aggregate results:

```text
frame_count= 4462
frame_bytes= 2097152
array_bytes= 9357492224
```

#### Channel 0

```text
min=0.0
max=1.0
nan=0
gt1=0
lt0=0
zero=1038932151
n=1169686528
```

#### Channel 1

```text
min=0.0
max=1.0
nan=0
gt1=0
lt0=0
zero=1032812473
n=1169686528
```

| Channel | Minimum | Maximum | NaNs | `>1.0` | `<0` | Exactly zero |
|---|---:|---:|---:|---:|---:|---:|
| 0 | `0.0` | `1.0` | `0` | `0` | `0` | `1,038,932,151` |
| 1 | `0.0` | `1.0` | `0` | `0` | `0` | `1,032,812,473` |

Each channel contains:

```text
1169686528 values
```

Because the dtype is `float32`, the uint8-specific count of exactly `255` is not applicable. The measured maximum is `1.0`, so there are no values equal to numeric `255`.

### 1.5 Interpretation

The values look like normalized data in `[0,1]`, not raw dBZ and not uint8 pixels, because:

1. The NPY header reports `float32`.
2. Both channels have minimum `0.0` and maximum `1.0`.
3. There are no values below `0` or above `1`.
4. The thesis loader normalizes values only when `np.nanmax(sequence) > 1.0`, as shown in `npz_dataset.py`, lines 108–111.
5. The RainCast project contract defines normalized reflectivity as:

   ```text
   x = (clip(dBZ, -10, 60) + 10) / 70
   ```

The archive’s exact channel semantics are not encoded in the archive itself. However, the thesis training and evaluation code explicitly selects channel 0 as reflectivity:

```python
inputs = inputs[:, :, 0:1, :, :]
targets = targets[:, :, 0:1, :, :]
```

in [`evaluator.py`](), lines 111–113, and the same logic appears in the training script.

For the model runs below, channel 0 was therefore used.

**VERDICT:** The archive contains one compressed `float32` array of shape `(4462,512,512,2)`, with both channels already bounded in `[0,1]`; channel 0 was used as reflectivity because the thesis code explicitly selects it.

---

## 2. Time and frame correspondence

### 2.1 Archive timestamps and metadata

The archive contains only:

```text
radar_sequence.npy
```

The NPY header contains only:

```text
dtype, fortran_order, shape
```

No timestamp array, datetime field, JSON metadata, or per-frame filename information was found.

Therefore:

```text
timestamps: NOT FOUND
per-frame metadata: NOT FOUND
```

The filename `nhb_2023_05.npz` identifies the nominal month, but does not identify the timestamp of frame index 0.

### 2.2 Expected number of ten-minute frames

May 2023 has 31 days.

At one frame every 10 minutes:

```text
31 × 24 × 6 = 4464 frames
```

The archive contains:

```text
4462 frames
```

Difference:

```text
4464 - 4462 = 2 frames
```

This indicates that the archive has two fewer frames than a complete uninterrupted 10-minute May sequence. The missing positions cannot be identified from the archive because timestamps are absent.

### 2.3 Locally available NetCDF data

The thesis repository contains one local NetCDF day:

```text
E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526
```

Real command output:

```text
nc_count=144
NHB_PPI_20230526_000303.nc
NHB_PPI_20230526_235304.nc
```

This is exactly one day of 144 ten-minute frames. The filenames include timestamps such as:

```text
NHB_PPI_20230526_000303.nc
NHB_PPI_20230526_235304.nc
```

However, there is no verified mapping between those local filenames and the archive’s frame indices.

### 2.4 Can archive index be mapped to time?

Not verified.

A possible assumption would be:

```text
archive index 0 = 2023-05-01 00:00
```

but the archive has 4,462 rather than 4,464 frames, and no timestamp metadata proves the starting offset or identifies the two missing frames.

The available evidence only supports:

- The archive is nominally May 2023 based on its filename.
- The frames appear intended to be sequential.
- Local filenames provide timestamp evidence only for the separate 2023-05-26 NetCDF files.
- No archive index-to-timestamp mapping is present.

**VERDICT:** The archive has 4,462 frames instead of the expected 4,464 ten-minute May frames, but exact index-to-time mapping is NOT FOUND and cannot be verified from this archive.

---

## 3. Train/validation/test membership

## 3.1 Configuration defaults

[`config.py`](), lines 53–65, defines:

```python
__C.NPZ.DATA_DIR = ...
__C.NPZ.TRAIN_GLOB = os.environ.get('NPZ_TRAIN_GLOB', '')
__C.NPZ.VALID_GLOB = os.environ.get('NPZ_VALID_GLOB', '')
__C.NPZ.TEST_GLOB = os.environ.get('NPZ_TEST_GLOB', '')
__C.NPZ.INPUT_LEN = 6
__C.NPZ.TARGET_LEN = 6
__C.NPZ.STRIDE = int(os.environ.get('NPZ_STRIDE', '1'))
__C.NPZ.VALID_RATIO = float(os.environ.get('NPZ_VALID_RATIO', '0.2'))
```

The default window is therefore:

```text
6 input frames + 6 target frames = 12 frames
```

with default stride `1`.

### 3.2 Training split code

[`experiments/convLSTM_balacned_mse_mae/main.py`](), lines 58–73, executes:

```python
if cfg.NPZ.TRAIN_GLOB and cfg.NPZ.VALID_GLOB:
    train_files = expand_npz_patterns(cfg.NPZ.TRAIN_GLOB)
    valid_files = expand_npz_patterns(cfg.NPZ.VALID_GLOB)
else:
    all_files = list_npz_files(cfg.NPZ.DATA_DIR)
    test_files = expand_npz_patterns(cfg.NPZ.TEST_GLOB) if cfg.NPZ.TEST_GLOB else [
        file_path for file_path in all_files
        if "nhb_2022_" in os.path.basename(file_path)
    ]
    if test_files and len(test_files) < len(all_files):
        all_files = [file_path for file_path in all_files
                     if file_path not in set(test_files)]
    train_files, valid_files = split_npz_files(
        all_files,
        valid_ratio=cfg.NPZ.VALID_RATIO,
    )
```

This yields two different possible behaviors.

### 3.3 Explicit split documented in `docs/guide.md`

[`docs/guide.md`](), lines 141–146, documents these environment variables:

```bash
NPZ_TRAIN_GLOB=
  nhb_2021_*.npy
  nhb_2022_01.npy ... nhb_2022_11.npy

NPZ_VALID_GLOB=
  nhb_2022_12.npy
  nhb_2023_01.npy
  nhb_2023_02.npy
  nhb_2023_03.npy

NPZ_TEST_GLOB=
  nhb_2023_05.npy
  nhb_2023_06.npy
```

The documented chronological split is:

| Split | Documented files |
|---|---|
| Train | `nhb_2021_*.npy` and `nhb_2022_01.npy` through `nhb_2022_11.npy` |
| Validation | `nhb_2022_12.npy`, `nhb_2023_01.npy`, `nhb_2023_02.npy`, `nhb_2023_03.npy` |
| Test | `nhb_2023_05.npy`, `nhb_2023_06.npy` |

April 2023 is described in the guide as a buffer month and is not included in the explicit lists.

Under this documented configuration, `nhb_2023_05` is held out for test.

### 3.4 Default split behavior

If `NPZ_TRAIN_GLOB` and `NPZ_VALID_GLOB` are empty:

1. The code lists all `.npy` files in `NPZ_DATA_DIR`.
2. It excludes files matching `nhb_2022_` as a default test exclusion.
3. It sorts the remaining files.
4. It uses the latest 20% of those files for validation.
5. It uses the earlier 80% for training.

The split helper is [`split_npz_files`](), lines 143–153:

```python
files = sorted(...)
valid_count = max(min_valid_files, int(round(len(files) * valid_ratio)))
return files[:-valid_count], files[-valid_count:]
```

This default branch does **not** itself guarantee that May 2023 is test. May 2023 would be included in the available files unless explicit test/training environment variables changed the behavior.

### 3.5 Evaluation fallback

[`nowcasting/evaluator.py`](), lines 355–363, has a separate fallback:

```python
if not test_glob:
    test_glob = (
        f"{cfg.NPZ.DATA_DIR}/nhb_2023_05.npy "
        f"{cfg.NPZ.DATA_DIR}/nhb_2023_06.npy "
    )
```

Thus, evaluation defaults to May–June 2023 if no test glob is supplied.

This evaluator fallback does not prove that the checkpoint was trained with the same split. It only proves what the current evaluator would use.

### 3.6 Does the downloaded month belong to test?

Evidence-based conclusion:

- **According to `docs/guide.md` and the evaluator fallback:** yes, May 2023 is held out for test.
- **According to the training code alone:** not guaranteed, because the code can use environment-variable globs or the default 20% split.
- **For checkpoint `encoder_forecaster_77000.pth`:** the actual environment variables used during training are not embedded in the checkpoint.

Therefore the exact checkpoint membership is:

```text
NOT VERIFIED
```

**VERDICT:** The documented/evaluator split treats `nhb_2023_05` as test, but the checkpoint’s actual train/validation/test environment is not recorded, so its membership cannot be proven from the checkpoint alone.

---

## 4. NaN and invalid-pixel handling

### 4.1 Archive NaNs and range violations

Full streamed scan:

| Channel | NaNs | Values `<0` | Values `>1` |
|---|---:|---:|---:|
| 0 | `0` | `0` | `0` |
| 1 | `0` | `0` | `0` |

The archive contains no NaN values.

### 4.2 Zero-value counts

Aggregate exactly-zero counts:

| Channel | Exactly-zero values | Total values | Fraction |
|---|---:|---:|---:|
| 0 | `1,038,932,151` | `1,169,686,528` | approximately `88.82%` |
| 1 | `1,032,812,473` | `1,169,686,528` | approximately `88.30%` |

The per-frame zero-count scan reported:

```text
channel 0 zero_count_per_frame_min=167404 max=261319 mean=232840.015912147
first3=[249923, 250594, 250132]
last3=[257209, 256896, 256546]

channel 1 zero_count_per_frame_min=166998 max=260486 mean=231468.50582698343
first3=[248246, 248987, 248324]
last3=[256308, 255883, 255582]
```

Zeros occur in every frame and occupy a large part of the grid. They are spatially distributed background-like values rather than a single isolated scalar fill value based on the observed per-frame counts. However, the archive has no validity mask or metadata proving that zero means invalid rather than no reflectivity/background.

Therefore:

```text
zero semantics: NOT VERIFIED
```

The value `255` is not present as a uint8 fill value because this archive is float32 and has maximum value `1.0`.

### 4.3 Thesis loader behavior

[`npz_dataset.py`](), lines 102–115, performs:

```python
sequence = np.asarray(sequence, dtype=np.float32)
...
if self.normalize and np.nanmax(sequence) > 1.0:
    sequence = sequence / self.max_dbz
if self.clip:
    sequence = np.clip(sequence, 0.0, 1.0)
```

This means:

- It converts to float32.
- It conditionally divides by `70.0` if the maximum exceeds `1.0`.
- It clips to `[0,1]`.
- It does not call `nan_to_num`.
- It does not call `fillna`.
- It does not load a source validity mask.
- NaNs would not be removed by `np.clip`; they would remain NaN.

The training and evaluator code creates an all-ones mask:

```python
mask = torch.ones_like(targets, dtype=torch.float32, device=...)
```

The evaluator code does this at [`evaluator.py`](), line 114.

No evidence was found that NaNs were filled or masked during the active NPY training path.

### 4.4 Conclusion

For this archive specifically:

- NaNs are absent.
- Values are already normalized.
- No explicit invalid mask is present.
- Many exact zeros exist, but their semantic meaning is unknown.
- The loader would preserve NaNs if they existed.
- The evaluator uses an all-ones mask.

**VERDICT:** No NaN filling or invalid-pixel masking is evidenced in the loader; this archive itself contains no NaNs, but the semantic status of its many zero-valued pixels is NOT FOUND.

---

## 5. Twelve-frame windows and heavy-rain candidates

### 5.1 Window assumptions

The analysis used:

- Channel 0.
- Native archive size: `512 × 512`.
- Twelve-frame windows:
  - Frames `start` through `start+5`: six inputs.
  - Frames `start+6` through `start+11`: six targets.
- Consecutive frames were assumed to be consecutive in time for window construction.
- The archive’s exact timestamps were not available.
- Heavy rain threshold: `R >= 10 mm/h`.
- Decoding assumption:

```text
dBZ = 70*x - 10
```

where `x` is the normalized channel-0 value.

Both requested Z–R relations were evaluated:

```text
R = (10^(dBZ/10) / 61.75)^(1/1.61)
R = (10^(dBZ/10) / 58.53)^(1/1.56)
```

The top-10 ranking scan used stride 1.

### 5.2 Top windows under `61.75 / 1.61`

All reported invalid fractions are zero because the archive contains no NaNs.

| Rank | Start index | Heavy target pixels across six targets | Invalid fraction |
|---:|---:|---:|---:|
| 1 | `3653` | `98,718` | `0.0` |
| 2 | `3654` | `97,804` | `0.0` |
| 3 | `3652` | `96,073` | `0.0` |
| 4 | `3655` | `90,580` | `0.0` |
| 5 | `3651` | `89,350` | `0.0` |
| 6 | `3650` | `80,159` | `0.0` |
| 7 | `3656` | `79,196` | `0.0` |
| 8 | `3641` | `73,190` | `0.0` |
| 9 | `3642` | `72,979` | `0.0` |
| 10 | `3643` | `72,090` | `0.0` |

### 5.3 Top windows under `58.53 / 1.56`

| Rank | Start index | Heavy target pixels across six targets | Invalid fraction |
|---:|---:|---:|---:|
| 1 | `3653` | `112,979` | `0.0` |
| 2 | `3654` | `111,300` | `0.0` |
| 3 | `3652` | `110,382` | `0.0` |
| 4 | `3655` | `103,373` | `0.0` |
| 5 | `3651` | `102,756` | `0.0` |
| 6 | `3650` | `92,029` | `0.0` |
| 7 | `3656` | `90,674` | `0.0` |
| 8 | `3649` | `81,994` | `0.0` |
| 9 | `3642` | `78,468` | `0.0` |
| 10 | `3641` | `78,458` | `0.0` |

### 5.4 Zero-heavy-window fraction

Because a full stride-1 scan is expensive for this 9.36 GB uncompressed stream, a stride-6 scan was also performed for this summary.

Results over `742` stride-6 windows:

```text
zero_fraction 61.75/1.61 0 / 742 = 0.0
zero_fraction 58.53/1.56 0 / 742 = 0.0
```

Therefore, in the measured stride-6 sample:

| Z–R pair | Zero-heavy windows | Total windows | Fraction |
|---|---:|---:|---:|
| `61.75 / 1.61` | `0` | `742` | `0.0` |
| `58.53 / 1.56` | `0` | `742` | `0.0` |

The stride-6 result does not mathematically prove the stride-1 fraction for every possible window, but it shows that all sampled windows contained at least one heavy-rain pixel in the six target frames.

**VERDICT:** Under the stated normalized-data decoding assumption, the strongest windows are starts `3653`, `3654`, and `3652`; all sampled stride-6 windows contained heavy-rain pixels, and all reported invalid fractions were zero.

---

## 6. Real-data RainCast forward and metrics

### 6.1 Model and checkpoint

The run used:

- RainCast [`model.py`]()
- `build_model()`
- Checkpoint:

  ```text
  E:\PrecipitationNowcasting\ConvLSMT\outputs\encoder_forecaster_77000.pth
  ```

- CPU
- `model.eval()`
- `torch.no_grad()`
- Input layout:

  ```text
  [T=6, B=1, C=1, H=512, W=512]
  ```

Checkpoint load output:

```text
load_result= <All keys matched successfully>
```

This confirms state-dictionary compatibility with RainCast’s current model class. It does **not** prove numerical equivalence with the thesis network. The prior equivalence audit found that equivalence to the documented thesis implementation is unverified and that the tested thesis-shaped reconstruction differed substantially.

### 6.2 Raw output ranges before clamping

The input range for each selected window was:

```text
input_min = 0.0
input_max = 1.0
```

RainCast raw outputs before clamping:

| Start index | Raw minimum | Raw maximum | Raw mean |
|---:|---:|---:|---:|
| `3653` | `-1.2767832279205322` | `0.11522473394870758` | `-0.9572809338569641` |
| `3654` | `-1.284783959388733` | `0.11522473394870758` | `-0.9571219086647034` |
| `3652` | `-1.2815696001052856` | `0.11522473394870758` | `-0.9569903016090393` |

The model output is therefore not naturally bounded in `[0,1]`. Metrics below use:

```python
prediction = clip(raw_output, 0.0, 1.0)
```

as required by the thesis evaluator behavior.

The persistence baseline repeats input frame 5 for all six leads and is also clipped to `[0,1]`.

### 6.3 Metrics definition

For each lead:

```text
H = predicted heavy AND observed heavy
M = predicted non-heavy AND observed heavy
F = predicted heavy AND observed non-heavy

CSI  = H / (H + M + F)
POD  = H / (H + M)
FAR  = F / (H + F)
BIAS = (H + F) / (H + M)
```

A zero denominator is reported as `null`.

---

### 6.4 Window start `3653`

#### ConvLSTM, Z–R `61.75 / 1.61`

| Lead | CSI | POD | FAR | BIAS |
|---:|---:|---:|---:|---:|
| 1 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 2 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 3 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 4 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 5 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 6 | `0.000000` | `0.000000` | `null` | `0.000000` |

Raw counts by lead were:

```text
H = 0
F = 0
M = 13052, 10410, 6922, 5837, 6016, 6253
```

#### Persistence, Z–R `61.75 / 1.61`

| Lead | CSI | POD | FAR | BIAS |
|---:|---:|---:|---:|---:|
| 1 | `0.433824` | `0.622816` | `0.411582` | `1.058458` |
| 2 | `0.220096` | `0.419789` | `0.683677` | `1.327089` |
| 3 | `0.111963` | `0.301647` | `0.848860` | `1.995810` |
| 4 | `0.086827` | `0.268974` | `0.886355` | `2.366798` |
| 5 | `0.083129` | `0.252992` | `0.889830` | `2.296376` |
| 6 | `0.062361` | `0.188390` | `0.914730` | `2.209340` |

#### ConvLSTM, Z–R `58.53 / 1.56`

| Lead | CSI | POD | FAR | BIAS |
|---:|---:|---:|---:|---:|
| 1 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 2 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 3 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 4 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 5 | `0.000000` | `0.000000` | `null` | `0.000000` |
| 6 | `0.000000` | `0.000000` | `null` | `0.000000` |

#### Persistence, Z–R `58.53 / 1.56`

| Lead | CSI | POD | FAR | BIAS |
|---:|---:|---:|---:|---:|
| 1 | `0.448350` | `0.637209` | `0.397974` | `1.058440` |
| 2 | `0.252433` | `0.456381` | `0.639028` | `1.264310` |
| 3 | `0.127767` | `0.331481` | `0.827883` | `1.925898` |
| 4 | `0.099104` | `0.295674` | `0.870271` | `2.279158` |
| 5 | `0.089289` | `0.268820` | `0.882070` | `2.279491` |
| 6 | `0.064845` | `0.189292` | `0.910221` | `2.108436` |

**CSI comparison:** ConvLSTM does not beat persistence at any of the six leads under either Z–R pair.

---

### 6.5 Window start `3654`

#### ConvLSTM, Z–R `61.75 / 1.61`

```text
CSI  = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
POD  = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
FAR  = [null, null, null, null, null, null]
BIAS = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
```

#### Persistence, Z–R `61.75 / 1.61`

```text
CSI  = [0.361537, 0.170397, 0.114724, 0.104559, 0.073992, 0.064975]
POD  = [0.598463, 0.420110, 0.333048, 0.300033, 0.212698, 0.183482]
FAR  = [0.522679, 0.777199, 0.851057, 0.861707, 0.898100, 0.908596]
BIAS = [1.253794, 1.885583, 2.236080, 2.169548, 2.087318, 2.007382]
```

#### ConvLSTM, Z–R `58.53 / 1.56`

```text
CSI  = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
POD  = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
FAR  = [null, null, null, null, null, null]
BIAS = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
```

#### Persistence, Z–R `58.53 / 1.56`

```text
CSI  = [0.398811, 0.193413, 0.132308, 0.116782, 0.079674, 0.074818]
POD  = [0.625668, 0.456959, 0.368460, 0.329776, 0.220795, 0.200973]
FAR  = [0.476210, 0.748863, 0.828888, 0.846874, 0.889160, 0.893504]
BIAS = [1.194503, 1.819563, 2.153318, 2.153632, 1.992023, 1.887152]
```

**CSI comparison:** ConvLSTM does not beat persistence at any of the six leads under either Z–R pair.

---

### 6.6 Window start `3652`

#### ConvLSTM, Z–R `61.75 / 1.61`

```text
CSI  = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
POD  = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
FAR  = [null, null, null, null, null, null]
BIAS = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
```

#### Persistence, Z–R `61.75 / 1.61`

```text
CSI  = [0.472671, 0.307628, 0.157081, 0.070428, 0.061230, 0.043727]
POD  = [0.703583, 0.532102, 0.350528, 0.222335, 0.220490, 0.156582]
FAR  = [0.409800, 0.578298, 0.778432, 0.906552, 0.921854, 0.942802]
BIAS = [1.192110, 1.261798, 1.582037, 2.379226, 2.821484, 2.737533]
```

#### ConvLSTM, Z–R `58.53 / 1.56`

```text
CSI  = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
POD  = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
FAR  = [null, null, null, null, null, null]
BIAS = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
```

#### Persistence, Z–R `58.53 / 1.56`

```text
CSI  = [0.483827, 0.317005, 0.184393, 0.084341, 0.068970, 0.047571]
POD  = [0.721303, 0.549515, 0.394276, 0.259355, 0.242765, 0.170881]
FAR  = [0.404931, 0.571686, 0.742726, 0.888901, 0.912125, 0.938154]
BIAS = [1.212133, 1.282970, 1.532512, 2.334445, 2.762643, 2.763046]
```

**CSI comparison:** ConvLSTM does not beat persistence at any of the six leads under either Z–R pair.

### 6.7 Interpretation

The RainCast checkpoint produced negative raw outputs for most pixels:

```text
raw means approximately -0.957
```

After clamping, the model produced no predicted heavy-rain pixels for any of the three selected windows, which resulted in:

```text
CSI = 0
POD = 0
FAR = null
BIAS = 0
```

The persistence baseline produced nonzero heavy-rain detections and outperformed ConvLSTM at every tested lead for all three windows and both Z–R relations.

This is an observation for three selected high-rain windows only. It is not an aggregate test-set score.

**VERDICT:** On the three highest-ranked real-data windows tested, RainCast loaded successfully but predicted no heavy-rain pixels after clamping; persistence outperformed it at every lead under both Z–R pairs. Equivalence between RainCast `model.py` and the thesis training network remains unverified.

---

# RECOMMENDED EVENT FILE CONTRACT

Based only on the archive and code evidence, an event file intended for the current RainCast service should contain:

```text
input:
    shape: (6, 512, 512)
    dtype: float32
    values: normalized [0,1]

target:
    shape: (6, 512, 512)
    dtype: float32
    values: normalized [0,1]
```

The current RainCast project documentation specifies `(6,360,360)` events, while this downloaded archive is `(4462,512,512,2)` and the thesis training configuration uses 512×512. Therefore the spatial contract is not unified between the archive, thesis training pipeline, and RainCast project documentation.

### Required preprocessing

The evidence supports:

```text
x = (clip(dBZ, -10, 60) + 10) / 70
```

If data is already in `[0,1]`, it should not be divided by 70 again.

### Channel handling

The thesis training and evaluator code select channel 0:

```python
inputs = inputs[:, :, 0:1, :, :]
targets = targets[:, :, 0:1, :, :]
```

Therefore an event file for the current single-channel RainCast model should provide a single reflectivity channel after preprocessing.

### NaN and validity handling

The archive contained no NaNs, but the loader does not explicitly fill or mask NaNs.

Recommended evidence-based contract:

```text
No NaNs should be present in input or target arrays.
```

A validity mask is **not currently part of the demonstrated event contract**, and the active training/evaluation path uses an all-ones mask. However, because the archive contains many exact zeros and their semantics are not documented, the need for a real invalid-pixel mask remains unresolved.

### Spatial size

The tested RainCast model accepts both:

```text
512 × 512
360 × 360
```

However:

- The downloaded archive is 512×512.
- The thesis configuration is 512×512.
- The RainCast project event contract documents 360×360.
- The prior equivalence audit found that shape acceptance does not prove model equivalence.
- No padding or resizing should be added without evidence because it changes the model input function.

For this archive, no padding is needed to run RainCast at its native 512×512 size.

### `startTime`

The archive does not contain timestamps. A valid event file for the application should therefore include timestamp metadata separately, for example:

```text
startTime: ISO-8601 timestamp for the first input frame
```

The exact frame timestamp cannot be derived from this archive alone.

---

# STILL UNKNOWN

1. The exact timestamp corresponding to archive frame index `0`.
2. The locations of the two missing frames relative to a complete 4,464-frame May sequence.
3. Whether channel 1 represents a second physical variable, a mask, or another normalized radar product.
4. Whether exact zero means:
   - no reflectivity,
   - background,
   - invalid data,
   - or a preprocessing fill value.
5. Whether a validity mask existed before archive creation.
6. The environment variables used when `encoder_forecaster_77000.pth` was trained.
7. Whether `nhb_2023_05` was definitely held out during the training that produced checkpoint `77000`.
8. Whether the downloaded archive was generated by the same preprocessing pipeline as the thesis checkpoint.
9. Whether the checkpoint’s poor behavior on these windows is caused by:
   - model/checkpoint mismatch,
   - spatial preprocessing# RainCast Monthly Archive Audit

## 1. Archive

### Input and memory constraint

Archive inspected:

- `E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz`

Real RAM measurement before processing:

```text
FreePhysicalMemoryKiB     : 2229432
TotalVisibleMemorySizeKiB : 16097532
```

That is approximately 2.13 GiB free RAM.

The archive was therefore streamed frame-by-frame from scratch code outside both repositories. The full array was not loaded into memory.

### Archive keys and array metadata

The archive contains exactly one key/member:

```text
members= ['radar_sequence.npy']
archive_bytes= 589351790
member radar_sequence.npy compressed= 589351616 uncompressed= 9357492352
header_bytes= ... {'descr': '<f4', 'fortran_order': False, 'shape': (4462, 512, 512, 2), } ...
```

| Key | Shape | Dtype | Array bytes |
|---|---:|---|---:|
| `radar_sequence` | `(4462, 512, 512, 2)` | `float32` | `9,357,492,224` |

The uncompressed `.npy` member including its header is `9,357,492,352` bytes.

| Storage form | Size |
|---|---:|
| `.npz` file on disk | `589,351,790` bytes |
| Uncompressed `.npy` member | `9,357,492,352` bytes |
| Numeric array in memory | `9,357,492,224` bytes |

The archive compression ratio is approximately 15.9:1.

### Per-channel statistics

The complete streamed scan reported:

```text
channel_stats= [
  {
    "min": 0.0,
    "max": 1.0,
    "nan": 0,
    "gt1": 0,
    "lt0": 0,
    "zero": 1038932151,
    "n": 1169686528
  },
  {
    "min": 0.0,
    "max": 1.0,
    "nan": 0,
    "gt1": 0,
    "lt0": 0,
    "zero": 1032812473,
    "n": 1169686528
  }
]
```

| Channel | Min | Max | NaNs | `>1.0` | `<0` | Exactly zero |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | `0.0` | `1.0` | `0` | `0` | `0` | `1,038,932,151` |
| 1 | `0.0` | `1.0` | `0` | `0` | `0` | `1,032,812,473` |

Each channel contains `1,169,686,528` values.

The archive is `float32`, not `uint8`. Therefore, a uint8-specific “exactly 255” interpretation is not applicable. Numerically, there are also no values equal to `255.0`, because the observed maximum is `1.0`.

### Interpretation

The values look like normalized data in `[0,1]`, not raw dBZ and not uint8 pixels:

1. The dtype is `float32`.
2. Both channels have exact global bounds `[0.0, 1.0]`.
3. There are no values outside `[0,1]`.
4. The thesis loader divides by `70.0` only when `np.nanmax(sequence) > 1.0`, at [`npz_dataset.py`](), lines 108–109.
5. The training/evaluation path explicitly selects channel 0 as reflectivity at [`main.py`](), lines 103–114, and `evaluator.py`, lines 100–115.

The archive itself does not contain a metadata field naming the channels. The conclusion that channel 0 is the model input channel is based on the thesis code, not archive metadata.

**VERDICT:** `radar_sequence.npy` contains 4462 frames of two-channel float32 data already bounded in `[0,1]`; it is not raw dBZ or uint8 data. Full in-memory loading is not feasible with the measured free RAM.

---

## 2. Time

### Archive timestamp metadata

The archive contains only:

```text
['radar_sequence.npy']
```

There are no timestamp arrays, datetime fields, JSON metadata members, or per-frame filenames inside the archive.

Therefore:

```text
timestamps: NOT FOUND
metadata: NOT FOUND
index-to-time mapping: NOT VERIFIED
```

The filename `nhb_2023_05.npz` identifies the calendar month at archive level, but not the timestamp of each frame.

### Expected monthly frame count

Assuming one frame every 10 minutes:

```text
24 hours × 6 frames/hour = 144 frames/day
31 days × 144 frames/day = 4464 frames
```

Observed archive frame count:

```text
frame_count= 4462
```

Difference:

```text
4464 expected - 4462 observed = 2 frames
```

The missing two frame positions cannot be identified because timestamps are absent.

### Local NetCDF comparison

The thesis repository has local NetCDF files only for 26 May 2023:

```text
nc_count=144
first= NHB_PPI_20230526_000303.nc
last=  NHB_PPI_20230526_235304.nc
```

The local filenames show timestamps approximately every 10 minutes for that day. However, there is no metadata in `nhb_2023_05.npz` proving which archive index corresponds to `20230526_000303`, or whether the archive was generated from exactly the same sequence.

Thus:

- Local 26 May timestamp evidence: available.
- Archive-to-26-May index mapping: NOT FOUND.
- Exact day of archive frame index 0: NOT FOUND.
- Exact timestamp for windows 3641–3656: NOT FOUND.

**VERDICT:** The archive is monthly and has 4462 frames instead of the expected 4464, but no timestamp metadata exists, so an index-to-time mapping cannot be verified.

---

## 3. Train/validation/test membership

## 3.1 Configuration defaults

[`config.py`](), lines 53–65, defines:

```python
NPZ_DATA_DIR   = .../nha-be-dataset/npy_uncompressed
NPZ_TRAIN_GLOB = os.environ.get('NPZ_TRAIN_GLOB', '')
NPZ_VALID_GLOB = os.environ.get('NPZ_VALID_GLOB', '')
NPZ_TEST_GLOB  = os.environ.get('NPZ_TEST_GLOB', '')
INPUT_LEN      = 6
TARGET_LEN     = 6
STRIDE         = 1
VALID_RATIO    = 0.2
```

The default training split behavior is implemented in [`main.py`](), lines 58–73:

```python
if cfg.NPZ.TRAIN_GLOB and cfg.NPZ.VALID_GLOB:
    train_files = expand_npz_patterns(cfg.NPZ.TRAIN_GLOB)
    valid_files = expand_npz_patterns(cfg.NPZ.VALID_GLOB)
else:
    all_files = list_npz_files(cfg.NPZ.DATA_DIR)
    test_files = expand_npz_patterns(cfg.NPZ.TEST_GLOB) if cfg.NPZ.TEST_GLOB else [
        file_path for file_path in all_files
        if "nhb_2022_" in os.path.basename(file_path)
    ]
    if test_files and len(test_files) < len(all_files):
        all_files = [file_path for file_path in all_files
                     if file_path not in set(test_files)]
    train_files, valid_files = split_npz_files(
        all_files,
        valid_ratio=cfg.NPZ.VALID_RATIO,
    )
```

The default behavior is therefore:

1. List all `.npy` files.
2. Exclude `nhb_2022_*` files as test files if no explicit test glob is supplied.
3. Sort the remaining files.
4. Put the latest 20% of the remaining files into validation.
5. Use the earlier files for training.

The exact split helper is [`npz_dataset.py`](), lines 143–153:

```python
valid_count = max(min_valid_files, int(round(len(files) * valid_ratio)))
return files[:-valid_count], files[-valid_count:]
```

## 3.2 Documented chronological split

[`docs/guide.md`](), lines 141–146, documents this explicit split:

```text
Train: 2021/01 through 2022/11
Validation: 2022/12 through 2023/03
Test: 2023/05 and 2023/06
```

The documented glob patterns are:

```bash
NPZ_TRAIN_GLOB=
nhb_2021_*.npy
nhb_2022_01.npy ... nhb_2022_11.npy

NPZ_VALID_GLOB=
nhb_2022_12.npy
nhb_2023_01.npy
nhb_2023_02.npy
nhb_2023_03.npy

NPZ_TEST_GLOB=
nhb_2023_05.npy
nhb_2023_06.npy
```

The code actually uses `NPZ_TRAIN_GLOB` and `NPZ_VALID_GLOB` when both are non-empty. The training loop itself does not evaluate the test split during training; the test glob is used by the evaluator.

## 3.3 Evaluator behavior

[`evaluator.py`](), lines 355–363, has this fallback if no explicit `--test-glob` or `NPZ_TEST_GLOB` is provided:

```python
test_glob = (
    f"{cfg.NPZ.DATA_DIR}/nhb_2023_05.npy "
    f"{cfg.NPZ.DATA_DIR}/nhb_2023_06.npy "
)
```

Therefore, the evaluator treats May and June 2023 as the test split by default.

## 3.4 Was May 2023 held out for the 77000 checkpoint?

The code and documentation indicate that May 2023 was intended to be held out under the documented chronological split.

However, the checkpoint does not contain:

- Environment variables
- Split filenames
- Training command
- Data manifest
- Source commit
- Configuration snapshot

Therefore, whether `nhb_2023_05` was actually held out when `encoder_forecaster_77000.pth` was trained is:

```text
NOT VERIFIED
```

The strongest code-based conclusion is:

- **Intended/documented split:** May 2023 is test data.
- **Actual split used for this checkpoint:** NOT FOUND.

**VERDICT:** The code supports a chronological May–June 2023 test split, but checkpoint provenance does not prove that this exact split was used for checkpoint `77000`.

---

## 4. NaN and invalid values

### Archive-level NaN results

The complete archive scan reported:

```text
channel 0 nan = 0
channel 1 nan = 0
```

There are no NaNs in either channel.

The archive also has:

```text
channel 0 min=0.0 max=1.0
channel 1 min=0.0 max=1.0
```

No values were below zero or above one.

### Zero values

Exact-zero counts are large:

| Channel | Total values | Exact zeros | Approximate fraction |
|---:|---:|---:|---:|
| 0 | `1,169,686,528` | `1,038,932,151` | ~88.8% |
| 1 | `1,169,686,528` | `1,032,812,473` | ~88.3% |

Per-frame zero counts from the streamed scan:

| Channel | Minimum zeros/frame | Maximum zeros/frame | Mean zeros/frame |
|---:|---:|---:|---:|
| 0 | `167,404` | `261,319` | `232,840.0159` |
| 1 | `166,998` | `260,486` | `231,468.5058` |

The first three channel-0 zero counts were:

```text
[249923, 250594, 250132]
```

The last three channel-0 zero counts were:

```text
[257209, 256896, 256546]
```

The zeros are widespread and vary by frame. They are consistent with zero-valued background or absent reflectivity, but the archive does not provide an invalid-pixel mask or fill-value documentation. A precise spatial invalid-mask pattern is:

```text
NOT FOUND
```

### Thesis loader behavior

The loader at [`npz_dataset.py`]():

- Converts data to `float32`, lines 102–103.
- Adds a channel axis if needed, lines 104–105.
- Moves channels before spatial dimensions, line 106.
- Checks `np.nanmax(sequence)`, line 108.
- Divides by `70.0` only if the maximum exceeds `1.0`, line 109.
- Clips with `np.clip(sequence, 0.0, 1.0)`, line 111.
- Returns input and target tensors, lines 113–115.

There is no:

```text
nan_to_num
fillna
invalid mask
zero-to-NaN conversion
source-frame validity-mask handling
```

in the inspected loader.

The training/evaluation code creates an all-ones mask:

```python
mask = torch.ones_like(targets, dtype=torch.float32, ...)
```

at [`main.py`](), lines 103–114, and [`evaluator.py`](), lines 100–115.

Because this archive contains no NaNs, the observed prepared data does not require NaN removal during loading. However, the code does not prove how any NaNs may have been handled before archive creation.

**VERDICT:** The downloaded archive contains no NaNs, negatives, or values above one. It contains many exact zeros, but no explicit invalid mask or documented invalid-pixel semantics were found, and the thesis evaluation mask is all ones.

---

## 5. Twelve-frame windows and heavy-rain candidates

### Window construction

The archive has:

```text
4462 frames
```

With 12-frame windows and stride 1, the number of possible windows is:

```text
4462 - 12 + 1 = 4451
```

For each window:

- Frames `start` through `start+5` are treated as input.
- Frames `start+6` through `start+11` are treated as the six-frame target.
- Channel 0 is used.
- The decoding assumption is explicitly:

```text
dBZ = 70*x - 10
```

where `x` is the archive’s normalized channel-0 value.

Heavy rain was computed under both requested Z–R relations:

```text
R = (10^(dBZ/10) / 61.75)^(1/1.61)
R = (10^(dBZ/10) / 58.53)^(1/1.56)
```

The top-candidate scan used stride 1.

### Top windows under `61.75 / 1.61`

| Rank | Start index | Heavy target pixels | Invalid target fraction |
|---:|---:|---:|---:|
| 1 | 3653 | 98,718 | 0.0 |
| 2 | 3654 | 97,804 | 0.0 |
| 3 | 3652 | 96,073 | 0.0 |
| 4 | 3655 | 90,580 | 0.0 |
| 5 | 3651 | 89,350 | 0.0 |
| 6 | 3650 | 80,159 | 0.0 |
| 7 | 3656 | 79,196 | 0.0 |
| 8 | 3641 | 73,190 | 0.0 |
| 9 | 3642 | 72,979 | 0.0 |
| 10 | 3643 | 72,090 | 0.0 |

### Top windows under `58.53 / 1.56`

| Rank | Start index | Heavy target pixels | Invalid target fraction |
|---:|---:|---:|---:|
| 1 | 3653 | 112,979 | 0.0 |
| 2 | 3654 | 111,300 | 0.0 |
| 3 | 3652 | 110,382 | 0.0 |
| 4 | 3655 | 103,373 | 0.0 |
| 5 | 3651 | 102,756 | 0.0 |
| 6 | 3650 | 92,029 | 0.0 |
| 7 | 3656 | 90,674 | 0.0 |
| 8 | 3649 | 81,994 | 0.0 |
| 9 | 3642 | 78,468 | 0.0 |
| 10 | 3641 | 78,458 | 0.0 |

No timestamp is included because the archive has no timestamp metadata.

### Zero-heavy-window fraction

A second scan used stride 6 because of the archive size:

```text
stride=6 windows=742
```

Results:

```text
zero_fraction 61.75/1.61 0 / 742 = 0.0
zero_fraction 58.53/1.56 0 / 742 = 0.0
```

The mean heavy-pixel count per sampled stride-6 window was:

```text
61.75/1.61: 6536.049865229111
58.53/1.56: 7079.153638814016
```

Thus, every sampled stride-6 window contained at least one heavy-rain target pixel under both Z–R relations.

**VERDICT:** The strongest heavy-rain windows are starts 3653, 3654, and 3652. No timestamp can be assigned to them, and no sampled stride-6 window had zero heavy-rain target pixels.

---

## 6. Real-data forward and metrics

### Model and execution

The following were used:

- RainCast [`model.py`]()
- `build_model()`
- Checkpoint `E:\PrecipitationNowcasting\ConvLSMT\outputs\encoder_forecaster_77000.pth`
- CPU
- `model.eval()`
- `torch.no_grad()`
- Input layout `[T=6,B=1,C=1,H=512,W=512]`
- Channel 0 from the archive
- Raw model output evaluated before clamping
- Predictions clamped to `[0,1]` before metrics
- Heavy-rain threshold computed from each requested Z–R relation

Checkpoint load result:

```text
load_result= <All keys matched successfully>
```

The previous equivalence audit did **not** prove that RainCast `model.py` is the exact thesis network. It found substantial differences from the documented thesis-shaped architecture. Therefore, these are RainCast checkpoint results, not verified thesis-network-equivalence results.

### Raw model output

| Window start | Input min | Input max | Raw output min | Raw output max | Raw output mean |
|---:|---:|---:|---:|---:|---:|
| 3653 | `0.0` | `1.0` | `-1.2767832279205322` | `0.11522473394870758` | `-0.9572809338569641` |
| 3654 | `0.0` | `1.0` | `-1.284783959388733` | `0.11522473394870758` | `-0.9571219086647034` |
| 3652 | `0.0` | `1.0` | `-1.2815696001052856` | `0.11522473394870758` | `-0.9569903016090393` |

The raw output is not itself bounded in `[0,1]`. It was clamped before metric calculation, as in [`evaluator.py`](), lines 127–130.

The model predictions produced no heavy-rain pixels after clamping for any of these three windows under either Z–R relation. Therefore, RainCast had:

```text
H = 0
F = 0
CSI = 0
POD = 0
FAR = null
BIAS = 0
```

for every lead in these samples.

### Metric notation

Each metric tuple below is:

```text
CSI / POD / FAR / BIAS
```

`null` means the denominator was zero, not NaN.

---

### Window start 3653

#### Z–R `61.75 / 1.61`

| Lead | ConvLSTM | Persistence | ConvLSTM CSI beats persistence? |
|---:|---|---|---|
| 1 | `0 / 0 / null / 0` | `0.433824 / 0.622816 / 0.411582 / 1.058458` | No |
| 2 | `0 / 0 / null / 0` | `0.220096 / 0.419789 / 0.683677 / 1.327089` | No |
| 3 | `0 / 0 / null / 0` | `0.111963 / 0.301647 / 0.848860 / 1.995810` | No |
| 4 | `0 / 0 / null / 0` | `0.086827 / 0.268974 / 0.886355 / 2.366798` | No |
| 5 | `0 / 0 / null / 0` | `0.083129 / 0.252992 / 0.889830 / 2.296376` | No |
| 6 | `0 / 0 / null / 0` | `0.062361 / 0.188390 / 0.914730 / 2.209340` | No |

#### Z–R `58.53 / 1.56`

| Lead | ConvLSTM | Persistence | ConvLSTM CSI beats persistence? |
|---:|---|---|---|
| 1 | `0 / 0 / null / 0` | `0.448350 / 0.637209 / 0.397974 / 1.058440` | No |
| 2 | `0 / 0 / null / 0` | `0.252433 / 0.456381 / 0.639028 / 1.264310` | No |
| 3 | `0 / 0 / null / 0` | `0.127767 / 0.331481 / 0.827883 / 1.925898` | No |
| 4 | `0 / 0 / null / 0` | `0.099104 / 0.295674 / 0.870271 / 2.279159` | No |
| 5 | `0 / 0 / null / 0` | `0.089289 / 0.268820 / 0.882070 / 2.279491` | No |
| 6 | `0 / 0 / null / 0` | `0.064845 / 0.189292 / 0.910221 / 2.108436` | No |

---

### Window start 3654

#### Z–R `61.75 / 1.61`

| Lead | ConvLSTM | Persistence | ConvLSTM CSI beats persistence? |
|---:|---|---|---|
| 1 | `0 / 0 / null / 0` | `0.361537 / 0.598463 / 0.522679 / 1.253794` | No |
| 2 | `0 / 0 / null / 0` | `0.170397 / 0.420110 / 0.777199 / 1.885582` | No |
| 3 | `0 / 0 / null / 0` | `0.114724 / 0.333048 / 0.851057 / 2.236080` | No |
| 4 | `0 / 0 / null / 0` | `0.104559 / 0.300033 / 0.861707 / 2.169548` | No |
| 5 | `0 / 0 / null / 0` | `0.073992 / 0.212698 / 0.898100 / 2.087318` | No |
| 6 | `0 / 0 / null / 0` | `0.064975 / 0.183482 / 0.908596 / 2.007382` | No |

#### Z–R `58.53 / 1.56`

| Lead | ConvLSTM | Persistence | ConvLSTM CSI beats persistence? |
|---:|---|---|---|
| 1 | `0 / 0 / null / 0` | `0.398811 / 0.625668 / 0.476210 / 1.194503` | No |
| 2 | `0 / 0 / null / 0` | `0.193413 / 0.456959 / 0.748863 / 1.819563` | No |
| 3 | `0 / 0 / null / 0` | `0.132308 / 0.368460 / 0.828888 / 2.153318` | No |
| 4 | `0 / 0 / null / 0` | `0.116782 / 0.329776 / 0.846874 / 2.153632` | No |
| 5 | `0 / 0 / null / 0` | `0.079674 / 0.220795 / 0.889160 / 1.992023` | No |
| 6 | `0 / 0 / null / 0` | `0.074818 / 0.200973 / 0.893504 / 1.887152` | No |

---

### Window start 3652

#### Z–R `61.75 / 1.61`

| Lead | ConvLSTM | Persistence | ConvLSTM CSI beats persistence? |
|---:|---|---|---|
| 1 | `0 / 0 / null / 0` | `0.472671 / 0.703583 / 0.409800 / 1.192110` | No |
| 2 | `0 / 0 / null / 0` | `0.307628 / 0.532102 / 0.578299 / 1.261798` | No |
| 3 | `0 / 0 / null / 0` | `0.157081 / 0.350528 / 0.778432 / 1.582037` | No |
| 4 | `0 / 0 / null / 0` | `0.070428 / 0.222335 / 0.906552 / 2.379226` | No |
| 5 | `0 / 0 / null / 0` | `0.061230 / 0.220490 / 0.921854 / 2.821484` | No |
| 6 | `0 / 0 / null / 0` | `0.043727 / 0.156582 / 0.942802 / 2.737533` | No |

#### Z–R `58.53 / 1.56`

| Lead | ConvLSTM | Persistence | ConvLSTM CSI beats persistence? |
|---:|---|---|---|
| 1 | `0 / 0 / null / 0` | `0.483827 / 0.721303 / 0.404931 / 1.212133` | No |
| 2 | `0 / 0 / null / 0` | `0.317005 / 0.549515 / 0.571686 / 1.282970` | No |
| 3 | `0 / 0 / null / 0` | `0.184393 / 0.394276 / 0.742726 / 1.532512` | No |
| 4 | `0 / 0 / null / 0` | `0.084341 / 0.259355 / 0.888901 / 2.334445` | No |
| 5 | `0 / 0 / null / 0` | `0.068970 / 0.242765 / 0.912126 / 2.762643` | No |
| 6 | `0 / 0 / null / 0` | `0.047571 / 0.170881 / 0.938154 / 2.763046` | No |

### Interpretation

For these three high-heavy-rain windows, the loaded RainCast checkpoint produced raw outputs with maximum approximately `0.1152`. Under the requested normalized decoding, this is below the heavy-rain normalized threshold, so the clamped ConvLSTM forecast contains no heavy-rain pixels.

Persistence outperformed RainCast at every lead for every tested window and both Z–R relations.

This is a result for three selected windows only. It is not an aggregate test-set score.

**VERDICT:** On all three top real-data windows, the RainCast `77000` checkpoint produced CSI `0` at every lead and was beaten by persistence at every lead under both Z–R relations. This does not establish that `model.py` is the original thesis network.

---

# RECOMMENDED EVENT FILE CONTRACT

Based only on the archive, loader, evaluator, and RainCast evidence:

## Required structure

An event file should contain:

```text
input:  float32 array with shape (6, H, W)
target: float32 array with shape (6, H, W)
```

For the RainCast project contract, the documented shape is:

```text
input:  (6, 360, 360)
target: (6, 360, 360)
```

The downloaded monthly archive is different:

```text
radar_sequence: (4462, 512, 512, 2)
```

The thesis training code keeps channel 0 and uses a `[T,B,C,H,W]` model layout. An event-preparation step would therefore need to select the intended reflectivity channel explicitly.

## Value representation

The event arrays should be:

```text
dtype: float32
normalisation: x = (clip(dBZ, -10, 60) + 10) / 70
expected value range: [0,1]
```

The downloaded archive already satisfies the observed numeric range `[0,1]`.

## Invalid pixels and masks

Evidence shows:

- No NaNs in the downloaded archive.
- Many exact zeros.
- No explicit archive validity mask.
- Thesis training/evaluation creates an all-ones mask.

Therefore:

```text
NaN handling: must be decided explicitly before event generation
valid mask: not currently evidenced as part of the thesis event contract
zero semantics: UNKNOWN; do not automatically reinterpret zero as invalid
```

A valid-mask field should not be added or assumed without confirming the intended scientific semantics.

## Grid size

The downloaded archive is 512×512. The RainCast implementation accepts 512×512 and 360×360 dynamically, but the project event contract documents 360×360.

No evidence justifies silently resizing, cropping, or padding 512×512 data for event files. The spatial conversion rule is:

```text
NOT FOUND
```

until the intended production grid is confirmed.

## Time metadata

The archive lacks timestamps. A curated event file should include a verified start time, for example as external event metadata:

```text
startTime: ISO-8601 timestamp
```

The six input frames represent:

```text
t-50, t-40, t-30, t-20, t-10, t0
```

and the six targets represent:

```text
t+10, t+20, t+30, t+40, t+50, t+60
```

However, the downloaded archive alone cannot supply `startTime`.

---

# STILL UNKNOWN

1. Exact timestamp for archive frame index 0.
2. Which two 10-minute frames are absent from the expected 4464-frame May sequence.
3. Whether archive channel 1 has a documented physical meaning.
4. Whether exact zeros are background, no-rain, invalid pixels, or another fill convention.
5. Whether `nhb_2023_05.npz` was actually used as held-out test data when `encoder_forecaster_77000.pth` was trained.
6. The exact environment variables used during checkpoint training.
7. The exact training source commit that produced checkpoint `77000`.
8. Whether 512×512 data was intended for the thesis checkpoint or whether it should be converted to 360×360 for RainCast events.
9. The required crop, resize, padding, or reprojection rule between 512×512 and 360×360.
10. Whether the two-channel archive was intended to be reduced to channel 0 or whether both channels have a documented role.
11. How any invalid pixels were handled before the monthly archive was generated.
12. Whether the downloaded monthly archive and the local 20230526 NetCDF files use identical frame ordering and preprocessing.
13. Whether RainCast [`model.py`]() is the exact network that generated checkpoint `77000`; the prior equivalence audit found this unverified and measured large differences from the documented thesis-shaped reconstruction.
14. Aggregate ConvLSTM metrics over the complete official test set; this audit evaluated only the three highest heavy-rain windows.
15. Permission to redistribute or commit any subset of the radar archive.