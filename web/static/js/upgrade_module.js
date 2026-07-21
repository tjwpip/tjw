
    async loadUpgradeModule() {
        const contentArea = document.querySelector('.page-content');
        
        contentArea.innerHTML = `
            <div class="module-container">
                <div class="module-container-header">
                    <h2 class="module-container-title">⬆️ 升级更新</h2>
                    <div class="module-container-actions">
                        <button class="header-btn secondary" onclick="tjwApp.loadModule('dashboard')">返回</button>
                    </div>
                </div>
                
                <div id="upgrade-content" style="max-width: 400px; margin: 0 auto;">
                    <div style="text-align: center; padding: 40px 20px;">
                        <div style="font-size: 3rem; margin-bottom: 16px;">🔄</div>
                        <h3 style="font-size: 1.3rem; margin-bottom: 8px;">正在检查更新...</h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem;">请稍候...</p>
                    </div>
                </div>
            </div>
        `;
        
        await this.checkVersion();
    }

    async checkVersion() {
        const contentArea = document.getElementById('upgrade-content');
        
        try {
            const result = await this.fetchAPI('/api/upgrade/version');
            
            if (result.success && result.data) {
                const data = result.data;
                const hasUpdate = data.has_update || data.update_available;
                
                contentArea.innerHTML = `
                    <div class="upgrade-panel">
                        <div class="upgrade-icon">${hasUpdate ? '🚀' : '✅'}</div>
                        <h3>${hasUpdate ? '发现新版本' : '已是最新版本'}</h3>
                        
                        <div class="version-row">
                            <div class="version-box">
                                <span class="version-label">当前版本</span>
                                <span class="version-value current">v${data.current_version}</span>
                            </div>
                            <div class="version-arrow">→</div>
                            <div class="version-box">
                                <span class="version-label">PyPI版本</span>
                                <span class="version-value ${hasUpdate ? 'new' : ''}">v${data.pypi_version}</span>
                            </div>
                        </div>
                        
                        ${hasUpdate ? `
                            <div class="update-notice">
                                <span>🔔</span>
                                <span>新版本 v${data.pypi_version} 已发布，建议升级</span>
                            </div>
                            <button class="upgrade-button" onclick="tjwApp.performUpgrade()">
                                <span>⬆️</span>
                                <span>立即升级</span>
                            </button>
                        ` : `
                            <button class="check-again-btn" onclick="tjwApp.checkVersion()">🔄 重新检查</button>
                            <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 12px;">系统会自动检查更新</p>
                        `}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Check version error:', error);
            contentArea.innerHTML = `
                <div style="text-align: center; padding: 40px 20px;">
                    <div style="font-size: 3rem; margin-bottom: 16px;">❌</div>
                    <h3 style="font-size: 1.3rem; margin-bottom: 8px;">检查失败</h3>
                    <p style="color: var(--text-muted); font-size: 0.9rem;">无法连接到PyPI服务器</p>
                    <button class="sfz-btn secondary" onclick="tjwApp.checkVersion()" style="margin-top: 16px;">🔄 重新检查</button>
                </div>
            `;
        }
    }

    async performUpgrade() {
        const contentArea = document.getElementById('upgrade-content');
        
        contentArea.innerHTML = `
            <div class="upgrade-panel upgrading">
                <div class="upgrade-icon">🔄</div>
                <h3>正在升级中...</h3>
                
                <div class="progress-container">
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" id="upgrade-progress" style="width: 0%;"></div>
                    </div>
                    <div class="progress-info">
                        <span id="progress-percent">0%</span>
                        <span id="progress-text">准备升级...</span>
                    </div>
                </div>
                
                <div class="upgrade-logs" id="upgrade-logs">
                    <div class="log-item">📝 开始升级流程</div>
                </div>
            </div>
        `;
        
        try {
            const response = await fetch('/api/upgrade/upgrade', { method: 'POST' });
            const result = await response.json();
            
            const progressBar = document.getElementById('upgrade-progress');
            const progressPercent = document.getElementById('progress-percent');
            const progressText = document.getElementById('progress-text');
            const logs = document.getElementById('upgrade-logs');
            
            progressBar.style.width = `${result.progress}%`;
            progressPercent.textContent = `${result.progress}%`;
            progressText.textContent = result.current_step;
            logs.innerHTML += `<div class="log-item">${result.progress >= 30 ? '⬇️' : '📦'} ${result.current_step}</div>`;
            
            if (result.success) {
                logs.innerHTML += `<div class="log-item success">✅ 升级成功</div>`;
                
                setTimeout(() => {
                    contentArea.innerHTML = `
                        <div class="upgrade-panel success">
                            <div class="upgrade-icon">🎉</div>
                            <h3>升级成功！</h3>
                            <p>${result.message}</p>
                            <div class="countdown-box">
                                <span>系统将在 <span id="countdown">3</span> 秒后重启...</span>
                            </div>
                        </div>
                    `;
                    
                    let countdown = 3;
                    const countdownEl = document.getElementById('countdown');
                    setInterval(() => {
                        countdown--;
                        countdownEl.textContent = countdown;
                        if (countdown <= 0) window.location.reload();
                    }, 1000);
                }, 1500);
            } else {
                logs.innerHTML += `<div class="log-item error">❌ ${result.message}</div>`;
                setTimeout(() => {
                    contentArea.innerHTML = `
                        <div class="upgrade-panel error">
                            <div class="upgrade-icon">❌</div>
                            <h3>升级失败</h3>
                            <p>${result.message}</p>
                            <button class="sfz-btn secondary" onclick="tjwApp.checkVersion()">🔄 返回重试</button>
                        </div>
                    `;
                }, 1000);
            }
        } catch (error) {
            contentArea.innerHTML = `
                <div class="upgrade-panel error">
                    <div class="upgrade-icon">❌</div>
                    <h3>升级失败</h3>
                    <p>网络错误，请检查后重试</p>
                    <button class="sfz-btn secondary" onclick="tjwApp.checkVersion()">🔄 返回重试</button>
                </div>
            `;
        }
    }
