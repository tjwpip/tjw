let currentUser = null;

const TJWUI = {
    confirmCallback: null,
    
    show(options) {
        const modal = document.getElementById('tjw-modal');
        const icon = document.getElementById('tjw-modal-icon');
        const title = document.getElementById('tjw-modal-title');
        const message = document.getElementById('tjw-modal-message');
        const cancelBtn = document.getElementById('tjw-modal-btn-cancel');
        const confirmBtn = document.getElementById('tjw-modal-btn-confirm');
        
        const type = options.type || 'info';
        title.textContent = options.title || '提示';
        message.textContent = options.message || '';
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: '📢',
            confirm: '❓'
        };
        
        icon.textContent = icons[type] || icons.info;
        icon.className = `tjw-modal-icon ${type}`;
        
        if (options.showCancel === false) {
            cancelBtn.style.display = 'none';
        } else {
            cancelBtn.style.display = 'inline-flex';
        }
        
        if (options.cancelText) {
            cancelBtn.textContent = options.cancelText;
        } else {
            cancelBtn.textContent = '取消';
        }
        
        if (options.confirmText) {
            confirmBtn.textContent = options.confirmText;
        } else {
            confirmBtn.textContent = '确定';
        }
        
        this.confirmCallback = options.onConfirm || null;
        
        modal.classList.remove('hidden');
    },
    
    hide() {
        document.getElementById('tjw-modal').classList.add('hidden');
    },
    
    confirm() {
        if (this.confirmCallback) {
            this.confirmCallback();
        }
        this.hide();
    },
    
    success(message, options = {}) {
        this.show({
            type: 'success',
            title: options.title || '成功',
            message: message,
            showCancel: false,
            confirmText: options.confirmText || '确定',
            onConfirm: options.onConfirm
        });
    },
    
    error(message, options = {}) {
        this.show({
            type: 'error',
            title: options.title || '错误',
            message: message,
            showCancel: false,
            confirmText: options.confirmText || '确定',
            onConfirm: options.onConfirm
        });
    },
    
    warning(message, options = {}) {
        this.show({
            type: 'warning',
            title: options.title || '警告',
            message: message,
            showCancel: options.showCancel !== undefined ? options.showCancel : true,
            confirmText: options.confirmText || '确定',
            onConfirm: options.onConfirm
        });
    },
    
    info(message, options = {}) {
        this.show({
            type: 'info',
            title: options.title || '提示',
            message: message,
            showCancel: false,
            confirmText: options.confirmText || '确定',
            onConfirm: options.onConfirm
        });
    },
    
    confirmDialog(message, options = {}) {
        this.show({
            type: 'confirm',
            title: options.title || '确认',
            message: message,
            showCancel: true,
            cancelText: options.cancelText || '取消',
            confirmText: options.confirmText || '确定',
            onConfirm: options.onConfirm
        });
    }
};

