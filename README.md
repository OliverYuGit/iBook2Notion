# iBooks2Notion

提取 macOS 的 iBooks 中的笔记和高亮，通过 OpenAI (LangChain) 根据高亮自动总结成 notion 的标题，然后在 notion 创建该笔记。
> Extract notes and highlights from iBooks on macOS, automatically summarize highlight into Notion title using OpenAI (LangChain), and create the note in Notion.
## 快速开始 (QuickStart)
获取 OpenAI 的 [API Key](https://platform.openai.com/account/api-keys)
> Get an OpenAI [API Key](https://platform.openai.com/account/api-keys)

创建 [Notion integrations](https://www.notion.so/my-integrations) 并获取 API key

> Create a [Notion integrations](https://www.notion.so/my-integrations) and get an API Key

获取 Notion 数据库的 ID 并记住相关字段名称

> Get Notion database ID and field names.

去除 `.env.template` 文件的 `.template` 后缀，并填写该文件的相关数据，并仔细检查。

> Remove the `.template` suffix from the `.env.template` file and fill in 
the relevant data. Please be sure to check carefully.

打开 Terminal 并运行以下命令：
1. 进入本程序所在文件夹
2. 加载相关依赖 `pip install -r requirements.txt`
3. 运行程序 `python -m main`

> Open the terminal and run the following command.
> 1. Enter the program path.
> 2. Loading program dependencies `pip install -r requirements.txt`
> 3. Run program `python -m main`

注意：本程序是根据创建时间过滤已导入 notion 的笔记（防止重复导入），如若程序运行失败，需要重新运行的情况，请记住要修改 `mark.yaml` ，将日期时间改到小于 time_mark 即可.

> note: This program filters notes based on their creation time to prevent duplicate imports into Notion. If the program fails to run and needs to be rerun, remember to modify 'mark.yaml' and change the datetime less than 'time_mark'.