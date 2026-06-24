const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: "new", args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  
  await page.goto('file://' + process.cwd() + '/Listening_204_FullTest/Test_1/Test_1.html');
  
  // Wait a bit to ensure JS loads
  await new Promise(r => setTimeout(r, 1000));
  
  // Set localStorage
  await page.evaluate(() => {
    localStorage.setItem('youpass_student_id', 'TESTING');
  });
  
  // Type in the input and click
  await page.type('#nickname-input', '1234');
  await page.click('.submit-btn');
  
  console.log("Clicked submit, waiting for 3 seconds...");
  await new Promise(r => setTimeout(r, 3000));
  
  const display = await page.evaluate(() => {
    const el = document.querySelector('.main-layout');
    return el ? el.style.display : 'NOT FOUND';
  });
  console.log("Main layout display is:", display);
  
  await browser.close();
})();
