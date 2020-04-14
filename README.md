# 美国新型冠状病毒最新发布数据

简单的python 脚本爬取腾讯每日发布的海外患病数据，并整理成CSV数据格式，方便数据处理。

## 改进 
- 4.13 
    1. 加入了错误捕获机制，防止网络错误导致程序无法运行；
    2. 添加缓存，保证在没有网络的情况下依然能够输出结果，但输出结果的时候会提示使用了缓存；
    3. 优化了代码结构，便于理解


参考[China_CoronaVirus_Data_Miner](https://github.com/dakula009/China_CoronaVirus_Data_Miner)