/**
 * =========================================================================
 * 江夏傳統整復推拿（板橋館）- Google 日曆與試算表雙向預約雲端橋樑 (GAS)
 * =========================================================================
 * 
 * 【主要功能】：
 * 1. 雙向同步：顧客線上預約即時寫入 Google 日曆，日曆行程即時反映至後台。
 * 2. Telegram 即時推播：顧客送出預約，賴師傅手機 Telegram 立刻收到推播提醒。
 * 3. 永久記帳：可自動同步將預約寫入 Google Sheets 試算表留存。
 * 4. 遠端銷毀：後台點擊刪除，同步自 Google 日曆移除事件。
 */

var API_SECRET = 'jiangxia_banqiao_2026';
var TARGET_CALENDAR_NAME = '江夏傳統整復推拿_板橋館';

// Telegram Bot 即時推播設定 (新預約立即叮咚通知師傅手機)
var TG_BOT_TOKEN = '7789811491:AAG2c7qWuhB2yIacI6_KSsZrXjRCcvClWcI';
var TG_CHAT_ID = '1890470289';

// (選配) Google 試算表 ID：若有建立專屬試算表，填入試算表網址中的 ID，留空則自動使用當前試算表
var SPREADSHEET_ID = '';

// 取得目標日曆（自動尋找「江夏傳統整復推拿_板橋館」，找不到則模糊搜尋，最後退回主日曆）
function getTargetCalendar() {
  if (TARGET_CALENDAR_NAME) {
    var cals = CalendarApp.getCalendarsByName(TARGET_CALENDAR_NAME);
    if (cals && cals.length > 0) {
      return cals[0];
    }
    var all = CalendarApp.getAllCalendars();
    for (var i = 0; i < all.length; i++) {
      if (all[i].getName().indexOf('江夏') !== -1) {
        return all[i];
      }
    }
  }
  return CalendarApp.getDefaultCalendar();
}

