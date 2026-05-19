document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    if (!form) return;
    const validators = {
        username: v => { v=v.trim(); if(!v) return 'Это поле обязательно'; if(v.length<3) return 'Минимум 3 символа'; if(v.length>30) return 'Максимум 30 символов'; if(!/^[a-zA-Z0-9_]+$/.test(v)) return 'Только латиница, цифры и _'; return ''; },
        name: v => { v=v.trim(); if(!v) return 'Это поле обязательно'; if(v.length<2) return 'Минимум 2 буквы'; if(v.length>30) return 'Максимум 30 букв'; if(!/^[a-zA-Zа-яА-ЯёЁ-]+$/.test(v)) return 'Только буквы и дефис'; if(v[0]!==v[0].toUpperCase()) return 'С заглавной буквы'; return ''; },
        email: v => { v=v.trim(); if(!v) return 'Это поле обязательно'; if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return 'Введите корректный email'; return ''; },
        city: v => { v=v.trim(); if(!v) return 'Это поле обязательно'; if(!/^[a-zA-Zа-яА-ЯёЁ\s-]+$/.test(v)) return 'Только буквы, пробелы и дефисы'; return ''; },
        password: v => { if(!v) return 'Это поле обязательно'; if(v.length<8) return 'Минимум 8 символов'; if(/^\d+$/.test(v)) return 'Не только цифры'; return ''; },
        password_confirm: v => { if(!v) return 'Это поле обязательно'; if(v!==document.getElementById('password').value) return 'Пароли не совпадают'; return ''; }
    };
    function validateField(f) {
        const err = document.getElementById(f.id+'Error'); if(!err) return true;
        const msg = validators[f.dataset.validate]?.(f.value) || '';
        if(msg) { f.classList.add('error'); err.textContent=msg; return false; }
        f.classList.remove('error'); err.textContent=''; return true;
    }
    form.querySelectorAll('input[data-validate]').forEach(inp => {
        inp.addEventListener('blur', ()=>validateField(inp));
        inp.addEventListener('input', ()=> inp.classList.contains('error') && validateField(inp));
    });
    form.addEventListener('submit', e => {
        if(![...form.querySelectorAll('input[data-validate]')].every(f=>validateField(f))) e.preventDefault();
    });
});