async function login() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    
    if (!username || !password) {
        showLoginError('请输入用户名和密码');
        return;
    }
    
    try {
        const response = await fetch(`/api/auth/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {
            method: 'POST'
        });
        const result = await response.json();
        
        if (result.success) {
            currentUser = result.data;
            document.getElementById('current-user').textContent = currentUser.username;
            document.getElementById('login-container').classList.add('hidden');
            document.getElementById('app-container').classList.remove('hidden');
            
            const loginError = document.getElementById('login-error');
            loginError.classList.remove('show');
            
            const loginData = {
                user: currentUser,
                loginTime: Date.now(),
                expiresIn: 24 * 60 * 60 * 1000
            };
            localStorage.setItem('tjw_login', JSON.stringify(loginData));
            
            tjwApp = new TJWApp();
        } else {
            showLoginError(result.message);
        }
    } catch (error) {
        showLoginError('登录失败，请检查网络连接');
        console.error('Login error:', error);
    }
}

function showLoginError(message) {
    TJWUI.error(message);
}

function showResetGuide() {
    document.getElementById('reset-guide-modal').classList.add('show');
}

function hideResetGuide() {
    document.getElementById('reset-guide-modal').classList.remove('show');
}

function showChangePassword() {
    document.getElementById('change-password-modal').classList.add('show');
}

function hideChangePassword() {
    document.getElementById('change-password-modal').classList.remove('show');
    document.getElementById('change-password-error').classList.remove('show');
    document.getElementById('change-password-form').reset();
}

async function changePassword() {
    const oldPassword = document.getElementById('old-password').value.trim();
    const newPassword = document.getElementById('new-password').value.trim();
    const confirmPassword = document.getElementById('confirm-password').value.trim();
    
    if (!oldPassword || !newPassword || !confirmPassword) {
        TJWUI.warning('请填写所有字段');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        TJWUI.warning('两次输入的密码不一致');
        return;
    }

    if (newPassword.length < 6) {
        TJWUI.warning('新密码长度至少6位');
        return;
    }
    
    try {
        const response = await fetch(`/api/auth/change-password?username=${encodeURIComponent(currentUser.username)}&old_password=${encodeURIComponent(oldPassword)}&new_password=${encodeURIComponent(newPassword)}`, {
            method: 'POST'
        });
        const result = await response.json();
        
        if (result.success) {
            TJWUI.success('密码修改成功，请重新登录', {
                onConfirm: function() {
                    hideChangePassword();
                    logout();
                }
            });
        } else {
            TJWUI.error(result.message);
        }
    } catch (error) {
        TJWUI.error('修改失败，请检查网络连接');
        console.error('Change password error:', error);
    }
}

function logout() {
    TJWUI.confirmDialog('确定要退出登录吗？', {
        title: '退出确认',
        confirmText: '确定退出',
        cancelText: '取消',
        onConfirm: function() {
            currentUser = null;
            localStorage.removeItem('tjw_login');
            document.getElementById('app-container').classList.add('hidden');
            document.getElementById('login-container').classList.remove('hidden');
            document.getElementById('login-form').reset();
            document.getElementById('login-error').classList.remove('show');
            TJWUI.success('已安全退出登录');
        }
    });
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const icon = document.getElementById('collapse-icon');
    const btn = document.getElementById('sidebar-collapse-btn');
    const overlay = document.getElementById('sidebar-overlay');
    
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        sidebar.classList.toggle('expanded');
        
        if (overlay) {
            overlay.classList.toggle('active');
        }
        
        if (sidebar.classList.contains('expanded')) {
            icon.textContent = '➖';
            btn.title = '收起侧边栏';
        } else {
            icon.textContent = '➕';
            btn.title = '展开侧边栏';
        }
    } else {
        sidebar.classList.toggle('collapsed');
        
        if (sidebar.classList.contains('collapsed')) {
            icon.textContent = '➕';
            btn.title = '展开侧边栏';
        } else {
            icon.textContent = '➖';
            btn.title = '折叠侧边栏';
        }
    }
}

function closeSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const icon = document.getElementById('collapse-icon');
    const btn = document.getElementById('sidebar-collapse-btn');
    const overlay = document.getElementById('sidebar-overlay');
    
    sidebar.classList.remove('expanded');
    if (overlay) {
        overlay.classList.remove('active');
    }
    icon.textContent = '➕';
    btn.title = '展开侧边栏';
}

function toggleTheme() {
    const icon = document.getElementById('theme-toggle-btn');
    const html = document.documentElement;
    
    if (html.classList.contains('light-theme')) {
        html.classList.remove('light-theme');
        icon.textContent = '🌙';
        icon.title = '切换到明亮主题';
        localStorage.setItem('tjw_theme', 'dark');
    } else {
        html.classList.add('light-theme');
        icon.textContent = '☀️';
        icon.title = '切换到暗黑主题';
        localStorage.setItem('tjw_theme', 'light');
    }
}

function checkAutoLogin() {
    const loginDataStr = localStorage.getItem('tjw_login');
    if (!loginDataStr) return false;
    
    try {
        const loginData = JSON.parse(loginDataStr);
        const now = Date.now();
        
        if (loginData.loginTime + loginData.expiresIn > now) {
            currentUser = loginData.user;
            document.getElementById('current-user').textContent = currentUser.username;
            document.getElementById('login-container').classList.add('hidden');
            document.getElementById('app-container').classList.remove('hidden');
            tjwApp = new TJWApp();
            return true;
        } else {
            localStorage.removeItem('tjw_login');
            return false;
        }
    } catch (error) {
        localStorage.removeItem('tjw_login');
        return false;
    }
}

function loadTheme() {
    const savedTheme = localStorage.getItem('tjw_theme') || 'dark';
    const icon = document.getElementById('theme-toggle-btn');
    
    if (savedTheme === 'light') {
        document.documentElement.classList.add('light-theme');
        icon.textContent = '☀️';
        icon.title = '切换到暗黑主题';
    } else {
        icon.textContent = '🌙';
        icon.title = '切换到明亮主题';
    }
}

let menuData = null;

async function loadMenu() {
    try {
        const response = await fetch('/static/data/menus.json');
        menuData = await response.json();
        renderMenu(menuData);
    } catch (error) {
        console.error('Failed to load menu data:', error);
    }
}

function renderMenu(data) {
    const nav = document.getElementById('sidebar-nav');
    nav.innerHTML = '';
    
    data.groups.forEach(group => {
        const groupElement = document.createElement('div');
        groupElement.className = 'menu-group';
        
        const header = document.createElement('div');
        header.className = 'menu-group-header';
        header.innerHTML = `
            <span class="group-icon">${group.icon}</span>
            <span class="group-name">${group.name}</span>
            <span class="group-count">${group.items.length}</span>
        `;
        
        header.addEventListener('click', () => {
            const items = groupElement.querySelector('.menu-group-items');
            items.classList.toggle('collapsed');
        });
        
        groupElement.appendChild(header);
        
        const itemsContainer = document.createElement('div');
        itemsContainer.className = 'menu-group-items';
        
        group.items.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = `nav-item${item.disabled ? ' disabled' : ''}`;
            itemElement.dataset.module = item.key;
            itemElement.title = item.description;
            
            if (!item.disabled) {
                itemElement.addEventListener('click', () => handleMenuClick(item));
            }
            
            itemElement.innerHTML = `
                <span class="nav-item-icon">${item.icon}</span>
                <span class="menu-item-id">${item.id}</span>
                <span class="nav-item-text">${item.name}</span>
            `;
            
            itemsContainer.appendChild(itemElement);
        });
        
        groupElement.appendChild(itemsContainer);
        nav.appendChild(groupElement);
    });
    
    const dashboardItem = nav.querySelector('[data-module="dashboard"]');
    if (dashboardItem) {
        dashboardItem.classList.add('active');
    }
}

function handleMenuClick(item) {
    if (item.action === 'open_url') {
        window.open(item.url, '_blank');
        return;
    }
    
    if (item.action === 'show_modal') {
        if (item.modal === 'change_password') {
            showChangePassword();
        }
        return;
    }
    
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(navItem => navItem.classList.remove('active'));
    
    const currentItem = document.querySelector(`[data-module="${item.key}"]`);
    if (currentItem) {
        currentItem.classList.add('active');
    }
    
    if (tjwApp) {
        tjwApp.loadModule(item.key);
    }
}

function searchMenu() {
    const searchInput = document.getElementById('sidebar-search-input');
    const query = searchInput.value.toLowerCase().trim();
    
    if (!menuData) return;
    
    const nav = document.getElementById('sidebar-nav');
    nav.innerHTML = '';
    
    if (!query) {
        renderMenu(menuData);
        return;
    }
    
    const matchedItems = [];
    
    menuData.groups.forEach(group => {
        group.items.forEach(item => {
            const idStr = item.id.toString().toLowerCase();
            const name = item.name.toLowerCase();
            
            if (idStr.includes(query) || name.includes(query)) {
                matchedItems.push({ ...item, groupName: group.name, groupIcon: group.icon });
            }
        });
    });
    
    if (matchedItems.length === 0) {
        nav.innerHTML = '<div class="nav-item" style="padding: 16px; color: var(--text-muted); text-align: center;">未找到匹配的菜单</div>';
        return;
    }
    
    const searchResult = document.createElement('div');
    searchResult.className = 'menu-group';
    
    const header = document.createElement('div');
    header.className = 'menu-group-header';
    header.innerHTML = `
        <span class="group-icon">🔍</span>
        <span class="group-name">搜索结果</span>
        <span class="group-count">${matchedItems.length}</span>
    `;
    searchResult.appendChild(header);
    
    const itemsContainer = document.createElement('div');
    itemsContainer.className = 'menu-group-items';
    
    matchedItems.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = `nav-item${item.disabled ? ' disabled' : ''}`;
        itemElement.dataset.module = item.key;
        itemElement.title = item.description;
        
        if (!item.disabled) {
            itemElement.addEventListener('click', () => handleMenuClick(item));
        }
        
        itemElement.innerHTML = `
            <span class="nav-item-icon">${item.icon}</span>
            <span class="menu-item-id">${item.id}</span>
            <span class="nav-item-text">${item.name}</span>
        `;
        
        itemsContainer.appendChild(itemElement);
    });
    
    searchResult.appendChild(itemsContainer);
    nav.appendChild(searchResult);
}

document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    loadMenu();
    checkAutoLogin();
    
    document.getElementById('login-form').addEventListener('submit', (e) => {
        e.preventDefault();
        login();
    });
    
    document.getElementById('change-password-form').addEventListener('submit', (e) => {
        e.preventDefault();
        changePassword();
    });
    
    document.querySelectorAll('.reset-guide-modal, .change-password-modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
            }
        });
    });
});

class TJWApp {
    constructor() {
        this.currentModule = null;
        this.modules = [
            { id: 1001, key: 'dashboard', name: '仪表盘', icon: '📊', description: '系统概览和快速访问' },
            { id: 1002, key: 'sfz', name: '身份证工具', icon: '🆔', description: '身份证生成、验证、归属地查询', stats: { count: 10000, today: 128 } },
            { id: 1003, key: 'tools', name: '实用工具', icon: '🔧', description: '各种实用小工具集合', stats: { count: 15, today: 3 } },
            { id: 1004, key: 'settings', name: '系统设置', icon: '⚙️', description: '系统配置和个性化设置' },
            { id: 1005, key: 'about', name: '关于', icon: 'ℹ️', description: '关于系统和版本信息' }
        ];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.handleURLParams();
    }

    getURLParams() {
        const params = new URLSearchParams(window.location.search);
        const idParam = params.get('id');
        return idParam ? parseInt(idParam) : null;
    }

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
            this.updateURL(module.id);
        }

        const contentArea = document.querySelector('.page-content');
        
        switch (moduleKey) {
            case 'dashboard':
                await this.loadDashboard();
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
            case 'about':
                await this.loadAboutModule();
                break;
            default:
                await this.loadDashboard();
        }

        this.currentModule = moduleKey;
        document.querySelector('.sidebar').classList.remove('open');
    }

    updateURL(moduleId) {
        const newUrl = `${window.location.origin}${window.location.pathname}?id=${moduleId}`;
        window.history.pushState({ moduleId: moduleId }, '', newUrl);
    }

    async loadDashboard() {
        const contentArea = document.querySelector('.page-content');
        
        try {
            const sfzStats = await this.fetchAPI('/api/sfz/stats');
            const sfzCount = sfzStats.success ? sfzStats.data.total_generated : 0;
            
            contentArea.innerHTML = `
                <div class="dashboard-header">
                    <h2>欢迎回来，${currentUser?.username || '用户'}！</h2>
                    <p class="dashboard-date">${this.getCurrentDate()} - 今天也是美好的一天</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">🆔</div>
                        <div class="stat-content">
                            <div class="value">${sfzCount.toLocaleString()}</div>
                            <div class="label">身份证处理记录</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">📊</div>
                        <div class="stat-content">
                            <div class="value">4</div>
                            <div class="label">功能模块</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">⚡</div>
                        <div class="stat-content">
                            <div class="value">100%</div>
                            <div class="label">系统状态</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">🔒</div>
                        <div class="stat-content">
                            <div class="value">已登录</div>
                            <div class="label">安全状态</div>
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
                                        <div class="stat-label">总记录</div>
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
            `;
        } catch (error) {
            console.error('Load dashboard error:', error);
            contentArea.innerHTML = `
                <div style="text-align: center; padding: 60px 20px;">
                    <div style="font-size: 5rem; margin-bottom: 24px;">🔴</div>
                    <h3 style="font-size: 1.6rem; margin-bottom: 12px;">加载失败</h3>
                    <p style="color: var(--text-secondary);">请检查网络连接</p>
                </div>
            `;
        }
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
                
                <div class="sfz-toolbar">
                    <div class="sfz-toolbar-item active" data-tab="generate" title="生成身份证">🆕</div>
                    <div class="sfz-toolbar-item" data-tab="verify" title="验证身份证">✅</div>
                    <div class="sfz-toolbar-item" data-tab="region" title="归属地查询">📍</div>
                    <div class="sfz-toolbar-item" data-tab="batch" title="批量生成">📦</div>
                </div>
                
                <div class="sfz-tab-content active" id="tab-generate">
                    <div class="sfz-card">
                        <h3>生成身份证号码</h3>
                        <div class="sfz-advanced-toggle" onclick="tjwApp.toggleAdvancedOptions()">
                            <span>⚙️ 高级选项</span>
                            <span class="sfz-advanced-arrow">▼</span>
                        </div>
                        <div class="sfz-advanced-options" id="advanced-options">
                            <div class="sfz-form-group">
                                <label>性别</label>
                                <select id="sfz-gender">
                                    <option value="">随机</option>
                                    <option value="male">男</option>
                                    <option value="female">女</option>
                                </select>
                            </div>
                            <div class="sfz-form-group">
                                <label>地区代码 (6位)</label>
                                <input type="text" id="sfz-region" placeholder="如 110000 表示北京">
                            </div>
                            <div class="sfz-form-group">
                                <label>出生日期 (YYYYMMDD)</label>
                                <input type="text" id="sfz-birthdate" placeholder="如 19900101">
                            </div>
                        </div>
                        <button class="sfz-btn" onclick="tjwApp.sfzGenerate()">生成身份证</button>
                        <div id="sfz-generate-result"></div>
                    </div>
                </div>
                
                <div class="sfz-tab-content" id="tab-verify">
                    <div class="sfz-card">
                        <h3>验证身份证号码</h3>
                        <div class="sfz-form-group">
                            <label>身份证号码</label>
                            <input type="text" id="sfz-verify" placeholder="请输入18位身份证号码">
                        </div>
                        <button class="sfz-btn" onclick="tjwApp.sfzVerify()">验证身份证</button>
                        <div id="sfz-verify-result"></div>
                    </div>
                </div>
                
                <div class="sfz-tab-content" id="tab-region">
                    <div class="sfz-card">
                        <h3>查询归属地</h3>
                        <div class="sfz-form-group">
                            <label>身份证号码或前6位</label>
                            <input type="text" id="sfz-region-input" placeholder="请输入身份证号码或地区代码">
                        </div>
                        <button class="sfz-btn" onclick="tjwApp.sfzGetRegion()">查询归属地</button>
                        <div id="sfz-region-result"></div>
                    </div>
                </div>
                
                <div class="sfz-tab-content" id="tab-batch">
                    <div class="sfz-card">
                        <h3>批量生成身份证</h3>
                        <div class="sfz-form-group">
                            <label>生成数量</label>
                            <input type="number" id="sfz-batch-count" value="10" min="1" max="100">
                        </div>
                        <button class="sfz-btn" onclick="tjwApp.sfzBatchGenerate()">批量生成</button>
                        <div id="sfz-batch-result"></div>
                    </div>
                </div>
            </div>
        `;
        
        document.querySelectorAll('.sfz-toolbar-item').forEach(item => {
            item.addEventListener('click', (e) => {
                document.querySelectorAll('.sfz-toolbar-item').forEach(i => i.classList.remove('active'));
                document.querySelectorAll('.sfz-tab-content').forEach(t => t.classList.remove('active'));
                e.currentTarget.classList.add('active');
                document.getElementById(`tab-${e.currentTarget.dataset.tab}`).classList.add('active');
            });
        });
    }

    toggleAdvancedOptions() {
        const options = document.getElementById('advanced-options');
        const arrow = document.querySelector('.sfz-advanced-arrow');
        options.classList.toggle('show');
        arrow.textContent = options.classList.contains('show') ? '▲' : '▼';
    }

    async sfzGenerate() {
        const gender = document.getElementById('sfz-gender').value;
        const region = document.getElementById('sfz-region').value;
        const birthdate = document.getElementById('sfz-birthdate').value;
        
        let url = '/api/sfz/generate';
        const params = [];
        if (gender) params.push(`sex=${gender}`);
        if (region) params.push(`region=${region}`);
        if (birthdate) params.push(`birth_date=${birthdate}`);
        if (params.length > 0) url += `?${params.join('&')}`;
        
        const result = await this.fetchAPI(url);
        this.showSFZResult('sfz-generate-result', result, true);
    }

    async sfzBatchGenerate() {
        const count = document.getElementById('sfz-batch-count').value;
        const result = await this.fetchAPI(`/api/sfz/generate/batch?count=${count}`);
        this.showSFZResult('sfz-batch-result', result, false);
    }

    async sfzVerify() {
        const idNumber = document.getElementById('sfz-verify').value.trim().replace(/\s/g, '');
        if (!idNumber || idNumber.length !== 18) {
            this.showSFZResult('sfz-verify-result', { success: false, message: '请输入18位身份证号码' }, true);
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
                            <value>${data.verified ? '✅已验证' : '⏳未验证'}</value>
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
                        <span>ℹ️</span>
                        <strong>${result.message}</strong>
                    </div>
                    <div class="sfz-id-card">
                        <div class="sfz-id-details">
                            <div class="sfz-id-detail">
                                <label>地区代码</label>
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
                    <p style="color: var(--text-secondary); font-size: 1.1rem;">更多实用工具将上线，请期待！</p>
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
                        <h4>📦 系统信息</h4>
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
                                <value style="color: #22c55e;">✅ 正常</value>
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
                                <span>📚</span>
                                <span>Redoc API 文档</span>
                            </a>
                            <a href="/health" target="_blank" class="settings-link">
                                <span>❤️</span>
                                <span>健康检查</span>
                            </a>
                        </div>
                    </div>
                    <div class="settings-section">
                        <h4>📋 模块ID映射</h4>
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

    async loadAboutModule() {
        const contentArea = document.querySelector('.page-content');
        
        try {
            const aboutInfo = await this.fetchAPI('/api/about/about');
            
            if (aboutInfo.success && aboutInfo.data) {
                const data = aboutInfo.data;
                contentArea.innerHTML = `
                    <div class="module-container">
                        <div class="module-container-header">
                            <h2 class="module-container-title">ℹ️ 关于系统</h2>
                            <div class="module-container-actions">
                                <button class="header-btn secondary" onclick="tjwApp.loadModule('dashboard')">返回</button>
                            </div>
                        </div>
                        <div style="max-width: 600px; margin: 0 auto;">
                            <div class="settings-section">
                                <div style="text-align: center; margin-bottom: 24px;">
                                    <div style="width: 80px; height: 80px; border-radius: 20px; background: linear-gradient(135deg, var(--accent-purple) 0%, var(--primary-purple) 100%); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 700; margin: 0 auto 16px; box-shadow: 0 10px 40px rgba(139, 92, 246, 0.4);">T</div>
                                    <h3 style="font-size: 1.5rem;">${data.name}</h3>
                                    <p style="color: var(--text-muted);">${data.description}</p>
                                </div>
                                <div class="settings-grid">
                                    <div class="settings-item">
                                        <label>版本号</label>
                                        <value style="color: var(--accent-purple); font-weight: 600;">${data.version}</value>
                                    </div>
                                    <div class="settings-item">
                                        <label>作者</label>
                                        <value>${data.author}</value>
                                    </div>
                                    <div class="settings-item">
                                        <label>联系方式</label>
                                        <value>${data.email}</value>
                                    </div>
                                    <div class="settings-item">
                                        <label>版权</label>
                                        <value>${data.copyright}</value>
                                    </div>
                                </div>
                            </div>
                            <div class="settings-section">
                                <h4>🖥️ 系统信息</h4>
                                <div class="settings-grid">
                                    <div class="settings-item">
                                        <label>Python版本</label>
                                        <value>${data.system?.python_version || '未知'}</value>
                                    </div>
                                    <div class="settings-item">
                                        <label>操作系统</label>
                                        <value>${data.system?.platform || '未知'}</value>
                                    </div>
                                    <div class="settings-item">
                                        <label>系统版本</label>
                                        <value>${data.system?.release || '未知'}</value>
                                    </div>
                                    <div class="settings-item">
                                        <label>架构</label>
                                        <value>${data.system?.machine || '未知'}</value>
                                    </div>
                                </div>
                            </div>
                            <div class="settings-section">
                                <h4>✨ 功能特性</h4>
                                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                                    ${data.features?.map(feature => `
                                        <span style="padding: 6px 12px; background: rgba(139, 92, 246, 0.15); border: 1px solid var(--border-color); border-radius: 20px; font-size: 0.85rem;">${feature}</span>
                                    `).join('')}
                                </div>
                            </div>
                            <div class="settings-section">
                                <h4>🔌 API端点</h4>
                                <div class="settings-links">
                                    ${Object.entries(data.api_endpoints || {}).map(([name, path]) => `
                                        <a href="${path}" target="_blank" class="settings-link">
                                            <span>🔗</span>
                                            <span>${name}</span>
                                        </a>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Load about error:', error);
            contentArea.innerHTML = `
                <div class="module-container">
                    <div class="module-container-header">
                        <h2 class="module-container-title">ℹ️ 关于系统</h2>
                        <div class="module-container-actions">
                            <button class="header-btn secondary" onclick="tjwApp.loadModule('dashboard')">返回</button>
                        </div>
                    </div>
                    <div style="text-align: center; padding: 60px 20px;">
                        <div style="font-size: 5rem; margin-bottom: 24px;">ℹ️</div>
                        <h3 style="font-size: 1.6rem; margin-bottom: 12px;">TJW 工具平台</h3>
                        <p style="color: var(--text-secondary); font-size: 1.1rem;">版本: v1.0.0</p>
                        <p style="color: var(--text-muted); margin-top: 16px;">提供身份证工具等实用功能的个人工作站和API服务</p>
                    </div>
                </div>
            `;
        }
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

window.addEventListener('popstate', (event) => {
    if (event.state && event.state.moduleId && tjwApp) {
        const module = tjwApp.modules.find(m => m.id === event.state.moduleId);
        if (module) {
            tjwApp.loadModule(module.key);
        }
    } else if (tjwApp) {
        tjwApp.loadModule('dashboard');
    }
});