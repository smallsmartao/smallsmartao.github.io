(function () {
  'use strict';

  // Only replace the site-wide homepage banner. Posts keep their own covers.
  if (window.location.pathname !== '/') return;

  var banner = document.getElementById('banner');
  var header = banner && banner.closest('.header-inner');
  if (!banner || !header) return;

  header.classList.add('home-video-header');
  banner.classList.add('home-video-banner');
  banner.style.backgroundImage = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ? "url('/videos/blog-cover-7959-poster.jpg')"
    : "url('/videos/blog-cover-7959-original-10fps.gif')";
})();
