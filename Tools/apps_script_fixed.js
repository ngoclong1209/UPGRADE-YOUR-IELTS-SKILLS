// ==========================================
// KỊCH BẢN APPS SCRIPT: ĐĂNG NHẬP, LƯU ĐIỂM, CHẶN THIẾT BỊ
// ==========================================

// 1. MENU ADMIN TẠO GÓI HỌC TẬP
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('⚙️ IELTS Admin')
    .addItem('Khôi phục Checkbox (Bấm vào đây nếu mất ô tick)', 'fixCheckboxes')
    .addSeparator()
    .addItem('Tạo Gói Reading (Từ dòng hiện tại)', 'createReadingPackage')
    .addItem('Tạo Gói Listening (Từ dòng hiện tại)', 'createListeningPackage')
    .addItem('Tạo Gói Full Test (Từ dòng hiện tại)', 'createFullTestPackage')
    .addToUi();
}

function fixCheckboxes() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Students");
  if (!sheet) return;
  
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) lastRow = 100; // Mặc định 100 dòng nếu rỗng
  
  // Các cột E, F, G, H là Checkbox (Cột 5, 6, 7, 8)
  var range = sheet.getRange(2, 5, lastRow - 1, 4);
  var rule = SpreadsheetApp.newDataValidation().requireCheckbox().build();
  range.setDataValidation(rule);
  
  SpreadsheetApp.getUi().alert("✅ Đã khôi phục toàn bộ Checkbox ở các cột E, F, G, H!");
}

function createReadingPackage() {
  createPackage({ dataSheet: 'Reading_Data', startCol: 3, name: 'Reading', color: '#FFF2CC' });
}

function createListeningPackage() {
  createPackage({ dataSheet: 'Listening_Data', startCol: 13, name: 'Listening', color: '#D9EAD3' });
}

function createFullTestPackage() {
  createPackage({ dataSheet: 'FullTest_Data', startCol: 23, name: 'Full Test', color: '#F4CCCC' });
}

// 2. HÀM TẠO GÓI HỌC TẬP CHUNG (CHO MENU)
function createPackage(pkgConfig) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  
  if (sheet.getName() !== "Students") {
    SpreadsheetApp.getUi().alert("❌ Lỗi: Vui lòng chuyển sang sheet 'Students' để thực hiện chức năng này.");
    return;
  }
  
  var dataSheet = ss.getSheetByName(pkgConfig.dataSheet);
  if (!dataSheet) {
    SpreadsheetApp.getUi().alert("❌ Lỗi: Không tìm thấy sheet '" + pkgConfig.dataSheet + "'");
    return;
  }
  
  var row = sheet.getActiveCell().getRow();
  var studentName = sheet.getRange(row, 1).getValue();
  var studentIdRaw = sheet.getRange(row, 2).getValue();
  
  if (!studentIdRaw || row === 1) {
    SpreadsheetApp.getUi().alert("❌ Lỗi: Vui lòng chọn một dòng học viên hợp lệ.");
    return;
  }
  
  var studentId = studentIdRaw.toString().trim().toUpperCase();
  var personalSheetName = "HV_" + studentId;
  var personalSheet = ss.getSheetByName(personalSheetName);
  
  if (!personalSheet) {
    personalSheet = ss.insertSheet(personalSheetName);
    personalSheet.insertRowsBefore(1, 3);
    personalSheet.getRange("A1").setValue("Tên: " + studentName).setFontWeight("bold");
    personalSheet.getRange("A2").setValue("Mã HV: " + studentId).setFontWeight("bold");
  }
  
  var headerRange = personalSheet.getRange(4, pkgConfig.startCol, 1, 7);
  headerRange.setValues([["TÊN BÀI TẬP", "LINK", "LẦN 1", "LẦN 2", "LẦN 3", "MAX", "TRẠNG THÁI"]]);
  headerRange.setFontWeight("bold").setBackground(pkgConfig.color).setHorizontalAlignment("center");
  
  var items = dataSheet.getDataRange().getValues().slice(1);
  var writeRow = 5; 
  
  for (var i = 0; i < items.length; i++) {
    var itemName = items[i][2]; // Lấy cột Title (Index 2)
    var itemLink = items[i][3]; // Lấy cột URL (Index 3)
    
    if (itemName) {
      personalSheet.getRange(writeRow, pkgConfig.startCol).setValue(itemName);
      if (itemLink) {
        personalSheet.getRange(writeRow, pkgConfig.startCol + 1).setFormula('=HYPERLINK("' + itemLink + '", "Làm bài")');
      }
      writeRow++;
    }
  }
  
  personalSheet.setColumnWidth(pkgConfig.startCol + 1, 120);
  personalSheet.setColumnWidth(pkgConfig.startCol + 2, 250);
  personalSheet.setColumnWidth(pkgConfig.startCol + 3, 150);
  
  SpreadsheetApp.getUi().alert("✅ Đã tạo/cập nhật thành công gói " + pkgConfig.name + " cho học viên: " + studentName);
}

