const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // Set localStorage
  await page.addInitScript(() => {
    window.localStorage.setItem('youpass_student_id', 'LONG123');
  });

  const fileUrl = 'file://' + path.resolve('Listening_204_FullTest/Test_1/Test_1.html');
  await page.goto(fileUrl);
  
  // Fill input and click
  await page.fill('#nickname-input', 'LONG123');
  await page.click('.submit-btn');
  
  // Wait 4 seconds for login and animations
  await page.waitForTimeout(4000);
  
  await page.screenshot({ path: 'screenshot_after_login.png' });
  console.log("Screenshot saved.");
  
  await browser.close();
})();
