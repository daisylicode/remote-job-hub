# 远程工作机会汇总

这是一个展示多个远程工作平台职位信息的静态网页应用。

## 功能特点

- 🌍 **多平台数据整合**: 整合了来自4个知名远程工作平台的数据
  - RemoteOK
  - Remote.co
  - WeWorkRemotely
  - Working Nomads

- 🔍 **智能搜索**: 支持按职位标题和公司名称搜索

- 🏷️ **来源筛选**: 可以按数据来源筛选职位

- 📊 **实时统计**: 显示总职位数、公司数量等统计信息

- 📱 **响应式设计**: 完美适配桌面和移动设备

- 🎨 **现代UI**: 美观的渐变背景和卡片式布局

## 使用方法

### 本地运行
1. **直接打开**: 在浏览器中打开 `index.html` 文件

2. **本地服务器**: 为了更好的体验，建议使用本地服务器
   ```bash
   # 使用Python
   python -m http.server 8000
   
   # 使用Node.js
   npx serve .
   
   # 使用PHP
   php -S localhost:8000
   ```

3. **访问页面**: 打开浏览器访问 `http://localhost:8000`

### 在线部署
这个项目已经配置好可以直接部署到 GitHub Pages：

1. **推送到 GitHub**: 按照 [DEPLOY.md](DEPLOY.md) 中的说明操作
2. **启用 GitHub Pages**: 在仓库设置中启用 Pages 功能
3. **自动更新**: 配置了 GitHub Actions 每天自动更新数据

**在线地址**: `https://你的用户名.github.io/remote-job-hub`

## 数据来源

页面会自动加载 `results/` 目录下的JSON文件：
- `remoteok.json` - RemoteOK平台数据
- `remoteco.json` - Remote.co平台数据  
- `weworkremotely.json` - WeWorkRemotely平台数据
- `workingnomads.json` - Working Nomads平台数据

## 技术特点

- **纯前端实现**: 无需后端服务器，完全静态
- **数据标准化**: 自动处理不同平台的数据格式差异
- **性能优化**: 异步加载数据，支持大量职位信息
- **用户体验**: 悬停效果、加载动画、错误处理

## 自定义

你可以通过修改以下部分来自定义页面：

- **样式**: 编辑 `<style>` 标签中的CSS
- **数据源**: 修改JavaScript中的 `sources` 数组
- **筛选条件**: 在 `filterJobs()` 函数中添加新的筛选逻辑

## 浏览器兼容性

支持所有现代浏览器：
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 许可证

MIT License 