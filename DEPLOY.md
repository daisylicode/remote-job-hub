# GitHub Pages 部署指南

## 1. 准备工作

### 1.1 创建 GitHub 仓库
1. 在 GitHub 上创建一个新的仓库，例如：`remote-job-hub`
2. 将本地代码推送到仓库：
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/remote-job-hub.git
git push -u origin main
```

### 1.2 设置 Google Analytics
1. 访问 [Google Analytics](https://analytics.google.com/)
2. 创建新账户和媒体资源
3. 获取测量 ID（格式：G-XXXXXXXXXX）
4. 在 `index.html` 中替换 `GA_MEASUREMENT_ID` 为你的实际测量 ID

## 2. 启用 GitHub Pages

### 2.1 配置 GitHub Pages
1. 进入你的 GitHub 仓库
2. 点击 "Settings" 标签
3. 在左侧菜单中找到 "Pages"
4. 在 "Source" 部分选择 "Deploy from a branch"
5. 选择 "main" 分支和 "/ (root)" 文件夹
6. 点击 "Save"

### 2.2 等待部署
- GitHub Pages 通常需要几分钟时间部署
- 部署完成后，你的网站将在 `https://你的用户名.github.io/remote-job-hub` 上线

## 3. 自定义域名（可选）

### 3.1 购买域名
- 在域名注册商处购买域名（如：`remotejobs.com`）

### 3.2 配置 DNS
1. 在域名注册商处添加 CNAME 记录：
   - 名称：`@` 或 `www`
   - 值：`你的用户名.github.io`

### 3.3 在 GitHub 中设置
1. 在仓库 Settings > Pages 中
2. 在 "Custom domain" 字段输入你的域名
3. 保存设置
4. 在仓库根目录创建 `CNAME` 文件，内容为你的域名

## 4. 更新网站

### 4.1 更新数据
```bash
# 运行爬虫脚本更新数据
python3 remoteok_scrape.py
python3 remoteco_scrape.py
python3 weworkremotely_scrape.py
python3 workingnomads_scrape.py

# 提交更新
git add results/
git commit -m "Update job data"
git push
```

### 4.2 自动更新（可选）
可以设置 GitHub Actions 来自动运行爬虫脚本：

1. 创建 `.github/workflows/update-jobs.yml` 文件
2. 配置定时任务（如每天运行一次）
3. 自动提交更新的数据

## 5. 性能优化

### 5.1 启用缓存
GitHub Pages 会自动设置适当的缓存头

### 5.2 压缩资源
- 图片使用 WebP 格式
- 启用 Gzip 压缩（GitHub Pages 自动处理）

### 5.3 CDN
GitHub Pages 使用全球 CDN，确保快速访问

## 6. 监控和分析

### 6.1 Google Analytics
- 查看访问量、用户来源、页面停留时间等
- 设置转化目标（如职位点击）

### 6.2 GitHub Pages 统计
- 在仓库 Settings > Pages 中查看访问统计

## 7. 故障排除

### 7.1 常见问题
- **404 错误**: 检查文件路径和大小写
- **样式问题**: 确保 CSS 文件正确引用
- **数据不显示**: 检查 JSON 文件格式

### 7.2 调试技巧
- 使用浏览器开发者工具检查控制台错误
- 验证 JSON 文件格式
- 检查网络请求状态

## 8. 安全考虑

### 8.1 内容安全策略
考虑添加 CSP 头来增强安全性

### 8.2 数据隐私
- 确保不收集敏感用户信息
- 遵守 GDPR 等隐私法规

## 9. 扩展功能

### 9.1 添加更多功能
- 职位收藏功能
- 邮件订阅
- 搜索历史
- 移动应用

### 9.2 集成其他服务
- 添加 RSS 订阅
- 集成社交媒体分享
- 添加评论系统

---

**注意**: 记得将 `GA_MEASUREMENT_ID` 替换为你的实际 Google Analytics 测量 ID！ 