// 1. TẠO MENU CÔNG CỤ
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Youpass Tool')
      .addItem('Đồng bộ & Khôi phục Lỗi', 'syncStudents')
      .addToUi();
}

function syncStudents() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var studentSheet = ss.getSheetByName("Students");
  var allSheets = ss.getSheets();
  
  var lastRow = studentSheet.getLastRow();
  if (lastRow < 2) return;
  
  // Khôi phục Checkbox cho toàn bộ (Cột E, F, G, H)
  var range = studentSheet.getRange(2, 5, lastRow - 1, 4);
  var rule = SpreadsheetApp.newDataValidation().requireCheckbox().build();
  range.setDataValidation(rule);
  
  var studentData = studentSheet.getDataRange().getValues();
  var validStudentIds = [];
  var idToRowMap = {};
  
  for (var i = 1; i < studentData.length; i++) {
    var studentId = studentData[i][1] ? studentData[i][1].toString().trim().toUpperCase() : "";
    if (studentId) {
      validStudentIds.push(studentId);
      idToRowMap[studentId] = i + 1;
    }
  }
  
  for (var i = 0; i < allSheets.length; i++) {
    var sheetName = allSheets[i].getName();
    if (sheetName.indexOf("HV_") === 0) {
      var sId = sheetName.substring(3);
      if (validStudentIds.indexOf(sId) === -1) {
        ss.deleteSheet(allSheets[i]);
      }
    }
  }
  
  for (var i = 0; i < validStudentIds.length; i++) {
    var sId = validStudentIds[i];
    var sheetName = "HV_" + sId;
    var personalSheet = ss.getSheetByName(sheetName);
    var rowNum = idToRowMap[sId];
    var studentName = studentSheet.getRange(rowNum, 1).getValue().toString().trim();
    
    if (!personalSheet) {
      personalSheet = ss.insertSheet(sheetName);
      personalSheet.insertRowsBefore(1, 3);
      personalSheet.getRange("A1").setValue("Tên: " + studentName).setFontWeight("bold");
      personalSheet.getRange("A2").setValue("Mã HV: " + sId).setFontWeight("bold");
    } else {
      personalSheet.getRange("A1").setValue("Tên: " + studentName).setFontWeight("bold");
    }
    
    var sheetId = personalSheet.getSheetId();
    var cell = studentSheet.getRange(rowNum, 1); 
    var link = '#gid=' + sheetId;
    
    if (studentName) {
      try {
        var richValue = SpreadsheetApp.newRichTextValue()
          .setText(studentName)
          .setLinkUrl(link)
          .build();
        cell.setRichTextValue(richValue);
      } catch (e) {}
    }
  }
  SpreadsheetApp.getUi().alert("✅ Đã đồng bộ Sheet và khôi phục Checkbox cho toàn bộ Học Viên!");
}

