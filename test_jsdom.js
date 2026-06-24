const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('Listening_204_FullTest/Test_1/Test_1.html', 'utf-8');
const dom = new JSDOM(html, { runScripts: "dangerously" });

setTimeout(() => {
  console.log("main-layout before:", dom.window.document.querySelector('.main-layout').style.display);
  
  // Simulate login success
  dom.window.grantAccess = async function() {
    console.log("Mocking grantAccess success...");
    
    dom.window.document.getElementById('login-overlay').style.display = "none";
    let mainLayout = dom.window.document.querySelector('.main-layout') || dom.window.document.querySelector('.container') || dom.window.document.body.firstElementChild;
    if(mainLayout && mainLayout.id !== 'login-overlay') {
        mainLayout.style.display = mainLayout.classList.contains('main-layout') ? 'flex' : 'block';
        mainLayout.style.visibility = 'visible';
        mainLayout.style.opacity = '1';
    }
    console.log("main-layout after:", mainLayout.style.display);
    console.log("main-layout visibility:", mainLayout.style.visibility);
  };
  
  dom.window.grantAccess();
  
}, 500);
