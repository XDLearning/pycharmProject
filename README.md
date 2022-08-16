## Description
存储用python完成的一些小插件以及实战项目

## Content
目录
- `220809rename.py`：将`文件名`改为`内容_教程_0_文件名`的形式
- `220814spider.py`:自动从可可英语索引页爬取人教版高中必修英语听力的MP3和LRC文件。
  - 需给定索引页链接`index_url`
  - 需给定下载的文件夹，`.py`文件同文件夹下：`RESULTS_DIR = 'name'`
  - 下载的文件命名为类`Book[num]Unit[num][Title]Reading`，如`Book2Unit1CulturalRelicsReading.mp3`
  - 有时候lrc文件不存在，所以lrc文件不保证全部下载
  - 有时候由于爬取次数太多，网络连接失败导致mp3文件也下载失败，可以稍后再尝试，MP3 文件一般都是存在的