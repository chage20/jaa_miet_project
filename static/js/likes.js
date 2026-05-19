document.addEventListener('DOMContentLoaded', function() {
    let socket = null;
    const isAuth = window.USER_IS_AUTHENTICATED === true;

    function paintLikes(likedIds) {
        likedIds.forEach(id => {
            const btn = document.querySelector(`.like-btn[data-car-id="${id}"]`);
            if (btn) {
                btn.classList.add('liked');
                btn.querySelector('i').className = 'bi bi-heart-fill';
            }
        });
    }

    if (isAuth) {
        fetch('/cars/api/my-likes/')
            .then(res => res.json())
            .then(data => {
                paintLikes(data.liked_ids);
                console.log('Likes loaded via AJAX:', data.liked_ids);
                connectWebSocket();
            })
            .catch(err => console.error(' AJAX error:', err));
    }
    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        socket = new WebSocket(`${protocol}${window.location.host}/ws/likes/`);

        socket.onopen = () => console.log('WS connected');

        socket.onmessage = (e) => {
            try {
                const data = JSON.parse(e.data);
                const btn = document.querySelector(`.like-btn[data-car-id="${data.car_id}"]`);
                if (!btn) return;

                const icon = btn.querySelector('i');
                const countSpan = btn.querySelector('.likes-count');

                countSpan.textContent = data.count;

                if (data.action === 'personal_color') {
                    if (data.is_liked) {
                        btn.classList.add('liked');
                        icon.className = 'bi bi-heart-fill';
                    } else {
                        btn.classList.remove('liked');
                        icon.className = 'bi bi-heart';
                    }
                }
            } catch (err) { console.error('WS parse error', err); }
        };

        socket.onclose = () => {
            if (window.USER_IS_AUTHENTICATED === true) {
                setTimeout(connectWebSocket, 3000);
            }
        };
    }

    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            if (!window.USER_IS_AUTHENTICATED) {
                if (confirm('Войдите в аккаунт, чтобы ставить лайки')) window.location.href = '/login/';
                return;
            }
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ car_id: parseInt(this.dataset.carId) }));
            }
        });
    });
});