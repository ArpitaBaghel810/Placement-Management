// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(a => {
        setTimeout(() => {
            a.style.opacity = '0';
            a.style.transition = 'opacity 0.5s';
            setTimeout(() => a.remove(), 500);
        }, 4000);
    });
});
