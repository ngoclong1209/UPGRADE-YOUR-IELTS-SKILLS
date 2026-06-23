function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Youpass Tool')
      .addItem('Đồng bộ & Khôi phục Lỗi', 'syncStudents')
      .addToUi();
}

function syncStudents() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var studentSheet = ss.getSheetByName("Students");
  var lastRow = studentSheet.getLastRow();
  if (lastRow < 2) return;
  
  // Khôi phục Checkbox cho toàn bộ (Cột E, F, G, H)
  var range = studentSheet.getRange(2, 5, lastRow - 1, 4);
  var rule = SpreadsheetApp.newDataValidation().requireCheckbox().build();
  range.setDataValidation(rule);
  SpreadsheetApp.getUi().alert("Đồng bộ thành công!");
}

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var action = data.action;

    if (action === 'login') {
      return handleLogin(data);
    } else if (action === 'submit_full_test') {
      return handleFullTestSubmit(data);
    }
    
    return ContentService.createTextOutput(JSON.stringify({status: 'error', message: 'Hành động không hợp lệ'}))
        .setMimeType(ContentService.MimeType.JSON);
  } catch(err) {
    return ContentService.createTextOutput(JSON.stringify({status: 'error', message: err.toString()}))
        .setMimeType(ContentService.MimeType.JSON);
  }
}

function handleLogin(data) {
  var studentId = data.student_id;
  if (!studentId) return jsonResponse('error', 'Thiếu ID học viên');

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Students");
  var values = sheet.getDataRange().getValues();
  
  for (var i = 1; i < values.length; i++) {
    if (values[i][1] && values[i][1].toString().toUpperCase() === studentId.toUpperCase()) {
      return jsonResponse('success', 'Đăng nhập thành công');
    }
  }
  return jsonResponse('error', 'Không tìm thấy ID Học viên trong hệ thống');
}

function handleFullTestSubmit(data) {
  var studentId = data.student_id;
  var module = data.module; // "Reading Full Test" or "Listening Full Test"
  var testName = data.test_name; // "Test_1"
  var answers = data.answers; // array of 40 strings
  
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Submissions");
  if (!sheet) {
    sheet = ss.insertSheet("Submissions");
    // Thêm header
    var headers = ["Timestamp", "Student ID", "Module", "Test Name"];
    for(var i=1; i<=40; i++) headers.push("Q" + i);
    sheet.appendRow(headers);
  }
  
  var rowData = [new Date(), studentId, module, testName];
  for(var i=0; i<40; i++) {
    rowData.push(answers[i] || "");
  }
  sheet.appendRow(rowData);
  
  return jsonResponse('success', 'Đã lưu đáp án thành công!');
}

function jsonResponse(status, message) {
  return ContentService.createTextOutput(JSON.stringify({status: status, message: message}))
      .setMimeType(ContentService.MimeType.JSON);
}

// Hàm doGet để tương thích web app
function doGet(e) {
  return ContentService.createTextOutput("Youpass System Online");
}
