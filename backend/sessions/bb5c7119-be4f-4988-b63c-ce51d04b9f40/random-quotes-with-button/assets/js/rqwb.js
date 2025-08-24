(function(){
    'use strict';

    function getQuotes(){
        if (typeof window.rqwbData !== 'undefined' && Array.isArray(window.rqwbData.quotes)) {
            return window.rqwbData.quotes;
        }
        return [];
    }

    function t(key){
        if (typeof window.rqwbData !== 'undefined' && window.rqwbData.i18n && window.rqwbData.i18n[key]) {
            return window.rqwbData.i18n[key];
        }
        return key;
    }

    function pickNewIndex(current, max){
        if (max <= 1) { return 0; }
        var idx = current;
        while (idx === current) {
            idx = Math.floor(Math.random() * max);
        }
        return idx;
    }

    function updateQuote(container, quotes, index){
        var textEl = container.querySelector('.rqwb-quote-text');
        var authorEl = container.querySelector('.rqwb-quote-author');
        var quote = quotes[index];
        if (!quote) { return; }
        if (textEl) { textEl.textContent = quote.text || ''; }
        if (authorEl) {
            var authorText = quote.author ? '— ' + quote.author : '';
            authorEl.textContent = authorText;
        }
        container.setAttribute('data-rqwb-index', String(index));
    }

    function init(){
        var quotes = getQuotes();
        var boxes = document.querySelectorAll('.rqwb-quote-box');
        boxes.forEach(function(box){
            var btn = box.querySelector('.rqwb-button');
            if (!btn) { return; }
            // Ensure button text and aria are present via localization
            if (!btn.textContent.trim()) { btn.textContent = t('newQuote'); }
            if (!btn.getAttribute('aria-label')) { btn.setAttribute('aria-label', t('buttonAria')); }

            btn.addEventListener('click', function(){
                var current = parseInt(box.getAttribute('data-rqwb-index') || '0', 10);
                var next = pickNewIndex(current, quotes.length);
                updateQuote(box, quotes, next);
                // Focus back to quote for SR users
                var quoteText = box.querySelector('.rqwb-quote-text');
                if (quoteText) { quoteText.setAttribute('tabindex', '-1'); quoteText.focus({preventScroll:true}); quoteText.removeAttribute('tabindex'); }
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
