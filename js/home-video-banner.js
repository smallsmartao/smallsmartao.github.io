(function () {
  'use strict';

  // Only replace the banner on the first index page. Posts keep their own covers.
  if (window.location.pathname !== '/') return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var banner = document.getElementById('banner');
  var header = banner && banner.closest('.header-inner');
  if (!banner || !header) return;

  header.classList.add('home-video-header');
  banner.classList.add('home-video-banner');
  banner.style.backgroundImage = "url('/videos/blog-cover-9512-1920.jpg')";

  var video = document.createElement('video');
  video.className = 'home-banner-video';
  video.autoplay = true;
  video.muted = true;
  video.loop = true;
  video.playsInline = true;
  video.preload = 'auto';
  video.poster = '/videos/blog-cover-9512-1920.jpg';
  video.setAttribute('aria-hidden', 'true');
  video.setAttribute('tabindex', '-1');

  var source = document.createElement('source');
  source.src = '/videos/blog-cover-9512-1920.mp4';
  source.type = 'video/mp4';
  video.appendChild(source);
  banner.insertBefore(video, banner.firstChild);

  var playPromise = video.play();
  if (playPromise && typeof playPromise.catch === 'function') {
    playPromise.catch(function () {});
  }
})();
