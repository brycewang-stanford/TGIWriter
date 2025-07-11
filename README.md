# TGIWriter - AI-Powered Writing Assistant<img width="1215" alt="image" src="https://github.com/user-attachments/assets/e7aa8994-5d7a-4b34-bb5b-65f10052682a" />

🚀 **An intelligent writing assistant for TOEFL, GRE, and IELTS test preparation with real-time AI analysis and feedback**

## ⚠️ Disclaimer / 免责声明

**English:**
This project is a simple reproduction and improvement of existing writing assistance tools, created solely for **personal learning and educational purposes**. We have **no commercial intentions** and do not plan to monetize this project. Please respect the intellectual property rights of the original websites and services. This project is intended for educational exploration and technical learning only.

**中文:**
本项目是对现有写作辅助工具（EasyWriting）的简单复现和改进，仅用于**个人学习和教育目的**。我们**没有任何商业化打算**，不会将此项目进行商业化运营。请尊重原网站和服务的知识产权。本项目仅用于教育探索和技术学习。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚧 Project Status

**⚠️ This is an incomplete version - We welcome your feedback and contributions!**

- 📝 **Share your needs**: Please submit feature requests and issues to help us improve
- 🤝 **Join us**: Developers interested in collaboration are welcome to contribute
- 💼 **Commercial inquiries**: For business opportunities, please contact the author via email

## 🌟 Features

### 🎯 Multi-Test Support
- **TOEFL** (Test of English as a Foreign Language)
- **GRE** (Graduate Record Examination)  
- **IELTS** (International English Language Testing System)

### 🤖 AI-Powered Analysis
- Real-time writing analysis using OpenAI GPT-4o-mini
- Comprehensive feedback on grammar, vocabulary, and structure
- Test-specific scoring based on official rubrics
- Intelligent error detection and suggestions

### 📊 Advanced Writing Analysis
- **6 Analysis Panels**: Errors, Strengths, Vocabulary, Structure, Test Tips, Overall Assessment
- **Real-time Highlighting**: Color-coded text highlighting for different feedback types
- **Detailed Scoring**: Official rubric-based scoring with justification
- **Smart Suggestions**: Prioritized, actionable improvement recommendations

### ⏰ Test Environment Simulation
- 30-minute countdown timer with warnings
- Test-specific prompts and requirements
- Distraction-free writing interface
- Word count and statistics tracking

### 🎨 Modern UI/UX
- Responsive design for all devices
- Beautiful, intuitive interface
- Smooth animations and transitions
- Professional test environment feel

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/brycewang-stanford/TGIWriter.git
   cd TGIWriter/flask_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask openai langchain-openai python-dotenv
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key:
   # OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5002`

## 🏗️ Project Structure

```
TGIWriter/
├── flask_app/
│   ├── app.py                 # Main Flask application
│   ├── templates/
│   │   ├── home.html         # Test selection homepage
│   │   ├── toefl.html        # TOEFL writing interface
│   │   ├── gre.html          # GRE writing interface
│   │   └── ielts.html        # IELTS writing interface
│   ├── .env.example          # Environment variables template
│   ├── .gitignore           # Git ignore file
│   └── requirements.txt      # Python dependencies
├── README.md                 # This file
└── LICENSE                  # MIT License
```

## 📖 Usage Guide

### 1. Select Your Test
Choose from TOEFL, GRE, or IELTS on the homepage

### 2. Pick a Writing Prompt
Select from curated, authentic test prompts

### 3. Choose Your Mode
- **Generate Sample**: AI creates a high-scoring sample essay
- **Write Your Own**: Practice writing with real-time feedback

### 4. Get AI Analysis
- Real-time writing analysis as you type
- Comprehensive feedback across 6 categories
- Detailed scoring and improvement suggestions

### 5. Improve Your Writing
- Follow AI recommendations
- Practice with different prompts
- Track your progress over time

## 🔧 Technical Details

### Backend
- **Framework**: Flask (Python)
- **AI Engine**: OpenAI GPT-4o-mini via LangChain
- **Analysis**: Custom prompt engineering for test-specific feedback

### Frontend
- **Styling**: Tailwind CSS
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Real-time Features**: AJAX-based live analysis
- **Responsive Design**: Mobile-first approach

### AI Analysis Features
- Spelling and grammar error detection
- Advanced vocabulary identification
- Sentence structure analysis
- Coherence and cohesion evaluation
- Test-specific tips and strategies
- Comprehensive scoring with justification

## 🎯 Supported Tests

### TOEFL (Test of English as a Foreign Language)
- Independent Writing tasks
- 30-minute time limit
- 5-point scoring scale
- ETS official rubric alignment

### GRE (Graduate Record Examination)
- Analytical Writing tasks
- Issue and Argument essays
- 6-point scoring scale
- Official GRE criteria

### IELTS (International English Language Testing System)
- Task 1 and Task 2 writing
- Academic and General Training
- 9-band scoring system
- British Council standards

## 🛠️ Development

### Adding New Tests
1. Create a new template in `templates/`
2. Add routing in `app.py`
3. Customize prompts and scoring rubrics
4. Update the homepage with new test option

### Customizing Analysis
- Modify prompts in `analyze_writing()` function
- Adjust scoring criteria for different tests
- Add new analysis categories as needed

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🤝 Feedback & Collaboration

We value your input! This project is actively being developed and improved:

- 🐛 **Found a bug?** Please open an [issue](https://github.com/brycewang-stanford/TGIWriter/issues)
- 💡 **Have a feature idea?** We'd love to hear about it in [discussions](https://github.com/brycewang-stanford/TGIWriter/discussions)
- 🛠️ **Want to contribute?** Check out our [contribution guidelines](CONTRIBUTING.md)
- 💼 **Business inquiries?** Contact the author at: [your-email@example.com]

Your feedback helps make TGIWriter better for everyone!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing GPT-4o-mini API
- ETS, GRE, and IELTS organizations for test format references
- Educational Testing Service for scoring rubric guidelines

---

# TGIWriter - AI智能写作助手

🚀 **为托福、GRE和雅思考试准备提供实时AI分析和反馈的智能写作助手**

## ⚠️ 免责声明 / Disclaimer

**中文:**
本项目是对现有写作辅助工具的简单复现和改进，仅用于**个人学习和教育目的**。我们**没有任何商业化打算**，不会将此项目进行商业化运营。请尊重原网站和服务的知识产权。本项目仅用于教育探索和技术学习。

**English:**
This project is a simple reproduction and improvement of existing writing assistance tools, created solely for **personal learning and educational purposes**. We have **no commercial intentions** and do not plan to monetize this project. Please respect the intellectual property rights of the original websites and services. This project is intended for educational exploration and technical learning only.

## 🚧 项目状态

**⚠️ 这是一个不完善的版本 - 欢迎大家多提需求和建议！**

- 📝 **分享您的需求**：请多提交功能需求和问题，帮助我们改进
- 🤝 **一起合作**：有兴趣的开发者朋友欢迎一起合作改进
- 💼 **商业合作**：有商业化兴趣的朋友可以发邮件联系作者

## 🌟 功能特色

### 🎯 多考试支持
- **托福 (TOEFL)** - 英语作为外语测试
- **GRE** - 研究生入学考试
- **雅思 (IELTS)** - 国际英语语言测试系统

### 🤖 AI智能分析
- 使用OpenAI GPT-4o-mini的实时写作分析
- 语法、词汇和结构的全面反馈
- 基于官方评分标准的考试专用评分
- 智能错误检测和建议

### 📊 高级写作分析
- **6个分析面板**：错误、优势、词汇、结构、考试技巧、总体评估
- **实时高亮显示**：不同反馈类型的彩色文本标记
- **详细评分**：基于官方评分标准的评分和理由说明
- **智能建议**：按优先级排序的可操作改进建议

### ⏰ 考试环境模拟
- 30分钟倒计时器与警告提示
- 考试专用题目和要求
- 无干扰写作界面
- 字数统计和数据追踪

### 🎨 现代化界面
- 适配所有设备的响应式设计
- 美观直观的用户界面
- 流畅的动画和过渡效果
- 专业的考试环境体验

## 🚀 快速开始

### 系统要求
- Python 3.8 或更高版本
- OpenAI API密钥

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/brycewang-stanford/TGIWriter.git
   cd TGIWriter/flask_app
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows系统: venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install flask openai langchain-openai python-dotenv
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑.env文件并添加你的OpenAI API密钥:
   # OPENAI_API_KEY=your_api_key_here
   ```

5. **运行应用**
   ```bash
   python app.py
   ```

6. **打开浏览器**
   访问 `http://localhost:5002`

## 📖 使用指南

### 1. 选择考试类型
在首页选择托福、GRE或雅思

### 2. 选择写作题目
从精选的真实考试题目中选择

### 3. 选择练习模式
- **生成范文**：AI创建高分范文
- **自主写作**：带实时反馈的写作练习

### 4. 获得AI分析
- 实时写作分析
- 6个类别的全面反馈
- 详细评分和改进建议

### 5. 提升写作能力
- 遵循AI建议
- 练习不同题目
- 追踪进步情况

## 🎯 支持的考试

### 托福 (TOEFL)
- 独立写作任务
- 30分钟时间限制
- 5分制评分
- ETS官方评分标准

### GRE研究生入学考试
- 分析性写作任务
- Issue和Argument题型
- 6分制评分
- GRE官方标准

### 雅思 (IELTS)
- Task 1和Task 2写作
- 学术类和培训类
- 9分制评分系统
- 英国文化教育协会标准

## 🛠️ 技术开发

### 后端技术
- **框架**：Flask (Python)
- **AI引擎**：OpenAI GPT-4o-mini via LangChain
- **分析系统**：针对考试的定制提示工程

### 前端技术
- **样式**：Tailwind CSS
- **JavaScript**：现代ES6+特性的原生JS
- **实时功能**：基于AJAX的实时分析
- **响应式设计**：移动优先方法

## 🤝 反馈与合作

我们非常重视您的意见！本项目正在积极开发和改进中：

- 🐛 **发现了Bug？** 请提交 [问题报告](https://github.com/brycewang-stanford/TGIWriter/issues)
- 💡 **有功能建议？** 欢迎在 [讨论区](https://github.com/brycewang-stanford/TGIWriter/discussions) 分享
- 🛠️ **想要参与开发？** 查看我们的[贡献指南](CONTRIBUTING.md)
- 💼 **商业合作咨询？** 请邮件联系作者：[your-email@example.com]

您的反馈让TGIWriter变得更好！

## 📄 开源协议

本项目采用MIT协议 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢OpenAI提供GPT-4o-mini API
- 感谢ETS、GRE和IELTS组织提供考试格式参考
- 感谢教育测试服务机构提供评分标准指导

---

**⭐ 如果这个项目对你有帮助，请给我们一个Star！**