// 2. TỰ ĐỘNG CHẠY KHI TÍCH VÀO CHECKBOX HOẶC NHẬP HỌC VIÊN MỚI
function onEdit(e) {
  if (!e || !e.range) return;
  var sheet = e.range.getSheet();
  
  if (sheet.getName() === "Students") {
    var col = e.range.getColumn();
    var row = e.range.getRow();
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
    if (row === 1) return;
    
    if (col === 1 || col === 2) {
      var studentName = sheet.getRange(row, 1).getValue();
      var studentIdRaw = sheet.getRange(row, 2).getValue();
      
      if (studentName && studentIdRaw && studentIdRaw.toString().trim() !== "") {
        var studentId = studentIdRaw.toString().trim().toUpperCase();
        var sheetName = "HV_" + studentId;
        
        var checkboxRange = sheet.getRange(row, 5, 1, 4);
        var currentValues = checkboxRange.getValues()[0];
        if (typeof currentValues[0] !== "boolean") {
          checkboxRange.insertCheckboxes();
          checkboxRange.setValues([[false, false, false, false]]);
        }
        
        var personalSheet = ss.getSheetByName(sheetName);
        if (!personalSheet) {
          personalSheet = ss.insertSheet(sheetName);
          personalSheet.insertRowsBefore(1, 3);
          personalSheet.getRange("A1").setValue("Tên: " + studentName).setFontWeight("bold");
          personalSheet.getRange("A2").setValue("Mã HV: " + studentId).setFontWeight("bold");
          ss.toast("Đã tạo hồ sơ trống cho: " + studentName, "Thành công");
        } else {
          personalSheet.getRange("A1").setValue("Tên: " + studentName).setFontWeight("bold");
        }
        
        try {
          var sheetId = personalSheet.getSheetId();
          var link = '#gid=' + sheetId;
          var richValue = SpreadsheetApp.newRichTextValue()
            .setText(studentName.toString())
            .setLinkUrl(link)
            .build();
          sheet.getRange(row, 1).setRichTextValue(richValue);
        } catch(err) {}
      }
    }
    
    var isReading = (col === 5 && (e.value === "TRUE" || e.value === true));
    var isListening = (col === 6 && (e.value === "TRUE" || e.value === true));
    var isFullTest = (col === 7 && (e.value === "TRUE" || e.value === true));
    
    if (isReading || isListening || isFullTest) {
      var pkgConfig;
      if (isReading) pkgConfig = {dataSheet: 'Reading_Data', startCol: 3, name: 'Reading 1323', color: '#FFF2CC'};
      if (isListening) pkgConfig = {dataSheet: 'Listening_Data', startCol: 13, name: 'Listening 3 Levels', color: '#D9EAD3'};
      if (isFullTest) pkgConfig = {dataSheet: 'FullTest_Data', startCol: 23, name: 'Full Tests', color: '#F4CCCC'};
      
      var studentName = sheet.getRange(row, 1).getValue();
      var studentIdRaw = sheet.getRange(row, 2).getValue();
      if (!studentIdRaw) {
        ss.toast("Lỗi: Không tìm thấy ID Học Viên", "Lỗi");
        e.range.uncheck();
        return;
      }
      var studentId = studentIdRaw.toString().trim().toUpperCase();
      var personalSheetName = "HV_" + studentId;
      var personalSheet = ss.getSheetByName(personalSheetName);
      
      if (!personalSheet) {
        ss.toast("Lỗi: Sheet học viên chưa được tạo. Hãy nhập lại ID.", "Lỗi");
        e.range.uncheck();
        return;
      }
      
      var existingHeader = personalSheet.getRange(4, pkgConfig.startCol).getValue();
      if (existingHeader === "TÊN BÀI TẬP") {
        ss.toast("Gói " + pkgConfig.name + " đã được tạo trước đó!", "Cảnh báo");
        return;
      }
      
      ss.toast("Đang tải dữ liệu gói " + pkgConfig.name + "...", "Hệ thống");
      
      var headerRange = personalSheet.getRange(4, pkgConfig.startCol, 1, 7);
      headerRange.setValues([["TÊN BÀI TẬP", "LINK", "LẦN 1", "LẦN 2", "LẦN 3", "MAX", "TRẠNG THÁI"]]);
      headerRange.setFontWeight("bold").setBackground(pkgConfig.color).setHorizontalAlignment("center");
      
      var items = [];
      if (isFullTest) {
        for (var idx = 1; idx <= 204; idx++) {
          items.push(["", "", "Full Test Listening - Test_" + idx, "https://ngoclong1209.github.io/UPGRADE-YOUR-IELTS-SKILLS/Listening_204_FullTest/Test_" + idx + "/Test_" + idx + ".html"]);
        }
        for (var idx = 1; idx <= 315; idx++) {
          if (idx === 105) continue; 
          items.push(["", "", "Full Test Reading - Test_" + idx, "https://ngoclong1209.github.io/UPGRADE-YOUR-IELTS-SKILLS/Reading_315_FullTest/Test_" + idx + "/Test_" + idx + ".html"]);
        }
      } else {
        var dataSheet = ss.getSheetByName(pkgConfig.dataSheet);
        if (!dataSheet) {
          ss.toast("Không tìm thấy sheet " + pkgConfig.dataSheet, "Lỗi");
          return;
        }
        items = dataSheet.getDataRange().getValues().slice(1);
      }
      
      var writeRow = 5;
      for (var i = 0; i < items.length; i++) {
        var itemName = items[i][2]; 
        var itemLink = items[i][3]; 
        if (itemName) {
          personalSheet.getRange(writeRow, pkgConfig.startCol).setValue(itemName);
          if (itemLink) {
            try {
              var richValue = SpreadsheetApp.newRichTextValue()
                .setText("Làm bài")
                .setLinkUrl(itemLink.toString().trim())
                .build();
              personalSheet.getRange(writeRow, pkgConfig.startCol + 1).setRichTextValue(richValue);
            } catch (e) {
              personalSheet.getRange(writeRow, pkgConfig.startCol + 1).setValue(itemLink);
            }
          }
          writeRow++;
        }
      }
      
      personalSheet.setColumnWidth(pkgConfig.startCol + 1, 120);
      personalSheet.setColumnWidth(pkgConfig.startCol + 2, 250);
      personalSheet.setColumnWidth(pkgConfig.startCol + 3, 150);
      
      ss.toast("Tạo thành công gói " + pkgConfig.name + "!", "Hoàn tất");
    }
    
    if (col === 8 && (e.value === "TRUE" || e.value === true)) {
      var studentIdRaw = sheet.getRange(row, 2).getValue();
      if (studentIdRaw) {
        var studentId = studentIdRaw.toString().trim().toUpperCase();
        var personalSheet = ss.getSheetByName("HV_" + studentId);
        ss.toast("Đang xoá học viên " + studentId + "...", "Hệ thống");
        if (personalSheet) {
          ss.deleteSheet(personalSheet);
        }
        sheet.deleteRow(row);
        ss.toast("Đã xoá thành công!", "Hoàn tất");
      }
    }
  }
}

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var action = data.action || "submit_score";
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
    // ==========================================
    // 1. XỬ LÝ LOGIN (Đăng nhập)
    // ==========================================
    if (action === "login") {
      var studentId = data.student_id ? data.student_id.toString().trim().toUpperCase() : "";
      var deviceId = data.device_id ? data.device_id.toString().trim() : "";
      if (!studentId || !deviceId) throw new Error("Missing parameters");
      
      var studentSheet = ss.getSheetByName("Students");
      var sData = studentSheet.getDataRange().getValues();
      
      var foundRow = -1;
      var currentDevices = "";
      for (var i = 1; i < sData.length; i++) {
        if (sData[i][1].toString().trim().toUpperCase() === studentId) {
          foundRow = i + 1;
          currentDevices = sData[i][2] ? sData[i][2].toString().trim() : ""; 
          break;
        }
      }
      
      if (foundRow === -1) {
        return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Sai ID Học Viên"})).setMimeType(ContentService.MimeType.JSON);
      }
      
      var devices = currentDevices ? currentDevices.split(",").map(function(d){ return d.trim(); }) : [];
      
      if (devices.indexOf(deviceId) !== -1) {
        return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "Login OK"})).setMimeType(ContentService.MimeType.JSON);
      }
      
      if (devices.length < 2) {
        devices.push(deviceId);
        studentSheet.getRange(foundRow, 3).setValue(devices.join(", "));
        return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "Login OK (Đã đăng ký thiết bị mới)"})).setMimeType(ContentService.MimeType.JSON);
      } else {
        return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Tài khoản của bạn đã đạt giới hạn 2 thiết bị. Vui lòng liên hệ Admin để reset."})).setMimeType(ContentService.MimeType.JSON);
      }
    }

    // ==========================================
    // 2. XỬ LÝ SUBMIT_FULL_TEST (Nộp bài 40 câu)
    // ==========================================
    if (action === "submit_full_test") {
      var studentId = data.student_id ? data.student_id.toString().trim().toUpperCase() : "";
      var module = data.module; // "Reading Full Test" or "Listening Full Test"
      var testName = data.test_name; // "Test_1"
      var answers = data.answers; // array of 40 strings
      
      var subSheet = ss.getSheetByName("Submissions_FullTest");
      if (!subSheet) {
        subSheet = ss.insertSheet("Submissions_FullTest");
        var headers = ["Timestamp", "Student ID", "Module", "Test Name"];
        for(var i=1; i<=40; i++) headers.push("Q" + i);
        subSheet.appendRow(headers);
      }
      
      var rowData = [new Date(), studentId, module, testName];
      for(var i=0; i<40; i++) {
        rowData.push(answers[i] || "");
      }
      subSheet.appendRow(rowData);
      
      return ContentService.createTextOutput(JSON.stringify({status: 'success', message: 'Đã lưu đáp án thành công!'}))
          .setMimeType(ContentService.MimeType.JSON);
    }
    
    // ==========================================
    // 3. XỬ LÝ SUBMIT_SCORE (Nộp điểm bài tập thường)
    // ==========================================
    if (action === "submit_score") {
      var studentId = data.student_id ? data.student_id.toString().trim().toUpperCase() : "";
      var lessonName = data.lesson_name;
      var newScoreStr = data.score;
      
      if (!studentId || !lessonName || !newScoreStr) throw new Error("Missing parameters");
      
      var scorePct = 0;
      if (newScoreStr.indexOf('/') !== -1) {
        var parts = newScoreStr.split('/');
        scorePct = (parseFloat(parts[0]) / parseFloat(parts[1])) * 100;
      } else if (newScoreStr.indexOf('%') !== -1) {
        scorePct = parseFloat(newScoreStr.replace('%', ''));
      } else {
        scorePct = parseFloat(newScoreStr); 
      }

      var personalSheet = ss.getSheetByName("HV_" + studentId);
      if (!personalSheet) {
        return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Không tìm thấy dữ liệu học viên"})).setMimeType(ContentService.MimeType.JSON);
      }
      
      var planData = personalSheet.getDataRange().getValues();
      var lessonRowIdx = -1;
      var lessonColIdx = -1;
      
      for (var r = 0; r < planData.length; r++) {
        for (var c = 0; c < planData[r].length; c++) {
          if (planData[r][c] === lessonName) {
            lessonRowIdx = r + 1;
            lessonColIdx = c + 1;
            break;
          }
        }
        if (lessonRowIdx !== -1) break;
      }
      
      if (lessonRowIdx === -1 || lessonColIdx === -1) {
        return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Bài tập không có trong kế hoạch"})).setMimeType(ContentService.MimeType.JSON);
      }
      
      var attempt1Col = lessonColIdx + 2;
      var attempt2Col = lessonColIdx + 3;
      var attempt3Col = lessonColIdx + 4;
      var maxScoreCol = lessonColIdx + 5;
      var statusCol = lessonColIdx + 6;
      
      var cIndex = lessonColIdx - 1;
      var attempt1 = planData[lessonRowIdx-1][cIndex + 2] || "";
      var attempt2 = planData[lessonRowIdx-1][cIndex + 3] || "";
      var attempt3 = planData[lessonRowIdx-1][cIndex + 4] || "";
      var maxScore = parseFloat(planData[lessonRowIdx-1][cIndex + 5]) || 0;
      
      var attemptCount = 0;
      if (attempt1 !== "") attemptCount++;
      if (attempt2 !== "") attemptCount++;
      if (attempt3 !== "") attemptCount++;
      
      if (attemptCount >= 3) {
        return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "MAX_ATTEMPTS_REACHED", "detail": "Bạn đã làm bài này quá 3 lần."})).setMimeType(ContentService.MimeType.JSON);
      }
      
      var writeCol = lessonColIdx + 2 + attemptCount; 
      personalSheet.getRange(lessonRowIdx, writeCol).setValue(newScoreStr);
      
      var finalMaxScore = maxScore;
      if (scorePct > maxScore || attemptCount === 0) {
        finalMaxScore = scorePct;
        personalSheet.getRange(lessonRowIdx, maxScoreCol).setValue(finalMaxScore.toFixed(2));
      }
      
      var status = finalMaxScore >= 70 ? "✅ Passed" : "❌ Failed";
      personalSheet.getRange(lessonRowIdx, statusCol).setValue(status);
      
      var subSheet = ss.getSheetByName("Submissions");
      if (subSheet) {
        subSheet.appendRow([new Date(), studentId, lessonName, newScoreStr, scorePct.toFixed(2)]);
      }
      
      return ContentService.createTextOutput(JSON.stringify({
        "status": "success", 
        "message": "Đã lưu điểm!",
        "attempt": attemptCount + 1,
        "max_score": finalMaxScore.toFixed(2),
        "passed": finalMaxScore >= 70
      })).setMimeType(ContentService.MimeType.JSON);
    }

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": err.toString()})).setMimeType(ContentService.MimeType.JSON);
  }
}

// Hàm doGet để tương thích web app
function doGet(e) {
  return ContentService.createTextOutput("Youpass System Online");
}
