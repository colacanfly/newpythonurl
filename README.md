爬取基金
>爬取将基金代码，并遍历所有代码，并爬取每个基金对应的代码，找到净值数据，按方差对其排序

配置环境
1.  python2.7
2.  linux操作系统
3.  python的urllib库
4.  python的json库
5.  python的logging库
6.  python的re库
7.  python的math库
8.  python的time库
9.  python的threading库
10. python的logging库

文件内容
1. conf文件夹下为配置文件
2. data下list文件夹下是排序好的列表
3. log下为日志信息
4. src下test.py为主要代码
5. src下config.py是自定义模块，作用为读取配置文件信息，并将其存入词典

使用说明
>运行：/newpythonurl/src/ python test.py
