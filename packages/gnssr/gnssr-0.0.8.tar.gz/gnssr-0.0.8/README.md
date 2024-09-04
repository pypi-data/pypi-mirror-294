# gnssr v0.0.7

## Introduction
GNSS-R Data Processing Package

This package provides a comprehensive set of tools and functions for processing and analyzing Global Navigation Satellite System Reflectometry (GNSS-R) data. GNSS-R is an emerging remote sensing technique that leverages the signals transmitted by navigation satellites (such as GPS, GLONASS, Galileo, and BDS) to observe the Earth's surface and atmosphere through reflections from the Earth's surface or other natural scatterers.

The package is designed to facilitate the entire GNSS-R data processing pipeline, from raw signal simulation and processing, to advanced data analysis and visualization. It includes algorithms for:

1. CYGNSS L1 processing
   - Data reading
   - Variable extraction
   - Quality control
   - Gridding
   - Surface reflectivity calculation
2. Under development...


## Installation
To avoid version conflicts between packages, it is recommended to create a virtual environment for gnssr
```python
conda create -n gnssr_env python=3.12.4
```
Activate the virtual environment
```python
conda activate gnssr_env
```
Install gnssr using pip
```python
pip install gnssr
```
Or, download and install from GitHub
```python
git clone https://github.com/QinyuGuo-Pot/gnssr
cd gnssr
pip install -e .
```

## Usage Overview
### Import Module
```python
# import gnssr
from gnssr import cygnss as cyg
```

### Data File Sorting
`sort_files_by_date()` organizes data files by day based on the date information in the CYGNSS L1 data file names. Files from the same day are automatically sorted into the same folder named yyyymm
```python
# source_dir: Directory where the data files are located
cyg.sort_files_by_date('source_dir')
```

### Read Data
`read_data()` calls xarray.open_mfdataset() to read single/multiple netcdf files and merge them into a single xarray.Dataset object.
```python
ds = cyg.read_data('~/path/*.nc')
```

### Variable Extraction
`extract_obs()` extracts variables from the dataset `ds` based on the input variable list, and reshapes the extracted variables into a one-dimensional array stored in a dataframe for return. If the original dimensions of the extracted variables include `'delay'` and `'doppler'`, the peak value will be calculated along these two axes. Parameters: the dataset `ds`, the list of variables, a boolean value indicating whether quality control is needed (default is False), the quality control method ('default' or 'custom', default is 'default'), and a custom quality control file in yaml format (optional for the last three parameters).
```python
# obs_list: List of variables to extract, which should match the variable names in the netcdf file  
obs_list = ['sp_lar','ddm_snr','brcs']  
  
# Without quality control  
df_obs = cyg.extract_obs(ds, obs_list)  
  
# With quality control using default criteria  
df_qc = cyg.extract_obs(ds, obs_list, True)  
  
# With quality control using custom criteria  
df_qc_custom = cyg.extract_obs(ds, obs_list, True, 'custom', 'quality_control_config.yaml')
```

