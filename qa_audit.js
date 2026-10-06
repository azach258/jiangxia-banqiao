const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'index.html');
const html = fs.readFileSync(filePath, 'utf8');

console.log('==================================================');
console.log('🔍 WEB QA & DEBUGGING SPECIALIST AUTOMATED AUDIT');
console.log('==================================================');
console.log('File:', filePath);
console.log('File Size:', html.length, 'bytes');

// 1. Check all href links
const hrefMatches = [...html.matchAll(/href=["']([^"']+)["']/g)];
const hrefs = hrefMatches.map(m => m[1]);
console.log('\n[1] HREF Links Analysis:');
console.log('Total Links Found:', hrefs.length);

const linkCategories = {
    anchors: hrefs.filter(h => h.startsWith('#')),
    tel: hrefs.filter(h => h.startsWith('tel:')),
    line: hrefs.filter(h => h.includes('lin.ee')),
    maps: hrefs.filter(h => h.includes('maps.google') || h.includes('maps.app.goo.gl')),
    placeholders: hrefs.filter(h => h.includes('placeholder'))
};

console.log('- Internal Anchors (#):', linkCategories.anchors);
console.log('- Tel Links (tel:):', linkCategories.tel);
console.log('- LINE Links (lin.ee):', linkCategories.line.length, 'instances');
console.log('- Google Maps Links:', linkCategories.maps);
console.log('- Remaining Placeholders:', linkCategories.placeholders);

// Verify that all anchor targets exist in the DOM
console.log('\n[2] Anchor Targets Verification:');
const uniqueAnchors = [...new Set(linkCategories.anchors)].filter(a => a !== '#');
uniqueAnchors.forEach(anchor => {
    const id = anchor.substring(1);
    const exists = html.includes(`id="${id}"`) || html.includes(`id='${id}'`);
    console.log(`- Anchor ${anchor}: ${exists ? '✅ Target Exists' : '❌ Target MISSING!'}`);
});

// 2. Check all onclick handlers
console.log('\n[3] Onclick Handlers Analysis:');
const onclickMatches = [...html.matchAll(/onclick=["']([^"']+)["']/g)];
const onclicks = onclickMatches.map(m => m[1]);
console.log('Total Onclick Handlers Found:', onclicks.length);
onclicks.forEach((oc, idx) => {
    console.log(`  ${idx + 1}. ${oc}`);
});

// 3. Check Google Tag & Conversion tracking
console.log('\n[4] Google Tag Tracking:');
const hasGtagScript = html.includes('https://www.googletagmanager.com/gtag/js?id=AW-18290344841');
const hasGtagConfig = html.includes("gtag('config', 'AW-18290344841')");
const hasTrackConversion = html.includes('function trackConversion(');
console.log('- Script Tag AW-18290344841:', hasGtagScript ? '✅ PASS' : '❌ FAIL');
console.log('- Config AW-18290344841:', hasGtagConfig ? '✅ PASS' : '❌ FAIL');
console.log('- Function trackConversion defined:', hasTrackConversion ? '✅ PASS' : '❌ FAIL');

// 4. Check Images & QR Codes
console.log('\n[5] Image Assets Analysis:');
const imgMatches = [...html.matchAll(/<img[^>]+src=["']([^"']+)["'][^>]*>/g)];
console.log('Total Images Found:', imgMatches.length);
imgMatches.forEach((m, idx) => {
    console.log(`  Img ${idx + 1}: ${m[0]}`);
});

// 5. Check Modals
console.log('\n[6] Modals Integrity:');
const hasPrivacyModal = html.includes('id="privacyModal"');
const hasTermsModal = html.includes('id="termsModal"');
const hasEscListener = html.includes("e.key === 'Escape'");
console.log('- Privacy Modal (id="privacyModal"):', hasPrivacyModal ? '✅ PASS' : '❌ FAIL');
console.log('- Terms Modal (id="termsModal"):', hasTermsModal ? '✅ PASS' : '❌ FAIL');
console.log('- Escape Key Listener:', hasEscListener ? '✅ PASS' : '❌ FAIL');

// 6. Check Schema.org
console.log('\n[7] Schema.org LocalBusiness:');
const hasSchema = html.includes('"@type": "HealthAndBeautyBusiness"') && html.includes('"telephone": "0989-879-614"');
console.log('- Schema JSON-LD:', hasSchema ? '✅ PASS' : '❌ FAIL');

// 7. Check Accordions (<details>)
console.log('\n[8] Accordion (<details>) Analysis:');
const detailsCount = (html.match(/<details/g) || []).length;
const summaryCount = (html.match(/<summary/g) || []).length;
console.log(`- <details> count: ${detailsCount}, <summary> count: ${summaryCount}`);

console.log('\n==================================================');
console.log('AUDIT COMPLETE');
console.log('==================================================');
