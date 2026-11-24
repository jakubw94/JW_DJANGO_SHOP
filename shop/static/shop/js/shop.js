  function filterProducts(categories, button) {
    if (!Array.isArray(categories)) {
      categories = [categories];
    }

    let products = document.getElementsByClassName('product-card');

    for (let i = 0; i < products.length; i++) {
      if (categories.includes('all') || categories.some(category => products[i].classList.contains(category))) {
        products[i].style.display = 'block';
      } else {
        products[i].style.display = 'none';
      }
    }

    let buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => {
      btn.classList.remove('btn-secondary');
      btn.classList.add('btn-outline-secondary');
    });

    button.classList.remove('btn-outline-secondary');
    button.classList.add('btn-secondary');
  }

  document.addEventListener('DOMContentLoaded', () => {
    filterProducts('all', document.getElementById('all-btn'));
  });

document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        let alerts = document.querySelectorAll('.auto-dismiss');
        alerts.forEach(function (alert) {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 4000);
});