window.onIndexDataLoaded = function(data) {
    renderIndex(data);
};

function loadData() {
    // Xóa script cũ nếu có để tránh phình DOM
    const oldScript = document.getElementById('data-script');
    if (oldScript) {
        oldScript.remove();
    }
    
    // Tạo script mới để tải dữ liệu (bỏ qua CORS khi mở file local)
    const script = document.createElement('script');
    script.id = 'data-script';
    script.src = 'data/index_data.js?t=' + new Date().getTime();
    script.onerror = () => {
        const grid = document.getElementById('level-grid');
        grid.innerHTML = `
            <div class="loading-state" style="border-color: #feb2b2;">
                <div style="font-size: 2.5rem; margin-bottom: 15px;">🚀</div>
                <div style="color: #e53e3e;">Chưa có dữ liệu bài thi</div>
                <div style="font-size: 0.95rem; font-weight: 400; margin-top: 10px; color: #718096;">
                    Hệ thống AI đang chạy ngầm để tạo các bài thi IELTS chất lượng cao.<br>
                    Quá trình này tự động hoàn toàn. Vui lòng đợi trong giây lát...
                </div>
            </div>
        `;
    };
    document.body.appendChild(script);
}

document.addEventListener('DOMContentLoaded', () => {
    loadData();
    // Tự động làm mới danh sách sau mỗi 5 giây khi có bài mới
    setInterval(loadData, 5000);
});

function renderIndex(data) {
    const grid = document.getElementById('level-grid');
    grid.innerHTML = ''; 
    
    const levels = [
        { id: 'A1-A2', class: 'a1-a2', label: 'Level A1 - A2' },
        { id: 'B1-B2', class: 'b1-b2', label: 'Level B1 - B2' },
        { id: 'C1-C2', class: 'c1-c2', label: 'Level C1 - C2' }
    ];
    
    levels.forEach(level => {
        const lessons = data[level.id] || [];
        
        const card = document.createElement('div');
        card.className = `level-card ${level.class}`;
        
        let lessonsHtml = '';
        if (lessons.length === 0) {
            lessonsHtml = '<p style="color: #a0aec0; text-align: center; padding: 30px; font-weight: 600;">Đang khởi tạo danh sách bài học...</p>';
        } else {
            lessons.forEach(lesson => {
                const jsFile = lesson.file.replace('.json', '.js').replace('data/', '');
                const href = `template_reading.html?file=${encodeURIComponent(jsFile)}`;
                const lessonNumber = lesson.id.split('_').pop();
                
                lessonsHtml += `
                    <li class="lesson-item">
                        <a href="${href}" class="lesson-link">
                            <span class="lesson-id">Bài luyện tập số ${lessonNumber}</span>
                            <span>${lesson.title || 'Chưa có tiêu đề'}</span>
                        </a>
                    </li>
                `;
            });
        }
        
        card.innerHTML = `
            <div class="level-header">
                <span class="level-title">${level.label}</span>
                <span class="count-badge">${lessons.length} bài</span>
            </div>
            <ul class="lesson-list">
                ${lessonsHtml}
            </ul>
        `;
        
        grid.appendChild(card);
    });
}
