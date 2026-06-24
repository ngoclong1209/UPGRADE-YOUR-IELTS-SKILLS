const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = `
<!DOCTYPE html>
<html>
<body>
    <div id="login-overlay"></div>
    <div class="main-layout" style="display: none;">CONTENT</div>
    <script>
        let fired = false;
        window.addEventListener('DOMContentLoaded', () => {
            fired = true;
            let mainLayout = document.querySelector('.main-layout');
            mainLayout.setAttribute('data-original-display', 'flex');
        });
        setTimeout(() => {
            console.log("Fired?", fired);
            let targetDisplay = document.querySelector('.main-layout').getAttribute('data-original-display') || 'block';
            console.log("Target display:", targetDisplay);
        }, 100);
    </script>
</body>
</html>
`;
const dom = new JSDOM(html, { runScripts: "dangerously" });
