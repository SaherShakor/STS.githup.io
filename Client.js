
const hamburger = document.querySelector('.header .nav-bar .nav-list .hamburger');
const mobile_menu = document.querySelector('.header .nav-bar .nav-list ul');
const menu_item = document.querySelectorAll('.header .nav-bar .nav-list ul li a');
const header = document.querySelector('.header.container');

hamburger.addEventListener('click', () => {
	hamburger.classList.toggle('active');
	mobile_menu.classList.toggle('active');
});

document.addEventListener('scroll', () => {
	var scroll_position = window.scrollY;
	if (scroll_position > 250) {
		header.style.backgroundColor = '#29323c';
	} else {
		header.style.backgroundColor = 'transparent';
	}
});

menu_item.forEach((item) => {
	item.addEventListener('click', () => {
		hamburger.classList.toggle('active');
		mobile_menu.classList.toggle('active');
	});
});
let icon=document.getElementsByClassName(`icon`)
let card=document.getElementById("card");
card.addEventListener(`focus`,function(){
card.style.transform="rotate(360deg);"
})
/* Demo purposes only */
document.addEventListener("DOMContentLoaded", function() {
	var elementsWithHoverClass = document.querySelectorAll('.hover');
  
	elementsWithHoverClass.forEach(function(element) {
	  element.addEventListener('mouseleave', function() {
		element.classList.remove('hover');
	  });
	});
  });
  
  document.addEventListener("DOMContentLoaded", function() {
	// انتظر حتى يتم تحميل الصفحة بشكل كامل
  
	// ابحث عن زر "ORDER NOW"
	var orderNowButton = document.querySelector('.cta');
  
	// قم بإضافة حدث النقر إلى الزر
	orderNowButton.addEventListener('click', function() {
	  // عند النقر، قم بفتح صفحة Service.htm
	  window.location.href = 'Service.html';
	});
  });
  