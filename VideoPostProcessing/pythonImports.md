### Within VSCode, the python environment is set to 3.13.9 from the Microsoft Store

`pip install --upgrade pip`
`pip install dxcam pillow opencv-python ultralytics`
`cls`

### Details

# Image capture from the screen
dxcam `pip install dxcam`
pillow `pip install pillow`

# OpenCV (motion tracking)
Base: `pip install opencv-python`
The model: `pip install ultralytics`
    If windows throws an error on the length of the path:
    Powershell admin: `New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force`