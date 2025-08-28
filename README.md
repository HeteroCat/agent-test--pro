# 🚀 API Tester Pro

一个现代化、功能强大的API测试工具，提供优雅的Web界面和高效的批量测试功能。

## ✨ 特色功能

### 🎯 核心功能
- **智能API测试** - 支持GET、POST、PUT、DELETE等多种HTTP方法
- **批量测试** - 一键测试多个API端点，提高测试效率
- **实时响应** - 即时显示API响应结果和状态码
- **自动保存** - 测试结果自动保存，支持历史记录查看
- **灵活配置** - 支持自定义请求头、认证token等参数

### 🎨 现代化界面
- **响应式设计** - 完美适配桌面端、平板和移动设备
- **深色/浅色主题** - 支持主题切换，保护视力
- **直观操作** - 简洁美观的用户界面，操作简单直观
- **实时反馈** - 加载动画和状态提示，提升用户体验

## 🛠️ 安装方式

### 方式一：直接安装
```bash
pip install -e . -i https://mirrors.aliyun.com/pypi/simple/
```

### 方式二：开发环境
```bash
git clone https://github.com/HeteroCat/agent-test--pro.git
cd agent-test--pro
pip install -e .
```

## 🚀 快速开始

### 启动Web界面
```bash
# 启动Web服务器
api-tester --web

# 或者指定端口
api-tester --web --port 8080
```

访问 `http://localhost:8080` 即可使用Web界面进行API测试。

### 命令行批量测试
```bash
# 测试指定目录下的所有JSON文件
api-tester --test-dir /path/to/json/files \
           --output-dir results \
           --url https://your-api.com/endpoint \
           --token your-auth-token

# 测试单个JSON文件
api-tester --input-file test.json \
           --output-file result.json \
           --url https://api.example.com/test
```

## 📖 使用指南

### Web界面功能

1. **首页** - 项目介绍和快速导航
2. **API测试** - 单个API端点测试
   - 输入API URL和请求参数
   - 选择HTTP方法
   - 设置请求头和认证信息
   - 查看实时响应结果

3. **批量测试** - 多个API端点批量测试
   - 上传JSON测试文件
   - 批量执行测试
   - 下载测试报告

### JSON文件格式

测试用的JSON文件应遵循以下格式：

```json
{
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer your-token"
  },
  "data": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

## 🔧 配置选项

### 命令行参数

| 参数 | 描述 | 示例 |
|------|------|------|
| `--web` | 启动Web界面 | `api-tester --web` |
| `--port` | 指定端口号 | `--port 8080` |
| `--test-dir` | 测试文件目录 | `--test-dir ./tests` |
| `--output-dir` | 结果输出目录 | `--output-dir ./results` |
| `--url` | API端点URL | `--url https://api.example.com` |
| `--token` | 认证Token | `--token your-auth-token` |

## 🎯 技术栈

- **后端**: Python Flask
- **前端**: HTML5 + CSS3 + JavaScript
- **样式**: Tailwind CSS
- **图标**: Font Awesome
- **字体**: Google Fonts (Noto Sans SC)

## 📝 更新日志

### v2.0.0 (最新)
- ✨ 全新的现代化Web界面
- 🎨 支持深色/浅色主题切换
- 📱 完全响应式设计
- 🚀 优化的用户体验和交互动画
- 🔧 改进的批量测试功能

### v1.0.0
- 🎉 初始版本发布
- ⚡ 基础API测试功能
- 📊 命令行批量测试

## 🤝 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目！

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👨‍💻 作者

**HeteroCat** - *项目维护者*

- GitHub: [@HeteroCat](https://github.com/HeteroCat)
- 项目链接: [https://github.com/HeteroCat/agent-test--pro](https://github.com/HeteroCat/agent-test--pro)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！