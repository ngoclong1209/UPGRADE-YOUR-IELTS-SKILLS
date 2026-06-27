const fs = require('fs');
const file = 'Reading_1232_Basic/frontend/template_reading.html';
let content = fs.readFileSync(file, 'utf8');

// The original logic is: lessonId: window.lessonData ? window.lessonData.title : 'Unknown',
// We need to change it to:
/*
                lessonId: (function(){
                    let fileParam = new URLSearchParams(window.location.search).get('file');
                    if(fileParam) {
                        let parts = fileParam.split('/');
                        if(parts.length === 2) {
                            return "Reading " + parts[0] + " - " + parts[1].replace('.js', '');
                        }
                    }
                    return window.lessonData ? window.lessonData.title : 'Unknown';
                })(),
*/

content = content.replace(
    /lessonId:\s*window\.lessonData \? window\.lessonData\.title : 'Unknown',/,
    `lessonId: (function(){
                    let fileParam = new URLSearchParams(window.location.search).get('file');
                    if(fileParam) {
                        let parts = fileParam.split('/');
                        if(parts.length === 2) {
                            return "Reading " + parts[0] + " - " + parts[1].replace('.js', '');
                        }
                    }
                    return window.lessonData ? window.lessonData.title : 'Unknown';
                })(),`
);

fs.writeFileSync(file, content);
console.log('patched');
