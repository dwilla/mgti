(async () => {
    // Resolve path to shared/ relative to current page location
    const depth = location.pathname.split('/').length - 2;
    const prefix = depth > 0 ? '../'.repeat(depth) : '';

    // 1. Inject all [data-include] partials
    const mounts = [...document.querySelectorAll('[data-include]')];
    await Promise.all(mounts.map(async el => {
        const name = el.dataset.include;
        try {
            const res = await fetch(`${prefix}shared/${name}.html`);
            el.innerHTML = await res.text();
        } catch (e) {
            console.warn(`Could not load partial: ${name}`, e);
        }
    }));

    // 2. Active nav state — match body[data-page] to [data-nav] links
    const page = document.body.dataset.page;
    if (page) {
        const activeLink = document.querySelector(`[data-nav="${page}"]`);
        if (activeLink) {
            activeLink.classList.add('is-active');
            // If the active link is inside a dropdown, also activate the parent trigger
            const parentDropdown = activeLink.closest('.navbar-item.has-dropdown');
            if (parentDropdown) {
                parentDropdown.classList.add('is-active');
            }
        }
    }

    // 3. Burger menu toggle
    document.querySelectorAll('.navbar-burger').forEach(burger => {
        burger.addEventListener('click', () => {
            const target = document.getElementById(burger.dataset.target);
            burger.classList.toggle('is-active');
            if (target) target.classList.toggle('is-active');
        });
    });
})();
