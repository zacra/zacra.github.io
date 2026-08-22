/*
 * 게만아 시스템 투자 공식 가이드 - Google Analytics 4
 *
 * 1) Google Analytics에서 웹 데이터 스트림을 만든 뒤
 * 2) 아래 GA_MEASUREMENT_ID 값만 실제 측정 ID(G-...)로 바꾸면 됩니다.
 *
 * 측정 ID는 비밀번호가 아니므로 공개 웹페이지에 포함되어도 괜찮습니다.
 */
(() => {
  'use strict';

  const GA_MEASUREMENT_ID = 'G-4VNRFRTG68'; // TODO: 실제 GA4 측정 ID로 교체

  // 실제 측정 ID가 입력되기 전에는 아무 데이터도 전송하지 않습니다.
  if (!/^G-[A-Z0-9]+$/i.test(GA_MEASUREMENT_ID) || GA_MEASUREMENT_ID.includes('XXXX')) {
    console.info('[GA4] /assets/analytics.js의 GA_MEASUREMENT_ID를 설정하면 방문 통계가 시작됩니다.');
    return;
  }

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){ window.dataLayer.push(arguments); };

  const loader = document.createElement('script');
  loader.async = true;
  loader.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA_MEASUREMENT_ID)}`;
  document.head.appendChild(loader);

  window.gtag('js', new Date());
  window.gtag('config', GA_MEASUREMENT_ID, {
    send_page_view: true
  });

  const PURCHASE_LINKS = {
    'https://forms.gle/fF2nEigv7uodQ7EZ9': { event_name: 'package_purchase_click', payment_method: 'bank_transfer' },
    'https://www.latpeed.com/products/Wxjik': { event_name: 'package_purchase_click', payment_method: 'card_simplepay' },
    'https://forms.gle/HooXu7DNkubKexhP6': { event_name: 'superma_purchase_click', payment_method: 'bank_transfer' },
    'https://www.latpeed.com/products/XJLqa': { event_name: 'superma_purchase_click', payment_method: 'card_simplepay' }
  };

  const PRODUCT_PAGES = {
    '/package.html': 'package_page_click',
    '/super-moving-average.html': 'superma_page_click',
    '/starter.html': 'starter_page_click'
  };

  function cleanText(text) {
    return (text || '').replace(/\s+/g, ' ').trim().slice(0, 100);
  }

  function sendEvent(name, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params);
    }
  }

  document.addEventListener('click', (event) => {
    const link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;

    let url;
    try {
      url = new URL(link.href, window.location.href);
    } catch (_) {
      return;
    }

    const linkText = cleanText(link.textContent || link.getAttribute('aria-label'));
    const sourcePage = window.location.pathname || '/';
    const normalizedHref = `${url.origin}${url.pathname}`.replace(/\/$/, '');

    // 패키지 / 슈퍼 이동평균 구매 버튼 클릭: 가장 중요한 전환 지표
    const purchase = PURCHASE_LINKS[normalizedHref];
    if (purchase) {
      sendEvent(purchase.event_name, {
        payment_method: purchase.payment_method,
        source_page: sourcePage,
        link_text: linkText,
        link_url: url.href
      });
      return;
    }

    // 사이트 내부에서 패키지 / 슈퍼 이동평균 / Starter로 이동한 관심 클릭
    if (url.origin === window.location.origin && PRODUCT_PAGES[url.pathname]) {
      sendEvent(PRODUCT_PAGES[url.pathname], {
        source_page: sourcePage,
        link_text: linkText,
        destination_path: url.pathname
      });
      return;
    }

    // 97개 패키지 콘텐츠 상세 가이드 관심도
    if (url.origin === window.location.origin && url.pathname === '/package-content-guide.html') {
      sendEvent('package_guide_click', {
        source_page: sourcePage,
        link_text: linkText,
        destination_path: url.pathname
      });
    }
  }, { passive: true });
})();
