function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = (textarea.scrollHeight) + 'px';
}

document.addEventListener('DOMContentLoaded', function () {
setTimeout(function () {
    let alerts = document.querySelectorAll('.auto-dismiss');
    alerts.forEach(function (alert) {
        let bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 4000);
});