### Quality Control
`quality_control_default()` performs quality control on the extracted variables using the following criteria:
1. quality_flags: s_band_powered_up, large_sc_attitude_err, black_body_ddm, ddm_is_test_pattern, direct_signal_in_ddm, low_confidence_gps_eirp_estimate, and **sp_over_land**
2. sp_inc_angle: less than 65 degrees
3. sp_rx_gain: greater than or equal to 0
4. ddm_snr: greater than or equal to 2
5. brcs_ddm_peak_bin_delay_row: between 4 and 15th
```python
# Pass in the dataframe and dataset as parameters
df_qc = cyg.quality_control_default(df_obs,ds) # df is the dataframe returned by extract_obs()
```
`quality_control_custom()` allows users to customize the quality control criteria, returning a filtered dataframe. Paramters: quality control configuration file (YAML), a dataframe, and dataset `ds`. Users can tailor the YAML file parameters as needed. Use template  at [link](https://github.com/QinyuGuo-Pot/gnssr/tree/master/test).
```yaml
quality_flags:  
  - s_band_powered_up: 0 
  - large_sc_attitude_err: 0  
  - black_body_ddm: 0
  - ddm_is_test_pattern: 0 
  - direct_signal_in_ddm: 0
  - low_confidence_gps_eirp_estimate: 0
  - sp_over_land: 1
sp_inc_angle: '<= 65'  
sp_rx_gain: '>= 0' 
ddm_snr: '>= 2'  
brcs_ddm_peak_bin_delay_row: '>= 4,<= 15' 
```
```python
df_qc_custom = cyg.quality_control_custom('quality_control_config.yaml',df_obs,ds)
```

### Surface Reflectivity Calculation
`cal_sr()` calculates surface reflectivity in dB form, returns a dataframe containing `'sp_lat'`, `'sp_lon'`, and `'sr'`. Parameters: the dataset `ds`, the list of variables, a boolean value indicating whether quality control is needed (default is False), the quality control method ('default' or 'custom', default is 'default'), and a custom quality control file in yaml format (optional for the last three parameters).
```python
# Without quality control  
df_sr = cyg.cal_sr(ds)  
  
# With quality control using default criteria  
df_sr = cyg.cal_sr(ds, True)  
  
# With quality control using custom criteria  
df_sr_custom = cyg.cal_sr(ds, True, 'custom', 'quality_control_config.yaml')
```


### Filter Data by location
`filter_data_by_lonlat()` filters data based on longitude and latitude range, returns a dataframe. Parameters: dataframe, longitude and latitude range; the dataframe must contain`'sp_lat'` and`'sp_lon'` variables, the longitude and latitude range format is [lon_min,lon_max,lat_min,lat_max]
```python
lonlat_range = [lon_min,lon_max,lat_min,lat_max]
df_region = cyg.filter_data_by_lonlat(df,lonlat_range)
```
`filter_data_by_vector()` filters data based on a vector file and returns a dataframe. The input parameters include: dataframe, and the path to the vector file. Supported vector file formats include `.shp`, `.shx`, `.dbf`, `.json`.
```python
shp_file = '~/path/shp_file.shp'
df_region = cyg.filter_data_by_vector(df,shp_file)
```


### Exclude GNSS-R Observations in Open Water
`filter_data_by_watermask()` excludes GNSS-R observations in open water, returns a dataframe. Parameters: GSW data file path, dataframe; the dataframe must contain`'sp_lat'` and`'sp_lon'` variables; the algorithm for exclusion is to match GNSS-R observation coordinates (`'sp_lat'`,`'sp_lon'`) with GSW data's coordinates, and exclude observations that fall within the water surface. Currently, the algorithm only supports GSW's seasonal products.
```python
gsw_file = '~/path/gsw_file.tif'
df_no_water = cyg.filter_data_by_watermask(gsw_file,df)
```


### Grid Data
`grid_obs()` grids the GNSS-R observations and returns a dictionary containing the gridded results of each observation variable. The input parameters include: dataframe, latitude grid, longitude grid, and a list of variables. The dataframe must contain 'sp_lat' and 'sp_lon' along with the variables to be gridded. The input latitude and longitude grids are required to be one-dimensional, increasing arrays. The gridding algorithm involves partitioning the GNSS-R observation coordinates ('sp_lat', 'sp_lon') and calculating the mean values. You can download the EASE-Grid 36km grid files from the [link](https://github.com/QinyuGuo-Pot/gnssr/tree/master/test) here, or generate grid files using the ease-grid library.
```python
from ease_grid import EASE2_grid
from matplotlib import pyplot as plt

egrid = EASE2_grid(36000)
glat = egrid.latdim[::-1]
glon = egrid.londim

grid_obs = cyg.grid_obs(df,glat,glon,['sr','brcs','ddm_snr'])
sr_array = grid_obs['sr']

plt.pcolormesh(sr_array)
```

## Version History
v0.0.4
 - Add documentation 

v0.0.5
 - Add user-defined quality control function `quality_control_custom()`

 v0.0.6
- Modified `quality_control_custom()`
- Modified `extract_obs()`
- Modified `'grid_obs()`
- Add `filter_data_by_vector()`

v0.0.7
 - Optimized `quality_control_custom()`
 - Optimized `quality_control_default()`
 - Modified `extract_obs()`
 - Modified `cal_sr()`


## Concat
 - Email：<qinyuguo@chd.edu.cn>

---
## 介绍
GNSS-R 数据处理包

gnssr提供了一系列用于处理和分析全球导航卫星系统反射(GNSS-R) 数据的工具和函数。GNSS-R 是一种新型的遥感技术，利用导航卫星（如 GPS、GLONASS、Galileo、BDS 等）的反射信号进行对地观测。

该包旨在为 GNSS-R 数据处理提供一个全面的工具，从原始信号仿真和处理，到高级数据分析和可视化。它包含了以下算法：

1. CYGNSS L1 处理
   - 数据读取
   - 变量提取
   - 质量控制
   - 网格化
   - 地表反射率计算
2. 正在开发中...


## 安装

为了避免包之间的版本冲突，建议为 gnssr 创建一个虚拟环境
```python
conda create -n gnssr_env python=3.12.4
```
激活虚拟环境
```python
conda activate gnssr_env
```
pip 安装 gnssr
```python
pip install gnssr
```
或从 GitHub 下载安装
```python
git clone https://github.com/QinyuGuo-Pot/gnssr
cd gnssr
pip install -e .
```

## 使用概览
### 导入模块
```python
# import gnssr
from gnssr import cygnss as cyg
```
### 数据文件整理
`sort_files_by_date()`根据CYGNSS L1数据文件名中的日期信息，对数据文件按天分类整理，同一天的数据会被自动分类至同一个文件夹中，文件夹命名:yyyymm
```python
# source_dir: 数据文件所在目录
cyg.sort_files_by_date('source_dir')
```
### 读取数据
`read_data()`调用xarray.open_mfdataset()，读取单个/多个netcdf文件，并自动合并成一个xarray.Dataset对象
```python
ds = cyg.read_data('~/path/*.nc')
```
### 变量提取
`extract_obs()`根据传入的变量列表对数据集ds进行变量提取，所提取的变量会被重塑为一维数组存储在dataframe中返回，如果提取的变量原始维度中包含'delay'和'doppler',会沿这两个轴求取峰值;传入参数：数据集ds，变量列表，布尔值（是否要进行质量控制，默认False），质量控制方法（提供'default'或'custom'，默认'default'），自定义质量控制文件（yaml格式），后三个参数为可选参数
```python
# obs_list: 要提取的变量列表，需与netcdf文件中的变量名一致
obs_list = ['sp_lar','ddm_snr','brcs']

# 不进行质量控制
df_obs = cyg.extract_obs(ds, obs_list)

# 以默认准则进行质量控制
df_qc = cyg.extract_obs(ds, obs_list, True)

# 以自定义准则进行质量控制
df_qc_custom = cyg.extract_obs(ds, obs_list, True, 'custom', 'quality_control_config.yaml')
```
### 质量控制
`quality_control_default()`对所提取的变量进行质量控制，默认使用了以下准则：
1. quality_flags: s_band_powered_up, large_sc_attitude_err, black_body_ddm, ddm_is_test_pattern,  
direct_signal_in_ddm, low_confidence_gps_eirp_estimate, and **sp_over_land** 
2. sp_inc_angle: less than 65 degrees   
3. sp_rx_gain: greater than or equal to 0 
4. ddm_snr: greater than or equal to 2  
5. brcs_ddm_peak_bin_delay_row: between 4 and 15th 
```python
# 传入参数：dataframe, 数据集ds
df_qc = cyg.quality_control_default(df_obs,ds) # df为extract_obs()返回的dataframe
```
`quality_control_custom()`允许用户自定义质量控制准则，返回经过质量控制的dataframe；传入参数：dataframe, 数据集ds，质量控制配置文件(yaml格式)；配置文件格式如下，用户可自定义yaml文件中的各项参数，请使用[模板](https://github.com/QinyuGuo-Pot/gnssr/tree/master/test)
```yaml
quality_flags:  
  - s_band_powered_up: 0 
  - large_sc_attitude_err: 0  
  - black_body_ddm: 0
  - ddm_is_test_pattern: 0 
  - direct_signal_in_ddm: 0
  - low_confidence_gps_eirp_estimate: 0
  - sp_over_land: 1
sp_inc_angle: '<= 65'  
sp_rx_gain: '>= 0' 
ddm_snr: '>= 2'  
brcs_ddm_peak_bin_delay_row: '>= 4,<= 15' 
```
```python
df_qc_custom = cyg.quality_control_custom(df_obs,ds，'quality_control_config.yaml')
```
### 地表反射率计算
`cal_sr()`计算dB形式的地表反射率，返回包含`'sp_lat'`, `'sp_lon'`, `'sr'`的dataframe，传入参数：数据集ds，布尔值（是否要进行质量控制，默认False），质量控制方法（提供'default'或'custom'，默认'default'），自定义质量控制文件（yaml格式），后三个参数为可选参数
```python
# df = pd.DataFrame()
df = df_obs.copy()
# 不进行质量控制
df_sr = cyg.cal_sr(ds)

# 以默认准则进行质量控制
df_sr = cyg.cal_sr(ds, True)

# 以自定义准则进行质量控制
df_sr_custom = cyg.cal_sr(ds, True, 'custom', 'quality_control_config.yaml')
```

### 根据位置筛选数据
`filter_data_by_lonlat()`根据经纬度范围筛选数据，返回dataframe，传入参数：dataframe, 经纬度范围；dataframe中需包含'sp_lat'和'sp_lon'变量,经纬度范围格式为[lon_min,lon_max,lat_min,lat_max]
```python
lonlat_range = [lon_min,lon_max,lat_min,lat_max]
df_region = cyg.filter_data_by_lonlat(df,lonlat_range)
```
`filter_data_by_vector()`根据矢量文件筛选数据，返回dataframe，传入参数：dataframe, 矢量文件路径；支持的矢量文件格式有`.shp`, `.shx`, `.dbf`, `.json`
```python
shp_file = '~/path/shp_file.shp'
df_region = cyg.filter_data_by_vector(df,shp_file)
```

### 剔除开放水域内的观测量
`filter_data_by_watermask()`剔除开放水域内的GNSS-R观测量，返回dataframe，传入参数：GSW数据文件路径，dataframe；dataframe中需包含'sp_lat'和'sp_lon'变量；水体剔除的算法是将GNSS-R观测量坐标（'sp_lat','sp_lon'）与GSW数据文件中水体的坐标进行匹配，剔除落在水体内的观测量；目前算法仅支持GSW数据的季节性产品
```python
gsw_file = '~/path/gsw_file.tif'
df_no_water = cyg.filter_data_by_watermask(gsw_file,df)
```

### 格网化
`grid_obs()`对GNSS-R观测量进行格网化，返回包含各个观测量格网化结果的字典，传入参数：dataframe，纬度格网，经度格网，变量列表；dataframe中需包含`'sp_lat'`和`'sp_lon'`以及待格网化的变量，传入的纬度格网和经度格网需为一维递增数组；格网化的算法是将GNSS-R观测量坐标（`'sp_lat'`,`'sp_lon'`）进行分割并计算均值；可从链接[下载](https://github.com/QinyuGuo-Pot/gnssr/tree/master/test)EASE-Grid 36km格网文件，或使用ease-grid库生成格网文件
```python
from ease_grid import EASE2_grid
from matplotlib import pyplot as plt

egrid = EASE2_grid(36000)
glat = egrid.latdim[::-1]
glon = egrid.londim

grid_obs = cyg.grid_obs(df,glat,glon,['sr','brcs','ddm_snr'])
sr_array = grid_obs['sr']

plt.pcolormesh(sr_array)
```


## 版本历史
v0.0.4
 - 添加说明文档 

v0.0.5
 - 添加用户自定义质量控制函数 `quality_control_custom()`

v0.0.6
 - 修改`quality_control_custom()`
 - 修改`extract_obs()`
 - 修改`grid_obs()`
 - 添加`filter_data_by_vector()`

v0.0.7
 - 优化`quality_control_custom()`
 - 优化`quality_control_default()`
 - 修改`extract_obs()`
 - 修改`cal_sr()`

## 联系方式
 - 邮箱：<qinyuguo@chd.edu.cn>
