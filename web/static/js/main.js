class TJWApp {
    constructor() {
        this.currentModule = null;
        this.modules = [
            { id: 1001, key: 'dashboard', name: '仪表盘', icon: '📊', description: '系统概览和快速访问' },
            { id: 1002, key: 'sfz', name: '身份证工具', icon: '🆔', description: '身份证生成、验证、归属地查询', stats: { count: 10000, today: 128 } },
            { id: 1003, key: 'tools', name: '实用工具', icon: '🔧', description: '各种实用小工具集合', stats: { count: 15, today: 3 } },
            { id: 1004, key: 'settings', name: '系统设置', icon: '⚙️', description: '系统配置和个性化设置' }
        ];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.handleURLParams();
    }

    // 解析URL参数
    getURLParams() {
        const params = new URLSearchParams(window.location.search);
        const idParam = params.get('id');
        return idParam ? parseInt(idParam) : null;
    }

    // 处理URL参数，自动跳转模块
    handleURLParams() {
        const moduleId = this.getURLParams();
        if (moduleId) {
            const module = this.modules.find(m => m.id === moduleId);
            if (module) {
                setTimeout(() => {
                    this.loadModule(module.key);
                }, 100);
                return;
            }
        }
        // 默认加载仪表盘
        this.loadDashboard();
    }

    setupEventListeners() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const moduleKey = e.currentTarget.dataset.module;
                this.loadModule(moduleKey);
            });
        });

        document.querySelector('.menu-toggle').addEventListener('click', () => {
            document.querySelector('.sidebar').classList.toggle('open');
        });

        document.addEventListener('click', (e) => {
            const card = e.target.closest('.module-card');
            if (card) {
                const moduleKey = card.dataset.module;
                this.loadModule(moduleKey);
            }
        });
    }

    async loadModule(moduleKey) {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        const activeNav = document.querySelector(`[data-module="${moduleKey}"]`);
        if (activeNav) {
            activeNav.classList.add('active');
        }

        const module = this.modules.find(m => m.key === moduleKey);
        if (module) {
            document.querySelector('.header-title').textContent = module.name;
            // 更新URL参数
            this.updateURL(module.id);
        }

        const contentArea = document.querySelector('.page-content');
        
        switch (moduleKey) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'sfz':
                await this.loadSFZModule();
                break;
            case 'tools':
                this.loadToolsModule();
                break;
            case 'settings':
                this.loadSettingsModule();
                break;
            default:
                this.loadDashboard();
        }

        this.currentModule = moduleKey;
        document.querySelector('.sidebar').classList.remove('open');
    }

    // 更新URL参数（不刷新页面）
    updateURL(moduleId) {
        const url = new URL(window.location);
        if (moduleId && moduleId !== 1001) { // 仪表盘不显示参数
            url.searchParams.set('id', moduleId.toString());
        } else {
            url.searchParams.delete('id');
        }
        window.history.pushState({ moduleId }, '', url);
    }

    loadDashboard() {
        const contentArea = document.querySelector('.page-content');
        contentArea.innerHTML = `
            <div class="dashboard">
                <div class="dashboard-header">
                    <h2>欢迎使用 TJW 工具平台</h2>
                    <p>一站式工具管理平台，轻松管理您的各种工具和服务</p>
                </div>
                
                <div class="quick-stats">
                    <div class="stat-card">
                        <div class="stat-icon">📦</div>
                        <div class="stat-content">
                            <div class="value">${this.modules.length}</div>
                            <div class="label">可用模块</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">👥</div>
                        <div class="stat-content">
                            <div class="value">1</div>
                            <div class="label">当前用户</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">🚀</div>
                        <div class="stat-content">
                            <div class="value">100%</div>
                            <div class="label">服务状态</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">📅</div>
                        <div class="stat-content">
                            <div class="value">${this.getCurrentDate()}</div>
                            <div class="label">当前日期</div>
                        </div>
                    </div>
                </div>

                <div class="modules-grid">
                    ${this.modules.map(module => `
                        <div class="module-card" data-module="${module.key}">
                            <div class="module-icon">${module.icon}</div>
                            <div class="module-name">${module.name}</div>
                            <div class="module-desc">${module.description}</div>
                            ${module.stats ? `
                                <div class="module-stats">
                                    <div class="stat-item">
                                        <div class="stat-value">${module.stats.count}</div>
                                        <div class="stat-label">总使用</div>
                                    </div>
                                    <div class="stat-item">
                                        <div class="stat-value">${module.stats.today}</div>
                                        <div class="stat-label">今日</div>
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>

                <div style="margin-top: 32px;">
                    <div class="settings-section">
                        <h4>🔗 快捷访问链接</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-top: 16px;">
                            ${this.modules.map(module => `
                                <div class="settings-item">
                                    <label>${module.icon} ${module.name}</label>
                                    <value style="font-family: monospace; font-size: 0.8rem; word-break: break-all;">
                                        /id/${module.id}
                                    </value>
                                </div>
                            `).join('')}
                        </div>
                        <p style="margin-top: 16px; font-size: 0.85rem; color: var(--text-muted);">
                            💡 提示：您可以使用 <code>/id/{模块ID}</code> 或 <code>/?id={模块ID}</code> 快速访问对应模块
                        </p>
                    </div>
                </div>
            </div>
        `;
    }

    async loadSFZModule() {
        const contentArea = document.querySelector('.page-content');
        contentArea.innerHTML = `
            <div class="module-container">
                <div class="module-container-header">
                    <h2 class="module-container-title">🆔 身份证工具</h2>
                    <div class="module-container-actions">
                        <button class="header-btn secondary" onclick="tjwApp.loadModule('dashboard')">返回</button>
                    </div>
                </div>
                <div id="sfz-content"></div>
            </div>
        `;
        await this.loadSFZContent();
    }

    async loadSFZContent() {
        const sfzContent = document.querySelector('#sfz-content');
        sfzContent.innerHTML = `
            <div style="max-width: 600px; margin: 0 auto;">
                <!-- 功能切换图标 -->
                <div class="sfz-toolbar">
                    <div class="sfz-toolbar-item active" onclick="tjwApp.switchSFZTab('generate')" title="生成身份证">
                        <span>🎯</span>
                    </div>
                    <div class="sfz-toolbar-item" onclick="tjwApp.switchSFZTab('batch')" title="批量生成">
                        <span>🔄</span>
                    </div>
                    <div class="sfz-toolbar-item" onclick="tjwApp.switchSFZTab('verify')" title="验证身份证">
                        <span>✅</span>
                    </div>
                    <div class="sfz-toolbar-item" onclick="tjwApp.switchSFZTab('region')" title="查询归属地">
                        <span>📍</span>
                    </div>
                </div>

                <!-- 生成单个身份证 -->
                <div id="sfz-tab-generate" class="sfz-tab-content active">
                    <div class="sfz-card">
                        <h3>🆔 生成身份证</h3>
                        <div class="sfz-form-group">
                            <label for="sfz-sex">性别选择</label>
                            <select id="sfz-sex" onkeydown="if(event.keyCode===13) tjwApp.sfzGenerate()">
                                <option value="">🎲 随机</option>
                                <option value="male">👨 男</option>
                                <option value="female">👩 女</option>
                            </select>
                        </div>
                        
                        <div class="sfz-advanced-toggle" onclick="tjwApp.toggleAdvancedOptions()">
                            <span>⚙️ 高级选项</span>
                            <span class="sfz-advanced-arrow">▼</span>
                        </div>
                        <div id="sfz-advanced-options" class="sfz-advanced-options">
                            <div class="sfz-form-group">
                                <label for="sfz-region-code">地区编码（6位）</label>
                                <input type="text" id="sfz-region-code" placeholder="如110000表示北京" onkeydown="if(event.keyCode===13) tjwApp.sfzGenerate()">
                            </div>
                            <div class="sfz-form-group">
                                <label for="sfz-birth-date">出生日期</label>
                                <input type="date" id="sfz-birth-date" onkeydown="if(event.keyCode===13) tjwApp.sfzGenerate()">
                            </div>
                        </div>
                        
                        <button class="sfz-btn" onclick="tjwApp.sfzGenerate()">
                            <span>🎯 生成身份证</span>
                        </button>
                        <div id="sfz-generate-result"></div>
                    </div>
                </div>

                <!-- 批量生成 -->
                <div id="sfz-tab-batch" class="sfz-tab-content">
                    <div class="sfz-card">
                        <h3>🔄 批量生成</h3>
                        <div class="sfz-form-group">
                            <label for="sfz-batch-count">生成数量 (1-100)</label>
                            <input type="number" id="sfz-batch-count" value="5" min="1" max="100" onkeydown="if(event.keyCode===13) tjwApp.sfzBatchGenerate()">
                        </div>
                        <button class="sfz-btn" onclick="tjwApp.sfzBatchGenerate()">
                            <span>🔄 批量生成</span>
                        </button>
                        <div id="sfz-batch-result"></div>
                    </div>
                </div>

                <!-- 验证身份证 -->
                <div id="sfz-tab-verify" class="sfz-tab-content">
                    <div class="sfz-card">
                        <h3>✅ 验证身份证</h3>
                        <div class="sfz-form-group">
                            <label for="sfz-verify">输入身份证号</label>
                            <input type="text" id="sfz-verify" placeholder="请输入18位身份证号" onkeydown="if(event.keyCode===13) tjwApp.sfzVerify()">
                        </div>
                        <button class="sfz-btn" onclick="tjwApp.sfzVerify()">
                            <span>✅ 验证</span>
                        </button>
                        <button class="sfz-btn sfz-btn-secondary" onclick="tjwApp.sfzRandomTest()">
                            <span>🎲 随机测试</span>
                        </button>
                        <div id="sfz-verify-result"></div>
                    </div>
                </div>

                <!-- 查询归属地 -->
                <div id="sfz-tab-region" class="sfz-tab-content">
                    <div class="sfz-card">
                        <h3>📍 查询归属地</h3>
                        <div class="sfz-form-group">
                            <label for="sfz-region-input">身份证号（至少前6位）</label>
                            <input type="text" id="sfz-region-input" placeholder="请输入身份证号前6位或完整号码" onkeydown="if(event.keyCode===13) tjwApp.sfzGetRegion()">
                        </div>
                        <button class="sfz-btn" onclick="tjwApp.sfzGetRegion()">
                            <span>📍 查询归属地</span>
                        </button>
                        <div id="sfz-region-result"></div>
                    </div>
                </div>
            </div>
        `;
    }

    switchSFZTab(tabName) {
        document.querySelectorAll('.sfz-toolbar-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelectorAll('.sfz-tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        event.currentTarget.classList.add('active');
        document.getElementById(`sfz-tab-${tabName}`).classList.add('active');
    }

    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.toggle('collapsed');
    }

    toggleAdvancedOptions() {
        const advancedOptions = document.getElementById('sfz-advanced-options');
        const arrow = document.querySelector('.sfz-advanced-arrow');
        advancedOptions.classList.toggle('show');
        arrow.textContent = advancedOptions.classList.contains('show') ? '▲' : '▼';
    }

    async sfzGenerate() {
        const sex = document.getElementById('sfz-sex').value;
        const regionCode = document.getElementById('sfz-region-code').value.trim();
        const birthDate = document.getElementById('sfz-birth-date').value;
        
        let url = '/api/sfz/generate';
        const params = [];
        if (sex) params.push(`sex=${sex}`);
        if (regionCode) params.push(`region=${regionCode}`);
        if (birthDate) params.push(`birth_date=${birthDate.replace(/-/g, '')}`);
        
        if (params.length > 0) url += '?' + params.join('&');
        
        const result = await this.fetchAPI(url);
        this.showSFZResult('sfz-generate-result', result, true);
    }

    async sfzBatchGenerate() {
        const count = document.getElementById('sfz-batch-count').value;
        if (!count || count < 1 || count > 100) {
            this.showSFZResult('sfz-batch-result', { success: false, message: '请输入1-100之间的数量' }, false);
            return;
        }
        const result = await this.fetchAPI(`/api/sfz/generate/batch?count=${count}`);
        this.showSFZResult('sfz-batch-result', result, false);
    }

    async sfzVerify() {
        const idNumber = document.getElementById('sfz-verify').value.trim().replace(/\s/g, '');
        if (!idNumber) {
            this.showSFZResult('sfz-verify-result', { success: false, message: '请输入身份证号' }, false);
            return;
        }
        if (idNumber.length !== 18) {
            this.showSFZResult('sfz-verify-result', { success: false, message: '身份证号必须为18位' }, false);
            return;
        }
        const result = await this.fetchAPI(`/api/sfz/verify?id_number=${encodeURIComponent(idNumber)}`);
        this.showSFZResult('sfz-verify-result', result, true);
    }

    async sfzGetRegion() {
        const idNumber = document.getElementById('sfz-region-input').value.trim().replace(/\s/g, '');
        if (!idNumber || idNumber.length < 6) {
            this.showSFZResult('sfz-region-result', { success: false, message: '请输入至少6位' }, false);
            return;
        }
        const result = await this.fetchAPI(`/api/sfz/region?id_number=${encodeURIComponent(idNumber)}`);
        this.showSFZResult('sfz-region-result', result, false);
    }

    async sfzRandomTest() {
        const genResult = await this.fetchAPI('/api/sfz/generate');
        if (genResult.success) {
            document.getElementById('sfz-verify').value = genResult.data.id_number;
            await this.sfzVerify();
        }
    }

    showSFZResult(elementId, result, showCard) {
        const element = document.getElementById(elementId);
        if (!element) return;

        if (!result.success) {
            element.innerHTML = `
                <div class="sfz-result error">
                    <div class="sfz-result-header">
                        <span>❌</span>
                        <strong>操作失败</strong>
                    </div>
                    <div>${result.message}</div>
                </div>
            `;
            return;
        }

        if (showCard && result.data) {
            const data = result.data;
            element.innerHTML = `
                <div class="sfz-result success">
                    <div class="sfz-result-header">
                        <span>✅</span>
                        <strong>${result.message}</strong>
                    </div>
                </div>
                <div class="sfz-id-card">
                    <div class="sfz-id-number">${data.id_number}</div>
                    <div class="sfz-id-details">
                        <div class="sfz-id-detail">
                            <label>归属地</label>
                            <value>${data.region}</value>
                        </div>
                        <div class="sfz-id-detail">
                            <label>出生日期</label>
                            <value>${data.birth_date}</value>
                        </div>
                        <div class="sfz-id-detail">
                            <label>性别</label>
                            <value>${data.gender}</value>
                        </div>
                        <div class="sfz-id-detail">
                            <label>验证状态</label>
                            <value>${data.verified ? '✓ 已验证' : '✗ 未验证'}</value>
                        </div>
                    </div>
                </div>
            `;
        } else if (result.data && Array.isArray(result.data)) {
            let items = '';
            result.data.forEach((item, index) => {
                items += `
                    <div class="sfz-batch-item">
                        <span>${item.id_number}</span>
                        <span style="color: var(--text-muted); font-size: 0.85rem;">${item.region}</span>
                    </div>
                `;
            });
            element.innerHTML = `
                <div class="sfz-result success">
                    <div class="sfz-result-header">
                        <span>✅</span>
                        <strong>${result.message}</strong>
                    </div>
                </div>
                <div class="sfz-batch-results">${items}</div>
            `;
        } else if (result.data) {
            const data = result.data;
            element.innerHTML = `
                <div class="sfz-result info">
                    <div class="sfz-result-header">
                        <span>📍</span>
                        <strong>${result.message}</strong>
                    </div>
                    <div class="sfz-id-card">
                        <div class="sfz-id-details">
                            <div class="sfz-id-detail">
                                <label>地区编码</label>
                                <value>${data.id_prefix}</value>
                            </div>
                            <div class="sfz-id-detail">
                                <label>归属地</label>
                                <value>${data.region}</value>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    loadToolsModule() {
        const contentArea = document.querySelector('.page-content');
        contentArea.innerHTML = `
            <div class="module-container">
                <div class="module-container-header">
                    <h2 class="module-container-title">🔧 实用工具</h2>
                    <div class="module-container-actions">
                        <button class="header-btn secondary" onclick="tjwApp.loadModule('dashboard')">返回</button>
                    </div>
                </div>
                <div style="text-align: center; padding: 60px 20px;">
                    <div style="font-size: 5rem; margin-bottom: 24px; opacity: 0.8;">🛠️</div>
                    <h3 style="font-size: 1.6rem; margin-bottom: 12px;">工具模块开发中</h3>
                    <p style="color: var(--text-secondary); font-size: 1.1rem;">更多实用工具即将上线，敬请期待！</p>
                </div>
            </div>
        `;
    }

    loadSettingsModule() {
        const contentArea = document.querySelector('.page-content');
        contentArea.innerHTML = `
            <div class="module-container">
                <div class="module-container-header">
                    <h2 class="module-container-title">⚙️ 系统设置</h2>
                    <div class="module-container-actions">
                        <button class="header-btn secondary" onclick="tjwApp.loadModule('dashboard')">返回</button>
                    </div>
                </div>
                <div style="max-width: 600px; margin: 0 auto;">
                    <div class="settings-section">
                        <h4>📝 系统信息</h4>
                        <div class="settings-grid">
                            <div class="settings-item">
                                <label>系统名称</label>
                                <value>TJW 工具平台</value>
                            </div>
                            <div class="settings-item">
                                <label>版本号</label>
                                <value>v1.0.0</value>
                            </div>
                            <div class="settings-item">
                                <label>API地址</label>
                                <value>/api</value>
                            </div>
                            <div class="settings-item">
                                <label>运行状态</label>
                                <value style="color: #22c55e;">✓ 正常</value>
                            </div>
                        </div>
                    </div>
                    <div class="settings-section">
                        <h4>🔗 快速链接</h4>
                        <div class="settings-links">
                            <a href="/docs" target="_blank" class="settings-link">
                                <span>📖</span>
                                <span>Swagger API 文档</span>
                            </a>
                            <a href="/redoc" target="_blank" class="settings-link">
                                <span>📘</span>
                                <span>Redoc API 文档</span>
                            </a>
                            <a href="/health" target="_blank" class="settings-link">
                                <span>🏥</span>
                                <span>健康检查</span>
                            </a>
                        </div>
                    </div>
                    <div class="settings-section">
                        <h4>🔢 模块ID映射</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px;">
                            ${this.modules.map(module => `
                                <div class="settings-item">
                                    <label>${module.icon} ${module.name}</label>
                                    <value style="color: var(--accent-purple);">ID: ${module.id}</value>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async fetchAPI(url) {
        try {
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            return { success: false, message: '网络错误，请检查服务是否启动' };
        }
    }

    getCurrentDate() {
        const now = new Date();
        return `${now.getMonth() + 1}/${now.getDate()}`;
    }
}

let tjwApp;

document.addEventListener('DOMContentLoaded', () => {
    tjwApp = new TJWApp();
});

// 监听浏览器前进/后退
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.moduleId) {
        const module = tjwApp.modules.find(m => m.id === event.state.moduleId);
        if (module) {
            tjwApp.loadModule(module.key);
        }
    } else {
        tjwApp.loadModule('dashboard');
    }
});