// 3. XỬ LÝ SỰ KIỆN EDIT TRỰC TIẾP TRÊN SHEET "Students"
function onEdit(e) {
  if (!e || !e.range) return;
  var sheet = e.range.getSheet();
  if (sheet.getName() === "Students") {
    var row = e.range.getRow();
    var col = e.range.getColumn();
    
    if (row <= 1) return; 
    
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
    // TẠO GÓI HỌC (CỘT E=5, F=6, G=7) DO BẠN ĐÃ THÊM CỘT "NGÀY BẮT ĐẦU" VÀO D
    var isReading = (col === 5 && (e.value === "TRUE" || e.value === true));
    var isListening = (col === 6 && (e.value === "TRUE" || e.value === true));
    var isFullTest = (col === 7 && (e.value === "TRUE" || e.value === true));
    
    if (isReading || isListening || isFullTest) {
      var pkgConfig;
      if (isReading) pkgConfig = {dataSheet: 'Reading_Data', startCol: 3, name: 'Reading', color: '#FFF2CC'};
      if (isListening) pkgConfig = {dataSheet: 'Listening_Data', startCol: 13, name: 'Listening', color: '#D9EAD3'};
      if (isFullTest) pkgConfig = {dataSheet: 'FullTest_Data', startCol: 23, name: 'Full Test', color: '#F4CCCC'};
      
      var studentName = sheet.getRange(row, 1).getValue();
      var studentIdRaw = sheet.getRange(row, 2).getValue();
      if (!studentIdRaw) {
        ss.toast("Dòng này chưa có ID Học viên!", "Lỗi");
        e.range.uncheck();
        return;
      }
      var studentId = studentIdRaw.toString().trim().toUpperCase();
      var personalSheetName = "HV_" + studentId;
      var personalSheet = ss.getSheetByName(personalSheetName);
      
      if (!personalSheet) {
        personalSheet = ss.insertSheet(personalSheetName);
        personalSheet.insertRowsBefore(1, 3);
        personalSheet.getRange("A1").setValue("Tên: " + studentName).setFontWeight("bold");
        personalSheet.getRange("A2").setValue("Mã HV: " + studentId).setFontWeight("bold");
      }
      
      var dataSheet = ss.getSheetByName(pkgConfig.dataSheet);
      if (!dataSheet) {
        ss.toast("Không tìm thấy sheet " + pkgConfig.dataSheet, "Lỗi");
        return;
      }
      
      var headerRange = personalSheet.getRange(4, pkgConfig.startCol, 1, 7);
      headerRange.setValues([["TÊN BÀI TẬP", "LINK", "LẦN 1", "LẦN 2", "LẦN 3", "MAX", "TRẠNG THÁI"]]);
      headerRange.setFontWeight("bold").setBackground(pkgConfig.color).setHorizontalAlignment("center");
      
      var items = dataSheet.getDataRange().getValues().slice(1);
      var writeRow = 5;
      
      for (var i = 0; i < items.length; i++) {
        var itemName = items[i][2]; // Cột C: Title
        var itemLink = items[i][3]; // Cột D: URL
        if (itemName) {
          personalSheet.getRange(writeRow, pkgConfig.startCol).setValue(itemName);
          if (itemLink) {
            personalSheet.getRange(writeRow, pkgConfig.startCol + 1).setFormula('=HYPERLINK("' + itemLink + '", "Làm bài")');
          }
          writeRow++;
        }
      }
      
      personalSheet.setColumnWidth(pkgConfig.startCol + 1, 120);
      personalSheet.setColumnWidth(pkgConfig.startCol + 2, 250);
      personalSheet.setColumnWidth(pkgConfig.startCol + 3, 150);
      
      ss.toast("Tạo thành công gói " + pkgConfig.name + "!", "Hoàn tất");
    }
    
    // XỬ LÝ XOÁ HỌC VIÊN (CỘT H = 8)
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

// 4. API BẮT ĐIỂM SỐ & ĐĂNG NHẬP (CHECK THIẾT BỊ)
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var action = data.action || "submit_score";
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
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

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": err.toString()})).setMimeType(ContentService.MimeType.JSON);
  }
}
