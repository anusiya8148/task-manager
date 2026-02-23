// Page load animation
document.addEventListener('DOMContentLoaded', function () {
  document.body.classList.add('loaded');
});

// Button ripple animation
document.addEventListener('click', function (e) {
  if (e.target.tagName === 'BUTTON') {
    const circle = document.createElement('span');
    circle.classList.add('ripple');

    const rect = e.target.getBoundingClientRect();
    circle.style.left = e.clientX - rect.left + 'px';
    circle.style.top = e.clientY - rect.top + 'px';

    e.target.appendChild(circle);

    setTimeout(() => {
      circle.remove();
    }, 600);
  }
});

// Smooth delete animation
function deleteTask(element) {
  const task = element.closest('.task');
  task.style.opacity = '0';
  task.style.transform = 'translateX(100px)';
  setTimeout(() => {
    window.location = element.href;
  }, 400);
  return false;
}
