# auto_arknights
明日方舟自动刷图

## 依赖
+ ADB
    - Android Debug Bridge
    - 用于和模拟器交互
    - 下载地址：https://dl.google.com/android/repository/platform-tools_r30.0.5-windows.zip?hl=zh-cn
+ python 3.6+
    - 运行核心逻辑
    - 使用opencv寻找页面按钮
+ opencv-python    

## 基本策略
+ 通过ABD进行截图和屏幕点击操作
+ 使用opencv的图像模板匹配已确定页面按钮位置
+ 按特征图像确定当前页面，一个页面是一种状态，随状态转移决策点击位置

## 使用方法
0. 下载adb，解压后放置到你喜欢的路径，得到压缩包内`platform-tools_r30.0.5-windows/platform-tools/adb.exe`的路径
0. 将`adb.exe`的路径写入项目文件`auto_click/config.json`的`adb_exe`字段
0. 启动模拟器，我用的是mumu
0. 进入游戏，进入到地图详情页面，勾选`代理指挥`
0. powershell执行`adb.exe connect 127.0.0.1:7555`，以建立与模拟器的连接
    - adb.exe需要写成绝对路径
0. 在入口脚本`run_ak_prepared.py`中的main部分设置最大执行次数和最大嗑药次数
0. 执行入口脚本`run_ak_prepared.py`


## 文件说明
+ img_tpl路径下的图片是用于图像识别的模板
+ auto_click对adb操作的封装
+ 主要逻辑存在于`run_ak_prepared.py`

## 特殊功能
+ 嗑药
    - 理智不足时可以自动嗑药，但目前不支持嗑原石，需要的可以照着代码自行实现
+ 设置作战时长
    - 作战时间不会轮询截图
    - 减少截图次数
+ 点击后等待
    - 点击按钮或页面后，不一定会立刻切换到下一个页面
    - 为避免画面延迟导致图像匹配识别，点击后会等待2-3秒
+ 操作日志
    - 对页面切换和执行轮数会写到日志文件    