// 發送 Telegram 即時推播通知
function sendTelegramNotification(text) {
  if (!TG_BOT_TOKEN || !TG_CHAT_ID) return;
  try {
    var url = 'https://api.telegram.org/bot' + TG_BOT_TOKEN + '/sendMessage';
    var payload = {
      chat_id: TG_CHAT_ID,
      text: text,
      parse_mode: 'HTML',
      disable_web_page_preview: true
    };
    UrlFetchApp.fetch(url, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
  } catch (e) {
    Logger.log('Telegram 通知發送失敗: ' + e.toString());
  }
}

// ==========================================
// 1. GET 請求處理 (Ping 診斷、拉取預約、刪除預約)
// ==========================================
function doGet(e) {
  try {
    var params = (e && e.parameter) ? e.parameter : {};
    var secret = params.secret || '';
    var action = params.action || 'ping';

    if (secret !== API_SECRET && action !== 'ping') {
      return createJsonResponse({ success: false, message: '未授權的安全金鑰' });
    }

    var cal = getTargetCalendar();

    // 1-1. 連線檢測
    if (action === 'ping') {
      var now = new Date();
      var startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0);
      var endOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);
      var todayEvents = cal.getEvents(startOfDay, endOfDay);

      var hasSpreadsheet = false;
      try {
        var ss = SPREADSHEET_ID ? SpreadsheetApp.openById(SPREADSHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
        if (ss) hasSpreadsheet = true;
      } catch (err) {
        hasSpreadsheet = false;
      }

      return createJsonResponse({
        success: true,
        message: 'Google 雲端橋樑運作正常！',
        diagnostics: {
          calendarName: cal ? cal.getName() : '主要日曆',
          serverTime: Utilities.formatDate(now, 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss'),
          todayEventsCount: todayEvents.length,
          hasSpreadsheet: hasSpreadsheet,
          hasTelegram: !!(TG_BOT_TOKEN && TG_CHAT_ID)
        }
      });
    }

    // 1-2. 抓取預約列表
    if (action === 'getEvents') {
      var now = new Date();
      var startTime = new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000);
      var endTime = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);
      var events = cal.getEvents(startTime, endTime);

      var data = [];
      for (var i = 0; i < events.length; i++) {
        var evt = events[i];
        var title = (evt.getTitle() || '').trim();
        var desc = evt.getDescription() || '';

        var customerName = title;
        var phone = '';

        // 從描述欄優先匹配顧客姓名與電話
        var nameMatch = desc.match(/(?:顧客姓名|姓名|預約人)[:：]\s*([^\n\r]+)/);
        if (nameMatch) {
          customerName = nameMatch[1].trim();
        }

        var phoneMatch = desc.match(/(?:聯絡電話|電話|手機)[:：]\s*([0-9-]+)/);
        if (phoneMatch) {
          phone = phoneMatch[1].trim();
        }

        // 若無描述欄姓名，從行程標題進行智慧解析 (相容 "粘玉明 - 0932122288"、"王大偉 0912345678"、"【預約】陳先生")
        if (!nameMatch) {
          if (title.indexOf(' - ') !== -1) {
            var dashParts = title.split(' - ');
            customerName = dashParts[0].trim();
            if (!phone && dashParts.length > 1 && /^[0-9-]+$/.test(dashParts[1].trim())) {
              phone = dashParts[1].trim();
            }
          } else {
            var titleParts = title.split(/\s+/);
            if (titleParts.length >= 2 && /^[0-9-]+$/.test(titleParts[titleParts.length - 1])) {
              if (!phone) phone = titleParts[titleParts.length - 1];
              customerName = titleParts.slice(0, titleParts.length - 1).join(' ');
            } else if (title.indexOf('【預約】') !== -1) {
              customerName = title.replace('【預約】', '').split('-')[0].trim();
            }
          }
        }

        // 清理姓名中的首尾符號
        customerName = customerName.replace(/^[-–—\s]+|[-–—\s]+$/g, '').trim();
        if (/^[0-9-]+$/.test(customerName) && !phone) {
          phone = customerName;
        }

        var serviceItem = '徒手調理放鬆';
        var status = '已確認';

        var serviceMatch = desc.match(/項目[:：]\s*([^\n\r]+)/);
        if (serviceMatch) serviceItem = serviceMatch[1].trim();

        var statusMatch = desc.match(/狀態[:：]\s*([^\n\r]+)/);
        if (statusMatch) status = statusMatch[1].trim();

        var startIso = Utilities.formatDate(evt.getStartTime(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss').replace(' ', 'T');
        var endIso = Utilities.formatDate(evt.getEndTime(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss').replace(' ', 'T');

        data.push({
          id: evt.getId(),
          customerName: customerName,
          phone: phone,
          serviceItem: serviceItem,
          status: status,
          notes: desc,
          start: startIso,
          end: endIso
        });
      }

      // 讀取試算表歷史客戶 CRM 名冊（跨設備防失憶）
      var sheetCustomers = [];
      try {
        var ss = SPREADSHEET_ID ? SpreadsheetApp.openById(SPREADSHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
        if (ss) {
          var bSheet = ss.getSheetByName('預約紀錄名冊');
          if (bSheet) {
            var bRows = bSheet.getDataRange().getValues();
            for (var bi = 1; bi < bRows.length; bi++) {
              var cName = String(bRows[bi][2] || '').trim();
              var cPhone = String(bRows[bi][3] || '').trim();
              var cNotes = String(bRows[bi][8] || '').trim();
              var cDate = String(bRows[bi][0] || '').slice(0, 10);
              if (cName || cPhone) {
                sheetCustomers.push({
                  name: cName,
                  phone: cPhone,
                  last_visited_at: cDate,
                  health_notes: cNotes
                });
              }
            }
          }
        }
      } catch (custErr) {
        Logger.log('讀取試算表顧客名冊非致命錯誤: ' + custErr.toString());
      }

      return createJsonResponse({
        success: true,
        count: data.length,
        data: data,
        sheetCustomers: sheetCustomers
      });
    }

    // 1-3. 刪除預約行程 (支援 deleteEvent / delete / cancel - 方案 B：日曆徹底乾淨，試算表永久留底)
    if (action === 'deleteEvent' || action === 'delete' || action === 'cancel') {
      var eventId = params.eventId || params.id;
      if (!eventId) {
        return createJsonResponse({ success: false, message: '缺少 eventId 或 id' });
      }
      try {
        var evt = cal.getEventById(eventId);
        if (!evt && eventId.indexOf('@google.com') === -1) {
          evt = cal.getEventById(eventId + '@google.com');
        }
        if (!evt && eventId.indexOf('@google.com') !== -1) {
          evt = cal.getEventById(eventId.replace('@google.com', ''));
        }
        if (evt) {
          var delTitle = evt.getTitle();
          var delStart = Utilities.formatDate(evt.getStartTime(), 'Asia/Taipei', 'yyyy/MM/dd (E) HH:mm');
          
          // 方案 B 核心：刪除前，先永久歸檔至 Google 試算表（更新名冊狀態並寫入取消名冊）
          recordCancellationToSpreadsheet(evt, eventId);

          // 徹底自 Google 日曆刪除，時段立即釋出，新客戶可約，日曆保持 100% 乾淨
          evt.deleteEvent();

          // 刪除時亦推播提醒師傅
          try {
            var tgDelMsg = '🗑️ <b>【江夏板橋館・預約取消/刪除提醒】</b>\n' +
              '━━━━━━━━━━━━━━━\n' +
              '👤 <b>排程資訊</b>：' + delTitle + '\n' +
              '📅 <b>原約時段</b>：' + delStart + '\n' +
              '━━━━━━━━━━━━━━━\n' +
              '✨ <b>日曆狀態</b>：該時段已自 Google 日曆移除並重新釋出為空檔。\n' +
              '📋 <b>歸檔備查</b>：資料已安全寫入 Google 試算表「預約取消備查名冊」。\n' +
              '👉 <a href="https://azach258.github.io/jiangxia-banqiao/dashboard/?openExternalBrowser=1">點此開啟師傅排程看板</a>';
            sendTelegramNotification(tgDelMsg);
          } catch(e) {}

          return createJsonResponse({
            success: true,
            message: '已成功歸檔至試算表並自 Google 日曆刪除行程！',
            eventId: eventId
          });
        } else {
          return createJsonResponse({
            success: true,
            message: '日曆上已無該行程 (可能已手動刪除)',
            eventId: eventId
          });
        }
      } catch (delErr) {
        return createJsonResponse({
          success: false,
          error: '刪除日曆事件失敗: ' + delErr.toString()
        });
      }
    }

    // 1-4. 更新預約備註主訴 (支援 updateNotes)
    if (action === 'updateNotes') {
      var updateRes = handleUpdateNotes(params);
      return createJsonResponse(updateRes);
    }

    // 1-5. 修改預約時段 (支援 updateBookingTime)
    if (action === 'updateBookingTime') {
      var updateTimeRes = handleUpdateBookingTime(params);
      return createJsonResponse(updateTimeRes);
    }

    // 1-6. 更新顧客 CRM 檔案 (支援 updateCustomer)
    if (action === 'updateCustomer') {
      var updateCustRes = handleUpdateCustomer(params);
      return createJsonResponse(updateCustRes);
    }

    return createJsonResponse({ success: false, message: '未知的 GET 操作指令: ' + action });

  } catch (error) {
    return createJsonResponse({ success: false, error: error.toString() });
  }
}

// ==========================================
// 2. POST 請求處理 (建立預約 ＆ 備援刪除)
// ==========================================
function doPost(e) {
  try {
    var payload = {};
    if (e && e.postData && e.postData.contents) {
      try {
        payload = JSON.parse(e.postData.contents);
      } catch (err) {
        payload = (e && e.parameter) ? e.parameter : {};
      }
    } else if (e && e.parameter) {
      payload = e.parameter;
    }

    var secret = payload.secret || '';
    if (secret !== API_SECRET) {
      return createJsonResponse({ success: false, message: '未授權的安全金鑰' });
    }

    var action = payload.action || 'create';

    // 2-1. 建立預約
    if (action === 'create') {
      var customerName = (payload.customerName || '顧客').trim();
      var phone = (payload.phone || '').trim();
      var serviceItem = payload.serviceItem || '傳統全身整復放鬆調理';
      var durationMin = parseInt(payload.durationMin || 60, 10);
      var startTimeStr = payload.startTime;
      var notes = payload.notes || '';
      var staff = payload.staff || '賴師傅';
      var status = payload.status || '已確認';

      if (!startTimeStr) {
        return createJsonResponse({ success: false, message: '缺少開始時間 startTime' });
      }

      var start = new Date(startTimeStr);
      var end = new Date(start.getTime() + durationMin * 60 * 1000);

      var cal = getTargetCalendar();
      var eventTitle = customerName + (phone ? ' ' + phone : '');
      
      var eventDescription = '顧客姓名：' + customerName + '\n' +
        '聯絡電話：' + phone + '\n' +
        '預約項目：' + serviceItem + '\n' +
        '預約時長：' + durationMin + ' 分鐘\n' +
        '服務師傅：' + staff + '\n' +
        '預約狀態：' + status + '\n' +
        '備註說明：' + notes + '\n' +
        '建立時間：' + Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');

      var event = cal.createEvent(eventTitle, start, end, {
        description: eventDescription,
        location: '新北市板橋區館前西路152號之1'
      });

      // 自動備份寫入 Google 試算表 (若有設定 SPREADSHEET_ID 或為試算表綁定專案)
      try {
        var ss = SPREADSHEET_ID ? SpreadsheetApp.openById(SPREADSHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
        if (ss) {
          var sheet = ss.getSheetByName('預約紀錄名冊');
          if (!sheet) {
            sheet = ss.insertSheet('預約紀錄名冊');
            sheet.appendRow(['預約時間', '結束時間', '顧客姓名', '手機號碼', '調理項目', '時長(分)', '服務師傅', '狀態', '備註說明', '日曆事件ID']);
            sheet.getRange(1, 1, 1, 10).setFontWeight('bold').setBackground('#FAF7F2');
          }
          sheet.appendRow([
            Utilities.formatDate(start, 'Asia/Taipei', 'yyyy-MM-dd HH:mm'),
            Utilities.formatDate(end, 'Asia/Taipei', 'yyyy-MM-dd HH:mm'),
            customerName,
            phone,
            serviceItem,
            durationMin,
            staff,
            status,
            notes,
            event.getId()
          ]);
        }
      } catch (sheetErr) {
        Logger.log('試算表非致命錯誤: ' + sheetErr.toString());
      }

      // 即時推播通知賴師傅的手機 Telegram
      try {
        var startFormatted = Utilities.formatDate(start, 'Asia/Taipei', 'yyyy/MM/dd (E) HH:mm');
        var tgMsg = '🔔 <b>【江夏板橋館・新線上預約通報】</b>\n' +
          '━━━━━━━━━━━━━━━\n' +
          '👤 <b>顧客姓名</b>：' + customerName + '\n' +
          '📱 <b>聯絡電話</b>：' + (phone || '未填寫') + '\n' +
          '💆 <b>預約方案</b>：' + serviceItem + '\n' +
          '⏱️ <b>預約時長</b>：' + durationMin + ' 分鐘\n' +
          '📅 <b>預約時段</b>：' + startFormatted + '\n' +
          '📝 <b>顧客備註</b>：' + (notes || '無') + '\n' +
          '━━━━━━━━━━━━━━━\n' +
          '👉 <a href="https://azach258.github.io/jiangxia-banqiao/dashboard/?openExternalBrowser=1">點此開啟師傅排程看板</a>';
        sendTelegramNotification(tgMsg);
      } catch (tgErr) {
        Logger.log('Telegram 通知非致命錯誤: ' + tgErr.toString());
      }

      var formattedStart = Utilities.formatDate(start, 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
      return createJsonResponse({
        success: true,
        message: '預約已成功寫入 Google 日曆與試算表！',
        calendarName: cal.getName(),
        eventTitle: eventTitle,
        eventId: event.getId(),
        start: formattedStart
      });
    }

    // 2-2. 刪除預約 (方案 B：日曆徹底乾淨，試算表永久留底)
    if (action === 'deleteEvent' || action === 'delete' || action === 'cancel') {
      var eventId = payload.eventId || payload.id;
      var cal = getTargetCalendar();
      if (!eventId) {
        return createJsonResponse({ success: false, message: '缺少 eventId 或 id' });
      }
      try {
        var evt = cal.getEventById(eventId);
        if (!evt && eventId.indexOf('@google.com') === -1) {
          evt = cal.getEventById(eventId + '@google.com');
        }
        if (!evt && eventId.indexOf('@google.com') !== -1) {
          evt = cal.getEventById(eventId.replace('@google.com', ''));
        }
        if (evt) {
          var pDelTitle = evt.getTitle();
          var pDelStart = Utilities.formatDate(evt.getStartTime(), 'Asia/Taipei', 'yyyy/MM/dd (E) HH:mm');
          
          // 方案 B 核心：刪除前，先永久歸檔至 Google 試算表
          recordCancellationToSpreadsheet(evt, eventId);

          // 徹底自 Google 日曆刪除，時段立即釋出，新客戶可約，日曆保持 100% 乾淨
          evt.deleteEvent();

          try {
            var tgPDelMsg = '🗑️ <b>【江夏板橋館・預約取消/刪除提醒】</b>\n' +
              '━━━━━━━━━━━━━━━\n' +
              '👤 <b>排程資訊</b>：' + pDelTitle + '\n' +
              '📅 <b>原約時段</b>：' + pDelStart + '\n' +
              '━━━━━━━━━━━━━━━\n' +
              '✨ <b>日曆狀態</b>：該時段已自 Google 日曆移除並重新釋出為空檔。\n' +
              '📋 <b>歸檔備查</b>：資料已安全寫入 Google 試算表「預約取消備查名冊」。\n' +
              '👉 <a href="https://azach258.github.io/jiangxia-banqiao/dashboard/?openExternalBrowser=1">點此開啟師傅排程看板</a>';
            sendTelegramNotification(tgPDelMsg);
          } catch(e) {}

          return createJsonResponse({
            success: true,
            message: '已成功歸檔至試算表並自 Google 日曆刪除行程！',
            eventId: eventId
          });
        } else {
          return createJsonResponse({
            success: true,
            message: '日曆上已無該行程 (可能已手動刪除)',
            eventId: eventId
          });
        }
      } catch (err) {
        return createJsonResponse({
          success: false,
          error: '刪除日曆事件失敗: ' + err.toString()
        });
      }
    }

    // 2-3. 更新預約備註主訴
    if (action === 'updateNotes') {
      var updatePostRes = handleUpdateNotes(payload);
      return createJsonResponse(updatePostRes);
    }

    // 2-4. 修改預約時段 (支援 updateBookingTime)
    if (action === 'updateBookingTime') {
      var updateTimePostRes = handleUpdateBookingTime(payload);
      return createJsonResponse(updateTimePostRes);
    }

    // 2-5. 更新顧客 CRM 檔案 (支援 updateCustomer)
    if (action === 'updateCustomer') {
      var updateCustPostRes = handleUpdateCustomer(payload);
      return createJsonResponse(updateCustPostRes);
    }

    return createJsonResponse({ success: false, message: '未知的 POST 操作指令: ' + action });

  } catch (error) {
    return createJsonResponse({ success: false, error: error.toString() });
  }
}

// ==========================================
// 3. 通用 JSON 回應處理
// ==========================================
function createJsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

// ==========================================
// 4. 測試診斷專用 (若在 GAS 介面按「執行」，請選此函式)
// ==========================================
function test_run_diagnostics() {
  var res = doGet({ parameter: { action: 'ping', secret: API_SECRET } });
  Logger.log(res.getContent());
}

// ==========================================
// 5. 方案 B 核心輔助函式：將取消預約安全歸檔至 Google 試算表
// ==========================================
function recordCancellationToSpreadsheet(evt, eventId) {
  try {
    var ss = SPREADSHEET_ID ? SpreadsheetApp.openById(SPREADSHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
    if (!ss) return;

    var nowStr = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
    var title = evt ? evt.getTitle() : '';
    var startStr = evt ? Utilities.formatDate(evt.getStartTime(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm') : '';
    var desc = evt ? (evt.getDescription() || '') : '';

    var phoneMatch = desc.match(/電話[:：]\s*([0-9-]+)/);
    var phone = phoneMatch ? phoneMatch[1].trim() : '';
    var name = title;
    var titleParts = title.split(/\s+/);
    if (titleParts.length >= 2 && /^[0-9-]+$/.test(titleParts[titleParts.length - 1])) {
      phone = phone || titleParts[titleParts.length - 1];
      name = titleParts.slice(0, titleParts.length - 1).join(' ');
    }

    var serviceMatch = desc.match(/項目[:：]\s*([^\n\r]+)/);
    var serviceItem = serviceMatch ? serviceMatch[1].trim() : '傳統整復調理';

    // 1. 嘗試在「預約紀錄名冊」中將對應紀錄標記為「已取消」
    var bookingSheet = ss.getSheetByName('預約紀錄名冊');
    if (bookingSheet) {
      var data = bookingSheet.getDataRange().getValues();
      var targetId = (eventId || '').replace('@google.com', '');
      for (var r = 1; r < data.length; r++) {
        var rowId = String(data[r][9] || '').replace('@google.com', ''); // 第10欄是日曆事件ID
        if (rowId && targetId && (rowId === targetId || rowId.indexOf(targetId) !== -1 || targetId.indexOf(rowId) !== -1)) {
          bookingSheet.getRange(r + 1, 8).setValue('已取消'); // 第8欄是狀態
          var oldNotes = String(data[r][8] || '');
          bookingSheet.getRange(r + 1, 9).setValue(oldNotes + ' [取消於 ' + nowStr + ']');
          break;
        }
      }
    }

    // 2. 獨立寫入「預約取消備查名冊」工作表，確保 100% 永久留存
    var cancelSheet = ss.getSheetByName('預約取消備查名冊');
    if (!cancelSheet) {
      cancelSheet = ss.insertSheet('預約取消備查名冊');
      cancelSheet.appendRow(['取消登記時間', '原約時段', '顧客姓名', '手機電話', '預約項目', '事件ID', '完整備註']);
      cancelSheet.getRange(1, 1, 1, 7).setFontWeight('bold').setBackground('#FEE2E2');
    }
    cancelSheet.appendRow([
      nowStr,
      startStr,
      name,
      phone,
      serviceItem,
      eventId || '',
      desc
    ]);
  } catch (err) {
    Logger.log('試算表取消歸檔非致命錯誤: ' + err.toString());
  }
}

// ==========================================
// 6. 備註即時更新函式：同步更新 Google 日曆事件與試算表備註
// ==========================================
function handleUpdateNotes(params) {
  var eventId = params.eventId || params.id;
  var newNotes = params.notes || '';
  if (!eventId) {
    return { success: false, message: '缺少 eventId 或 id' };
  }
  try {
    var cal = getTargetCalendar();
    var evt = cal.getEventById(eventId);
    if (!evt && eventId.indexOf('@google.com') === -1) {
      evt = cal.getEventById(eventId + '@google.com');
    }
    if (!evt && eventId.indexOf('@google.com') !== -1) {
      evt = cal.getEventById(eventId.replace('@google.com', ''));
    }
    // 備援搜尋：若以 ID 未尋獲，透過電話號碼、姓名與預約時間進行精確模糊搜尋
    if (!evt && (params.startTime || params.phone || params.customerName)) {
      var searchTime = params.startTime ? new Date(params.startTime) : new Date();
      var startRange = new Date(searchTime.getTime() - 24 * 60 * 60 * 1000);
      var endRange = new Date(searchTime.getTime() + 24 * 60 * 60 * 1000);
      var nearbyEvents = cal.getEvents(startRange, endRange);
      var cleanP = (params.phone || '').replace(/[^0-9]/g, '');
      for (var k = 0; k < nearbyEvents.length; k++) {
        var ne = nearbyEvents[k];
        var nTitle = ne.getTitle() || '';
        var nDesc = ne.getDescription() || '';
        if ((cleanP && (nTitle.indexOf(cleanP) !== -1 || nDesc.indexOf(cleanP) !== -1)) || 
            (params.customerName && nTitle.indexOf(params.customerName) !== -1)) {
          evt = ne;
          eventId = ne.getId();
          break;
        }
      }
    }
    if (evt) {
      var oldDesc = evt.getDescription() || '';
      var updatedDesc = '';
      if (oldDesc.indexOf('備註說明：') !== -1) {
        updatedDesc = oldDesc.replace(/備註說明：[^\n\r]*/, '備註說明：' + newNotes);
      } else {
        updatedDesc = oldDesc + '\n備註說明：' + newNotes;
      }
      evt.setDescription(updatedDesc);

      // 同步更新 Google 試算表中的備註
      try {
        var ss = SPREADSHEET_ID ? SpreadsheetApp.openById(SPREADSHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
        if (ss) {
          var sheet = ss.getSheetByName('預約紀錄名冊');
          if (sheet) {
            var data = sheet.getDataRange().getValues();
            var targetId = (eventId || '').replace('@google.com', '');
            for (var r = 1; r < data.length; r++) {
              var rowId = String(data[r][9] || '').replace('@google.com', '');
              if (rowId && targetId && (rowId === targetId || rowId.indexOf(targetId) !== -1 || targetId.indexOf(rowId) !== -1)) {
                sheet.getRange(r + 1, 9).setValue(newNotes);
                break;
              }
            }
          }
        }
      } catch (se) {
        Logger.log('試算表備註更新非致命錯誤: ' + se.toString());
      }

      return {
        success: true,
        message: '已成功同步更新 Google 日曆與試算表備註！',
        eventId: eventId,
        notes: newNotes
      };
    } else {
      return { success: false, message: '日曆上未找到該行程 (可能已手動刪除)' };
    }
  } catch (err) {
    return { success: false, error: err.toString() };
  }
}

// ==========================================
// 7. 修改預約時段函式：同步更新 Google 日曆事件開始與結束時間
// ==========================================
function handleUpdateBookingTime(params) {
  var eventId = params.eventId || params.id;
  var newStartTimeStr = params.startTime;
  var durationMin = parseInt(params.durationMin || 60, 10);

  if (!eventId) {
    return { success: false, message: '缺少 eventId 或 id' };
  }
  if (!newStartTimeStr) {
    return { success: false, message: '缺少新的開始時間 startTime' };
  }

  try {
    var cal = getTargetCalendar();
    var evt = cal.getEventById(eventId);
    if (!evt && eventId.indexOf('@google.com') === -1) {
      evt = cal.getEventById(eventId + '@google.com');
    }
    if (!evt && eventId.indexOf('@google.com') !== -1) {
      evt = cal.getEventById(eventId.replace('@google.com', ''));
    }

    if (!evt) {
      return { success: false, message: '日曆上未找到該行程' };
    }

    var newStart = new Date(newStartTimeStr);
    var newEnd = new Date(newStart.getTime() + durationMin * 60 * 1000);

    var oldStartStr = Utilities.formatDate(evt.getStartTime(), 'Asia/Taipei', 'yyyy/MM/dd (E) HH:mm');
    var newStartStr = Utilities.formatDate(newStart, 'Asia/Taipei', 'yyyy/MM/dd (E) HH:mm');

    evt.setTime(newStart, newEnd);

    // 同步更新日曆 Description 內的建立/變更紀錄
    var oldDesc = evt.getDescription() || '';
    var nowLog = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
    var updatedDesc = oldDesc + '\n[時段變更] 於 ' + nowLog + ' 從 ' + oldStartStr + ' 變更為 ' + newStartStr;
    evt.setDescription(updatedDesc);

    // 發送 Telegram 推播通知
    try {
      var tgMsg = '🔄 <b>【江夏板橋館・預約時段改期通報】</b>\n' +
        '━━━━━━━━━━━━━━━\n' +
        '👤 <b>排程資訊</b>：' + evt.getTitle() + '\n' +
        '⏳ <b>原約時段</b>：' + oldStartStr + '\n' +
        '✨ <b>改至新時段</b>：' + newStartStr + '\n' +
        '━━━━━━━━━━━━━━━\n' +
        '👉 <a href="https://azach258.github.io/jiangxia-banqiao/dashboard/?openExternalBrowser=1">點此開啟師傅排程看板</a>';
      sendTelegramNotification(tgMsg);
    } catch(tgE) {}

    return {
      success: true,
      message: '已成功更新 Google 日曆行程時段！',
      eventId: eventId,
      oldStart: oldStartStr,
      newStart: Utilities.formatDate(newStart, 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss')
    };
  } catch (err) {
    return { success: false, error: err.toString() };
  }
}

// ==========================================
// 8. 顧客 CRM 檔案變更函式：同步更新 Google 試算表顧客名冊
// ==========================================
function handleUpdateCustomer(params) {
  var origPhone = (params.origPhone || params.phone || '').trim().replace(/[^0-9]/g, '');
  var origName = (params.origName || params.name || '').trim();
  var newName = (params.name || '').trim();
  var newPhone = (params.phone || '').trim();
  var newNotes = (params.health_notes !== undefined) ? String(params.health_notes).trim() : '';

  if (!origPhone && !origName) {
    return { success: false, message: '缺少比對的顧客電話或姓名' };
  }
  if (!newName && !newPhone) {
    return { success: false, message: '缺少欲變更的顧客姓名或電話' };
  }

  try {
    var ss = SPREADSHEET_ID ? SpreadsheetApp.openById(SPREADSHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
    if (!ss) {
      return { success: false, message: '未連結 Google 試算表，請先設定試算表' };
    }

    var updatedRows = 0;
    var bSheet = ss.getSheetByName('預約紀錄名冊');
    if (bSheet) {
      var data = bSheet.getDataRange().getValues();
      for (var r = 1; r < data.length; r++) {
        var rowName = String(data[r][2] || '').trim();
        var rowPhone = String(data[r][3] || '').replace(/[^0-9]/g, '');

        var matched = false;
        // 電話為單一真相源 (SSOT) 優先匹配
        if (origPhone && rowPhone && (origPhone === rowPhone || rowPhone.indexOf(origPhone) !== -1 || origPhone.indexOf(rowPhone) !== -1)) {
          matched = true;
        } else if (!origPhone && origName && rowName && (origName === rowName || rowName.indexOf(origName) !== -1)) {
          matched = true;
        }

        if (matched) {
          if (newName) bSheet.getRange(r + 1, 3).setValue(newName);
          if (newPhone) bSheet.getRange(r + 1, 4).setValue(newPhone);
          if (params.health_notes !== undefined) bSheet.getRange(r + 1, 9).setValue(newNotes);
          updatedRows++;
        }
      }
    }

    // 同步更新日曆中該電話對應的所有近期事件標題與描述
    try {
      var cal = getTargetCalendar();
      if (cal && (origPhone || newPhone)) {
        var cleanTargetP = origPhone || newPhone.replace(/[^0-9]/g, '');
        var now = new Date();
        var calEvents = cal.getEvents(new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000), new Date(now.getTime() + 60 * 24 * 60 * 60 * 1000));
        for (var ci = 0; ci < calEvents.length; ci++) {
          var ce = calEvents[ci];
          var cTitle = ce.getTitle() || '';
          var cDesc = ce.getDescription() || '';
          if (cTitle.indexOf(cleanTargetP) !== -1 || cDesc.indexOf(cleanTargetP) !== -1) {
            // 更新行程標題
            ce.setTitle((newName || '顧客') + ' ' + (newPhone || cleanTargetP));
            // 更新行程描述內的姓名與電話
            var newDesc = cDesc;
            if (newName && newDesc.indexOf('顧客姓名：') !== -1) {
              newDesc = newDesc.replace(/顧客姓名：[^\n\r]*/, '顧客姓名：' + newName);
            }
            if (newPhone && newDesc.indexOf('聯絡電話：') !== -1) {
              newDesc = newDesc.replace(/聯絡電話：[^\n\r]*/, '聯絡電話：' + newPhone);
            }
            if (newNotes && newDesc.indexOf('備註說明：') !== -1) {
              newDesc = newDesc.replace(/備註說明：[^\n\r]*/, '備註說明：' + newNotes);
            }
            ce.setDescription(newDesc);
          }
        }
      }
    } catch(calUpdateErr) {
      Logger.log('日曆行程批次姓名同步非致命錯誤: ' + calUpdateErr.toString());
    }

    return {
      success: true,
      message: '已成功在 Google 試算表更新顧客資料 (共更新 ' + updatedRows + ' 筆紀錄)！',
      updatedRows: updatedRows,
      customer: {
        name: newName,
        phone: newPhone,
        health_notes: newNotes
      }
    };
  } catch (err) {
    return { success: false, error: err.toString() };
  }
}

// ==========================================
// 9. 歷史資料清洗與格式統一引擎 (Admin Cleanup Engine)
// 執行方式：在 Google Apps Script 編輯器中選擇此函式並點擊「執行」
// 功能：掃描所有試算表紀錄與日曆行程，套用電話單一真相源(SSOT)、統一 10 碼格式 (09xx-xxxxxx) 並合併分裂的姓名
// ==========================================
function adminCleanUpHistoricalData() {
  Logger.log('【開始執行】歷史資料清洗與格式統一引擎...');
  var ss = SPREADSHEET_ID ? SpreadsheetApp.openById(SPREADSHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) {
    Logger.log('找不到試算表，無法執行清理。');
    return;
  }

  // 1. 輔助函式區
  function formatStandardPhone(rawPhone) {
    if (!rawPhone) return '';
    var digits = String(rawPhone).replace(/[^0-9]/g, '');
    if (digits.length === 10 && digits.startsWith('09')) {
      return digits.slice(0, 4) + '-' + digits.slice(4, 7) + '-' + digits.slice(7);
    }
    return rawPhone;
  }

  function getCleanPhoneKey(rawPhone) {
    if (!rawPhone) return '';
    return String(rawPhone).replace(/[^0-9]/g, '');
  }

  function isDummyName(name) {
    if (!name) return true;
    var n = String(name).trim();
    return n.indexOf('QA') !== -1 || n.indexOf('測試') !== -1 || n === '線上預約顧客' || n === '預約顧客' || n === '新顧客' || /^[0-9-]+$/.test(n) || n === '王大偉' || n === '李小姐' || n === '張經理';
  }

  // 2. 建立全域電話真相源地圖 (Phone SSOT Map)
  var phoneMap = {};
  var bSheet = ss.getSheetByName('預約紀錄名冊');
  if (!bSheet) {
    Logger.log('找不到「預約紀錄名冊」工作表。');
    return;
  }
  
  var data = bSheet.getDataRange().getValues();
  // 第一次掃描：建立最佳姓名地圖
  for (var r = 1; r < data.length; r++) {
    var rawName = String(data[r][2] || '').trim();
    var rawPhone = String(data[r][3] || '').trim();
    var phoneKey = getCleanPhoneKey(rawPhone);
    
    if (phoneKey && !isDummyName(rawName)) {
      if (!phoneMap[phoneKey]) {
        phoneMap[phoneKey] = rawName;
      } else {
        // 保留字串較長或更像真實姓名的
        if (rawName.length > phoneMap[phoneKey].length && rawName.indexOf('先生') === -1 && rawName.indexOf('小姐') === -1) {
          phoneMap[phoneKey] = rawName;
        }
      }
    }
  }

  // 3. 第二次掃描：清洗試算表
  var updatedRows = 0;
  for (var r = 1; r < data.length; r++) {
    var rawName = String(data[r][2] || '').trim();
    var rawPhone = String(data[r][3] || '').trim();
    var phoneKey = getCleanPhoneKey(rawPhone);
    
    if (isDummyName(rawName) && !phoneKey) continue;

    if (phoneKey) {
      var standardPhone = formatStandardPhone(rawPhone);
      var bestName = phoneMap[phoneKey] || rawName || '預約顧客';
      
      var changed = false;
      if (rawName !== bestName) {
        bSheet.getRange(r + 1, 3).setValue(bestName);
        changed = true;
      }
      if (rawPhone !== standardPhone) {
        bSheet.getRange(r + 1, 4).setValue(standardPhone);
        changed = true;
      }
      if (changed) updatedRows++;
    }
  }
  Logger.log('✅ 試算表清洗完成！共更新 ' + updatedRows + ' 筆名冊資料。');

  // 4. 第三次掃描：清洗 Google 日曆 (過去 3 個月到未來 6 個月)
  Logger.log('開始清洗 Google 日曆行程...');
  var cal = getTargetCalendar();
  if (!cal) {
    Logger.log('找不到 Google 日曆。');
    return;
  }
  
  var now = new Date();
  var startRange = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000); 
  var endRange = new Date(now.getTime() + 180 * 24 * 60 * 60 * 1000); 
  var events = cal.getEvents(startRange, endRange);
  var updatedEvents = 0;

  for (var i = 0; i < events.length; i++) {
    var evt = events[i];
    var oldTitle = evt.getTitle() || '';
    var oldDesc = evt.getDescription() || '';
    
    var phoneMatch = oldDesc.match(/(?:聯絡電話|電話|手機)[:：]\s*([0-9-]+)/);
    var phone = phoneMatch ? phoneMatch[1].trim() : '';
    
    if (!phone) {
      var titleParts = oldTitle.split(/\s+/);
      if (titleParts.length >= 2 && /^[0-9-]+$/.test(titleParts[titleParts.length - 1])) {
        phone = titleParts[titleParts.length - 1];
      }
    }

    var phoneKey = getCleanPhoneKey(phone);
    if (phoneKey) {
      var bestName = phoneMap[phoneKey] || '預約顧客';
      var standardPhone = formatStandardPhone(phoneKey);
      var newTitle = bestName + ' ' + standardPhone;
      
      var newDesc = oldDesc;
      if (newDesc.indexOf('顧客姓名：') !== -1) {
         newDesc = newDesc.replace(/顧客姓名：[^\n\r]*/, '顧客姓名：' + bestName);
      }
      if (newDesc.indexOf('聯絡電話：') !== -1) {
         newDesc = newDesc.replace(/聯絡電話：[^\n\r]*/, '聯絡電話：' + standardPhone);
      }
      
      var changedCal = false;
      if (oldTitle !== newTitle) {
        evt.setTitle(newTitle);
        changedCal = true;
      }
      if (oldDesc !== newDesc) {
        evt.setDescription(newDesc);
        changedCal = true;
      }
      if (changedCal) updatedEvents++;
    }
  }

  Logger.log('✅ Google 日曆清洗完成！共修正 ' + updatedEvents + ' 筆行程格式。');
  Logger.log('【執行完畢】歷史資料已全面統一格式與歸戶！');
}
