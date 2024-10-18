# 项目名称

LLM地理位置推荐应用

## 项目简介

LLM地理位置推荐应用旨在为用户提供一种智能化的商户推荐服务。通过结合用户的需求分析与地理位置，该应用利用大型语言模型（LLM）来理解用户的需求，并通过 Google Maps Places API 查找并推荐最适合的商户。无论是寻找美食、购物场所还是娱乐活动，这款应用都能为用户提供个性化的推荐。

## 功能特点

- **自然语言需求分析**：用户只需输入自己的需求，应用将通过 LLM 解析并理解用户的偏好和意图。
- **地理位置匹配**：结合用户所在位置，通过 Google Maps Places API 查找附近的商户。
- **个性化推荐**：将分析结果与地理位置相结合，为用户提供最合适的商户推荐。

## 使用的技术栈

- **Google Maps Places API**：用于根据用户的地理位置查找附近的商户和服务。
- **LangChain**：用于构建和管理大型语言模型（LLM），以便更好地理解用户的需求。
- **Streamlit**：作为前端框架，为用户提供简洁直观的界面，使用户能够轻松地输入需求并查看推荐结果。

## 安装与使用

1. **克隆仓库**

   ```bash
   git clone https://github.com/brucehe3/glee-bear.git
   cd blee-bear
   ```

2. **安装依赖**

   建议使用 Python 虚拟环境来管理依赖。

   ```bash
   python -m venv env
   source env/bin/activate  # Windows 系统请使用 `env\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **设置环境变量**

   请创建一个 `.env` 文件，用于存储 Google Maps API 密钥和其他配置项。

   ```
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **运行应用**

   使用 Streamlit 启动应用：

   ```bash
   streamlit run app.py
   ```

   访问 `http://localhost:8501` 查看应用界面。

## 项目结构

- `app.py`：主应用文件，通过 Streamlit 提供用户界面。
- `requirements.txt`：包含项目的依赖列表。
- `.env`：用于存放环境变量（未提交到仓库）。

## 贡献指南

欢迎任何形式的贡献！如果你发现了问题或者有改进建议，请提交 Issue 或创建 Pull Request。

1. Fork 本项目。
2. 创建你的 Feature 分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目基于 MIT 许可证进行发布。详情请查看 [LICENSE](LICENSE)。

## 联系方式

如果你有任何疑问或建议，欢迎通过以下方式联系：

- **邮箱**: designerhe@gmail.com
- **GitHub**: [brucehe](https://github.com/brucehe3)

感谢你对本项目的关注！

